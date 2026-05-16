# scripts agent instructions

## Purpose

`scripts/` 保存独立的 Excel 辅助工具：拆分 CSV、按 sheet 切割、合并 sheet，以及客户名称分类。它们服务于数据整理，不是 `XDB.py` 的核心导入路径。

## Scope

适用于 `scripts/` 下的 Python 脚本、`config_template.ini` 和脚本文档。

## Read first

- `scripts/README_XLSX-split.md`
- `scripts/config_template.ini`
- 修改目标脚本本身的 CLI 参数、输入列和输出文件逻辑。
- `.github/workflows/multi-platform-build.yaml` 中对应 PyInstaller 构建命令。

## Local rules

- 保持脚本可从仓库根目录直接运行；修改参数时同步脚本文档或用法提示。
- `XLSX-split.py` 依赖 INI 的 `General`、`TagDepartments`、`ColumnMappings`，可选 `DELLIST`；不要破坏这些 key 名称的兼容性。
- `XLSX-SheetCutter.py` 和 `XLSX-SheetMerger.py` 当前只复制单元格值，不复制样式；如果改变语义，要在用法说明中写清楚。
- `客户分类切割.py` 依赖输入表的 `Name` 列，分类规则顺序会影响结果；修改关键词或顺序时用样例数据验证。
- 输出的 CSV/XLSX 是用户数据产物；测试时写入临时目录。

## Do not

- 不把本机真实绝对路径写进脚本默认值；示例路径只放在模板或文档中。
- 不手动提交脚本生成的 CSV/XLSX 输出文件。
- 不让辅助脚本反向依赖 `XDB.py` 的内部实现，除非同时补测试说明和打包验证。

## Validation

无法从仓库中确认专用自动测试命令，优先运行根目录通用验证命令。按改动脚本补最小 smoke：

- `python scripts/XLSX-split.py -c <config.ini>`
- `python scripts/XLSX-SheetCutter.py <input.xlsx>`
- `python scripts/XLSX-SheetMerger.py <input1.xlsx> <input2.xlsx>`
- `python scripts/客户分类切割.py <input.xlsx> <output_dir>`

## Notes for future agents

CI 会用 PyInstaller 分别打包 `XLSX-split.py`、`XLSX-SheetCutter.py`、`XLSX-SheetMerger.py`；重命名文件或入口会影响 release 资产。
