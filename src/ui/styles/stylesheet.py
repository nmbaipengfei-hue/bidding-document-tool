"""
样式表定义
"""

# 亮色主题样式表
LIGHT_STYLESHEET = """
    QMainWindow {
        background-color: #f5f5f5;
    }
    
    QMenuBar {
        background-color: #ffffff;
        border-bottom: 1px solid #ddd;
    }
    
    QMenuBar::item:selected {
        background-color: #e3f2fd;
    }
    
    QMenu {
        background-color: #ffffff;
        border: 1px solid #ddd;
    }
    
    QMenu::item:selected {
        background-color: #e3f2fd;
    }
    
    QToolBar {
        background-color: #ffffff;
        border-bottom: 1px solid #ddd;
    }
    
    QToolButton {
        border: none;
        padding: 5px;
        border-radius: 3px;
    }
    
    QToolButton:hover {
        background-color: #e3f2fd;
    }
    
    QToolButton:pressed {
        background-color: #bbdefb;
    }
    
    QPushButton {
        background-color: #2196F3;
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #1976D2;
    }
    
    QPushButton:pressed {
        background-color: #0D47A1;
    }
    
    QPlainTextEdit {
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 5px;
        background-color: #ffffff;
        color: #333;
    }
    
    QLabel {
        color: #333;
    }
    
    QTreeWidget {
        border: 1px solid #ddd;
        border-radius: 4px;
        background-color: #ffffff;
    }
    
    QHeaderView::section {
        background-color: #f5f5f5;
        padding: 5px;
        border: none;
        border-right: 1px solid #ddd;
        border-bottom: 1px solid #ddd;
    }
    
    QStatusBar {
        background-color: #ffffff;
        border-top: 1px solid #ddd;
    }
    
    QProgressBar {
        border: 1px solid #ddd;
        border-radius: 4px;
        background-color: #f5f5f5;
        height: 20px;
    }
    
    QProgressBar::chunk {
        background-color: #4CAF50;
    }
"""

# 暗色主题样式表
DARK_STYLESHEET = """
    QMainWindow {
        background-color: #2d2d2d;
    }
    
    QMenuBar {
        background-color: #3d3d3d;
        color: #ffffff;
        border-bottom: 1px solid #555;
    }
    
    QMenuBar::item:selected {
        background-color: #4d4d4d;
    }
    
    QMenu {
        background-color: #3d3d3d;
        color: #ffffff;
        border: 1px solid #555;
    }
    
    QMenu::item:selected {
        background-color: #4d4d4d;
    }
    
    QToolBar {
        background-color: #3d3d3d;
        border-bottom: 1px solid #555;
    }
    
    QToolButton {
        color: #ffffff;
        border: none;
        padding: 5px;
        border-radius: 3px;
    }
    
    QToolButton:hover {
        background-color: #4d4d4d;
    }
    
    QPushButton {
        background-color: #2196F3;
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #1976D2;
    }
    
    QPlainTextEdit {
        border: 1px solid #555;
        border-radius: 4px;
        padding: 5px;
        background-color: #2d2d2d;
        color: #ffffff;
    }
    
    QLabel {
        color: #ffffff;
    }
    
    QTreeWidget {
        border: 1px solid #555;
        border-radius: 4px;
        background-color: #2d2d2d;
        color: #ffffff;
    }
    
    QHeaderView::section {
        background-color: #3d3d3d;
        padding: 5px;
        border: none;
        color: #ffffff;
        border-right: 1px solid #555;
        border-bottom: 1px solid #555;
    }
    
    QStatusBar {
        background-color: #3d3d3d;
        color: #ffffff;
        border-top: 1px solid #555;
    }
    
    QProgressBar {
        border: 1px solid #555;
        border-radius: 4px;
        background-color: #3d3d3d;
        height: 20px;
    }
    
    QProgressBar::chunk {
        background-color: #4CAF50;
    }
"""
