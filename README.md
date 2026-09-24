# Film Visual

独立的影视视觉开发 Skill，当前版本 **1.3.0**。直接处理视觉方案、场景与人物/服饰/道具设计、图像提示词、参考编辑指令和图片审阅、视频画面基调，以及已有 prompt 的授权视觉段修订。

不依赖或调用其他影视 Skill，不要求固定项目文件或上游工作流。文本与视觉判断由 Agent 宿主提供；本版本不自动调用生成服务、不上传媒体、不创作故事对白或完整正式分镜。

## 使用

源代码入口：[film-visual/SKILL.md](film-visual/SKILL.md)。可以让宿主直接读取这个文件，再给出视觉任务。例如：

> 使用 film-visual：给一个年轻夜店 club 的 MJ 场景 prompt，16:9，不要暗黄。只要一条。

> 使用 film-visual：只改下面 prompt 的 LOOK 段，其他文字保留，给完整稿。

编辑或审阅特定图片需要实际原图；普通文字任务不需要项目资料或 API 密钥。

## Midjourney 提示词

[MJ 编写模块](film-visual/references/midjourney.md)把视觉方案编译成一条可复制的 prompt，先保留主体、相邻/前后/通行/视线等关键关系，再删除重复修饰与操作说明。普通 Imagine 描述最终画面；Edit Model 允许直接写修改要求。参数和参考角色按官方说明核对，来源与日期随模块提供。

英文正文采用 **20–50 / 50–90 / 90–140 词**三档软预算，分别用于简单、一般与复杂任务。它们是本 Skill 的编辑约定，**不是官方 token 上限**；必要内容多时允许超出，用户明确的语言、长度和细节要求优先。只读词量工具可对正文复核，不自动截断、不估算 MJ token、不写入文件或调用生成服务。

> 使用 film-visual：把下面方案写成 MJ prompt，保留人物位置和入场通道，最多 90 个英文词：……

## 服饰资产

[服饰资产流程](film-visual/references/clothing-assets.md)覆盖资产范围、参考分工、成稿与审阅。默认采用**正面、白底、隐形人台式立体穿着展示**：衣服像被穿起一样有体积、松量与垂坠，人体及支撑不可见。

> 使用 film-visual：服饰资产设计，全队穿灰色训练 T 恤。

现在这类简短请求会直接使用立体展示，单件只画完整上衣；整套按同一穿着体上的搭配关系组合。展示参考不会自动变成款式参考：球衣的号码、品牌、护肩和下装不会被复制进普通训练 T 恤。用户明确要平铺、真人试穿或动画媒介时仍按该任务执行，道具流程独立。

[验证摘要](docs/VALIDATION.md)记录实际测试结果与待测范围。

## 审美方法

[设计方法](film-visual/references/design-methods.md)、[7 条影视依据](film-visual/references/style-cases.md)和[目标驱动的看图审阅](film-visual/references/visual-review.md)。它们已接入实际方案与 prompt 入口：

- 风格：将形状、线条、边缘、材质和明暗组织成相容的选择；备选方向说明区别和代价。
- 构图：处理人物/物件关系、视觉竞争、留白与边界；支持有意多中心和失衡。
- 画幅：按必留内容选择或重构；指出裁切、拉远、换机位与扩展区域的代价。
- 色彩与光线：区分环境大色块、主体、局部强调、本色与受光；黑白用灰阶和材料区分。
- 审阅：实际看图后把可见问题、局部修正和复查目标对应起来，保留有意颗粒、彩光和光泽。

例如：

> 使用 film-visual：设计亲近、朴素的双人修鞋铺画面，画幅未定。给首选、取舍和两个成图检查点。

> 使用 film-visual：为同一个雨天候车亭做木刻与透明水彩两个方向，分别给成稿，并推荐一个。

> 使用 film-visual：看这张图，保留粗颗粒与上方留白，只找最影响人物注意力的问题。

案例摘要区分主创说明与方法推导；原作品的角色、地点、配色不会成为项目默认。方法指导 Agent 作出视觉选择，不代表底层模型经过训练或生成画质已通过验证。

## 安装

下载 [独立安装包](dist/film-visual-1.3.0.zip)，解压后进入其中的 `film-visual/`：

```sh
python3 scripts/install.py --workspace /absolute/path/to/authorized-project
```

从本仓库安装则在仓库根目录运行：

```sh
python3 film-visual/scripts/install.py --workspace /absolute/path/to/authorized-project
```

仅复制到指定项目的 `.agents/skills/film-visual/`，拒绝覆盖已有同名目录。随后在该项目新任务中调用 `$film-visual`。没有修改全局配置的要求。更多说明见 [Skill README](film-visual/README.md)。

## 验证

Python 3.9+ 标准库即可运行源码测试：

```sh
cd film-visual
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

[验证摘要](docs/VALIDATION.md)记录确定性测试与隔离 Agent 用例结果，原始记录链接到 Git 历史。真实图像及视频生成效果均为 **待测**；文本行为通过不代表画质或动态连续性已验证。

本仓库不包含开发参考包、项目人物和图片、认证信息或本地运行日志。独立安装包仅包含 `film-visual/` 自身，校验值见 [SHA256SUMS](dist/SHA256SUMS)。

维护者可用 `python3 tools/build_release.py` 重建 ZIP，或用 `python3 tools/build_release.py --check` 核对当前发布包与源码逐文件一致。
