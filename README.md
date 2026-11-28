# MGEasy

**把一份口播变成能交给 Google Flow 的 2.5D 动效分镜。**

MGEasy 是一个 Codex Skill。给它一个主题、一份文案、一段口播录音或一个 SRT，它会按内容拆镜，为每镜设计主体、动作、运镜、排版和衔接，并写好可以粘贴到 Gemini Omni 的英文 Prompt。适合产品介绍、口播配画面、数据解释和发布会式动态排版。

## 快速开始

### 安装

在终端把仓库克隆到 Codex 的技能目录。

```sh
mkdir -p "$HOME/.codex/skills"
git clone https://github.com/louchi1984-coder/mgeasy.git "$HOME/.codex/skills/mgeasy"
```

如果已经通过 Git 克隆安装，可以用下面的命令更新。

```sh
git -C "$HOME/.codex/skills/mgeasy" pull --ff-only
```

### 跑第一个镜头

新开一个 Codex 会话，上传录音或 SRT，也可以直接粘贴文案。输入这句话。

> 用 $mgeasy 把这段口播做成 16:9 横屏的 2.5D 商业动效。用 Google Flow / Gemini Omni Flash，先给我看时间规划。

先确认它给出的时间规划，再逐镜确认画面。拿到某镜的 Prompt 后，在 Google Flow 面板里选对应比例、时长和参考帧，把英文 Prompt 粘贴到生成框。以实际面板提供的选项为准。

## 一个镜头长什么样

**输入**　「这项任务已经完成了 72%。」

**分镜思路**　让进度条快速填到 72%，推近到数值稳住的画面。保留完成率与进度条的对应关系，给观众留出读数时间。

**Flow 设置**　16:9 横屏 · 6 秒 · 纯文生视频

<details>
<summary>展开完整英文 Prompt</summary>

```text
Sleek Google Keynote kinetic typography and data motion graphics in Google Brand Studio and Material 3 expressive style — high-craft 2.5D graphic design featuring bold editorial typography, precision data visuals, clean vector geometry and subtle frosted-glass accents on a luminous abstract color-field canvas. One continuous shot, no scene cuts.

The camera opens on a bright warm-gray luminous canvas split by a soft alabaster geometric plane: in the midground, an oversized bold deep-indigo geometric sans-serif "72%" anchors above a sleek frosted-glass Material segmented progress track whose vivid cobalt fill measures exactly 72% of one whole, paired with crisp high-contrast labels reading "完成率" and "示例数据". Translucent glass tick-mark tabs with delicate hairline borders and soft UI elevation shadows float near the foreground corners.

[0–3s] With snappy After Effects pop-in and tight overshoot bounce, "72%", "完成率", "示例数据" and the frosted progress track snap into view as the cobalt bar zips swiftly across the subdivisions toward 72% while 2.5D layers glide forward. [3–6s] Without pausing, the camera punches smoothly closer toward "72%" with energetic parallax as the fill locks decisively onto the exact 72% mark with a crisp micro-overshoot settle, finishing on a razor-sharp commercial data layout.

Refined Google commercial 2.5D motion design polish, snappy After Effects bounce-and-snap rhythm, dynamic 2.5D camera choreography, crisp accurate Chinese typography, clean silent visuals.
```

</details>

还有路线地图、标题动画、UI 操作和人物剧情等示例。 [查看分镜范例](references/gold-examples.md)

## 从口播到成片

| 阶段 | 怎么做 |
| --- | --- |
| 时间规划 | 有录音或 SRT 时沿用实际时间，保留开场、句间与片尾空白。只有文案时先估时。生成档位按 `3–15` 整数秒规划。 |
| 逐镜设计 | 先确认观众要看懂什么，再决定画面里什么东西会动、怎么动、最后停在哪。末镜按内容收束。 |
| 生成与修片 | Prompt 通过脚本校验和独立评审后交付。到 Flow 生成。需要微调时，可用一条对话式指令改错字、节奏或底色。 |
| 衔接 | 顺序生成时，可把上一镜的清晰末帧上传为下一镜的 Start Frame。独立生成时，可选同色场接力。 |
| 合并与验收 | 把选定的生成片段发回 Codex，按原时间轴裁切、合并、去除生成音轨，再对齐原口播。生成素材与导出成片分别校验。 |

[首尾帧与局部精修指南](references/omni-iteration.md) · [多镜衔接示例](references/gold-examples-continuity.md)

## 项目里会得到什么

| 文件或产物 | 用途 |
| --- | --- |
| `timeline-plan.json` | 镜号、字幕起止、实际时长、空白和生成档位 |
| 单镜英文 Prompt | 可复制到 Flow 的画面指令，面板参数随镜单列 |
| `delivery.json` | 记录模型与比例、各镜采用版本、实际素材、剪点及后期待办 |
| 声画对照表 | 按镜核对口播、画面动作、可见文字及衔接 |
| 合并成片 | 素材齐全后按时间轴导出，保留原口播的语速 |

## 本地校验

脚本使用 Python 3。素材探测与合并阶段需要 `ffprobe` 和 `ffmpeg`。在你的项目目录运行下面的命令，必要时按实际位置调整文件路径。

```sh
mgeasy_dir="$HOME/.codex/skills/mgeasy"
python3 -B "$mgeasy_dir/scripts/validate_timeline.py" timeline-plan.json
python3 -B "$mgeasy_dir/scripts/validate_delivery.py" delivery.json prompt --shot 01
python3 -B "$mgeasy_dir/scripts/validate_delivery.py" delivery.json intake
python3 -B "$mgeasy_dir/scripts/validate_delivery.py" delivery.json final
```

`prompt` 检查当前镜的 Prompt。`intake` 检查素材与剪点，`final` 检查导出、音轨及后期待办。画面上的字、首尾帧和音画同步还要看片确认。 [交付记录格式与验收步骤](references/delivery-checks.md)

## 设计参考

- [Skill 完整工作流](SKILL.md)
- [时间轴与口播规则](references/timeline-rules.md)
- [2.5D 视觉与运镜规则](references/mg-design.md)
- [英文 Prompt 输出合同](references/output-contract.md)
- [独立评审标准](references/review.md)
