# Film Visual 1.0.0

可独立安装的影视视觉 Skill。入口为 [SKILL.md](SKILL.md)，方法、模板与工具均在此目录。无需其他影视 Skill、开发参考包、剧本格式、API 密钥或第三方 Python 包。语言与视觉判断由宿主模型提供；这不是离线语言模型，也不自带图像/视频生成器。

## 使用入口

在能读取本地文件的 Agent 中直接说：

> 请读取此目录的 SKILL.md，并使用 film-visual：给一个年轻夜店 club 的 MJ 场景 prompt，16:9，不要暗黄。只要一条。

已由宿主发现 Skill 后可使用：

> $film-visual 给停车层的视频画面基调。

> $film-visual 只改下面 prompt 的 LOOK 段，其他文字保留，给完整修订稿：……

> $film-visual 只审阅这张实际附件的视觉问题，不生成、不保存。

编辑特定原图需提供实际图片；仅文字任务不用上传图片。输出默认留在对话，只有用户要求才写文件。生成服务调用与媒体上传不在本版本中。

## 安装到指定项目

先把独立压缩包解压为 `film-visual/`，从该目录运行：

```sh
python3 scripts/install.py --workspace /absolute/path/to/authorized-project
```

只复制到该项目的 `.agents/skills/film-visual/`；要求项目目录已存在，拒绝已有同名 Skill 和符号链接父目录，不覆盖全局安装。不要将全局配置目录作为项目路径。用户授权仅及当前工作区时，仅在该工作区内使用此命令。

在目标项目打开新任务，输入 `$film-visual`。若宿主未刷新发现列表，直接指定完整 `SKILL.md` 路径读取即可，不必修改全局设置。[官方 Codex 本地技能发现说明](https://learn.chatgpt.com/docs/build-skills)于 2026-09-22 核对，项目位置为 `.agents/skills`。其他宿主可显式读取入口，但其自动发现/安装未在此版本承诺通过。实际验证范围见交付包外层的测试报告。

## 本地检查

Python 3.9+ 标准库即可：

```sh
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

测试使用本 Skill 的临时目录，不读取其他仓库。它检查路径、模板与精确替换边界；不证明视觉质量。真实语言行为场景见 [cases.md](tests/cases.md)，须实际运行并保存输出，不能把案例清单当作通过记录。

文件精确替换的使用与限制见 [video-look](references/video-look.md)。该工具不自动解析视频 prompt，不确认用户授权，也不自动修改源文件。

## 内容与状态

- [视觉开发与审阅](references/visual-development.md)：作品、地点、状态、机位及可见问题判断。
- [图像提示词](references/image-prompts.md)：MJ / GPT Image、身份与素材职责、官方适配来源。
- [视频视觉](references/video-look.md)：直接基调、按区间修订、跨场照明和可选测试文本。
- [作品模板](templates/visual-bible.md)、[场景模板](templates/scene-visual.md)：按需使用，不要求用户先填表。

没有预装真实项目图片、角色或审美实例。本次只提炼交付参考中的通用方法；不打包其原文和资产。未附第三方素材授权或自行宣告其开源许可。

源码可用、文本边界通过、Agent 行为通过、图像通过、视频通过是不同状态。实际生成画质与动态效果需另行授权后验证，未运行就保持待测。
