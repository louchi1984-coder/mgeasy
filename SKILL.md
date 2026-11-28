---
name: mgeasy
description: 将主题、完整文案、口播录音或 SRT 设计成 Google Keynote 2.5D 商业动效分镜，交付面向 Google Flow / Omni 的精简纯视觉英文 Prompt，支持首尾帧衔接、对话式局部微调，并按原时间轴校验与合并生成素材。用于商业级动态文字、磨砂玻璃 UI 与图形图表动效设计，不用于实拍写实或代码动画实现。
---

# MGEasy（Omni 2.0 · Google Keynote 2.5D 商业动效）

面向 **Google Flow / Gemini Omni** 的 Google Brand Studio / Material 3 风格 2.5D 商业动效分镜与交付工作流：先锁时间轴，再逐镜做信息与动效设计，最后经脚本硬校验与独立盲审交付高信噪比、可直接复制的导演级英文 Prompt，并支持首尾帧衔接、对话式局部修片与无损对轨合并。

## 工作流程

已有明确选择和批准状态直接沿用，不重复确认。

1. **接收输入**：接收主题、完整文案、口播录音或 SRT。只有录音时先获取带时间戳的转写；有录音和文案时以实际读法和录音时间为准，用文案校对字词；已有获准且与录音对应的字幕直接沿用。录音处理见 [references/timeline-rules.md](references/timeline-rules.md)。主题先形成口播和候选标题，纯文案默认保留原文；时效性事实和数据先核验。
2. **时间轴规划与校验**：完整读取 [references/timeline-rules.md](references/timeline-rules.md)，按语义规划 Shot，保留原始时间与全部空白，向上取整吸附到 `3–15` 整数秒（常规节奏建议优先控制在 `3–10` 秒）。保存为 `timeline-plan.json`，运行 `python3 -B scripts/validate_timeline.py <plan.json>`。
3. **第一次确认（时间轴门禁）**：向用户确认字幕、Shot 边界、真实时长、空白和生成档位；尚未确认时只交付时间规划表，不进入画面设计。
4. **确认生成参数与衔接模式**：确定生成模型、实际比例（在 Flow / Omni 面板设置并记录于 `delivery.json`，**不写入 Prompt 正文**）以及多镜衔接方式：
   - 推荐默认：`Gemini Omni Flash`、`16:9`（横屏）或 `9:16`（竖屏）；
   - 多镜衔接模式二选一：**首尾帧参考衔接**（Omni 推荐：上一镜末帧作为下一镜 Start Frame，转场自由且零色差）或 **纯文生色场接力**（独立并发生成时，用全屏纯色场无缝过渡）。
5. **逐镜设计（一次只做一个 Shot）**：完整读取 [references/expression-routing.md](references/expression-routing.md) 和 [references/mg-design.md](references/mg-design.md)。先用几句自然话把**当前这一镜**的设计思路讲给用户看：
   - 核心主体、2–3 个具体定制图形/UI 对象、连续形变对象、2.5D 前中后分层与画布色调；
   - **运镜与节奏设计**：AE 2.5D 摄像机怎么走、2–3 个时间段分别如何快起脆落（弹跳/瞬切/急推）；
   - **衔接设计**：有上一镜时说明如何承接（首尾帧接力或同色场展开）；有下一镜时说明结尾状态（首尾帧目标构图，或靠已有形体收成全屏纯色场）。**末镜（含单镜成片）**只设计内容收束，写清最后一帧定格画面，省略出场衔接。
   - **本轮到此结束**：回复以“请确认或修改。”收尾。设计思路不是表格，不是 Prompt。用户未明确回复前，不写这一镜的 Prompt，也不铺开后面的镜头。
6. **编写 Prompt、脚本硬校验与独立盲审**：用户确认当前镜设计思路后，完整读取 [references/output-contract.md](references/output-contract.md)，对照 [references/gold-examples.md](references/gold-examples.md) 中最接近的 1–2 条（多镜衔接再看 [references/gold-examples-continuity.md](references/gold-examples-continuity.md)）。写出 **140–220 词**的高信号纯视觉英文 Prompt，保存文件并更新 `delivery.json`，运行：
   `python3 -B scripts/validate_delivery.py <delivery.json> prompt --shot <id>`
   脚本通过后，按 [references/review.md](references/review.md) 另起独立子 agent 盲审一次（不传设计笔记），只修改不通过项；每次修改后重跑 `prompt` 校验。
7. **交付当前镜 Prompt 与局部修片支持**：交付可直接复制的英文 Prompt，并附上对应的 Flow 面板参数提示（比例 / 时长 / 是否需上传上一镜末帧）。**非末镜**以“请确认或修改。”收尾；**末镜**以“请确认这一镜、告诉我需要修改的地方，或在生成完成后把全部视频发给我合并。”收尾并结束本轮。若某镜出片后仅局部有瑕疵（如单个错字、节奏偏慢、底色微偏），按 [references/omni-iteration.md](references/omni-iteration.md) 给出 2–3 句 **Omni 对话式局部精修指令（Delta Edit）**，无需整段重抽。全部确认后补声画对照表。
8. **素材验收与成片合并**：用户上传素材后，按 [references/delivery-checks.md](references/delivery-checks.md) 核对实际片段、记录剪点与 `post_tasks`，运行 `intake` 校验。素材齐全后按原时间轴合并（生成片段统一剥离音轨，原口播原速对齐；无口播或要求静音时导出无音轨成片）。完成全部后期动作、通过 `final` 校验并复核关键帧与音画同步后交付成片。

用户只讨论原理时直接回答问题；单镜测试只规划指定 Shot。用户明确授权跳过某次确认时沿用其授权，未确定的必要参数仍需补齐。

## 核心红线

- **视觉定位（Google Keynote 2.5D 商业动效）**：通透抽象色场 + 纯平 2D 锐利动态排版（**默认无 3D 体积感**，除非用户明确要求）+ 4 种轻材质轮换（纯平哑光矢量色块、不透明 Material 3 实心色卡、克制点缀的磨砂玻璃 UI、精良 2D 商业插画——**避免连续多镜堆砌磨砂玻璃造成疲劳**）+ 干脆利落的 AE 2.5D 运镜与弹跳节奏；**绝不出现实景环境、真人实拍、物理镜头虚化或密集真软件截屏**。
- **高信噪比纯视觉 Prompt**：比例/时长/模型全交由 Flow 面板与 `delivery.json` 管理；Prompt 正文控制在 **140–220 词**，**禁止** `--ar`、JSON 数组白名单、Hex 色码、长串负面免责声明与 LLM 元指令。
- **文字空间绑定**：获准可见文字直接在场景描写中与对应物体、字号、位置绑定，使用粗几何无衬线高对比排版；易错长句提前降级交给口播或后期字幕。
