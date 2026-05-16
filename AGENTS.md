# XDB repository agent instructions

## Purpose

本仓库是 Python CLI 工具仓库。核心入口是 `XDB.py`，用于把 Excel/CSV 导入 SQLite 或 MySQL，并提供字段映射、表名映射、分块处理、并行处理、类型推断、CSV 参数处理和数据库写入验证。

## Codex startup behavior

- Codex 通常从仓库根目录 `/Users/sky/GitHub/XDB` 启动；本文件是启动期主规则。
- 子目录 `AGENTS.md` 是按需 navigation card；从根目录启动时不会天然进入上下文，必须按本文件的目录地图主动读取。
- 修改 `scripts/`、`tests/`、`.github/` 下文件前，先读取对应目录的 `AGENTS.md`。
- 如果从子目录启动，Codex 也可能自动加载路径链上的本地 `AGENTS.md`；仍以本文件的目录地图作为根启动 workflow 的 router。
- 如果新增目录需要独立职责边界、专属验证或高风险保护，只创建必要的 `AGENTS.md`；不要为了覆盖率给纯组织目录建空卡片。

## Directory map

| Path | Responsibility | Local AGENTS.md | Read when |
|---|---|---:|---|
| `XDB.py` | 主 CLI、数据库抽象、Excel/CSV 解析、映射、类型推断、SQL 安全和写入流程 | No | 修改导入行为、CLI 参数、数据库写入、字段/表名映射、chunk/并行处理、CSV/Excel 兼容性前 |
| `README.md` | 用户可见说明、参数语义、示例和映射格式 | No | 修改 CLI 参数、默认值、输出行为、映射语法或用户可见兼容性前 |
| `requirements.txt` | 运行依赖来源 | No | 新增、删除或升级 Python 依赖前 |
| `tests/` | 标准库 `unittest` 回归测试 | Yes | 新增或修改测试、fixture、CLI 子进程调用、数据库 fake/smoke 前 |
| `scripts/` | 独立 Excel 辅助工具和脚本文档，不是 `XDB.py` 核心导入路径 | Yes | 修改 `XLSX-split.py`、sheet cutter/merger、客户分类脚本、脚本配置或脚本文档前 |
| `.github/` | GitHub Actions 测试、MySQL/SQLite smoke、多平台 PyInstaller 构建和 Release 资产发布 | Yes | 修改 workflow、artifact 名称、release 权限、Python 版本、MySQL 服务或 CI 验证步骤前 |
| `.codex/` | 本地 Codex 相关元数据，当前不在 `git ls-files` 跟踪清单内 | No | 仅用户明确要求维护本地 Codex 配置时读取；不要把它当作仓库产品代码 |
| `.claude/` | 本地 Claude/agent 相关元数据，当前不在 `git ls-files` 跟踪清单内 | No | 仅用户明确要求维护本地 agent 配置时读取 |
| `__pycache__/`, `dist/`, `build/`, coverage 输出 | 缓存、构建或测试产物 | No | 不手动编辑；需要验证时删除/重建也必须先确认是否属于当前任务 |

## On-demand cat protocol

修改带有本地 `AGENTS.md` 的目录前，先读取对应文件：

```bash
cat <path>/AGENTS.md
```

如果目标路径上未来出现多层嵌套 `AGENTS.md`，按从浅到深的顺序读取后再修改。如果目标目录存在 `AGENTS.override.md`，先暂停并询问用户维护 override 还是调整策略；不要写入会被同目录 override 屏蔽的普通 `AGENTS.md`。

## Commands

| Command | Purpose | Scope | Sandbox notes |
|---|---|---|---|
| `python -m pip install -r requirements.txt` | 安装仓库运行依赖 | repo | 依赖未缓存时需要网络 |
| `python -m unittest discover -s tests -p 'test_*.py'` | 运行本地回归测试 | repo/tests | 默认本地验证；不需要外部数据库 |
| `python XDB.py <input.csv> --db-type sqlite --sqlite-path <tmp.db> --target-table <table> --mode overwrite --quiet` | 最小 CSV-to-SQLite CLI smoke | `XDB.py` | 只使用临时输入和临时 SQLite 文件 |
| `python XDB.py <input.xlsx> --db-type sqlite --sqlite-path <tmp.db> --target-table <table> --mode overwrite --quiet` | 最小 Excel-to-SQLite CLI smoke | `XDB.py` | 只使用临时 workbook 和临时 SQLite 文件 |
| `python XDB.py <input.csv> --db-type mysql --mysql-host 127.0.0.1 --mysql-user root --mysql-password testpass --mysql-database testdb --target-table <table> --mode overwrite` | CI 风格 CSV-to-MySQL smoke | `XDB.py` | 需要 MySQL 8.0 测试服务；不要指向用户数据 |
| `python scripts/XLSX-split.py -c <config.ini>` | 验证 `XLSX-split.py` 显式配置路径 | `scripts/` | config 中使用临时输入/输出路径 |
| `python scripts/XLSX-SheetCutter.py <input.xlsx>` | 验证 sheet cutter | `scripts/` | 使用临时 workbook |
| `python scripts/XLSX-SheetMerger.py <input1.xlsx> <input2.xlsx>` | 验证 sheet merger | `scripts/` | 使用临时 workbook |
| `python scripts/客户分类切割.py <input.xlsx> <output_dir>` | 验证客户分类切割脚本 | `scripts/` | 使用临时 workbook 和临时输出目录 |
| `pyinstaller --onefile --hidden-import=pandas,openpyxl,pymysql,tqdm,psutil,chardet,concurrent.futures,multiprocessing --strip XDB.py --distpath dist/<platform>` | CI 中的 XDB 二进制构建命令 | `.github/workflows/multi-platform-build.yaml` | 需要 PyInstaller 和平台构建环境；输出是生成产物 |
| `pyinstaller --onefile --hidden-import=csv,os,codecs,configparser,argparse,openpyxl --strip scripts/XLSX-split.py --distpath dist/<platform>` | CI 中的 `XLSX-split` 构建命令 | `.github/workflows/multi-platform-build.yaml` | 需要 PyInstaller；输出是生成产物 |

仓库没有 `pyproject.toml`、`Makefile`、`Dockerfile`、本地 lint 配置、本地 typecheck 配置或自定义 package manager 命令。不要编造 `make`、`pytest`、`ruff`、`mypy`、`poetry`、`uv`、`npm` 或 Docker 命令，除非仓库之后真实新增对应配置。

## Global rules

- 保持 `XDB.py` 作为单文件 CLI 边界。拆分模块必须同步更新入口路径、测试、打包 workflow、README 和 CLI smoke 说明。
- README 可见行为属于用户契约。修改 CLI flags、默认值、mapping 语法、表名行为、输出行为或用户依赖的错误信息时，同步更新 `README.md` 和回归测试。
- 保持表名优先级：`--table-mapping` 高于 `--target-table`，再高于源 sheet 名或 CSV fallback。
- 保持字段映射顺序和类型对齐。mapping 变更必须让源列顺序与目标列类型在 SQLite/MySQL 写入中保持一致。
- SQL 表名和列名必须经过 `validate_sql_identifier`、`safe_sql_identifier`、`sanitize_table_name`、`sanitize_column_name` 等现有路径；不要把未校验外部输入拼进 SQL。
- `overwrite` 会 drop 并重建目标表；本地验证必须使用临时 SQLite 文件或明确的可丢弃 MySQL 数据库。
- `append` 必须保留既有表语义；修改 append 时验证目标列匹配、缺列行为、行数、commit/rollback。
- CSV 处理必须保留显式 `--csv-encoding`、`--csv-separator`、`--csv-quotechar`、`--csv-no-header` 行为；不要用字符串切割替代结构化 CSV 解析。
- Excel 处理必须继续覆盖 sheet 选择、merged cells、header 提取和大文件 chunk；除非明确验证，不要无意增加内存占用。
- 并行/chunk 变更要检查测试依赖的行顺序、chunk 边界丢失/重复、异常传播和 rollback 安全。
- MySQL 行为优先用 fake connection/cursor 做单元验证；真实 MySQL 验证按 CI service 设置执行，服务不可用时可标注跳过。
- 生成文件、构建输出、缓存目录和用户数据输出不是 source of truth；应修改源脚本、workflow 或测试 fixture。

## Do not

- 不把 `dist/`、`build/`、`__pycache__/`、coverage 输出、PyInstaller `*.spec`、release bundle 或临时 CSV/XLSX/SQLite 输出当作源码修改。
- 不把验证指向用户真实 SQLite 数据库、MySQL schema、生产 host 或不可丢弃的 spreadsheet。
- 不引入新的 package manager、formatter、linter、typechecker、test runner 或 build system，除非同时提交配置并说明验证路径。
- 不移除 CI 的 MySQL 或 SQLite smoke 覆盖，除非同一改动提供等价检查。
- 不在日志或提交文件里打印非测试凭据、真实数据库连接串或用户数据样本；CI 的 `testpass` 仅限测试服务。
- 不重命名 CLI 入口、workflow artifact 或 release asset 路径，除非追踪 `.github/workflows/` 中所有消费者。
- 不在窄 bugfix 中混入大范围重构；行为改动要绑定可复现问题和回归测试。

## Validation

默认本地环境下，代码修改完成后：

1. 运行 `python -m unittest discover -s tests -p 'test_*.py'`。
2. 如果改动涉及 CLI parsing、CSV/Excel 输入、数据库写入或 mapping 行为，用临时文件运行 SQLite smoke：`python XDB.py ... --db-type sqlite ... --mode overwrite --quiet`。
3. 如果改动涉及 MySQL SQL、连接、commit/rollback 或 CI MySQL smoke，补 fake-connection 单元测试，或在可丢弃 MySQL 8.0 测试服务上运行 CI 风格命令。
4. 如果改动涉及 `scripts/`，用临时输入/输出运行 Commands 表中的对应脚本 smoke。
5. 如果改动涉及 `.github/workflows/`，按 install → build/test → artifact download → bundle → publish 检查 diff；不假设本地能完整执行 GitHub Actions。

仅修改 `AGENTS.md` 时，不需要运行数据导入测试，除非需要额外信心；改为确认只改了 `AGENTS.md` 文件，且目录地图仍指向正确的本地卡片。

## Notes for future agents

- 这个仓库里 edge case 正确性比 happy path 导入速度更重要。高价值回归点包括 sample-based primary-key inference、merged cells、raw header mapping、已有 `id` 列、显式 `--csv-quotechar`、field mapping order 和 chunk rollback。
- 当前测试框架是标准库 `unittest`。保持 `python -m unittest discover -s tests -p 'test_*.py'` 可发现。
- 最快的安全 review 路径：先看 `XDB.py` 中被改行为；共享行为补 `tests/test_xdb_regressions.py`；用户可见导入路径再做临时 SQLite CLI smoke。
- 工作树可能已有非 `AGENTS.md` 修改。除非用户明确要求，不要 revert。
