"""
PDF 文件解析模块
"""
import logging
from pathlib import Path
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)


class PDFParser:
    """PDF 文件解析器"""
    
    def __init__(self, file_path):
        """
        初始化 PDF 解析器
        
        Args:
            file_path: PDF 文件路径
        """
        self.file_path = Path(file_path)
        self.reader = None
        self.content = []
        
    def parse(self):
        """
        解析 PDF 文件
        
        Returns:
            dict: 解析结果，包含文本内容
        """
        try:
            with open(self.file_path, 'rb') as file:
                self.reader = PdfReader(file)
                
            self.content = []
            for page_num, page in enumerate(self.reader.pages):
                text = page.extract_text()
                self.content.append({
                    'page': page_num + 1,
                    'text': text
                })
            
            logger.info(f"成功解析 PDF 文件: {self.file_path}")
            return {
                'success': True,
                'file': str(self.file_path),
                'pages': len(self.reader.pages),
                'content': self.content
            }
        except Exception as e:
            logger.error(f"PDF 解析失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_text(self):
        """
        获取提取的文本内容
        
        Returns:
            str: 合并后的文本内容
        """
        return '\n'.join([item['text'] for item in self.content])
    
    def extract_keywords(self, keywords):
        """
        从 PDF 中提取关键词相关内容
        
        Args:
            keywords: 关键词列表
            
        Returns:
            dict: 关键词及其上下文
        """
        results = {}
        text = self.get_text()
        
        for keyword in keywords:
            if keyword.lower() in text.lower():
                # 找到关键词的位置和上下文
                start = max(0, text.lower().find(keyword.lower()) - 100)
                end = min(len(text), text.lower().find(keyword.lower()) + len(keyword) + 100)
                results[keyword] = text[start:end]
        
        return results