"""
内容匹配模块 - 智能匹配招标文件与标书内容
"""
import logging
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class ContentMatcher:
    """内容匹配引擎"""
    
    def __init__(self):
        """初始化内容匹配器"""
        self.keywords_mapping = {
            '项目名称': ['项目名称', '工程名称', 'project name'],
            '招标人': ['招标人', '业主', 'client'],
            '招标代理': ['招标代理', '代理', 'agency'],
            '工程地点': ['工程地点', '地点', '地址', 'location'],
            '工程造价': ['工程造价', '造价', '预算', 'budget'],
            '招标范围': ['招标范围', '范围', 'scope'],
            '技术要求': ['技术要求', '技术指标', 'technical'],
            '资质要求': ['资质要求', '资质', '质量体系', 'qualification'],
        }
        self.cached_matches = {}
    
    def extract_keywords(self, text, keywords=None):
        """
        从文本中提取关键词
        
        Args:
            text: 输入文本
            keywords: 关键词列表
            
        Returns:
            dict: 关键词及其值
        """
        if keywords is None:
            keywords = list(self.keywords_mapping.keys())
        
        results = {}
        text_lower = text.lower()
        
        for keyword in keywords:
            # 检查主关键词
            if keyword.lower() in text_lower:
                results[keyword] = self._extract_value(text, keyword)
            else:
                # 检查关键词映射
                for alias in self.keywords_mapping.get(keyword, []):
                    if alias.lower() in text_lower:
                        results[keyword] = self._extract_value(text, alias)
                        break
        
        return results
    
    def _extract_value(self, text, keyword, context_length=200):
        """
        提取关键词的值
        
        Args:
            text: 输入文本
            keyword: 关键词
            context_length: 上下文长度
            
        Returns:
            str: 提取的值
        """
        try:
            # 查找关键词位置
            idx = text.lower().find(keyword.lower())
            if idx == -1:
                return ""
            
            # 从关键词后面提取内容
            start = idx + len(keyword)
            end = min(start + context_length, len(text))
            
            # 查找冒号、等号等分隔符
            extracted = text[start:end]
            for sep in [':', '：', '=', '。', '\n']:
                if sep in extracted:
                    extracted = extracted.split(sep)[0]
                    break
            
            return extracted.strip()
        except Exception as e:
            logger.error(f"值提取失败: {str(e)}")
            return ""
    
    def match_content(self, source_text, target_template_keys):
        """
        匹配源文本与目标模板键
        
        Args:
            source_text: 源文本（招标文件）
            target_template_keys: 目标模板键列表
            
        Returns:
            dict: 匹配结果
        """
        results = {}
        extracted = self.extract_keywords(source_text, target_template_keys)
        
        for key in target_template_keys:
            if key in extracted:
                results[key] = extracted[key]
            else:
                results[key] = ""
        
        return results
    
    def similarity(self, text1, text2):
        """
        计算两个文本的相似度
        
        Args:
            text1: 文本1
            text2: 文本2
            
        Returns:
            float: 相似度 (0-1)
        """
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def find_best_match(self, query, options):
        """
        从选项中找到最佳匹配
        
        Args:
            query: 查询文本
            options: 选项列表
            
        Returns:
            dict: 最佳匹配及其相似度
        """
        best_match = None
        best_score = 0
        
        for option in options:
            score = self.similarity(query, option)
            if score > best_score:
                best_score = score
                best_match = option
        
        return {
            'match': best_match,
            'score': best_score
        }
    
    def extract_table_data(self, table_data, target_columns):
        """
        从表格数据中提取目标列
        
        Args:
            table_data: 表格数据（行列表）
            target_columns: 目标列标题
            
        Returns:
            list: 提取的数据
        """
        if not table_data or len(table_data) == 0:
            return []
        
        # 假设第一行是表头
        headers = table_data[0]
        results = []
        
        for col in target_columns:
            for idx, header in enumerate(headers):
                if self.similarity(col, str(header)) > 0.8:
                    # 找到匹配的列
                    column_data = []
                    for row in table_data[1:]:
                        if idx < len(row):
                            column_data.append(row[idx])
                    results.append({
                        'column': col,
                        'data': column_data
                    })
                    break
        
        return results
    
    def merge_content(self, *texts):
        """
        合并多个文本内容
        
        Args:
            texts: 多个文本
            
        Returns:
            str: 合并后的文本
        """
        return '\n'.join([str(t) for t in texts if t])