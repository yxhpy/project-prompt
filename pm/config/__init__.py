"""
配置管理模块
提供项目配置的加载、验证和管理功能
"""

from .config_manager import ConfigManager
from .default_config import DEFAULT_CONFIG

__all__ = ['ConfigManager', 'DEFAULT_CONFIG']