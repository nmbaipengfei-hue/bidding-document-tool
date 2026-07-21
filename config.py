"""
项目配置文件
"""
import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 工作目录
WORK_DIR = PROJECT_ROOT / "workspace"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
RESOURCES_DIR = PROJECT_ROOT / "resources"
OUTPUT_DIR = PROJECT_ROOT / "output"

# 创建必要的目录
for directory in [WORK_DIR, TEMPLATES_DIR, RESOURCES_DIR, OUTPUT_DIR]:
    directory.mkdir(exist_ok=True)

# 支持的文件格式
SUPPORTED_FORMATS = {
    'pdf': ['.pdf'],
    'word': ['.docx', '.doc'],
    'excel': ['.xlsx', '.xls'],
    'image': ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']
}

# 输出格式
OUTPUT_FORMAT = 'docx'

# UI 配置
UI_CONFIG = {
    'window_title': '标书制作工具',
    'window_width': 1200,
    'window_height': 800,
    'theme': 'light'
}

# 模板配置
TEMPLATE_CONFIG = {
    'default_font': 'Microsoft YaHei',
    'default_font_size': 11,
    'margin_top': 2.54,
    'margin_bottom': 2.54,
    'margin_left': 2.54,
    'margin_right': 2.54,
}

# 日志配置
LOG_LEVEL = 'INFO'
LOG_FILE = PROJECT_ROOT / 'logs' / 'app.log'
LOG_FILE.parent.mkdir(exist_ok=True)