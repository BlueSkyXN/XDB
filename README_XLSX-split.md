# XLSX-split
通过KEY键列进行分类提取，简化信息分类工作

当你运行此程序时，它将处理一个名为 "input.xlsx" 的Excel文件，并根据配置文件中的设置将数据拆分为多个CSV文件。

### 准备工作

在运行程序之前，需要进行以下准备工作：

1. 确保已安装 Python 3.x 版本。
2. 确保已安装所需的 Python 包，可以使用以下命令进行安装：

   ```
   pip install openpyxl
   ```

### 配置文件

在配置文件 "config.ini" 中，你可以进行以下设置：

#### [General]

- `xlsx_file`：指定要处理的Excel文件的路径。
- `output_directory`：指定输出CSV文件的目录路径。
- `raw_sheet_name`：指定要处理的原始表格的名称。
- `csv_encoding`：指定CSV文件的编码格式。
- `KEY`：指定用于匹配部门的列名称。

#### [TagDepartments]

在这个部分，你可以为不同的标签（部门）指定对应的部门列表。

#### [ColumnMappings]

这个部分指定了原始表格中列名称和CSV文件中的字段名称之间的映射关系。确保列名称与原始表格的列名称一致。

### 运行程序

运行以下命令来运行程序：

```
python XLSX-split.py -c config.ini
```

程序将读取配置文件 "config.ini" 中的设置，并根据设置将原始表格的数据拆分为多个CSV文件。

请注意，确保已将正确的Excel文件放置在指定的路径，并且目标输出目录已存在。