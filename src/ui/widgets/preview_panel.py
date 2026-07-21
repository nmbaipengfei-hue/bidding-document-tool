"""
预览面板 Widget
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, 
    QTreeWidget, QTreeWidgetItem, QFont
)
from PyQt5.QtCore import Qt

logger = logging.getLogger(__name__)


class PreviewPanel(QWidget):
    """预览面板组件"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 标题
        title = QLabel('预览面板')
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(11)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 创建树形视图显示提取的信息
        self.info_tree = QTreeWidget()
        self.info_tree.setHeaderLabel('提取的信息')
        self.info_tree.setColumnCount(2)
        self.info_tree.setHeaderLabels(['项目', '值'])
        self.info_tree.setColumnWidth(0, 150)
        self.info_tree.setColumnWidth(1, 150)
        
        layout.addWidget(self.info_tree)
        
        # 信息标签
        self.status_label = QLabel('等待加载文件或输入内容...')
        layout.addWidget(self.status_label)
    
    def show_keywords(self, keywords):
        """显示提取的关键词"""
        self.info_tree.clear()
        
        if not keywords:
            self.status_label.setText('未找到关键词')
            return
        
        # 添加到树
        for key, value in keywords.items():
            item = QTreeWidgetItem()
            item.setText(0, key)
            # 截断长值
            value_str = str(value)[:100] + '...' if len(str(value)) > 100 else str(value)
            item.setText(1, value_str)
            self.info_tree.addTopLevelItem(item)
        
        self.status_label.setText(f'已提取 {len(keywords)} 个关键词')
    
    def show_image_info(self, metadata):
        """显示图片信息"""
        self.info_tree.clear()
        
        if not metadata:
            return
        
        for key, value in metadata.items():
            item = QTreeWidgetItem()
            item.setText(0, str(key))
            item.setText(1, str(value))
            self.info_tree.addTopLevelItem(item)
        
        self.status_label.setText('已加载图片信息')
    
    def clear(self):
        """清空预览"""
        self.info_tree.clear()
        self.status_label.setText('已清空')