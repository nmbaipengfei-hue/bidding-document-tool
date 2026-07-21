"""
文件浏览器 Widget
"""
import logging
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QFileDialog, QLabel
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QFont

logger = logging.getLogger(__name__)


class FileBrowser(QWidget):
    """文件浏览器组件"""
    
    file_selected = pyqtSignal(str)  # 文件选中信号
    
    def __init__(self):
        super().__init__()
        self.current_dir = Path.home()
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 标题
        title = QLabel('文件浏览器')
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(11)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        
        open_btn = QPushButton('打开文件')
        open_btn.clicked.connect(self.browse_file)
        btn_layout.addWidget(open_btn)
        
        open_dir_btn = QPushButton('打开文件夹')
        open_dir_btn.clicked.connect(self.browse_directory)
        btn_layout.addWidget(open_dir_btn)
        
        layout.addLayout(btn_layout)
        
        # 文件树
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabel('文件')
        self.file_tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.file_tree.setColumnCount(1)
        layout.addWidget(self.file_tree)
        
        # 加载当前目录
        self.load_directory(self.current_dir)
    
    def load_directory(self, directory):
        """加载目录"""
        self.file_tree.clear()
        self.current_dir = Path(directory)
        
        root_item = QTreeWidgetItem()
        root_item.setText(0, str(self.current_dir))
        self.file_tree.addTopLevelItem(root_item)
        
        self.populate_tree(root_item, self.current_dir)
    
    def populate_tree(self, parent_item, directory):
        """递归填充树"""
        try:
            for item in sorted(directory.iterdir()):
                if item.is_file() and self.is_supported_file(item):
                    child_item = QTreeWidgetItem()
                    child_item.setText(0, item.name)
                    child_item.setData(0, Qt.UserRole, str(item))
                    parent_item.addChild(child_item)
                elif item.is_dir() and not item.name.startswith('.'):
                    dir_item = QTreeWidgetItem()
                    dir_item.setText(0, item.name + '/')
                    parent_item.addChild(dir_item)
                    # 递归添加子目录（限制深度）
                    if len(list(item.iterdir())) < 50:
                        self.populate_tree(dir_item, item)
        except PermissionError:
            pass
    
    def is_supported_file(self, file_path):
        """检查是否支持的文件格式"""
        supported = ['.pdf', '.docx', '.doc', '.xlsx', '.xls', 
                    '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']
        return file_path.suffix.lower() in supported
    
    def on_item_double_clicked(self, item, column):
        """项目双击事件"""
        file_path = item.data(0, Qt.UserRole)
        if file_path:
            self.file_selected.emit(file_path)
    
    def browse_file(self):
        """浏览单个文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择文件', str(self.current_dir),
            'All Supported (*.pdf *.docx *.doc *.xlsx *.xls *.png *.jpg);;PDF Files (*.pdf);;Word Files (*.docx *.doc);;Excel Files (*.xlsx *.xls);;Image Files (*.png *.jpg *.jpeg);;All Files (*)'
        )
        if file_path:
            self.file_selected.emit(file_path)
            self.load_directory(Path(file_path).parent)
    
    def browse_directory(self):
        """浏览文件夹"""
        directory = QFileDialog.getExistingDirectory(
            self, '选择文件夹', str(self.current_dir)
        )
        if directory:
            self.load_directory(directory)