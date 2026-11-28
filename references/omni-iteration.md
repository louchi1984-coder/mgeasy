# Omni 首尾帧衔接与对话式局部精修指南

发挥 Google Flow / Gemini Omni Flash 的两项原生优势，大幅降低多镜色差与抽卡返工成本。

---

## 一、首尾帧参考衔接（Start Frame Image-to-Video）

当用户选择“首尾帧参考衔接”时，跨镜不再强求每镜末尾拉满纯色屏，而是直接用**上一镜的干净末帧**驱动下一镜：

1. **截帧时机**：从上一镜满意视频的最后 0.2 秒内截取一张运动稳定、无残影的清晰静帧（PNG）上传至 Flow / Omni 作为下一镜的 Start Frame。
2. **Prompt 写作铁律（只写变化，不重描静态）**：
   - **不要**重新描述首帧里已存在的背景颜色、物体外形和静态布局（重描反而容易导致首帧跳变重绘）；
   - **专注写**：首帧中的哪个现有图形/磨砂玻璃卡片/色块如何以干脆的 AE 动效变形、甩镜滑出或急推缩放，进而带出下一镜的新主体与文字。
3. **`delivery.json` 标记**：在对应镜号下添加 `"continuity_mode": "start_frame"`，校验脚本会自动切换到首尾帧模式检验。

示例（承接上一镜末帧的“昆仑芯”卡片，甩镜滑入下一镜“80% 央企客户”）：

```text
Continue seamlessly from the opening reference frame in sleek Google Keynote 2.5D commercial motion graphics style, preserving the exact opening graphic palette and crisp frosted-glass and vector aesthetic. One continuous shot, no scene cuts.

[0–4s] With a brisk horizontal whip-pan and snappy After Effects ease-out, the opening chip module slides swiftly off the left edge while a sweeping soft pale-cyan architectural plane snaps across the canvas, revealing an oversized bold deep-indigo "80%" anchored beside a tiered cluster of rounded frosted-glass enterprise cards and crisp emerald shield emblems labeled "央企客户", "合规" and "可追责" in sharp high-contrast geometric sans-serif typography, leaving the bottom band clear. [4–8s] Without pausing, the 2.5D camera punches smoothly forward into "80%" with tight spring overshoot while foreground translucent glass framing tabs zip past the edges in energetic parallax, locking cleanly onto the crisp percentage-and-enterprise composition.

Refined Google commercial 2.5D motion design polish, snappy After Effects bounce-and-snap rhythm, dynamic 2.5D camera choreography, crisp accurate Chinese typography, clean silent visuals.
```

---

## 二、对话式局部精修（Delta Edit，不重抽盲盒）

如果 Omni 已经生成了构图、材质和运镜都非常满意的片段，**仅存在局部小瑕疵**，直接在当前视频对话线程里发送 **2–3 句「锁定（Keep）+ 精准改动（Change）」增量指令**，不要改写整段 Prompt 重抽：

### 1. 修正个别错别字 / 英文混写
```text
Keep the exact camera movement, pacing, frosted-glass UI cards, layout and color palette from this clip unchanged. Only correct the on-screen Chinese text so it reads cleanly and accurately as "最简单的文案配视频工具" and "MGeasy" in bold geometric sans-serif typography, with no extra characters.
```

### 2. 节奏偏慢，提速成更干脆利落的 AE 弹跳/瞬切感
```text
Keep the exact visual design, frosted-glass elements, typography and composition identical. Make the animation timing noticeably snappier and punchier with tighter After Effects exponential ease-out curves, faster transitions and crisp micro-overshoot settles, eliminating any slow drifting pauses.
```

### 3. 清除卡片内部杂字或角落噪点
```text
Keep the exact composition, camera choreography, main title and motion timing unchanged. Replace any tiny unreadable text inside the floating UI cards with clean minimalist horizontal color bars and solid graphic shapes so only the approved main typography appears.
```

### 4. 调整画布明暗 / 商业通透度
```text
Keep the exact animation, camera motion, frosted-glass cards and typography layout unchanged. Brighten the background canvas to a crisp luminous warm-ivory graphic studio field with clean high-contrast deep-indigo typography so the whole shot feels airier and more commercial.
```
