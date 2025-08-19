"""
CSS样式管理器
负责管理CSS样式的生成
"""

import sys
from pathlib import Path

# 添加父目录到路径以支持导入
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from templates.css_templates import CSSTemplates


class StyleManager:
    """CSS样式管理器类"""
    
    def __init__(self, platform_type: str = "mobile"):
        self.platform_type = platform_type
        self.css_templates = CSSTemplates()
    
    def generate_style_css(self) -> str:
        """
        生成style.css文件内容
        
        Returns:
            str: CSS样式内容
        """
        return self.css_templates.get_style_css()
    
    def get_platform_specific_styles(self) -> str:
        """
        获取平台特定的样式
        
        Returns:
            str: 平台特定的CSS样式
        """
        if self.platform_type == "mobile":
            return """
/* 手机端特有样式 */
@media (max-width: 768px) {
  .iphone-frame {
    margin: 10px auto;
    transform: scale(0.9);
  }
  
  .page-content {
    font-size: 14px;
  }
}"""
        else:
            return """
/* PC端特有样式 */
@media (min-width: 769px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .grid-responsive {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
  }
}"""