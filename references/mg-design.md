# Google-like Kinetic MG

这是 MGEasy 的 MG 设计原理层，沿用“3 个 AI 会员”制作阶段的规则。用于 `MG`、`motion graphics`、`Google-like MG`、`kinetic MG`、`文字图表 MG`、`谷歌 MG 动画` 等方向；根据内容设计画面，不把 Google-like 词汇机械塞进每条 Prompt。

## 1. 设计顺序

MG 先做信息设计，再做画面和运动：

```text
内容意图
→ 信息关系
→ 主表达载体
→ 辅助载体
→ 运动任务
→ 注意力路径
→ 透视强度
→ 衔接策略
→ 连续性对象
→ 背景状态
→ Prompt 压缩
```

不要先假设文字、路径、卡片或图表一定是主体。主体由当前 Shot 的内容意图决定。

自由度原则：本文件只约束信息判断、可读文字、连续性、背景洁净度和禁止项；不要把下列分类当成镜头模板。逐镜判断主表达载体、构图关系、运动任务和视角强度是否适合内容；已有视觉关系适合时可以延续，不为差异强行重新设计。允许大模型在这些边界内自由选择合适的几何组合、镜头路径、节奏和转场。不要写成“某内容类型必然对应某图形”的填空题。

整片风格锁：同一条视频的所有 Shot 必须保持同一套 Google-like MG 视觉语法。章节颜色、背景明暗和主表达载体可以变化，但渲染方式始终是干净色场、粗体排版、扁平矢量几何、遮罩、缩放、视差和动态 MG 透视。透视不是 3D 科技空间，而是通过大前景形状、中景文字、背景色场、尺度变化、斜向构图、推拉镜头和视差建立层次。不要因为进入 coding、Agent、模型或深色章节，就漂移成暗黑科技广告、真实软件界面或电影化 3D 空间。玻璃感 UI 层可在内容需要时克制使用，但不能成为默认风格或压过 MG 色场、排版和矢量几何。

## 2. SRT 输入

如果用户给 SRT：

- 先按 `timeline-rules.md` 做 Shot 边界，保留原始时间、空白和吸附时长。
- 不要一条字幕机械等于一个动画；按观点、例子、数字解释、流程步骤、操作链或总结判断合并。
- 第一次确认仍只确认字幕、时间、空白和吸附时长。
- 参数和风格确认后，第二次确认改用 MG 设计表；确认前不输出最终 Flow Prompt。

MG 设计表列：

| Shot | 字幕范围 | 内容意图 | 信息关系 | 主表达载体 | 辅助载体 | 运动任务 | 注意力路径 | 透视强度 | 背景状态 | Entry | Exit | 共享元素 | 可见文字 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## 3. 内容意图

每个 Shot 先判断它主要在做什么：

- `judgment`：观点、钩子、推荐、结论。
- `quantity`：价格、额度、比例、次数、容量。
- `comparison`：两个或多个对象的大小、强弱、取舍。
- `process`：步骤、工作流、前后因果。
- `collection`：功能集合、资产集合、分类集合。
- `operation`：读文件、改代码、跑命令、写测试等可执行动作。
- `relationship`：连接、远程控制、系统能力、工具网络。
- `summary`：最终归纳、三列推荐、选择清单。

## 4. 信息关系

再判断观众需要看懂哪种关系：

- 层级：主次、核心和辅助。
- 数量：额度、计数、容量。
- 因果：A 触发 B，资料变成视频。
- 选择：从很多选项收束到少数。
- 连接：节点、设备、工具之间的关系。
- 顺序：先后步骤、任务链。
- 分类：同类集合、三列归纳。
- 状态变化：混乱到整理、待办到完成。

## 5. 主表达载体

按内容选择主视觉，不要套固定模板：

- 判断/观点：文字块、关键词、数字焦点可以做主体。
- 数字/额度：计数器、条形图、刻度、容量块可以做主体。
- 流程/工作流：时间线、步骤链、路径可以做主体。
- 集合/分类：网格、堆栈、模块组可以做主体。
- 操作/代码：光标、文件树、终端线、测试状态可以做主体。
- 连接/系统能力：节点、线、设备关系可以做主体。
- 总结/推荐：排版结构、列、清单可以做主体。

这些是候选，不是死规则。若当前句子的含义更适合别的载体，优先内容。路径、圆点、图表或文字块可因信息关系或视觉连续而延续，也可按内容变化；不要机械重复，更不要为了不同而强行更换。

## 6. 辅助载体

辅助元素围绕主关系、共同动作或构图节奏组织；下列是可选载体，不是需要凑齐的清单：

需要辅助元素时，优先从当前主题、内容和信息关系中寻找有意义的视觉线索，让它们帮助表达主体；不要用无关碎片机械填空。抽象点线、色块等仍可用于强调、衔接或节奏，不要求每个形状都具象，也不固定造型、数量、位置或运动。

- 点：焦点、选择、转场种子。
- 线：连接、方向、步骤，不默认每段都用。
- 色条：节奏、品牌动势、章节提示。
- 图标化模块：功能集合。
- 网格：资产或分类集合。
- 图表：数量、对比和增长。

背景元素只能是低密度抽象几何，不承载文字信息。

以同屏可见的独立形体、细碎程度和视觉竞争判断密度，不以“几组”判断。允许多种造型与装饰性元素，但应有清楚主次和留白，避免多个独立小场景同时围绕主体铺开。优先通过已有元素的形变、尺度变化和接续进出获得丰富度，不在每次变化后累积一套新元素。减少杂乱时只调整密度和组织，不擅自压成单一载体，不固定形状、位置或运动轨迹。Prompt 写当前镜头需要的密度方向，不罗列一长串装饰种类，也不逐个规定进出路径。

干净指信息层级清晰、焦点明确、背景不干扰阅读，不等于画面稀疏、主体简陋或大面积空白。可以用围绕同一信息关系组织的粗体排版、几何组合、前后景遮挡、尺度差和连续运动增加表现力。不要为了补细节，将抽象概念机械地翻译成芯片、云朵、建筑或人物插画；具体对象能直接解释内容时仍可使用。

## 7. 运动任务

每个 Shot 只选一个主运动任务：

- `reveal`：让信息出现。
- `focus`：把注意力推到关键词、数字或对象。
- `transform`：对象变成另一个对象。
- `connect`：建立两个对象关系。
- `compare`：展示数量或优先级差异。
- `sequence`：展示步骤和先后。
- `assemble`：多个元素组装成结构。
- `resolve`：收束成结论。

4/6/8 秒使用两段粗时间；10 秒最多三段。按内容和阅读需要选择整数秒分界，覆盖完整生成时长，不强制均分。不要写 `0.6s` 等细时间控制；结尾按内容与实际衔接需要设计，不默认每镜静止或全屏转场。

## 8. 注意力路径和视角

视角跟随注意力，不按内容类型预设。

按当前内容写清观众的注意力路径，例如：

```text
先看到哪个对象或信息
→ 其余信息如何成立，注意力如何转移
→ 构图或镜头如何跟到它
→ 需要视觉连续时如何衔接下一 Shot
```

透视强度必须逐 Shot 选择，不要一律轻微：

- `none`：正面、稳定、排版优先。适合完整标题先读清、总结锁定、密集文字白名单。
- `shallow`：小幅推近、轻视差、轻重构图。适合普通解释、模块展开、任务词扫描。
- `strong`：明显推近、快速重构图、斜向空间穿越、前中景尺度差。适合开场钩子、章节切换、关键数字、强焦点对象和最终收束。

选择 `shallow` 时仍需让透视和空间层次可感知，而非退化为完全正面平面。可按内容用克制的斜向构图、前中后景、尺度差、轻视差或小幅镜头运动实现；具体组合和路径留给画面设计，不要求每项同时出现。`none` 仍可按内容使用。

强透视可以用，但必须满足：

- 有阅读任务时留出足够阅读机会；信息可以完整呈现后聚焦，也可以随运动逐步成立。
- 只强化一个焦点对象，不同时强化多组元素。
- 不牺牲中文白名单可读性。
- 不靠复杂背景透视线制造空间感。

风格锁不等于压平画面。即使保持扁平 MG，也要按 Shot 需要使用动态 MG 透视：大前景形状快速掠过，中景文字保持可读，背景色场提供层次，斜向构图、尺度变化、视差和镜头推拉共同制造空间感。避免只写 `shallow` 或 `strong`，却没有写出具体层次方法。
- 不得变成 2.5D 卡片世界、浮空盒子、阴影面或无意义透视背景。

强化已有焦点时保留理解它所需的关系和单位，不凭空复制焦点，也不把信息简化成孤立的装饰物。焦点可以是数字、文字、图形或真实主体，由内容决定；强推近只是可选的运镜，不是每镜默认动作。

### 按需使用的连续标题镜

当用户选择“纯色开场 → 标题动态出现 → 纯色结尾”时，先从纯色背景开始，再让完整标题和与主题有关的辅助元素动态建立，给予标题足够阅读机会；之后由当前画面自然进入纯色。若用户选择轻度透视，在标题构图可见时呈现可感知但克制的前后层次，不把“轻度”省略成无透视。

时间段只描述同一段连续视觉演变的不同阶段，不因分段而停顿、重置画面或切镜；已确认的景别变化与运动强度仍须保留。结尾可用遮罩，也可聚焦到画面中已有的对应颜色直至铺满画面；按内容选择，不固定配色、遮罩形状或运动路径。该方案按用户需求选用，不作为所有标题镜的默认模板。

## 9. 背景状态

背景的明暗、饱和度和章节变化按内容与用户偏好选择，确保文字对比和整片视觉语言协调。以下浅色仅为候选：

- `white`
- `very light gray`
- `very pale blue`
- `very pale green`
- `very pale yellow`
- `very pale cyan`

先在设计表写 `background_state`，例如：

```json
"background_state": "very pale yellow solid canvas for image-assets section"
```

最终 Prompt 只输出当前 Shot 的具体背景一句话，例如：

```text
Single very pale yellow full-frame MG canvas.
```

不要每段都塞整套背景规则。不要可读背景字、标签雨、复杂线图、彩纸片、阴影面。若画面太平，先增加中景主体层、浅视差或红黄绿蓝短色条，不靠背景噪音补。

深色章节仍按 MG 处理：写 `solid deep charcoal full-frame MG field` 或 `near-black full-frame MG model field`，不要写成沉浸式科技空间、隧道或真实终端环境。深色只是章节色，不是换风格；如需表达界面层级，可以加入克制的半透明玻璃 UI 层，但主体仍是 MG 排版、几何和色场。

## 10. 衔接策略和连续性对象

先判断相邻镜头是否需要视觉连续。需要时可考虑以下对象或状态；不需要时可以按内容或节奏切换：

- 点
- 模块
- 光标
- 节点
- 图表顶点
- 时间线头
- 网格格子
- 设备落点
- 排版列
- 全屏色场或全屏遮罩

写清：

```json
"entry_state": "...",
"exit_state": "...",
"shared_element": "..."
```

需要视觉连续时，下一 Shot 的 `entry_state` 应与上一 Shot 的 `exit_state` 真实对应。不需要连续时可直接按内容或节奏切换，`shared_element` 可为 `null`，不强行制造共享对象。

独立生成片段、需要视觉连续且没有上一条视频的最后一帧作为参考图时，不要依赖小点、细线、小节点或微小图形保持精确位置。可优先考虑更稳的桥接状态：

- 已出现的关键字、数字或图形放大到贴近镜头，填满整个画面。
- 结束为一个可复现的全屏实心色场、全屏几何遮罩或大面积纯净形状。
- 下一 Shot 从同一全屏状态打开、收缩、切开或显影出新主体。
- 不要为了衔接，把当前 Shot 的内容强行变成下一 Shot 的具体界面、软件窗口、设备局部、光标、路径端点或图表局部。具体界面应在下一 Shot 内部生成。
- 当前 Shot 可以交付全屏色场、大面积遮罩或大形状等抽象桥；下一 Shot 从该状态展开自己的主视觉。按内容选择具体动作，不必每镜使用同一种桥接或打开方式。
- `shared_element` 优先写抽象全屏状态，而不是小物件或具体 UI，例如写 `plain deep charcoal field`，不要写 `terminal window`；写 `blue signal field`，不要写 `pointer path`。

如选择全屏桥接，根据当前内容和剪辑需要确定转场时机，避免提前清空画面而打断主要信息；用户要求留白或停顿时按其要求设计。

生成档位长于真实音频区间时，不默认提前结束画面以便裁切。先保留完整结尾动作；实际剪辑中根据生成结果选择调整画面速度、剪点或重新生成，并检查桥接是否保留，音频默认保持原速。若尾部裁短不影响内容和衔接，也可以直接裁短；不得声称这些处理在生成前已验证成功。

示例逻辑：

```text
Shot A: printed 3 turns blue, pushes toward camera, and fills the frame as a clean solid blue field.
Shot B: start from the same solid blue full-frame canvas; the blue field opens as a mask to reveal the next subject.
```

小点、节点和图表顶点可以表达“语义连续”，但在无参考图的多视频拼接里，不要要求它们跨 Shot 精确同位。只有用户提供最后一帧参考图或同一生成片段内连续生成时，才写精确位置延续。

常见错误：

```text
错误：NotebookLM 的 PPT 页面最后变成 coding terminal，为下一条 coding shot 做桥。
正确：NotebookLM 的 PPT 页面推近并消失为 plain deep charcoal full-frame field；下一条 coding shot 从该深色场中生成自己的抽象 coding 动作。

错误：价格 shot 结尾留下 enlarged green cursor，下一条模型 shot 从这个 cursor 开始。
正确：价格 shot 的绿色确认脉冲扩成 near-black full-frame model field；下一条模型 shot 从该模型场显影出模型节点。
```

## 11. 文字规则

文字不一定是主体。它可能是主体、标签、数字锚点或完全不出现。

- 观点、产品名、价格、额度、任务词、最终推荐通常需要可读文字。
- 可见文字必须来自白名单，同屏不铺满密集小字。
- 白名单里的中文必须按原字形逐字显示；不要把中文翻译、拼音化、英文化、改写或拆成中英混排，除非白名单本身就含英文产品名。
- 英文只能出现在白名单已包含的产品名、模型名或术语中；不要把英文 prompt 描述词、风格词、字段词渲染成画面字幕或标题。
- 最终 Prompt 在可见文字白名单后必须补一句：`Preserve every Chinese character exactly as written in the approved text; do not translate, romanize, replace, or mix Chinese words with English words. English words may appear only when they are part of an approved visible text string; never render prompt-description words as captions.`
- 如果某个中文可见短语在生成测试中反复被翻译、错字或中英混写，不要继续堆叠否定词。改用文本安全降级：画面只保留该 Shot 的最短必要视觉文字，例如产品名、核心数字或关键词；被模型反复写错的时间单位、长句或修饰词交给字幕、口播或后期文字层承载。
- 文本安全降级后，`visible_text` 也必须同步缩短，避免 JSON 和 Prompt 白名单不一致。字幕和 `voiceover_text` 保留原文，不因画面白名单缩短而改口播。
- 标题里的数字若作为转场对象，不要生成第二个数字；应从已出现数字的位置、颜色或形体关系中转出。
- 背景不得使用伪文字、灰色碎字、模型名碎片或价格碎片表达“复杂”。

## 12. Prompt 压缩

MG 原理留在设计表和 JSON，不机械粘贴进 Flow Prompt。最终 Prompt 只写当前 Shot 的具体执行：

```text
style anchor + ratio + duration
current background_state
entry_state and shared_element when continuity is needed
primary carrier and support carriers
approved visible text
two or three coarse timeline beats
attention-led camera/composition move
perspective_intensity only when it changes the shot
full-frame transition bridge when cross-video alignment would be fragile
exit_state
Hex invisibility, no watermark, silent video
```

Prompt 要给模型留空间：写清结果、关系、注意力路径、限制和禁区，不要把每个元素的坐标、数量、入场顺序和微动作都列死。除非用户已经确认具体画面，不要反复使用同一句构图模板。

当一条视频有多个 Prompt 时，每条 Prompt 都要包含一句简短风格锁，例如：`Style continuity: keep the same flat Google-like MG visual system as the whole video; create dynamic MG perspective with large foreground shapes, midground typography, background color fields, scale changes, parallax, angled composition, and camera push/pull; depth must come from flat vector layers, not realistic 3D or cinematic tech scenery; subtle translucent glass UI layers are allowed only when they support the information hierarchy and must not replace the clean MG color-field and typography system.`

避免：

- 长篇设计理论。
- 固定内容类型镜头表。
- 模板填空式句子，例如每段都写同一种路径、同一种圆点、同一种卡片或同一种推近。
- `0.6s` 等小数秒。
- `Information logic:`、`Anchor:` 等会被误渲染的字段名。
- 英文提示语污染可见文字，例如把 `一个月30块` 生成成 `month30块`。
- 后半段因题材变化而风格漂移，例如 coding/Agent/model Shot 变成暗黑科技界面，前半段仍是干净 MG。
- 过多否定词堆叠。

## 13. JSON

在每个 Shot 的 `style_specific.mg_design` 中保留 MG 设计决策：

```json
{
  "style_specific": {
    "mg_design": {
      "content_intent": "quantity",
      "information_relation": "capacity comparison",
      "primary_carrier": "bar chart and large quota number",
      "support_carriers": ["model labels", "accent dots"],
      "motion_task": "compare",
      "attention_path": "establish the chart, move attention to the tallest bar, end on the quota number",
      "perspective_intensity": "strong for the final push toward the tallest bar, after the chart is readable",
      "transition_bridge": "the tallest bar top expands beyond frame into a full-frame color wipe if the next clip is generated separately",
      "background_state": "very light gray solid canvas",
      "entry_state": "amber passed-test dot",
      "exit_state": "full-frame color wipe",
      "shared_element": "full-frame color wipe"
    }
  }
}
```

`style_specific` 不替代公共字段；它只保存 MG 设计层，防止 Prompt 变长。

## 14. 交付前检查

- 是否先判断内容意图和信息关系，而不是直接套文字/路径/图表？
- 主表达载体是否服务当前句子？
- 是否给模型留下构图、几何组合、镜头路径和节奏的发挥空间，而不是模板填充？
- 整片是否保持同一套 Google-like MG 视觉语法，而不是不同章节换成不同广告风格？
- 辅助元素是否解释关系，而非装饰？
- 注意力路径是否符合内容并给予必要阅读机会；强化已有焦点时，其关系和单位是否清楚？
- 透视强度是否明确为 none / shallow / strong，并根据当前内容、注意力和可读性选择，而非按类型限制？
- 视角变化是否写出了具体 MG 层次方法：大前景、中景文字、背景色场、尺度变化、斜向构图、视差或推拉，而不是只写强弱？
- 多视频独立生成、需要视觉连续且无参考图时，是否选择可靠的桥接状态，而不是要求小元素精确同位？
- 当前 Shot 是否没有提前生成下一 Shot 的具体界面或软件窗口？
- 需要跨片连续且无参考帧时，`shared_element` 是否优先考虑可靠的大面积状态，而非依赖小物件精准同位？
- 需要视觉连续时，Exit 是否能真实接到下一 Shot 的 Entry；不需要时是否避免强造共享对象？
- 白名单中的中文是否有逐字保真约束，避免被翻译、拼音化或中英混写？
- 背景是否适合内容与用户偏好、保持文字对比，并避免无关的可读噪音？
- 深色章节是否仍以纯净 MG 色场为主，而不是漂移成暗黑科技空间或真实软件 UI？若使用玻璃感 UI 层，是否足够克制且服务信息层级？
- Prompt 是否只输出当前 Shot 决策，没有把本文件理论粘进去？
- 是否没有小数秒控制、假文字、重复数字和复杂背景线图？
