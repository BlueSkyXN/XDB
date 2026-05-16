# scripts navigation card

`scripts/` 保存独立 Excel 辅助工具，不属于 `XDB.py` 核心导入路径。
修改脚本 CLI、`config_template.ini` 或脚本文档前先读本卡片。
关键文件：`XLSX-split.py`、`XLSX-SheetCutter.py`、`XLSX-SheetMerger.py`、`客户分类切割.py`、`README_XLSX-split.md`。

## Local invariants

- 保持脚本可从仓库根目录用 `python scripts/<name>.py ...` 运行。
- `XLSX-split.py` 依赖 `General`、`TagDepartments`、`ColumnMappings`，并读取可选 `DELLIST`；改配置解析时保持 key 兼容。
- `XLSX-SheetCutter.py`、`XLSX-SheetMerger.py` 当前只复制单元格值，不复制样式；语义变化要同步用法说明。
- `客户分类切割.py` 要求输入有 `Name` 列；分类关键词/regex 顺序会影响结果。
- 脚本输出是用户数据产物；smoke 必须写到临时目录。

## Local rules

- 修改 flag、位置参数、config key、输出文件名或必需输入列时，同步 README/help/config template。
- 不让辅助脚本依赖 `XDB.py` 私有实现，除非同时说明并验证这个耦合。
- CI 会打包 `XLSX-split.py`、`XLSX-SheetCutter.py`、`XLSX-SheetMerger.py`；重命名入口必须改 workflow。

## Do not

- 不新增本机绝对路径作为默认值；示例路径只放模板或文档。
- 不提交本地运行生成的 CSV/XLSX。
- 不静默改变 CSV 输出编码；保持配置驱动。

## Validation

使用根验证，并按改动脚本补 smoke：

- `python scripts/XLSX-split.py -c <config.ini>`
- `python scripts/XLSX-SheetCutter.py <input.xlsx>`
- `python scripts/XLSX-SheetMerger.py <input1.xlsx> <input2.xlsx>`
- `python scripts/客户分类切割.py <input.xlsx> <output_dir>`
