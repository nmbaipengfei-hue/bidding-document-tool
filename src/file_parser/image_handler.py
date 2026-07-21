"""
图像处理模块
"""
import logging
from pathlib import Path
from PIL import Image
import cv2
import numpy as np

logger = logging.getLogger(__name__)


class ImageHandler:
    """图像处理器"""
    
    def __init__(self, file_path):
        """
        初始化图像处理器
        
        Args:
            file_path: 图像文件路径
        """
        self.file_path = Path(file_path)
        self.image = None
        self.image_cv = None
        self.metadata = {}
        
    def load(self):
        """
        加载图像文件
        
        Returns:
            dict: 加载结果
        """
        try:
            # 使用 PIL 加载图像
            self.image = Image.open(self.file_path)
            
            # 使用 OpenCV 加载图像用于处理
            self.image_cv = cv2.imread(str(self.file_path))
            
            self.metadata = {
                'width': self.image.width,
                'height': self.image.height,
                'format': self.image.format,
                'mode': self.image.mode,
                'size': self.file_path.stat().st_size
            }
            
            logger.info(f"成功加载图像: {self.file_path}")
            return {
                'success': True,
                'file': str(self.file_path),
                'metadata': self.metadata
            }
        except Exception as e:
            logger.error(f"图像加载失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def resize(self, width, height, maintain_aspect=True):
        """
        调整图像大小
        
        Args:
            width: 目标宽度
            height: 目标高度
            maintain_aspect: 是否保持宽高比
            
        Returns:
            Image: 调整后的图像
        """
        if maintain_aspect:
            self.image.thumbnail((width, height), Image.Resampling.LANCZOS)
        else:
            self.image = self.image.resize((width, height), Image.Resampling.LANCZOS)
        
        return self.image
    
    def detect_best_position(self, target_width, target_height):
        """
        检测最佳插入位置（基于图像内容检测）
        
        Args:
            target_width: 目标宽度
            target_height: 目标高度
            
        Returns:
            dict: 建议的插入位置
        """
        try:
            if self.image_cv is None:
                return {'success': False, 'error': '图像未加载'}
            
            # 将图像转换为灰度
            gray = cv2.cvtColor(self.image_cv, cv2.COLOR_BGR2GRAY)
            
            # 检测边缘
            edges = cv2.Canny(gray, 100, 200)
            
            # 检测轮廓
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                # 如果没有找到轮廓，返回图像中心
                return {
                    'success': True,
                    'position': 'center',
                    'recommended_width': target_width,
                    'recommended_height': target_height
                }
            
            # 找到最大的轮廓
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            return {
                'success': True,
                'position': 'detected',
                'x': x,
                'y': y,
                'width': w,
                'height': h,
                'recommended_width': target_width,
                'recommended_height': target_height
            }
        except Exception as e:
            logger.error(f"位置检测失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def save(self, output_path, quality=95):
        """
        保存图像
        
        Args:
            output_path: 输出路径
            quality: 图像质量 (1-100)
            
        Returns:
            dict: 保存结果
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if self.image.format == 'JPEG' or output_path.suffix.lower() == '.jpg':
                self.image.save(output_path, quality=quality)
            else:
                self.image.save(output_path)
            
            logger.info(f"图像已保存: {output_path}")
            return {
                'success': True,
                'file': str(output_path)
            }
        except Exception as e:
            logger.error(f"图像保存失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_image_array(self):
        """
        获取图像数组
        
        Returns:
            np.ndarray: 图像数组
        """
        return self.image_cv