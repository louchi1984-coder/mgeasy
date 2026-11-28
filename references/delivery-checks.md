# Prompt、素材与成片校验

在本次项目的工作目录维护一份 `delivery.json`，边交付边补记录；字幕与镜头时间继续从同一份 `timeline_plan` 读取。无台词成片用 `"cues": []`，无台词 Shot 用 `"cue_indices": []`。路径相对于 `delivery.json`，也可使用绝对路径。

```json
{
  "timeline_plan": "timeline-plan.json",
  "model": "Gemini Omni Flash 1.2",
  "aspect_ratio": "16:9",
  "audio_mode": "voiceover",
  "voiceover": "narration.m4a",
  "output_file": "final.mp4",
  "shots": {
    "02": {
      "continuity_mode": "t2v",
      "prompt_revision": "v3",
      "prompt_file": "shot-02-v3.txt",
      "visible_text": ["文案"],
      "source": {
        "file": "shot-02.mp4",
        "prompt_revision": "v3",
        "cut": [0, 5.9],
        "visual_check": "磨砂文案卡入槽、分镜展开与片尾珊瑚色场均已查看。"
      },
      "post_tasks": []
    }
  }
}
```

> `continuity_mode` 可选：`"t2v"`（默认，纯文生 / 纯色场接力）或 `"start_frame"`（上传上一镜末帧做首尾帧参考衔接）。

## 交付 Prompt

保存可直接复制的精简英文 Prompt 原文（不含模型名、`--ar`、JSON 数组与 Hex 色码）。镜号沿用时间轴，每次修改保存新文件和新版本号，已交付版本留作素材对应依据。`visible_text` 记录全部获准字符串，校验脚本会自动确认它们逐字出现在 Prompt 中。此阶段只需填写 `timeline_plan`、`model`、`aspect_ratio` 和当前镜的 Prompt 字段。

```bash
python3 -B scripts/validate_delivery.py <delivery.json> prompt --shot 02
```

每次改完重跑，修复全部报错后再进入盲审与用户确认；若某镜出片后仅局部有错字或节奏偏差，优先按 [omni-iteration.md](omni-iteration.md) 用对话式 Delta Edit 局部修正，定稿后再记入 `source`。

## 素材齐全后合并

1. 用文件名、版本和画面内容匹配镜号；文件名缺少镜号时查看实际画面。缺片时指出缺失镜号；有多条候选且无法确认采用版时只询问对应镜头。
2. 查看实际画面的关键动作、可见文字、首尾衔接状态以及准备保留的剪点，简记在 `visual_check`。用 `ffprobe` 的视频流实长填写 `source.cut` 的起止秒数。若需补字、嵌片或修正剪点，在当前镜的 `post_tasks` 登记，例如 `{"description":"用 01 镜实片替换播放器示意画面","status":"pending"}`。
3. 运行 `python3 -B scripts/validate_delivery.py <delivery.json> intake`，修复全部错误后再合并。
4. **时长适配原则（保留转场优先）**：
   - 当生成档位长于真实音频区间（例如 `6s` 素材对齐 `5.2s` 区间）且当前镜带有**片尾纯色场转场或关键收束动作**时，优先在合理范围内对画面做轻微均匀加速（通常 `1.05x–1.25x`，如 `setpts`），完整保留转场，不要硬裁尾巴切掉衔接。
   - 末镜或片尾为稳定定格的镜头，在不截断核心动作和读字时间的前提下可直接尾裁。
   - 原口播音轨始终保持原速对齐。
5. 按 `audio_mode` 交付：`voiceover` 时先剥离全部生成片段音轨（`-an`），再将原录音原速对齐到时间轴；`silent` 时导出无音轨成片（用于对齐的原录音路径可保留）。

## 成片验收

核对实际导出的关键帧与声音：检查镜头顺序、首尾帧/色场衔接、剪点、口播与字幕同步（如有）以及已登记的 `post_tasks`。每项待办完成后改 `done` 并填写简短 `evidence`；用户明确接受的偏差填 `accepted` 并记录批准依据。

填写 `output_file` 后运行：

```bash
python3 -B scripts/validate_delivery.py <delivery.json> final
```

裁切成片时用 `output_ratio` 记录成片比例，生成比例仍在 `aspect_ratio`。脚本通过后仍需目视复核成片关键帧和听音核对口播；未完成的导出须标明预览状态并列出剩余待办。
