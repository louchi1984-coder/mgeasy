# MGEasy

**主要适配 Google Flow 的 Omni Flash 1.2（Omni 1.2）。**

MGEasy 是一个 Codex 技能，把主题、完整口播稿或 SRT 设计成 Google-like 动态图形（MG）分镜。每镜根据内容选择文字、图形或图表，再设计运动、视线和相邻镜头的衔接。

## 怎么用

将仓库放入 Codex 的技能目录。使用能访问此仓库的 GitHub 账号运行：

```sh
gh repo clone louchi1984-coder/mgeasy "$HOME/.codex/skills/mgeasy"
```

新开一个 Codex 会话，附上口播稿或 SRT，然后输入：

> 用 $mgeasy 把这份 SRT 做成 16:9 的 Google-like MG 分镜。生成目标用 Google Flow 的 Omni Flash 1.2，先给我看时间规划。

1. **确认时间规划。** SRT 保留原始时间轴和空白，按语义拆镜。用能覆盖实际镜头时长的最小档位规划生成时长，档位为 4、6、8、10 秒。
2. **确认画面。** 选择生成模型和比例，逐镜确认主视觉、运动、入场、出场及画面文字。可选参数以当前 Flow 界面为准。
3. **拿到生成材料。** 技能交付声画对照表、每镜可复制到 Google Flow 的英文 Prompt，以及记录镜头安排和生成参数的 JSON。

## 文件

- [SKILL.md](SKILL.md) 提供工作流程和适用范围。
- [画面设计规则](references/mg-design.md) 和 [输出合同](references/output-contract.md) 记录分镜设计和交付要求。
- [时间轴校验脚本](scripts/validate_timeline.py) 使用 Python 3 检查分镜计划 JSON 的字幕覆盖、时间间隔和时长档位。
