"""
内容编辑器 Widget
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit, 
    QLabel, QPushButton, QFont
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont as QGuiFont

logger = logging.getLogger(__name__)


class ContentEditor(QWidget):
    """内容编辑器组件"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 标题
        title = QLabel('内容编辑器')
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(11)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 工具栏
        toolbar_layout = QHBoxLayout()
        
        font_size_label = QLabel('字体大小:')
        toolbar_layout.addWidget(font_size_label)
        
        clear_btn = QPushButton('清空')
        clear_btn.clicked.connect(self.clear)
        toolbar_layout.addWidget(clear_btn)
        
        select_all_btn = QPushButton('全选')
        select_all_btn.clicked.connect(self.select_all)
        toolbar_layout.addWidget(select_all_btn)
        
        toolbar_layout.addStretch()
        layout.addLayout(toolbar_layout)
        
        # 文本编辑器
        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlaceholderText('在此输入或粘贴内容...\n\n支持的格式:\n• PDF 文本\n• Word 文档\n• Excel 表格\n• 纯文本')
        
        # 设置字体
        font = QGuiFont('Microsoft YaHei', 10)
        self.text_edit.setFont(font)
        
        layout.addWidget(self.text_edit)
        
        # 底部信息
        self.info_label = QLabel('0 字符 | 0 行')
        layout.addWidget(self.info_label)
        
        # 更新字符计数
        self.text_edit.textChanged.connect(self.update_info)
    
    def set_content(self, text):
        """设置内容"""
        self.text_edit.setPlainText(str(text))
        self.update_info()
    
    def get_content(self):
        """获取内容"""
        return self.text_edit.toPlainText()
    
    def clear(self):
        """清空内容"""
        self.text_edit.clear()
        self.update_info()
    
    def select_all(self):
        """全选"""
        self.text_edit.selectAll()
    
    def update_info(self):
        """更新信息"""
        text = self.text_edit.toPlainText()
        char_count = len(text)
        line_count = len(text.split('\n'))
        self.info_label.setText(f'{char_count} 字符 | {line_count} 行')