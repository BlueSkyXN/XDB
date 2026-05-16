# tests agent instructions

## Purpose

`tests/` 保存 XDB 的回归测试，重点覆盖字段映射、列顺序、类型推断、SQL 标识符清理和数据库写入行为。

## Scope

适用于 `tests/` 下的所有测试文件和测试 fixture。

## Read first

- `tests/test_xdb_regressions.py`
- `XDB.py` 中被测函数或类。
- `.github/workflows/test.yml` 的 CI 测试步骤。

## Local rules

- 使用标准库 `unittest` 风格，保持 `python -m unittest discover -s tests -p 'test_*.py'` 可发现。
- 需要调用 CLI 时使用 `sys.executable` 和仓库根目录的 `XDB.py`，避免依赖 shell alias 或当前目录偶然状态。
- 测试文件、SQLite 数据库和输出结果必须放在 `tempfile.TemporaryDirectory()` 或等价临时位置。
- 单元级 MySQL 行为优先用 fake connection/cursor；需要真实 MySQL 时对齐 CI 的测试服务参数。
- 修复 mapping、chunk、append/overwrite、SQL 安全或 CSV/Excel 解析问题时，添加能失败再通过的回归测试。

## Do not

- 不让测试依赖执行顺序、用户本机数据库、固定绝对路径或仓库外部样本文件。
- 不在测试中写入持久 `.db`、`.xlsx`、`.csv` 或日志文件到仓库根目录。
- 不吞掉子进程 stderr/stdout；CLI 失败时要能看见诊断信息。

## Validation

- `python -m unittest discover -s tests -p 'test_*.py'`

## Notes for future agents

当前测试目录在 CI 中先于完整 CSV/Excel/MySQL smoke 执行；这里适合放快速、可本地运行的回归用例。
