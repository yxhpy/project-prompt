"""
模板定义模块
包含HTML、CSS、JavaScript模板的定义
"""

from .html_templates import HTMLTemplates
from .css_templates import CSSTemplates
from .js_templates import JSTemplates

__all__ = ['HTMLTemplates', 'CSSTemplates', 'JSTemplates']