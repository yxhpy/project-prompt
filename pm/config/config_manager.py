"""
配置管理器
负责配置文件的加载、验证和合并处理
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# 添加当前目录到路径以支持导入
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from default_config import DEFAULT_CONFIG


class ConfigManager:
    """配置管理器类"""
    
    def __init__(self):
        self.config = DEFAULT_CONFIG.copy()
    
    def load_from_file(self, config_file: str) -> bool:
        """
        从文件加载配置
        
        Args:
            config_file: 配置文件路径
            
        Returns:
            bool: 加载是否成功
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                custom_config = json.load(f)
                self.config.update(custom_config)
                return True
        except FileNotFoundError:
            print(f"❌ 配置文件 {config_file} 不存在")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ 配置文件格式错误: {e}")
            return False
    
    def update_from_args(self, title: Optional[str] = None, 
                        description: Optional[str] = None) -> None:
        """
        从命令行参数更新配置
        
        Args:
            title: 项目标题
            description: 项目描述
        """
        if title:
            self.config['project_name'] = title
        if description:
            self.config['project_description'] = description
    
    def validate_config(self) -> bool:
        """
        验证配置文件格式
        
        Returns:
            bool: 配置是否有效
        """
        required_fields = ['project_name', 'project_description', 'roles']
        
        for field in required_fields:
            if field not in self.config:
                print(f"❌ 配置缺少必需字段: {field}")
                return False
        
        if not isinstance(self.config['roles'], list) or len(self.config['roles']) == 0:
            print("❌ 配置中的roles字段必须是非空数组")
            return False
        
        return True
    
    def get_config(self) -> Dict[str, Any]:
        """
        获取当前配置
        
        Returns:
            Dict[str, Any]: 配置字典
        """
        return self.config
    
    def generate_menu_json(self) -> str:
        """
        根据配置生成menu.json内容
        
        Returns:
            str: JSON格式的菜单配置
        """
        menu_data = []
        
        for role_index, role in enumerate(self.config['roles']):
            role_data = {
                "name": role['name'],
                "modules": []
            }
            
            for module_index, module in enumerate(role['modules']):
                module_data = {
                    "name": module['name'],
                    "pages": []
                }
                
                for page_index, page in enumerate(module['pages']):
                    role_dir = f"role{role_index + 1}"
                    module_dir = f"module{chr(65 + module_index)}"
                    page_file = f"page{page_index + 1}.html"
                    
                    page_data = {
                        "name": page['name'],
                        "url": f"pages/{role_dir}/{module_dir}/{page_file}",
                        "status": page.get('status', 'pending'),
                        "completed_at": page.get('completed_at', None),
                        "priority": page.get('priority', 'normal')
                    }
                    module_data['pages'].append(page_data)
                
                role_data['modules'].append(module_data)
            
            menu_data.append(role_data)
        
        return json.dumps(menu_data, ensure_ascii=False, indent=2)