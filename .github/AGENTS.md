# .github agent instructions

## Purpose

`.github/` 管理 GitHub Actions：基础测试、MySQL/SQLite smoke、多平台 PyInstaller 构建和 Release 资产发布。

## Scope

适用于 `.github/workflows/` 下的所有 workflow。

## Read first

- `.github/workflows/test.yml`
- `.github/workflows/multi-platform-build.yaml`
- 根目录 `AGENTS.md` 的验证和安全规则。

## Local rules

- `test.yml` 是仓库当前最完整的行为验证来源：Python 3.11、依赖安装、`unittest`、CSV/Excel 到 SQLite/MySQL smoke。
- 数据库相关代码变化时，不要移除 MySQL 8.0 服务或 SQLite/MySQL smoke，除非提供等价覆盖。
- `multi-platform-build.yaml` 分别构建 XDB 主程序和 3 个 XLSX 辅助工具，并用 artifact 名称驱动后续平台包和 Release 包；重命名 artifact 时必须更新所有下载、打包和上传步骤。
- Release zip 期望按 `linux-x64`、`linux-arm64`、`windows-x64`、`macos-arm64` 输出，并包含 XDB 与 3 个 XLSX 工具。
- 当前版本号来自提交标题 `git log --format=%B -1 | head -1`；修改版本策略会影响 artifact 和 Release 名称。

## Do not

- 不在 workflow 日志中打印非测试密钥、真实数据库连接串或用户数据。
- 不把构建产物提交到仓库；artifact 和 release asset 由 Actions 生成。
- 不随意扩大 `contents: write` 权限范围；只在发布任务需要时保留。

## Validation

无法从仓库中确认专用本地 workflow 校验命令，优先运行根目录通用验证命令：`python -m unittest discover -s tests -p 'test_*.py'`。涉及 PyInstaller 命令时，对照 workflow 中的实际 install/build 命令检查依赖和入口文件名。

## Notes for future agents

这里的改动风险主要是 CI 覆盖下降和 release 资产命名断链；提交前用 diff 顺序检查 build、download、bundle、publish 四段是否仍匹配。
