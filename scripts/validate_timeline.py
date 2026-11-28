#!/usr/bin/env python3
"""Validate an MGEasy SRT shot plan without making semantic decisions."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path


TIME_RE = re.compile(r"^(?:(\d+):)?(\d{1,2}):(\d{2})(?:[,.](\d{1,3}))?$")
EPSILON = 0.002


def number(value: object) -> float:
    try:
        if isinstance(value, bool):
            raise ValueError
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"invalid number: {value!r}") from exc
    if not math.isfinite(result) or result < 0:
        raise ValueError(f"expected a finite non-negative number, got {value!r}")
    return result


def parse_time(value: object) -> float:
    if isinstance(value, (int, float)):
        return number(value)
    if not isinstance(value, str):
        raise ValueError(f"unsupported time value: {value!r}")
    match = TIME_RE.match(value.strip())
    if not match:
        raise ValueError(f"invalid time format: {value!r}")
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2))
    seconds = int(match.group(3))
    millis = int((match.group(4) or "0").ljust(3, "0"))
    if minutes >= 60 or seconds >= 60:
        raise ValueError(f"invalid time value: {value!r}")
    return number(hours * 3600 + minutes * 60 + seconds) + millis / 1000


def snap_duration(actual: float) -> int | None:
    for duration in range(3, 16):
        if actual <= duration or math.isclose(actual, duration, rel_tol=0, abs_tol=1e-9):
            return duration
    return None


def close(left: float, right: float) -> bool:
    return abs(left - right) <= EPSILON


def check_optional_seconds(shot: dict, shot_id: str, field: str, expected: float, errors: list[str]) -> None:
    if shot.get(field) is None:
        return
    try:
        valid = close(number(shot[field]), expected)
    except ValueError:
        valid = False
    if not valid:
        errors.append(f"shot {shot_id}: {field} must be {expected:.3f}, got {shot[field]!r}")


def validate(data: object) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    computed_shots: list[dict] = []
    if not isinstance(data, dict):
        return {"ok": False, "errors": ["plan must be a JSON object"],
                "warnings": warnings, "computed_shots": computed_shots}

    cues = data.get("cues")
    shots = data.get("shots", [])
    if not isinstance(cues, list):
        errors.append("cues must be a list")
    if not isinstance(shots, list) or not shots:
        errors.append("shots must be a non-empty list")
    if errors:
        return {"ok": False, "errors": errors, "warnings": warnings, "computed_shots": computed_shots}

    parsed_cues: dict[int, tuple[float, float]] = {}
    previous_cue_end = None
    for index, cue in enumerate(cues):
        try:
            start = parse_time(cue["start"])
            end = parse_time(cue["end"])
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"cue {index}: {exc}")
            continue
        if end <= start:
            errors.append(f"cue {index}: end must be later than start")
        if previous_cue_end is not None and start < previous_cue_end - EPSILON:
            errors.append(f"cue {index}: overlaps the previous cue")
        previous_cue_end = end
        parsed_cues[index] = (start, end)

    assigned: dict[int, str] = {}
    previous_end: float | None = None
    seen_ids: set[str] = set()

    for index, shot in enumerate(shots):
        if not isinstance(shot, dict):
            errors.append(f"shot at index {index} must be an object")
            continue
        value = shot.get("shot_id", index + 1)
        if type(value) not in (str, int) or not str(value).strip():
            errors.append(f"shot at index {index}: invalid shot_id {value!r}")
            continue
        shot_id = str(value).strip()
        if shot_id in seen_ids:
            errors.append(f"duplicate shot_id: {shot_id}")
        seen_ids.add(shot_id)
        try:
            start = parse_time(shot["start"])
            end = parse_time(shot["end"])
        except (KeyError, ValueError) as exc:
            errors.append(f"shot {shot_id}: {exc}")
            continue

        actual = end - start
        if actual <= 0:
            errors.append(f"shot {shot_id}: end must be later than start")
        if index == 0 and not close(start, 0.0):
            errors.append(f"shot {shot_id}: first shot must start at 00:00.000 to preserve opening blank")
        if previous_end is not None and not close(start, previous_end):
            errors.append(f"shot {shot_id}: starts at {start:.3f}s but previous shot ends at {previous_end:.3f}s")
        previous_end = end

        expected = snap_duration(actual)
        declared_duration = shot.get("duration_seconds")
        if expected is None:
            errors.append(f"shot {shot_id}: actual duration {actual:.3f}s exceeds 15 seconds")
        elif declared_duration != expected:
            errors.append(f"shot {shot_id}: duration_seconds must be {expected}, got {declared_duration!r}")

        check_optional_seconds(shot, shot_id, "actual_duration_seconds", actual, errors)

        cue_indices = shot.get("cue_indices")
        if not isinstance(cue_indices, list):
            errors.append(f"shot {shot_id}: cue_indices must be a list")
            cue_indices = []

        spoken = 0.0
        for cue_index in cue_indices:
            if type(cue_index) is not int or cue_index not in parsed_cues:
                errors.append(f"shot {shot_id}: invalid cue index {cue_index!r}")
                continue
            if cue_index in assigned:
                errors.append(f"cue {cue_index}: assigned to both {assigned[cue_index]} and {shot_id}")
            assigned[cue_index] = shot_id
            cue_start, cue_end = parsed_cues[cue_index]
            if cue_start < start - EPSILON or cue_end > end + EPSILON:
                errors.append(f"shot {shot_id}: cue {cue_index} lies outside the shot interval")
            spoken += cue_end - cue_start

        blank = max(0.0, actual - spoken)
        check_optional_seconds(shot, shot_id, "included_blank_seconds", blank, errors)

        computed_shots.append(
            {
                "shot_id": shot_id,
                "actual_duration_seconds": round(actual, 3),
                "duration_seconds": expected,
                "included_blank_seconds": round(blank, 3),
            }
        )

    for cue_index in parsed_cues:
        if cue_index not in assigned:
            errors.append(f"cue {cue_index}: not assigned to any shot")

    if previous_end is not None and data.get("media_end") is not None:
        try:
            media_end = parse_time(data["media_end"])
            if not close(previous_end, media_end):
                errors.append(f"last shot ends at {previous_end:.3f}s but media_end is {media_end:.3f}s")
        except ValueError as exc:
            errors.append(f"media_end: {exc}")
    elif previous_end is not None:
        warnings.append("media_end missing; trailing blank cannot be verified")

    return {"ok": not errors, "errors": errors, "warnings": warnings, "computed_shots": computed_shots}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="JSON file containing cues, shots, and optional media_end")
    args = parser.parse_args()
    try:
        data = json.loads(args.plan.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        return 2
    result = validate(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
