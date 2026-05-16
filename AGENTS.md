# XDB agent instructions

## Purpose

本仓库是 Python CLI 工具，核心入口是 `XDB.py`，用于将 Excel/CSV 转换到 SQLite 或 MySQL，并提供字段映射、表名映射、分块并行处理和类型推断。

## Scope

本文件适用于整个仓库。进入 `scripts/`、`tests/`、`.github/` 时还要读取对应子目录的 `AGENTS.md`。

## Read first

- `README.md`：用户可见的 CLI 行为、参数和映射格式。
- `requirements.txt`：运行依赖来源。
- `XDB.py`：主程序、数据库抽象、映射、SQL 安全和 CLI 参数。
- `tests/test_xdb_regressions.py`：当前回归覆盖点。
- `.github/workflows/test.yml`：CI 中的回归测试和 MySQL/SQLite smoke。

## Local rules

- 保持 `XDB.py` 作为单文件 CLI 的现有边界；拆分模块前必须同步更新入口、测试和打包流程。
- 修改 CLI 参数、默认值、字段映射格式、表名映射格式或输出行为时，同步更新 README 和回归测试。
- SQL 表名/列名必须经过现有 `validate_sql_identifier`、`safe_sql_identifier`、`sanitize_table_name`、`sanitize_column_name` 等路径处理；不要把外部输入直接拼进 SQL。
- 保持表名优先级：`--table-mapping` 高于 `--target-table`，再回退到工作表名。
- 字段映射必须保留源列顺序和目标列类型对应关系；涉及 mapping、chunk、CSV/Excel 兼容性时优先补回归测试。
- `overwrite` 会删除并重建目标表。验证时使用临时 SQLite 文件或明确的测试 MySQL 库，不要指向用户现有数据库。

## Do not

- 不手动修改 `dist/`、`build/`、`__pycache__/`、coverage、PyInstaller `*.spec` 等生成或缓存产物。
- 不引入新的 package manager、格式化器、lint/typecheck 工具，除非同时提交配置和验证说明。
- 不提交非测试用途的数据库密码、token 或用户数据样本；CI 里已有的 `testpass` 仅用于测试服务。

## Validation

- 安装依赖：`python -m pip install -r requirements.txt`
- 通用回归：`python -m unittest discover -s tests -p 'test_*.py'`
- CLI smoke：用临时 CSV/XLSX 运行 `python XDB.py <input.csv> --db-type sqlite --sqlite-path <tmp.db> --target-table <table> --mode overwrite --quiet`
- 涉及 MySQL 写入时，参考 `.github/workflows/test.yml` 的 MySQL 8.0 服务和连接参数补充验证。

## Notes for future agents

仓库没有 `pyproject.toml`、`Makefile`、`Dockerfile` 或本地 lint/typecheck 配置；不要编造这些命令。当前测试框架是标准库 `unittest`。
