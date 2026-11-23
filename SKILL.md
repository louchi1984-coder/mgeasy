---
name: mgeasy
description: 将主题、完整文案或 SRT 设计成 Google-like MG 动画分镜，交付 Google Flow 视频 Prompt 与 JSON。用于动态文字、图形与图表动画的内容设计，不用于其他画风、代码动画实现或成片剪辑。
---

# MGEasy

以“3 个 AI 会员”制作阶段的 Google-like MG 规则为基础，为 Google Flow 完成信息设计和分镜，保留该阶段的视角、配色、文字和跨片衔接规则。

## 工作流程

已有明确选择和批准状态直接沿用，不重复确认。

1. 接收主题、完整文案或 SRT。主题先形成口播和候选标题；完整文案默认保留原文。时效性事实和数据先核验。
2. 完整读取 [references/timeline-rules.md](references/timeline-rules.md)，按语义规划 Shot，保留原始时间与空白，向上吸附到 `4/6/8/10` 秒。SRT 计划运行 `python3 scripts/validate_timeline.py <plan.json>`。
3. 第一次确认字幕、Shot 边界、真实时长、空白和生成档位；尚未确认时只交付时间规划。
4. 确定生成模型和实际比例。可推荐 `Google Flow / Omni Flash`、`9:16`，推荐不能代替用户选择。本 skill 的视觉方向为 Google-like MG；已经调用 MGEasy 时无需再询问是否选择 MG。
5. 完整读取 [references/expression-routing.md](references/expression-routing.md) 和 [references/mg-design.md](references/mg-design.md)。逐镜完成内容意图、信息关系、主辅载体、运动任务、注意力路径、透视强度、背景和衔接设计。
6. 使用 MG 设计表完成第二次画面确认。画面确认后完整读取 [references/output-contract.md](references/output-contract.md)，交付声画表、每镜连续英文 Prompt 和 JSON。

用户只讨论原理时回答当前问题；单镜测试只规划指定 Shot。用户明确授权跳过某次确认时沿用其授权，未确定的必要参数仍需补齐。

## 输入与生成参数

- SRT 原时间轴优先，不归零、不删空白、不自动增加标题时长。非 SRT 默认增加独立 4 秒标题 Shot，`voiceover_text` 为空，标题原样保留；用户已有结构要求优先。
- 根据模型实际能力提供比例和时长，不能猜测当前支持范围。未确认 Flow 原生支持 `1:1` 时提供 `9:16` 或 `16:9`；需要方形成片时在已确认生成比例内设计中央方形安全区，记录 `crop_target_ratio`。
- 同一视频统一生成比例和 MG 视觉语法。章节可以换背景明暗、配色和主体；风格锁与玻璃感 UI 的边界服从 `mg-design.md`。
- 口播和后期字幕不等于画面可见文字。`visible_text` 单独确认，并与 Prompt 白名单一致。

## MG 设计

根据内容选择主体，文字不默认是中心，图表、图形、集合、具体操作或关系都可承担主表达。内容分类提供候选，不成为固定镜头模板。构图、几何组合、节奏和镜头路径保留模型发挥空间。

每个内容 Shot 只承载一个核心信息、一种主要表达方式和一次主要转变。按内容决定信息呈现顺序与注意力路径；需要阅读的信息要有足够阅读机会，已有焦点的关系和单位保持清楚。标题中的数字不能被复制成另一个焦点对象。

第二次确认表使用 `mg-design.md` 的列：

| Shot | 字幕范围 | 内容意图 | 信息关系 | 主表达载体 | 辅助载体 | 运动任务 | 注意力路径 | 透视强度 | 背景状态 | Entry | Exit | 共享元素 | 可见文字 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

视角随注意力设计，逐镜选择 `none`、`shallow` 或 `strong`，并写出实际层次与运动。相邻镜头先判断是否需要视觉连续；Flow 多个短片独立生成且无参考帧、又需要连续时，可优先使用全屏色场、遮罩或大形状等可靠桥接状态。

## Flow 时长和输出

- 4/6/8 秒使用两段粗时间，10 秒最多三段；根据内容和阅读需要选择整数秒分界，不要求均分。时间段连续覆盖完整生成时长，不写小数秒微控制。
- 各段围绕当前核心信息组织主要变化，信息可以先完整呈现，也可以在运动中逐步成立；不固定每镜为同一动作顺序。辅助元素按同屏视觉密度与主次组织，不以分组数量代替密度判断，具体规则见 `mg-design.md`。
- `actual_duration_seconds` 是原始连续区间，`duration_seconds` 是生成档位。真实时长、Prompt 和生成参数保持一致。
- 沿用制作阶段的颜色处理：Hex 只作为不可见颜色控制，最终 Prompt 包含 `output-contract.md` 指定的 Hex 禁显句。不要同时套用后来的“删去 Hex 禁显句”规则。
- 可见文字逐字保真，禁止翻译中文、伪文字和额外数字。最终生成视频无水印、无配音、无人声、静音。
- `visual_style` 固定为 `google-kinetic-mg`，MG 中间设计保存到 `style_specific.mg_design`。不要把设计分类标签和字段名输出成画面文字。

## 反馈记录

每次运行 `python3 scripts/self_learning.py validate`。状态不存在时运行 `init`。真实失败、用户纠正、第五次成功复盘或应用补丁时读取 [references/self-learning.md](references/self-learning.md)。用户接受结果后运行 `record-success`；未验证候选不影响当前设计。

学习状态独立保存到 `~/.mgeasy/learning-state.json`，不读取或继承 VoxEasy 的旧候选和成功计数。
