#!/usr/bin/env python3
"""Check a saved Omni v2.0 prompt, source clips, or a completed MGEasy export."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path

from validate_timeline import number, parse_time, validate

BEAT = re.compile(r"\[(\d+)\s*[–-]\s*(\d+)\s*s\]")
DECIMAL_SEC = re.compile(r"\[\s*\d+\.\d+\s*[–-]|\b\d+\.\d+\s*s\b")
HEX_CODE = re.compile(r"#[0-9A-Fa-f]{3}(?:[0-9A-Fa-f]{3})?\b")
CSS_UNIT = re.compile(r"\b\d+(?:\.\d+)?\s*(?:px|pt|dp|rem|em)\b", re.IGNORECASE)
CLI_FLAG = re.compile(r"(?:^|\s)--[a-zA-Z][a-zA-Z0-9-]*\b")
JSON_WHITELIST = re.compile(r"\bDisplay only (?:these|this) exact strings?\s*:", re.IGNORECASE)
OLD_BOILERPLATE = (
    (re.compile(r"Use the specified Hex values only", re.IGNORECASE),
     "remove legacy Hex boilerplate (use clear color names instead of Hex codes)"),
    (re.compile(r"Preserve every Chinese character exactly as written", re.IGNORECASE),
     "remove 40-word legacy Chinese legal disclaimer (bind text spatially and use crisp positive typography cues)"),
)
TEMPLATE_LABEL = re.compile(
    r"(?:^|[.\n]\s*)(?:background|subject|camera|information logic|anchor|scene anchor|style lock)\s*:"
    r"|(?:背景|主体|运镜|镜头)\s*：",
    re.IGNORECASE,
)
BANNED_PHRASES = (
    (re.compile(r"\busing\s+(?:gemini|omni|veo|google\s+flow)\b", re.IGNORECASE),
     "do not include model names inside the video prompt (keep model in delivery.json)"),
    (re.compile(r"\blet\s+the\s+model\s+choose\b|\ballow\s+the\s+model\b", re.IGNORECASE),
     "remove LLM meta-instruction ('let/allow the model...')"),
    (re.compile(r"\bbuild\s+a\s+more\s+developed\s+composition\b", re.IGNORECASE),
     "remove LLM meta-instruction ('build a more developed composition')"),
    (re.compile(r"\bplanned\s+preceding\b|\bfor\s+the\s+next\s+(?:shot|clip)\b|\bnext\s+(?:shot|clip)(?:'s|’s)?\s+content\b", re.IGNORECASE),
     "describe visual entry/exit directly without cross-shot meta-references"),
    (re.compile(r"\bphotorealistic\b|\breal-world\b|\b3D\s+render\b|\blive-action\b", re.IGNORECASE),
     "avoid realism/live-action trigger words ('photorealistic', 'real-world', '3D render', 'live-action'); keep the stylized graphic/2D editorial aesthetic"),
    (re.compile(r"\blens\b", re.IGNORECASE),
     "avoid physical camera word 'lens' (triggers depth-of-field blur/realism); use 'frame edges', 'canvas', or '2.5D camera'"),
    (re.compile(r"\bicons\b", re.IGNORECASE),
     "avoid clip-art word 'icons'; use 'frosted-glass cards', 'UI tiles', 'graphic modules', or 'vector emblems'"),
    (re.compile(r"\bcurtain\b", re.IGNORECASE),
     "avoid fabric word 'curtain' (triggers realistic cloth folds); use 'flat solid matte 2D graphic wipe panel'"),
    (re.compile(r"\bsubtitles?\b|\bcaptions?\b", re.IGNORECASE),
     "avoid words 'subtitle'/'caption' (triggers unwanted on-screen subtitles in Omni); use 'leaving the bottom third empty'"),
)
BRAND_COLOR_FIELD = re.compile(r"\bGoogle[-\s]+(?:blue|green|red|yellow)\s+field\b", re.IGNORECASE)
ONE_SHOT = "One continuous shot, no scene cuts."
RATIO_REL_TOL = 0.015
MAX_RECOMMENDED_WORDS = 240
MIN_RECOMMENDED_WORDS = 70


def object_field(value: object, name: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def text_field(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value


def path_field(root: Path, value: object, name: str) -> Path:
    path = (root / text_field(value, name)).resolve()
    if not path.is_file():
        raise ValueError(f"{name}: file not found: {path}")
    return path


def load_json(path: Path) -> dict:
    def unique_object(pairs: list[tuple[str, object]]) -> dict:
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{path.name}: duplicate JSON key {key!r}")
            result[key] = value
        return result

    return object_field(json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object), path.name)


def parse_ratio(value: object) -> Fraction:
    if not isinstance(value, str) or not re.fullmatch(r"[1-9]\d*:[1-9]\d*", value):
        raise ValueError(f"expected an aspect ratio such as 16:9, got {value!r}")
    width, height = map(int, value.split(":"))
    return Fraction(width, height)


def ratios_match(actual: Fraction, expected: Fraction) -> bool:
    if actual == expected:
        return True
    return abs(float(actual) - float(expected)) / float(expected) <= RATIO_REL_TOL


def check_prompt(root: Path, shot: dict, row: dict) -> tuple[list[str], list[str]]:
    text_field(row.get("prompt_revision"), "prompt_revision")
    prompt = path_field(root, row.get("prompt_file"), "prompt_file").read_text(encoding="utf-8-sig").strip()
    approved = row.get("visible_text")
    if not isinstance(approved, list) or not all(isinstance(s, str) and s.strip() for s in approved):
        raise ValueError("visible_text must be an array of approved strings; use [] for no text")

    mode = row.get("continuity_mode", "t2v")
    if mode not in ("t2v", "start_frame"):
        raise ValueError("continuity_mode must be 't2v' or 'start_frame'")

    errors: list[str] = []
    warnings: list[str] = []
    duration = int(shot["duration_seconds"])

    # 1. Style & one-shot opening check
    if mode == "start_frame":
        if not prompt.startswith("Continue seamlessly from the opening reference frame"):
            errors.append("start_frame prompt must open with 'Continue seamlessly from the opening reference frame...'")
    else:
        valid_openings = (
            "Sleek Google Keynote commercial motion graphics",
            "Sleek Google Keynote kinetic typography and data motion graphics",
        )
        if not prompt.startswith(valid_openings):
            errors.append(
                "t2v prompt must open with 'Sleek Google Keynote commercial motion graphics...' "
                "or 'Sleek Google Keynote kinetic typography and data motion graphics...'"
            )

    if "2.5D" not in prompt:
        errors.append("missing '2.5D' depth/camera style anchor")
    if ONE_SHOT not in prompt:
        errors.append(f"missing required one-shot lock: {ONE_SHOT!r}")

    # 2. Integer beat coverage check
    if DECIMAL_SEC.search(prompt):
        errors.append("decimal seconds are not allowed; use integer beat intervals only")
    beats = [(int(m.group(1)), int(m.group(2))) for m in BEAT.finditer(prompt)]
    if duration <= 8:
        allowed_counts = (2,)
    elif duration <= 12:
        allowed_counts = (2, 3)
    else:
        allowed_counts = (3, 4)
    if (len(beats) not in allowed_counts or beats[0][0] != 0 or beats[-1][1] != duration
            or any(start >= end for start, end in beats)
            or any(left[1] != right[0] for left, right in zip(beats, beats[1:]))):
        errors.append(f"integer beat intervals must cover 0–{duration}s continuously in {allowed_counts} parts")

    # 3. Spatially anchored visible text verification
    if approved:
        for item in approved:
            quoted_variants = (f'"{item}"', f"“{item}”")
            if not any(variant in prompt for variant in quoted_variants):
                errors.append(f"approved visible_text string not found verbatim in quotes inside prompt: {item!r}")
    else:
        if not re.search(r"\bno text\b|\bwordless\b", prompt, re.IGNORECASE):
            errors.append("empty visible_text requires stating 'no text' or 'wordless' in the prompt")

    # 4. Omni v2.0 prompt purity checks
    if CLI_FLAG.search(prompt):
        errors.append("remove CLI flags such as '--ar 16:9' (set aspect ratio in Flow/Omni UI and delivery.json)")
    if JSON_WHITELIST.search(prompt):
        errors.append("remove JSON whitelist clause ('Display only...'); bind text spatially in natural prose instead")
    if HEX_CODE.search(prompt):
        errors.append("remove raw Hex color codes (#xxxxxx) from video prompt; use clear perceptual color names")
    if CSS_UNIT.search(prompt):
        errors.append("remove CSS/spec units like '1px' (Omni renders them as Figma-style annotation text); use 'hairline' or 'ultra-thin'")
    if TEMPLATE_LABEL.search(prompt):
        errors.append("remove template field labels (e.g., Camera:, Subject:, Background:, Style lock:)")
    for pattern, reason in OLD_BOILERPLATE:
        if pattern.search(prompt):
            errors.append(reason)
    for pattern, reason in BANNED_PHRASES:
        if pattern.search(prompt):
            errors.append(reason)
    if BRAND_COLOR_FIELD.search(prompt):
        warnings.append("avoid brand-named closing color fields like 'Google-blue field' (may trigger a Google logo); use 'royal-blue field with zero logos'")

    # 5. Concise signal-density budget
    words = len(re.findall(r"\S+", prompt))
    if words > MAX_RECOMMENDED_WORDS:
        warnings.append(f"prompt is {words} words (> {MAX_RECOMMENDED_WORDS}); tighten to keep high visual signal density")
    elif words < MIN_RECOMMENDED_WORDS:
        warnings.append(f"prompt is only {words} words (< {MIN_RECOMMENDED_WORDS}); ensure layers, motion and camera are clear")

    return errors, warnings


def probe(path: Path) -> dict:
    command = [
        "ffprobe", "-v", "error", "-show_entries",
        "stream=codec_type,duration,start_time,width,height,display_aspect_ratio,avg_frame_rate:format=duration",
        "-of", "json", str(path),
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=20)
        return json.loads(result.stdout)
    except FileNotFoundError as exc:
        raise ValueError("ffprobe is required for intake and final checks") from exc
    except (subprocess.SubprocessError, json.JSONDecodeError) as exc:
        raise ValueError(f"ffprobe could not read {path.name}") from exc


def stream_duration(stream: dict, media: dict) -> float:
    return number(stream.get("duration") or media.get("format", {}).get("duration"))


def group_streams(media: dict) -> tuple[list[dict], list[dict]]:
    streams = media.get("streams", [])
    return ([s for s in streams if s.get("codec_type") == "video"],
            [s for s in streams if s.get("codec_type") == "audio"])


def video_ratio(video: dict) -> Fraction:
    display = video.get("display_aspect_ratio")
    if display not in (None, "N/A", "0:1"):
        return parse_ratio(display)
    return Fraction(video["width"], video["height"])


def check_source(root: Path, row: dict, used_paths: set[Path], ratio: Fraction) -> dict:
    source = object_field(row.get("source"), "source")
    if source.get("prompt_revision") != row["prompt_revision"]:
        raise ValueError("source prompt_revision does not match the adopted prompt_revision")
    path = path_field(root, source.get("file"), "source.file")
    text_field(source.get("visual_check"), "source.visual_check")
    if path in used_paths:
        raise ValueError(f"source file is already assigned to another shot: {path.name}")
    used_paths.add(path)
    media = probe(path)
    videos, audio = group_streams(media)
    if len(videos) != 1:
        raise ValueError(f"source must have one video stream: {path.name}")
    if not ratios_match(video_ratio(videos[0]), ratio):
        raise ValueError(f"source display aspect ratio differs from the adopted ratio: {path.name}")
    duration = stream_duration(videos[0], media)
    cut = source.get("cut")
    if not isinstance(cut, list) or len(cut) != 2:
        raise ValueError("source.cut must contain [in_seconds, out_seconds]")
    start, end = map(number, cut)
    if not start < end <= duration + 0.002:
        raise ValueError(f"source.cut must fit within the {duration:.3f}s video stream")
    return {"duration_seconds": duration, "audio_streams": len(audio)}


def check_post_tasks(tasks: object, final: bool) -> list[str]:
    if not isinstance(tasks, list):
        raise ValueError("post_tasks must be a list; use [] when no post work remains")
    errors = []
    for task in tasks:
        task = object_field(task, "post_tasks entry")
        description = text_field(task.get("description"), "post task description")
        status = task.get("status")
        if status not in ("pending", "done", "accepted"):
            errors.append(f"invalid post task status: {description}")
        elif status == "pending":
            if final:
                errors.append(f"pending post task: {description}")
        elif not isinstance(task.get("evidence"), str) or not task["evidence"].strip():
            errors.append(f"record inspection or approval evidence for post task: {description}")
    return errors


def check_export(root: Path, manifest: dict, source_paths: set[Path], expected_end: float) -> list[str]:
    output = path_field(root, manifest.get("output_file"), "output_file")
    if output in source_paths:
        return ["output_file must differ from the source clips and recording"]
    media = probe(output)
    videos, audio = group_streams(media)
    if len(videos) != 1:
        raise ValueError("output_file must have exactly one video stream")
    video = videos[0]
    try:
        fps = float(Fraction(video.get("avg_frame_rate", "0/1")))
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("could not read the output frame rate") from exc
    if fps <= 0:
        raise ValueError("output frame rate must be positive")
    tolerance = 1 / fps + 0.002
    expected_ratio = parse_ratio(manifest.get("output_ratio", manifest["aspect_ratio"]))
    errors = []
    if not ratios_match(video_ratio(video), expected_ratio):
        errors.append("output display aspect ratio differs from the approved ratio")
    if abs(stream_duration(video, media) - expected_end) > tolerance:
        errors.append(f"output video duration differs from the {expected_end:.3f}s timeline by more than one frame")
    if abs(float(video.get("start_time", 0))) > tolerance:
        errors.append("output video must start at the timeline origin")
    if manifest["audio_mode"] == "silent":
        if audio:
            errors.append("silent export must contain no audio stream")
    elif len(audio) != 1:
        errors.append("voiceover export must contain exactly one audio stream")
    else:
        if abs(float(audio[0].get("start_time", 0))) > tolerance:
            errors.append("voiceover output must start at the timeline origin")
        if abs(stream_duration(audio[0], media) - expected_end) > max(tolerance, 0.075):
            errors.append("voiceover duration differs from the timeline; check edits and sample rate")
    return errors


def check(manifest_path: Path, phase: str, shot_id: str | None) -> dict:
    root = manifest_path.parent
    manifest = load_json(manifest_path)
    plan = load_json(path_field(root, manifest.get("timeline_plan"), "timeline_plan"))
    report = validate(plan)
    errors = list(report["errors"])
    warnings = list(report["warnings"])
    result = {"ok": False, "phase": phase, "errors": errors, "warnings": warnings, "sources": {}}
    if errors:
        return result
    shots = {str(s.get("shot_id", i + 1)).strip(): s for i, s in enumerate(plan["shots"])}
    rows = object_field(manifest.get("shots"), "shots")
    text_field(manifest.get("model"), "model")
    ratio = text_field(manifest.get("aspect_ratio"), "aspect_ratio")
    aspect = parse_ratio(ratio)

    if phase == "prompt":
        if shot_id not in shots:
            raise ValueError(f"unknown shot_id: {shot_id!r}")
        check_ids = [shot_id]
    else:
        check_ids = list(shots)
        for extra in rows.keys() - shots.keys():
            errors.append(f"unknown shot_id: {extra}")
        if manifest.get("audio_mode") not in ("voiceover", "silent"):
            raise ValueError("audio_mode must be 'voiceover' or 'silent'")
        media_end = plan.get("media_end")
        expected_end = parse_time(plan["shots"][-1]["end"] if media_end is None else media_end)
        voice = None
        if manifest.get("voiceover") is not None or manifest["audio_mode"] == "voiceover":
            voice = path_field(root, manifest.get("voiceover"), "voiceover")
            original = probe(voice)
            _, audio = group_streams(original)
            if len(audio) != 1 or abs(stream_duration(audio[0], original) - expected_end) > 0.075:
                errors.append("source recording must have one audio stream and match the timeline duration")
    used_paths: set[Path] = set()
    for identifier in check_ids:
        if identifier not in rows:
            errors.append(f"shot {identifier}: missing delivery record")
            continue
        try:
            row = object_field(rows[identifier], "shot delivery record")
            shot_errors, shot_warnings = check_prompt(root, shots[identifier], row)
            if phase != "prompt" and not shot_errors:
                result["sources"][identifier] = check_source(root, row, used_paths, aspect)
                shot_errors.extend(check_post_tasks(row.get("post_tasks"), phase == "final"))
            errors.extend(f"shot {identifier}: {message}" for message in shot_errors)
            warnings.extend(f"shot {identifier}: {message}" for message in shot_warnings)
        except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
            errors.append(f"shot {identifier}: {exc}")

    if phase == "final":
        if voice is not None:
            used_paths.add(voice)
        try:
            errors.extend(check_export(root, manifest, used_paths, expected_end))
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f"export: {exc}")
    result["ok"] = not errors
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("phase", choices=("prompt", "intake", "final"))
    parser.add_argument("--shot", help="shot_id to check in the prompt phase")
    args = parser.parse_args()
    if (args.phase == "prompt") != (args.shot is not None):
        parser.error("--shot is required in the prompt phase only")
    try:
        result = check(args.manifest, args.phase, args.shot)
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
        result = {"ok": False, "phase": args.phase, "errors": [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
