# Film Visual

独立的影视视觉开发 Skill，当前版本 **1.0.0**。直接处理视觉方案、场景与人物/服饰/道具设计、图像提示词、参考编辑指令和图片审阅、视频画面基调，以及已有 prompt 的授权视觉段修订。

不依赖或调用其他影视 Skill，不要求固定项目文件或上游工作流。文本与视觉判断由 Agent 宿主提供；本版本不自动调用生成服务、不上传媒体、不创作故事对白或完整正式分镜。

## 使用

源代码入口：[film-visual/SKILL.md](film-visual/SKILL.md)。可以让宿主直接读取这个文件，再给出视觉任务。例如：

> 使用 film-visual：给一个年轻夜店 club 的 MJ 场景 prompt，16:9，不要暗黄。只要一条。

> 使用 film-visual：只改下面 prompt 的 LOOK 段，其他文字保留，给完整稿。

编辑或审阅特定图片需要实际原图；普通文字任务不需要项目资料或 API 密钥。

## 安装

下载 [独立安装包](dist/film-visual-1.0.0.zip)，解压后进入其中的 `film-visual/`：

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

[验收摘要](docs/VALIDATION.md)记录了 10 项确定性测试、实际隔离 Agent 用例、首次失败和修复重测。真实图像及视频生成效果均为 **待测**；文本行为通过不代表画质或动态连续性已验证。

本仓库不包含开发参考包、项目人物和图片、认证信息或本地运行日志。独立安装包仅包含 `film-visual/` 自身，校验值见 [SHA256SUMS](dist/SHA256SUMS)。
