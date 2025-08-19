"""
JavaScript脚本管理器
负责管理JavaScript文件的生成
"""

import sys
from pathlib import Path

# 添加父目录到路径以支持导入
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from templates.js_templates import JSTemplates


class ScriptManager:
    """JavaScript脚本管理器类"""
    
    def __init__(self):
        self.js_templates = JSTemplates()
    
    def generate_progress_js(self) -> str:
        """
        生成progress.js文件内容
        
        Returns:
            str: JavaScript内容
        """
        return self.js_templates.get_progress_js()
    
    def get_additional_scripts(self) -> str:
        """
        获取额外的JavaScript功能
        
        Returns:
            str: 额外的JavaScript代码
        """
        return """
// 额外的交互功能
function initializeTooltips() {
  const elements = document.querySelectorAll('[data-tooltip]');
  elements.forEach(element => {
    element.addEventListener('mouseenter', function() {
      const tooltip = document.createElement('div');
      tooltip.className = 'tooltip';
      tooltip.textContent = this.getAttribute('data-tooltip');
      document.body.appendChild(tooltip);
      
      const rect = this.getBoundingClientRect();
      tooltip.style.left = rect.left + 'px';
      tooltip.style.top = (rect.bottom + 5) + 'px';
    });
    
    element.addEventListener('mouseleave', function() {
      const tooltip = document.querySelector('.tooltip');
      if (tooltip) {
        tooltip.remove();
      }
    });
  });
}

// 键盘快捷键支持
function initializeKeyboardShortcuts() {
  document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + F: 聚焦搜索框
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
      e.preventDefault();
      const searchBox = document.getElementById('search');
      if (searchBox) {
        searchBox.focus();
      }
    }
    
    // Escape: 清空搜索框
    if (e.key === 'Escape') {
      const searchBox = document.getElementById('search');
      if (searchBox && searchBox.value) {
        searchBox.value = '';
        searchBox.dispatchEvent(new Event('input'));
      }
    }
  });
}

// 页面加载完成后初始化额外功能
document.addEventListener('DOMContentLoaded', function() {
  initializeTooltips();
  initializeKeyboardShortcuts();
});"""