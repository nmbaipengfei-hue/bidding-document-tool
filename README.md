# 标书制作工具

一个功能强大的标书自动制作工具，可以自动处理招标文件、图片和内容，生成美观的标书文档。

## 功能特性

### 1. 文件处理
- ✅ 支持 PDF 文件解析
- ✅ 支持 Word 文档解析（.docx、.doc）
- ✅ 支持 Excel 文件解析（.xlsx、.xls）
- ✅ 支持图片处理（.png、.jpg、.jpeg、.bmp、.gif、.tiff）

### 2. 内容提取与匹配
- ✅ 自动关键词提取
- ✅ 智能内容匹配
- ✅ 表格数据提取
- ✅ 相似度计算

### 3. 文档生成
- ✅ Word 文档自动生成
- ✅ 模板管理
- ✅ 自动排版布局
- ✅ 美观度优化

### 4. 图像处理
- ✅ 图像加载与处理
- ✅ 自动尺寸调整
- ✅ 最佳位置检测
- ✅ 图像优化

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基本使用

```python
from src.file_parser import PDFParser, WordParser, ExcelParser, ImageHandler
from src.document_processor import TemplateManager, ContentMatcher, LayoutEngine

# 1. 解析招标文件
pdf_parser = PDFParser('bidding_document.pdf')
result = pdf_parser.parse()
text = pdf_parser.get_text()

# 2. 提取关键信息
matcher = ContentMatcher()
keywords = matcher.extract_keywords(text)

# 3. 创建标书文档
template_manager = TemplateManager()
doc = template_manager.create_blank_template('我的标书')

# 4. 填充内容
template_manager.add_heading('项目信息', level=1)
for key, value in keywords.items():
    template_manager.add_paragraph(f"{key}: {value}")

# 5. 优化排版
layout_engine = LayoutEngine()
layout_engine.optimize_layout(doc)

# 6. 保存文档
template_manager.save_document('output/标书.docx')
```

## 项目结构

```
bidding-document-tool/
├── src/
│   ├── file_parser/           # 文件解析模块
│   │   ├── pdf_parser.py
│   │   ├── word_parser.py
│   │   ├── excel_parser.py
│   │   └── image_handler.py
│   ├── document_processor/    # 文档处理模块
│   │   ├── template_manager.py
│   │   ├── content_matcher.py
│   │   └── layout_engine.py
│   └── utils/                 # 工具函数
├── templates/                 # 模板目录
├── resources/                 # 资源文件
├── output/                    # 输出目录
├── config.py                  # 配置文件
└── requirements.txt           # 依赖列表
```

## 核心模块说明

### 文件解析模块 (file_parser)

#### PDFParser
- `parse()` - 解析 PDF 文件
- `get_text()` - 获取文本内容
- `extract_keywords()` - 提取关键词

#### WordParser
- `parse()` - 解析 Word 文件
- `get_text()` - 获取文本内容
- `get_tables()` - 获取表格数据
- `extract_keywords()` - 提取关键词

#### ExcelParser
- `parse()` - 解析 Excel 文件
- `get_sheet_data()` - 获取工作表数据
- `get_all_data()` - 获取所有数据
- `extract_keywords()` - 提取关键词

#### ImageHandler
- `load()` - 加载图像
- `resize()` - 调整大小
- `detect_best_position()` - 检测最佳位置
- `save()` - 保存图像

### 文档处理模块 (document_processor)

#### TemplateManager
- `create_blank_template()` - 创建空白模板
- `load_template()` - 加载模板
- `save_template()` - 保存模板
- `add_heading()` - 添加标题
- `add_paragraph()` - 添加段落
- `add_table()` - 添加表格
- `add_image()` - 添加图像
- `save_document()` - 保存文档

#### ContentMatcher
- `extract_keywords()` - 提取关键词
- `match_content()` - 匹配内容
- `similarity()` - 计算相似度
- `find_best_match()` - 找最佳匹配
- `extract_table_data()` - 提取表格数据

#### LayoutEngine
- `set_page_margin()` - 设置页边距
- `set_font()` - 设置字体
- `set_paragraph_style()` - 设置段落样式
- `style_table()` - 设置表格样式
- `optimize_layout()` - 优化排版

## 配置说明

编辑 `config.py` 文件来自定义：

- 支持的文件格式
- 输出格式
- UI 配置
- 模板配置
- 日志配置

## 完整工作流示例

```python
from pathlib import Path
from src.file_parser import PDFParser, ImageHandler
from src.document_processor import TemplateManager, ContentMatcher, LayoutEngine

# 1. 解析招标文件
print("正在解析招标文件...")
pdf_parser = PDFParser('bidding_file.pdf')
pdf_result = pdf_parser.parse()

if not pdf_result['success']:
    print(f"PDF 解析失败: {pdf_result['error']}")
    exit()

# 2. 提取关键信息
print("正在提取关键信息...")
matcher = ContentMatcher()
text = pdf_parser.get_text()
keywords = matcher.extract_keywords(text)

# 3. 处理图片
print("正在处理图片...")
image_handler = ImageHandler('company_logo.png')
image_handler.load()
image_handler.resize(400, 300)
image_handler.save('output/logo_resized.png')

# 4. 创建标书
print("正在创建标书...")
template_manager = TemplateManager()
doc = template_manager.create_blank_template('项目标书')

# 5. 填充内容
template_manager.add_heading('一、项目概况', level=1)
for key, value in keywords.items():
    if value:
        template_manager.add_paragraph(f"{key}：{value}")

# 6. 添加图片
template_manager.add_image('output/logo_resized.png', width=3, height=2)

# 7. 优化排版
layout_engine = LayoutEngine()
layout_engine.optimize_layout(doc)

# 8. 保存
template_manager.save_document('output/最终标书.docx')
print("标书已生成: output/最终标书.docx")
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
