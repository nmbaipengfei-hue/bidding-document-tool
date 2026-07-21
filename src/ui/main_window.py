"""
主窗口 - 应用主界面
"""
import logging
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMenuBar, QMenu, QAction, QToolBar, QStatusBar, QMessageBox,
    QProgressBar, QLabel, QFileDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont

from src.file_parser import PDFParser, WordParser, ExcelParser, ImageHandler
from src.document_processor import TemplateManager, ContentMatcher, LayoutEngine
from .widgets.file_browser import FileBrowser
from .widgets.content_editor import ContentEditor
from .widgets.preview_panel import PreviewPanel

logger = logging.getLogger(__name__)


class ProcessThread(QThread):
    """后台处理线程"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, task_type, file_path):
        super().__init__()
        self.task_type = task_type
        self.file_path = file_path
        self.result = {}
    
    def run(self):
        try:
            self.progress.emit(10)
            
            if self.task_type == 'pdf':
                parser = PDFParser(self.file_path)
                result = parser.parse()
                self.result = {'text': parser.get_text(), 'info': result}
                
            elif self.task_type == 'word':
                parser = WordParser(self.file_path)
                result = parser.parse()
                self.result = {'text': parser.get_text(), 'info': result}
                
            elif self.task_type == 'excel':
                parser = ExcelParser(self.file_path)
                result = parser.parse()
                self.result = {'data': parser.get_all_data(), 'info': result}
                
            elif self.task_type == 'image':
                handler = ImageHandler(self.file_path)
                result = handler.load()
                self.result = {'metadata': handler.metadata, 'info': result}
            
            self.progress.emit(90)
            self.finished.emit(self.result)
            self.progress.emit(100)
            
        except Exception as e:
            logger.error(f"处理失败: {str(e)}")
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('标书制作工具')
        self.setGeometry(100, 100, 1400, 900)
        
        # 初始化组件
        self.template_manager = TemplateManager()
        self.content_matcher = ContentMatcher()
        self.layout_engine = LayoutEngine()
        
        self.current_document = None
        self.current_file = None
        self.process_thread = None
        
        # 创建UI
        self.init_ui()
        self.init_menu()
        self.init_toolbar()
        self.init_status_bar()
    
    def init_ui(self):
        """初始化用户界面"""
        # 创建中央窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # 左侧：文件浏览器
        self.file_browser = FileBrowser()
        self.file_browser.file_selected.connect(self.on_file_selected)
        
        # 中央：内容编辑器
        self.content_editor = ContentEditor()
        
        # 右侧：预览面板
        self.preview_panel = PreviewPanel()
        
        # 创建分割器
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.file_browser)
        splitter1.addWidget(self.content_editor)
        splitter1.addWidget(self.preview_panel)
        splitter1.setStretchFactor(0, 1)
        splitter1.setStretchFactor(1, 2)
        splitter1.setStretchFactor(2, 1)
        splitter1.setSizes([300, 600, 300])
        
        main_layout.addWidget(splitter1)
    
    def init_menu(self):
        """初始化菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')
        
        open_pdf = QAction('打开PDF文件', self)
        open_pdf.triggered.connect(self.open_pdf)
        file_menu.addAction(open_pdf)
        
        open_word = QAction('打开Word文件', self)
        open_word.triggered.connect(self.open_word)
        file_menu.addAction(open_word)
        
        open_excel = QAction('打开Excel文件', self)
        open_excel.triggered.connect(self.open_excel)
        file_menu.addAction(open_excel)
        
        open_image = QAction('打开图片文件', self)
        open_image.triggered.connect(self.open_image)
        file_menu.addAction(open_image)
        
        file_menu.addSeparator()
        
        save_action = QAction('保存文档', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_document)
        file_menu.addAction(save_action)
        
        save_as = QAction('另存为...', self)
        save_as.setShortcut('Ctrl+Shift+S')
        save_as.triggered.connect(self.save_as)
        file_menu.addAction(save_as)
        
        file_menu.addSeparator()
        
        exit_action = QAction('退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu('编辑(&E)')
        
        new_doc = QAction('新建文档', self)
        new_doc.setShortcut('Ctrl+N')
        new_doc.triggered.connect(self.new_document)
        edit_menu.addAction(new_doc)
        
        load_template = QAction('加载模板', self)
        load_template.triggered.connect(self.load_template)
        edit_menu.addAction(load_template)
        
        extract_keywords = QAction('提取关键词', self)
        extract_keywords.triggered.connect(self.extract_keywords)
        edit_menu.addAction(extract_keywords)
        
        # 工具菜单
        tools_menu = menubar.addMenu('工具(&T)')
        
        auto_fill = QAction('自动填充内容', self)
        auto_fill.triggered.connect(self.auto_fill)
        tools_menu.addAction(auto_fill)
        
        optimize_layout = QAction('优化排版', self)
        optimize_layout.triggered.connect(self.optimize_layout)
        tools_menu.addAction(optimize_layout)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')
        
        about = QAction('关于', self)
        about.triggered.connect(self.show_about)
        help_menu.addAction(about)
    
    def init_toolbar(self):
        """初始化工具栏"""
        toolbar = self.addToolBar('主工具栏')
        toolbar.setMovable(False)
        
        # 新建按钮
        new_action = toolbar.addAction('新建')
        new_action.triggered.connect(self.new_document)
        
        # 打开按钮
        open_action = toolbar.addAction('打开')
        open_action.triggered.connect(self.open_file)
        
        # 保存按钮
        save_action = toolbar.addAction('保存')
        save_action.triggered.connect(self.save_document)
        
        toolbar.addSeparator()
        
        # 提取关键词按钮
        extract_action = toolbar.addAction('提取关键词')
        extract_action.triggered.connect(self.extract_keywords)
        
        # 自动填充按钮
        auto_fill_action = toolbar.addAction('自动填充')
        auto_fill_action.triggered.connect(self.auto_fill)
        
        # 优化排版按钮
        optimize_action = toolbar.addAction('优化排版')
        optimize_action.triggered.connect(self.optimize_layout)
    
    def init_status_bar(self):
        """初始化状态栏"""
        self.status_label = QLabel('就绪')
        self.statusBar().addWidget(self.status_label, 1)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setVisible(False)
        self.statusBar().addPermanentWidget(self.progress_bar)
    
    def on_file_selected(self, file_path):
        """文件选中事件"""
        self.current_file = file_path
        self.load_file(file_path)
    
    def load_file(self, file_path):
        """加载文件"""
        file_path = Path(file_path)
        suffix = file_path.suffix.lower()
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText(f'正在加载: {file_path.name}...')
        
        # 确定文件类型
        task_type = None
        if suffix == '.pdf':
            task_type = 'pdf'
        elif suffix in ['.docx', '.doc']:
            task_type = 'word'
        elif suffix in ['.xlsx', '.xls']:
            task_type = 'excel'
        elif suffix in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']:
            task_type = 'image'
        
        if task_type:
            self.process_thread = ProcessThread(task_type, str(file_path))
            self.process_thread.progress.connect(self.update_progress)
            self.process_thread.finished.connect(self.on_file_loaded)
            self.process_thread.error.connect(self.on_error)
            self.process_thread.start()
        else:
            self.status_label.setText('不支持的文件格式')
            self.progress_bar.setVisible(False)
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
    
    def on_file_loaded(self, result):
        """文件加载完成"""
        self.progress_bar.setVisible(False)
        
        if 'text' in result:
            self.content_editor.set_content(result['text'])
            # 提取关键词并显示
            keywords = self.content_matcher.extract_keywords(result['text'])
            self.preview_panel.show_keywords(keywords)
        elif 'data' in result:
            self.content_editor.set_content(str(result['data']))
        elif 'metadata' in result:
            self.preview_panel.show_image_info(result['metadata'])
        
        self.status_label.setText(f'已加载: {self.current_file}')
    
    def on_error(self, error_msg):
        """错误处理"""
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, '错误', f'处理失败:\n{error_msg}')
        self.status_label.setText('加载失败')
    
    def open_pdf(self):
        """打开PDF文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, '打开PDF文件', '',
            'PDF Files (*.pdf);;All Files (*)'
        )
        if file_path:
            self.load_file(file_path)
    
    def open_word(self):
        """打开Word文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, '打开Word文件', '',
            'Word Files (*.docx *.doc);;All Files (*)'
        )
        if file_path:
            self.load_file(file_path)
    
    def open_excel(self):
        """打开Excel文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, '打开Excel文件', '',
            'Excel Files (*.xlsx *.xls);;All Files (*)'
        )
        if file_path:
            self.load_file(file_path)
    
    def open_image(self):
        """打开图片文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, '打开图片文件', '',
            'Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;All Files (*)'
        )
        if file_path:
            self.load_file(file_path)
    
    def open_file(self):
        """打开文件（通用）"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, '打开文件', '',
            'All Supported (*.pdf *.docx *.doc *.xlsx *.xls *.png *.jpg);;PDF Files (*.pdf);;Word Files (*.docx *.doc);;Excel Files (*.xlsx *.xls);;Image Files (*.png *.jpg *.jpeg);;All Files (*)'
        )
        if file_path:
            self.load_file(file_path)
    
    def new_document(self):
        """创建新文档"""
        self.current_document = self.template_manager.create_blank_template('新标书')
        self.content_editor.clear()
        self.preview_panel.clear()
        self.status_label.setText('已创建新文档')
    
    def load_template(self):
        """加载模板"""
        templates = self.template_manager.list_templates()
        if not templates:
            QMessageBox.information(self, '提示', '没有可用的模板')
            return
        
        # 简单的选择对话框
        from PyQt5.QtWidgets import QInputDialog
        template_name, ok = QInputDialog.getItem(
            self, '选择模板', '可用模板:', templates, 0, False
        )
        
        if ok:
            self.current_document = self.template_manager.load_template(template_name)
            self.status_label.setText(f'已加载模板: {template_name}')
    
    def extract_keywords(self):
        """提取关键词"""
        content = self.content_editor.get_content()
        if not content:
            QMessageBox.warning(self, '警告', '请先加载或输入内容')
            return
        
        keywords = self.content_matcher.extract_keywords(content)
        self.preview_panel.show_keywords(keywords)
        self.status_label.setText(f'已提取 {len(keywords)} 个关键词')
    
    def auto_fill(self):
        """自动填充内容"""
        if not self.current_document:
            self.new_document()
        
        content = self.content_editor.get_content()
        if not content:
            QMessageBox.warning(self, '警告', '请先加载内容')
            return
        
        # 提取关键词
        keywords = self.content_matcher.extract_keywords(content)
        
        # 添加到文档
        self.template_manager.add_heading('提取的信息', level=1)
        for key, value in keywords.items():
            if value:
                self.template_manager.add_paragraph(f'{key}: {value}')
        
        self.status_label.setText('已自动填充内容')
        QMessageBox.information(self, '成功', '内容已自动填充到文档')
    
    def optimize_layout(self):
        """优化排版"""
        if not self.current_document:
            QMessageBox.warning(self, '警告', '请先创建或加载文档')
            return
        
        self.layout_engine.optimize_layout(self.current_document)
        self.status_label.setText('排版已优化')
        QMessageBox.information(self, '成功', '文档排版已优化')
    
    def save_document(self):
        """保存文档"""
        if not self.current_document:
            QMessageBox.warning(self, '警告', '没有要保存的文档')
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, '保存文档', 'output/标书.docx',
            'Word Files (*.docx);;All Files (*)'
        )
        
        if file_path:
            if self.template_manager.save_document(file_path):
                self.status_label.setText(f'已保存: {file_path}')
                QMessageBox.information(self, '成功', f'文档已保存到:\n{file_path}')
            else:
                QMessageBox.error(self, '错误', '保存失败')
    
    def save_as(self):
        """另存为"""
        self.save_document()
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self, '关于标书制作工具',
            '标书制作工具 v1.0\n\n'
            '一个功能强大的标书自动制作工具\n'
            '支持PDF、Word、Excel和图片处理\n\n'
            '功能:\n'
            '• 自动解析招标文件\n'
            '• 智能提取关键信息\n'
            '• 自动生成标书文档\n'
            '• 优化文档排版和美观度\n\n'
            '© 2026 Bidding Tool Team'
        )