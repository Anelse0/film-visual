# 验证摘要｜1.3.0

验证日期：2026-09-24。本轮完成 MJ 官方提示指南调研、编写方案与实现，未调用图像/视频生成服务。官方结论、来源、核对日期及非官方预算约定统一保存在 [MJ 模块](../film-visual/references/midjourney.md)，不另留重复开发设计稿。

## 调研如何进入实现

- 官方基础指南要求清楚、具体、简洁；新版 Describe 同时支持更详细的 V8.1/V8.2 描述。因此采用按任务复杂度的编辑软预算，不设未经核对的 token 硬上限。
- 单独 MJ 路由区分普通出图、Image Prompt、Style Reference 与 Edit Model。普通出图写最终画面，Edit Model 保留指令式修改能力；GPT Image 与视频 LOOK 不套 MJ 英文预算。
- 先锁定主体与关键关系，再压缩重复描述、无关修饰及操作话术，最后检查语义、词量与参数。三档 20–50 / 50–90 / 90–140 词均是本 Skill 的约定，允许为必要内容超出，用户明确限制优先。
- 新增 [只读词量工具](../film-visual/scripts/check_mj_prompt.py)，计量英文正文，排除 URL 与参数，保留引号文字计数；不计算 MJ token、不截断、不生成、不写文件。用户硬上限才触发非零超限退出码。
- 当前参数兼容性与来源集中维护，处理 V8 正文 `::` / Quality 不兼容、`--no` 误伤、画面文字引号及真实参考地址等问题。

## 实际行为结果

通过 **8 项新版任务 + 1 项同请求旧版对照**。下表判定来自开发 Agent 阅读实际输出、工具记录和独立计数，不是关键词打分或盲评。每项只一次正式采样，没有失败重采样；判据在 [cases.md](../film-visual/tests/cases.md) 中预先列出。

| 用例 | 正文词数 | 实际结果 |
| --- | ---: | --- |
| M01 球场登记区与参考图 | 125 | 真正看图；保留板邻桌、通道、球员散聚、手套、脚边包、后侧来宾双向视线、灰 T 恤和上午；场地背景压缩，正文直接描述画面 |
| M02 灰陶杯 | 28 | 单主体简洁成稿，不为凑长补无关设计 |
| M03 灰色训练 T 恤 | 66 | 保留立体穿着、自然撑起与垂坠、不可见支撑、白底、单件范围，未变平铺 |
| M04 V8.2 Edit Model | 79 | 真正看图；英文修改指令只改变照明，保留原布局、视角与对象，没有伪造上传 URL |
| M05 明确最多 70 词 | 62 | Agent 实际调用词量工具；独立复核同为 62；保留桌/板、入场通道、前后人群、视线、手套/包和双引号 CHECK IN |
| M06 V8.2 不兼容参数 | 57 | 先说明 `::` 和 `--q 4` 不兼容，再给普通描述替代；未声称实现精确 2:1 权重 |
| M07 77-token 说法 | 不适用 | 纠正未经核对的统一截断上限；区分官方资料与 Skill 编辑预算，不伪造 tokenizer 计量 |
| M08 GPT Image 中文编辑 | 不适用 | 真正看图，中文完整保留局部提亮与现有夕照/布局要求，没有强改英文或压成 MJ 关键词 |

英文计数采用随包工具定义：连字符/含撇号词合并，数字计数，URL、参数与正文外说明不计。M07 是中文规则问答，M08 是非 MJ 编辑，不纳入英文 prompt 词量评价。

**同请求对照：1.2.0 的 B01 为 229 词，1.3.0 的 M01 为 125 词，减少 104 词（约 45%）。** 两次均保留核心场景要求；新样本主要减少重复的左中右布局说明、背景铺陈和操作句。这个结果证明该样本更精练，不证明生成质量提升 45%，也不代表跨任务的稳定胜率。

M01 实际成稿：

```text
Sharks baseball field entrance on a Monday morning, cinematic realism. Eye-level oblique wide view: a lineup board stands beside the chain-link entrance fence, with a registration table immediately next to it. A clear passage beside the table leads through the open gate onto the field. Players crowd irregularly outside the table, all wearing matching gray training T-shirts with natural drape. Some tuck baseball gloves under their arms; others have training bags at their feet, clear of the passage. Several guests stand behind and slightly beside the players, with unobstructed views of both the board and the players ahead. Full figures and bags remain visible. Coastal greenery and stone buildings frame the field beyond. Neutral morning sunlight from the side, soft shadows, restrained greens and grays. --ar 16:9
```

## 环境与确定性验证

- Codex CLI 0.155.0-alpha.16.3；实际模型均为宿主默认 **gpt-6-astra**，未指定模型覆盖。相同前缀与球场请求分别用于 B01/M01，新会话不继承开发对话、判据或其他案例答案。
- 9 个会话的 Skill 目录均只有 film-visual；新版从 1.3.0 ZIP 安装，旧版从清理提交中的 1.2.0 ZIP 安装。全部命令成功，8 个新版安装副本逐文件与发布源码一致。
- M01/M04/M08/B01 各有 1 个实际返回的本地图片视觉输入块。原图不随源码、安装包或报告分发。
- 外层 macOS 沙箱限制写入本次 work，拒绝读取其他 Skill、插件、开发源码和其他案例目录；只有在外层保护内关闭 CLI 内层沙箱。实际探针：本案 Skill 可读，其他影视 Skill、源码、旧版项目和 work 外写入均 OS denied。
- 独立运行目录与认证只读链接；插件、Apps、联网检索、图像生成等功能关闭，系统 Skill 按路径禁用。未改全局 Skill 或其他项目。
- 标准库测试在源码与 ZIP 解压副本各 **16/16 通过**：原有 10 项 + 新计量 6 项，覆盖引号内参数样式文字、URL/参数排除、不截断、中文不误报、输入错误、硬上限及文件字节不变。
- skill-creator 格式检查 **Skill is valid!**；PyYAML 仅临时安装用于校验。ZIP 共 **18 个文件**，CRC、SHA-256 与逐文件源码一致性检查通过。

发布包 SHA-256：`b0c4d26ab06e826fc954f4a2a1aa384e40289b28cd82922df7b06357b062d509`。

复核：`python3 tools/build_release.py --check`。源码测试命令见 [README](../README.md)。按工作区清理要求，仅保留此摘要及可复用源码/测试；本轮完整运行日志、测试项目、参考副本、临时认证链接与依赖在验证后删除，不宣称这些临时文件仍可访问。

## 待测与历史

**MJ 实际生成、参数在用户账号入口的运行、压缩前后画质、参考保持和视频连续性均待测。** 本轮没有登录 MJ 执行生成、Describe 或上传；词数及文本行为不替代成图检查。

[1.2.0 服饰验证摘要](https://github.com/Anelse0/film-visual/blob/b53aa2f/docs/VALIDATION.md)与更早完整记录保存在 Git 历史。现行 dist 只保留最新独立安装包。
