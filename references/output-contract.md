# 最终输出合同（Omni 2.0 · 3 类差异化导演规范）

当前 Shot 的时间轴、参数和设计思路经用户确认后，按本合同交付可直接粘贴到 Google Flow / Omni 的连续英文 Prompt（总词数建议 **140–220 词**，**90% 以上为纯正向视觉与动效信号**）。

## 交付内容

1. **Flow / Omni 面板参数提示**（给用户手动设置的 1 行摘要，不放进 Prompt 正文）：
   - 比例（`16:9` / `9:16`）、时长（`3s–15s` 整数秒）、衔接方式（首尾帧参考 / 纯文生色场接力 / 动势硬切）。
2. **可直接复制的英文 Prompt**（纯自然段落，无中英文模板标签、无 `--ar`、无模型名、无 JSON 数组、无 Hex 色码、无 `1px` 等 CSS 单位）。
3. 全部镜头确认后，补一份声画对照表（镜号、时间范围、档位、口播、表达方式、画面与动效要点、可见文字、衔接方式）。

---

## 规范 4 段式导演结构（按 3 类表达方式精准差异化）

### 1. 风格、媒介与一镜锁定（开头 2 句，按类型选用）
- **`direct_info` 直接信息（文字 / 数据 / 表格 / 清单）**：
  `Sleek Google Keynote kinetic typography and data motion graphics in Google Brand Studio and Material 3 expressive style — high-craft 2.5D graphic design featuring flat 2D bold editorial typography, precision data visuals and clean matte vector geometry on a luminous abstract color-field canvas. One continuous shot, no scene cuts.`
- **`visual` 视觉化展示（产品结构 / UI 元素化微剧情 / 图形隐喻）**：
  `Sleek Google Keynote commercial motion graphics in Google Brand Studio and Material 3 expressive style — high-craft 2.5D hybrid motion design blending crisp matte vector geometry, opaque Material 3 UI cards or restrained frosted-glass accents and flat 2D bold typography on a luminous abstract color-field canvas. One continuous shot, no scene cuts.`
- **`story` 剧情推动（精良 2D 商业插画人物 + 克制 UI，绝不用真人实拍）**：
  `Sleek Google Keynote commercial motion graphics in Google Brand Studio and Buck editorial 2D illustration style — high-craft 2.5D hybrid animation pairing a refined modern 2D illustrated character with clean Material UI cards on a luminous abstract color-field canvas. One continuous shot, no scene cuts.`
- **首尾帧参考模式（`continuity_mode: "start_frame"`，通用）**：
  `Continue seamlessly from the opening reference frame in sleek Google Keynote 2.5D commercial motion graphics style, preserving the exact opening graphic palette and crisp frosted-glass and vector aesthetic. One continuous shot, no scene cuts.`

### 2. 画布、2.5D 分层与**仅限首帧存在的**元素（2–3 句，按类型侧重）
- **严格因果铁律（防提前剧透）**：本段**只描写第 0 秒开场时真正存在的元素**；凡是在后半段才触发弹出的文字、卡片或遮罩，一律留到第 3 段对应时间段里再按先后依赖关系出场，**严禁提前写在本段**，也**严禁在画边提前停放一块等待转场的纯色板**。
- **`direct_info`**：强调**排版主权与数据精确比例**——写清大色面分割、悬殊字号层级、进度条/柱图/表格的清晰结构（基线轴、网格、表头，不极简到看不出），磨砂只做进度条或轻装饰。
- **`visual`**：强调**核心对象与一眼可辨结构**——写清起点物体与具体可辨特征（如视频卡带播放三角与进度条），同体变形锁死物理延续；文字压低篇幅只作短标签。
- **`story`**：强调**精良 2D 人物造型与极简舞台**——必须明确指定**人物性别**、现代发型、穿搭色、干净克制的五官神态与 2D 平面色块；周围悬浮磨砂 UI 卡片必须写明 `zero tiny text`。
- **可见文字直接空间绑定（严禁 `Display only these exact strings: [...]` JSON 数组）**：
  - 开场即见的文字写在本段；延迟触发的文字写在对应时间段并写明触发前置动作；均用英文双引号逐字写出并锁死 `bold geometric sans-serif typography with high contrast`。
  - 无文字镜写明 `purely visual graphic composition with no text`。

### 3. 快起脆落连续时间段（`[0–Xs]`、`[X–Ys]`，10 秒可选 `[Y–Zs]`）
- 整数秒连续覆盖 `0–{duration}s`，**严禁小数秒**。
- 动势重心差异化：
  - `direct_info`：侧重**锁格与强调**（`snappy pop-in`、`locks decisively onto the exact 72% mark`、阅读段镜头稳推不乱晃）；
  - `visual`：侧重**连续变形与强 2.5D 运镜**（`zero-lag morph`、`magnetic snap`、`whip-pan`、斜向穿推/指数急推）；
  - `story`：侧重**情绪微表演（一问一答）**（外部磨砂卡片弹出触发 → 人物眼神/眉毛/肩膀/手势反应 → 镜头推近定格情绪）。
- 结尾按选定衔接方式收束：
  - **首尾帧直连**：收在干净无残影、动势清晰的构图上供截帧；
  - **纯文生色场接力**：靠已有形体/大色块疾速扫满或急推填满全屏纯色场（用高辨识度色名，不用 Hex）；
  - **动势硬切 / 末镜**：干脆弹性定格在清晰可读的最终画面（跨镜硬切时让动势方向与下一镜自然顺接）。

### 4. 紧凑正向商业质感收尾（1 句）
`Refined Google commercial 2.5D motion design polish, snappy After Effects bounce-and-snap rhythm, dynamic 2.5D camera choreography, crisp accurate Chinese typography, clean silent visuals.`
*(剧情镜可微调为 `modern 2D editorial character contrasting with frosted glassmorphism UI`；无中文时写 `crisp bold typography`；无文字时写 `pure wordless graphic clarity`。)*

---

## 严禁出现在视频 Prompt 中的内容（脚本会自动拦截）

1. **Midjourney / 外部参数语法**：`--ar 16:9` 等一切 `--` 参数。
2. **JSON 数组白名单与模型名**：`Display only these exact strings: [...]`、`using Gemini Omni Flash ...`。
3. **Hex 色码、CSS/设计标注单位与冗长负面免责句**：`#E7F3F5` 等色码、`1px / 2px / pt / dp / rem`（一律改用 `hairline / ultra-thin`）、40 词中文免责句、26 词 Hex 免责句。
4. **LLM / 流程元指令与模板标签**：`Let the model choose`、`Build a more developed composition`、`planned preceding`、`for the next shot`、`Camera:`、`Subject:`、`Background:`、`背景：`、`主体：`。
5. **拉偏写实、真人实拍或廉价剪贴画的高危词**：`photorealistic`、`real-world`、`3D render`、`live-action`、`lens`、`icons`。
6. **小数秒微控制**：`[0.5–2.5s]`、`0.6s`。

## 交付前门禁

1. 运行 `python3 -B scripts/validate_delivery.py <delivery.json> prompt --shot <id>` 必须 `ok: true`（尽量清零 warnings）。
2. 通过 [review.md](review.md) 独立子 agent 盲审 6 项全部 `PASS`。
