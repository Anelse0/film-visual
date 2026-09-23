# 1.2.0 服饰行为证据

C01–C09 保存真实请求和隔离会话的原始输出，不是手写示范答案。[behavior.json](behavior.json)另含统一前缀、实际模型、Skill 发现目录条目、工具输入、命令退出状态、视觉工具返回的内容类型、耗时、源码/安装包/参考图哈希，以及开发 Agent 的判据审阅。只替换了本机绝对路径；未改写回答。不保存认证状态、模型推理、图片数据或完整内部日志。

本轮每个任务仅一次采样，实际模型均为宿主默认 gpt-6-astra，未指定模型覆盖。9 个会话的 Skill 列表均只有 film-visual，且安装副本逐文件与发布源码一致。C07 有两次成功的本地图片视觉输入，C08 有一次；工具记录中的 `input_image` 只记类型，未分发图像。

## 复现

1. 将 1.2.0 ZIP 解压，以其中安装器安装到新的授权测试项目。
2. 在宿主中启用该项目的 film-visual，禁用其他 Skill、插件、Apps、联网检索及媒体生成工具。每个案例新建空会话，不传开发讨论、判据、其他案例答案或预期结果。
3. 输入 behavior.json 的 `common_instruction` 加对应 `request`。C01–C06/C09 无需图片；C07/C08 需要有权使用的原始本地参考。原图未公开分发，若采用其他图，只能记为等效用例，不能声称精确复现本轮图片测试。
4. 按 [预先定义的用例](../../../film-visual/tests/cases.md)审阅完整输出、实际加载模块和看图调用。文字设计与实际生成效果分开评价。

本轮环境为 macOS、Codex CLI 0.155.0-alpha.9.2。独立运行目录与 CODEX_HOME，仅临时只读引用现有认证状态。CLI 使用 `--ignore-user-config --ignore-rules --skip-git-repo-check --json`，关闭 plugins、remote_plugin、apps、image_generation、browser_use、computer_use、multi_agent，web_search 为 disabled；系统 Skill 使用其精确 SKILL.md 路径设 enabled=false。

外层 macOS 沙箱限制写入到本次 work 目录，拒绝读取全局 Skill/插件、开发源码、原交接包、解压源及其他案例项目。只有在该外层沙箱内才关闭 CLI 内层沙箱，不能脱离外层保护照搬该配置。实际探针确认当前安装 Skill 可读、其他受限路径及 work 外写入均为 OS denied。

验证后删除临时认证链接、日志、项目副本、图片副本和仅供格式校验的依赖。保留此处精简证据，不包含可直接运行的免确认脚本。完整结论与待测范围见 [验收报告](../../VALIDATION.md)。
