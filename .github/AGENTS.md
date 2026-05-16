# .github navigation card

`.github/` 管理 CI、MySQL/SQLite smoke、多平台 PyInstaller 构建和 Release 发布。
任何 workflow、artifact 名称或权限改动前先读本卡片。
关键文件：`.github/workflows/test.yml`、`.github/workflows/multi-platform-build.yaml`。

## Why this is high-risk

- `test.yml` 是最完整行为 gate：Python 3.11、依赖安装、`unittest`、CSV/Excel 到 SQLite/MySQL。
- `multi-platform-build.yaml` 把入口文件、hidden imports、artifact 名称、平台包和 release upload 串在一起。
- Release 发布使用 `contents: write`；权限变化会影响仓库发布权。

## Required before changes

- 读取被改 workflow，追踪被重命名 job、artifact、path、platform 或 output variable 的下游消费者。
- 数据库行为改动必须保留或等价替换 SQLite 与 MySQL smoke。
- 打包改动要核对 install、PyInstaller、upload-artifact、download-artifact pattern、bundle layout、release upload。
- 保持平台集合有意为之：`linux-x64`、`linux-arm64`、`windows-x64`、`macos-arm64`。
- 当前版本号来自最新提交标题：`git log --format=%B -1 | head -1`。

## Do not

- 不移除 `test.yml` 的 MySQL 8.0 service，除非提供等价 MySQL 验证。
- 不提交构建产物；artifact 和 release asset 由 Actions 生成。
- 不把 `contents: write` 扩大到非发布 job，除非 workflow 确实需要。
- 不在 workflow 日志打印非测试 secrets、真实数据库 URL 或用户数据。

## Validation

- 默认本地检查：`python -m unittest discover -s tests -p 'test_*.py'`。
- 仅 workflow 改动时逐段检查 diff；不假设本地能执行 GitHub Actions。
- PyInstaller 命令需要 workflow 依赖安装步骤和平台构建环境。
