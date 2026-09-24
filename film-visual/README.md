# Film Visual 1.3.0

可独立安装的影视视觉 Skill。入口为 [SKILL.md](SKILL.md)，方法、模板与工具均在此目录。无需其他影视 Skill、开发参考包、剧本格式、API 密钥或第三方 Python 包。语言与视觉判断由宿主模型提供；这不是离线语言模型，也不自带图像/视频生成器。

## 使用入口

在能读取本地文件的 Agent 中直接说：

> 请读取此目录的 SKILL.md，并使用 film-visual：给一个年轻夜店 club 的 MJ 场景 prompt，16:9，不要暗黄。只要一条。

已由宿主发现 Skill 后可使用：

> $film-visual 给停车层的视频画面基调。

> $film-visual 只改下面 prompt 的 LOOK 段，其他文字保留，给完整修订稿：……

> $film-visual 只审阅这张实际附件的视觉问题，不生成、不保存。

> $film-visual 服饰资产设计：全队穿灰色训练 T 恤。

服饰资产默认正面、白底、隐形人台式立体穿着展示：单件只展示该件，整套按穿着关系组合；保留衣服体积与垂坠，看不到人体或支撑。参考图的展示方式与衣服款式分开迁移。明确指定的平铺、真人试穿或项目媒介仍按当前要求处理。

编辑特定原图需提供实际图片；仅文字任务不用上传图片。输出默认留在对话，只有用户要求才写文件。生成服务调用与媒体上传不在本版本中。

MJ 提示词使用 [专用编写规则](references/midjourney.md)：先保留主体与空间关系，再压缩重复修饰。英文正文按内容采用 20–50、50–90 或 90–140 词的软预算，不是官方 token 上限；复杂任务可为必要信息超出。普通出图描述最终画面，Edit Model 可以直接写修改指令；用户明确词数或语言优先。

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
- [审美设计方法](references/design-methods.md)：风格、构图、画幅、色彩和光线的具体选择与取舍。
- [影视依据案例](references/style-cases.md)：六部作品及一项工作室流程的来源摘要、方法与迁移边界。
- [看图审阅](references/visual-review.md)：按目标判断，局部修正，比较方案和修订前后。
- [图像提示词](references/image-prompts.md)：MJ / GPT Image、身份与素材职责、官方适配来源。
- [Midjourney](references/midjourney.md)：官方依据、入口区分、描述取舍、词量预算与只读计量工具。
- [服饰资产](references/clothing-assets.md)：单件与整套范围、款式/展示参考分工、立体穿着成稿、服饰编辑与检查。
- [视频视觉](references/video-look.md)：直接基调、按区间修订、跨场照明和可选测试文本。
- [作品模板](templates/visual-bible.md)、[场景模板](templates/scene-visual.md)：按需使用，不要求用户先填表。

没有预装用户项目图片或角色。影视依据只包含可追溯短摘要与方法归纳，不打包来源文章和影视媒体；其风格不成为通用默认。B/D 仍仅提取方法，不带入项目实例。未自行宣告第三方素材的开源许可。

源码可用、文本边界通过、Agent 行为通过、图像通过、视频通过是不同状态。实际生成画质与动态效果需另行授权后验证，未运行就保持待测。
