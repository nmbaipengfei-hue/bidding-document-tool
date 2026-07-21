"""
应用程序入口
"""
import sys
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

from src.ui.main_window import MainWindow
from src.ui.styles.stylesheet import LIGHT_STYLESHEET


def main():
    """主函数"""
    logger.info('=' * 60)
    logger.info('标书制作工具启动')
    logger.info('=' * 60)
    
    # 创建应用
    app = QApplication(sys.argv)
    
    # 设置全局字体
    font = QFont('Microsoft YaHei', 10)
    app.setFont(font)
    
    # 应用样式表
    app.setStyleSheet(LIGHT_STYLESHEET)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    logger.info('主窗口已显示')
    
    # 启动应用
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()