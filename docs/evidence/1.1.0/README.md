# 1.1.0 行为验证证据

这里保留 4 项旧版和 12 项新版的原始请求与实际输出。`baseline-A01.md` 等对应旧版，`candidate-A01.md` 等对应本次发布副本；不是手写的示范答案。除本机路径脱敏外未改写内容。

[behavior.json](behavior.json)额外保留统一前缀、实际模型与可用 Skill 列表、工具调用/命令、完成状态、耗时、源码清单、安装 ZIP/草图 SHA 和 A08 的字节核对材料。工具输入包含生成临时文本的代码，属于测试记录，不是要求读者执行的指令。不要将其中的占位路径直接当成本机路径。

## 复现任务

1. 把发布 ZIP 解压，用其 `scripts/install.py --workspace <authorized-test-project>` 安装到新的授权目录；旧版对照可用 Git 提交 `9225783` 中的源码另装一份。
2. 用新会话，确保 Skill 发现列表只包含 film-visual，不继承研究、评审和其他用例输出。实际输入为 behavior.json 中的 common_instruction 加 request。保持模型/宿主配置相同；报告每次实际模型，不能把新模型变化算作 Skill 收益。
3. A05 在测试项目放入匿名草图。开发环境需 Pillow，运行 `python3 tools/make_review_fixture.py --output <authorized-test-project>/waiting-room.png`。测试时必须实际打开图；只给文字不算看图验证。生成器是原始绘图源码，仓库不附 PNG、不上传媒体。
4. A08 从 behavior.json 的 byte_check.original_utf8 按 UTF-8 **字节写入** original.txt（不要转换 CRLF），让 Agent 写 revised.txt。独立核对授权正文外的字节与原件哈希，不能只接受 Agent 的自报。
5. 按 [行为用例](../../../film-visual/tests/cases.md)对应判据审阅输出。将是否符合目标、方法是否落实、保留项有无损伤和仍待测的结果分开记录。

本轮 CLI 核心参数：`exec --ignore-user-config --ignore-rules --skip-git-repo-check --json`，不指定模型；关闭插件、remote_plugin、Apps、image_generation、browser_use、computer_use、multi_agent，web_search 为 disabled。系统 Skill 用本次独立 CODEX_HOME 下各 SKILL.md 的精确路径配置 enabled=false。禁用方式核对了 [官方 Skill 文档](https://learn.chatgpt.com/docs/build-skills)，实际生效以会话 catalog 为准。

运行时用了限制写入与读取范围的外层 macOS 沙箱，因此 CLI 内层 sandbox 被关闭。**不得脱离外层沙箱照搬关闭内层沙箱的选项。** 本证据目录没有包含认证状态或自动执行脚本；复现者按自己的宿主设置等效隔离即可。其他系统尚未实测。

每个任务只做了一次正式采样；开发 Agent 按预定判据审阅，没有独立盲评。完整结论与限制见 [1.1.0 验收报告](../../VALIDATION-1.1.0.md)。
