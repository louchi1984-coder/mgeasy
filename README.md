# MGEasy

**面向 Google Flow / Gemini Omni 的 Google Keynote 2.5D 商业动效技能。**

MGEasy 把主题、文案、口播录音或 SRT 拆成动效分镜。每镜按内容选择动态文字、图形、图表或 UI，再设计动作、运镜和衔接，交付可直接复制的英文 Prompt。

## 怎么用

公开仓库可以直接克隆到 Codex 的技能目录。

```sh
git clone https://github.com/louchi1984-coder/mgeasy.git "$HOME/.codex/skills/mgeasy"
```

新开一个 Codex 会话，附上口播录音、文案或 SRT，输入下面这条指令即可从时间规划开始。

> 用 $mgeasy 把这段口播做成 16:9 的 Google Keynote 2.5D MG 分镜。用 Google Flow / Gemini Omni Flash，先给我看时间规划。

1. **确认时间轴。** 按语义拆镜，保留原始时间、空白和录音中已读出的标题。按 `3–15` 秒整数档规划生成时长，实际可用参数以 Flow 面板为准。
2. **逐镜确认画面。** 选择比例和衔接方式，可用上一镜末帧作为下一镜的开场参考，也可用纯文生色场衔接。
3. **复制 Prompt 到 Flow。** 每镜交付经脚本校验和独立盲审的纯视觉英文 Prompt，并在正文外列出面板参数。出片后可针对错字、节奏或底色使用局部精修指令。
4. **交付成片。** 全部镜头确认后获得声画对照表。把生成片段发回 Codex，可按原时间轴校验、合并并对齐原口播。

## 文件

- [SKILL.md](SKILL.md) 提供工作流程和适用范围。
- [画面设计规则](references/mg-design.md) 和 [输出合同](references/output-contract.md) 记录分镜与 Prompt 要求。
- [首尾帧与局部精修](references/omni-iteration.md) 提供操作说明和示例。
- [交付校验](references/delivery-checks.md) 说明如何校验时间轴、Prompt、素材和成片。脚本使用 Python 3，媒体检查需要 `ffprobe`。
