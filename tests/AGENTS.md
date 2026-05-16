# tests navigation card

`tests/` 保存 XDB 导入正确性的快速回归覆盖。
修改测试、fixture、CLI subprocess helper 或数据库 fake 前先读本卡片。
关键文件：`tests/test_xdb_regressions.py` 以及 `XDB.py` 中对应被测代码。

## Local invariants

- 使用标准库 `unittest`；保持 `python -m unittest discover -s tests -p 'test_*.py'` 可发现。
- CLI 测试用 `sys.executable` 调仓库根目录 `XDB.py`；不要依赖 shell alias、已安装包或偶然 cwd。
- 临时 CSV/XLSX/SQLite 文件放在 `tempfile.TemporaryDirectory()` 或等价可丢弃位置。
- MySQL 单元行为优先用 fake connection/cursor；真实 MySQL 默认交给 CI smoke，除非用户要求 live 验证。

## Local rules

- 修复 mapping、chunk、append/overwrite、SQL identifier、CSV parsing、Excel merged-cell 或 rollback 时，补一个修复前会失败的回归测试。
- 保留 subprocess stdout/stderr capture，让 CLI 失败可诊断。
- 测试不得依赖执行顺序、用户数据库、本机绝对路径或仓库外样本。

## Do not

- 不从测试向仓库根目录写持久 `.db`、`.xlsx`、`.csv` 或日志。
- 不因为场景难搭就跳过断言；用小型合成 fixture。
- 不把测试目录改成 `pytest`，除非仓库新增依赖并更新 CI。

## Validation

- `python -m unittest discover -s tests -p 'test_*.py'`
