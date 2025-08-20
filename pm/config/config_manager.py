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
        self.menu_data = None  # 存储加载的menu.json数据
    
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
    
    def load_menu_json(self, project_name: str) -> bool:
        """
        加载现有项目的menu.json文件
        
        Args:
            project_name: 项目名称
            
        Returns:
            bool: 加载是否成功
        """
        try:
            menu_file = Path(project_name) / 'menu.json'
            with open(menu_file, 'r', encoding='utf-8') as f:
                self.menu_data = json.load(f)
                return True
        except FileNotFoundError:
            print(f"❌ 菜单配置文件 {menu_file} 不存在")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ 菜单配置文件格式错误: {e}")
            return False
    
    def save_menu_json(self, project_name: str) -> bool:
        """
        保存menu.json文件
        
        Args:
            project_name: 项目名称
            
        Returns:
            bool: 保存是否成功
        """
        try:
            menu_file = Path(project_name) / 'menu.json'
            with open(menu_file, 'w', encoding='utf-8') as f:
                json.dump(self.menu_data, f, ensure_ascii=False, indent=2)
                return True
        except Exception as e:
            print(f"❌ 保存菜单配置文件失败: {e}")
            return False
    
    def find_page_by_name(self, page_name: str) -> Optional[Dict[str, Any]]:
        """
        根据页面名称查找页面信息
        
        Args:
            page_name: 页面名称
            
        Returns:
            Optional[Dict[str, Any]]: 页面信息字典，如果未找到返回None
        """
        if not self.menu_data:
            return None
        
        for role in self.menu_data:
            for module in role.get('modules', []):
                for page in module.get('pages', []):
                    if page.get('name') == page_name:
                        return page
        
        return None
    
    def list_all_pages(self) -> list:
        """
        列出所有页面信息
        
        Returns:
            list: 包含所有页面信息的列表
        """
        pages = []
        if not self.menu_data:
            return pages
        
        for role in self.menu_data:
            for module in role.get('modules', []):
                for page in module.get('pages', []):
                    page_info = page.copy()
                    page_info['role_name'] = role.get('name')
                    page_info['module_name'] = module.get('name')
                    pages.append(page_info)
        
        return pages
    
    def add_page_to_structure(self, role_name: str, module_name: str, 
                             page_name: str, page_desc: str = "") -> bool:
        """
        在现有结构中添加新页面
        
        Args:
            role_name: 角色名称
            module_name: 模块名称
            page_name: 页面名称
            page_desc: 页面描述
            
        Returns:
            bool: 添加是否成功
        """
        try:
            # 查找角色
            target_role = None
            for role in self.config['roles']:
                if role['name'] == role_name:
                    target_role = role
                    break
            
            if not target_role:
                print(f"❌ 未找到角色: {role_name}")
                return False
            
            # 查找模块
            target_module = None
            for module in target_role['modules']:
                if module['name'] == module_name:
                    target_module = module
                    break
            
            if not target_module:
                print(f"❌ 在角色 '{role_name}' 中未找到模块: {module_name}")
                return False
            
            # 检查页面是否已存在
            for page in target_module['pages']:
                if page['name'] == page_name:
                    print(f"❌ 页面 '{page_name}' 已存在")
                    return False
            
            # 添加新页面
            new_page = {
                "name": page_name,
                "description": page_desc or f"{page_name}功能页面"
            }
            target_module['pages'].append(new_page)
            
            print(f"✅ 成功添加页面 '{page_name}' 到 {role_name}/{module_name}")
            return True
            
        except Exception as e:
            print(f"❌ 添加页面失败: {e}")
            return False
    
    def add_module_to_role(self, role_name: str, module_name: str, 
                          module_desc: str = "", pages_list: list = None) -> bool:
        """
        为现有角色添加新模块
        
        Args:
            role_name: 角色名称
            module_name: 模块名称
            module_desc: 模块描述
            pages_list: 页面列表
            
        Returns:
            bool: 添加是否成功
        """
        try:
            # 查找角色
            target_role = None
            for role in self.config['roles']:
                if role['name'] == role_name:
                    target_role = role
                    break
            
            if not target_role:
                print(f"❌ 未找到角色: {role_name}")
                return False
            
            # 检查模块是否已存在
            for module in target_role['modules']:
                if module['name'] == module_name:
                    print(f"❌ 模块 '{module_name}' 已存在")
                    return False
            
            # 创建页面列表
            pages = []
            if pages_list:
                for page_name in pages_list:
                    pages.append({
                        "name": page_name.strip(),
                        "description": f"{page_name.strip()}功能页面"
                    })
            else:
                pages.append({
                    "name": f"{module_name}页面1",
                    "description": f"{module_name}功能页面"
                })
            
            # 添加新模块
            new_module = {
                "name": module_name,
                "description": module_desc or f"{module_name}功能模块",
                "pages": pages
            }
            target_role['modules'].append(new_module)
            
            print(f"✅ 成功添加模块 '{module_name}' 到角色 '{role_name}'")
            return True
            
        except Exception as e:
            print(f"❌ 添加模块失败: {e}")
            return False
    
    def add_role_to_project(self, role_name: str, role_desc: str = "", 
                           modules_config: list = None) -> bool:
        """
        为项目添加新角色
        
        Args:
            role_name: 角色名称
            role_desc: 角色描述
            modules_config: 模块配置列表
            
        Returns:
            bool: 添加是否成功
        """
        try:
            # 检查角色是否已存在
            for role in self.config['roles']:
                if role['name'] == role_name:
                    print(f"❌ 角色 '{role_name}' 已存在")
                    return False
            
            # 创建默认模块配置
            if not modules_config:
                modules_config = [{
                    "name": f"{role_name}核心功能",
                    "description": f"{role_name}的核心功能模块",
                    "pages": [{
                        "name": f"{role_name}主页",
                        "description": f"{role_name}的主要功能页面"
                    }]
                }]
            
            # 添加新角色
            new_role = {
                "name": role_name,
                "description": role_desc or f"{role_name}用户角色",
                "modules": modules_config
            }
            self.config['roles'].append(new_role)
            
            print(f"✅ 成功添加角色 '{role_name}'")
            return True
            
        except Exception as e:
            print(f"❌ 添加角色失败: {e}")
            return False