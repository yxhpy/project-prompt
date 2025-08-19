"""
文件系统管理器
负责文件和目录的创建、写入等操作
"""

import os
from pathlib import Path
from typing import Dict, Any


class FileManager:
    """文件系统管理器类"""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_path = Path(project_name)
    
    def create_project_structure(self, config: Dict[str, Any]) -> bool:
        """
        创建项目目录结构
        
        Args:
            config: 项目配置
            
        Returns:
            bool: 创建是否成功
        """
        try:
            # 创建主项目目录
            self.project_path.mkdir(exist_ok=True)
            
            # 创建pages目录结构
            pages_dir = self.project_path / "pages"
            pages_dir.mkdir(exist_ok=True)
            
            for role_index, role in enumerate(config['roles']):
                role_dir = pages_dir / f"role{role_index + 1}"
                role_dir.mkdir(exist_ok=True)
                
                for module_index, module in enumerate(role['modules']):
                    module_dir = role_dir / f"module{chr(65 + module_index)}"
                    module_dir.mkdir(exist_ok=True)
            
            return True
        except Exception as e:
            print(f"❌ 创建目录结构失败: {e}")
            return False
    
    def write_file(self, filename: str, content: str) -> bool:
        """
        写入文件
        
        Args:
            filename: 文件名（相对于项目根目录）
            content: 文件内容
            
        Returns:
            bool: 写入是否成功
        """
        try:
            file_path = self.project_path / filename
            
            # 确保父目录存在
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 写入文件
            file_path.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"❌ 写入文件 {filename} 失败: {e}")
            return False
    
    def create_page_files(self, config: Dict[str, Any], page_generator) -> bool:
        """
        创建所有页面文件
        
        Args:
            config: 项目配置
            page_generator: 页面生成器函数
            
        Returns:
            bool: 创建是否成功
        """
        try:
            for role_index, role in enumerate(config['roles']):
                for module_index, module in enumerate(role['modules']):
                    for page_index, page in enumerate(module['pages']):
                        # 生成文件路径
                        role_dir = f"role{role_index + 1}"
                        module_dir = f"module{chr(65 + module_index)}"
                        page_file = f"page{page_index + 1}.html"
                        
                        file_path = f"pages/{role_dir}/{module_dir}/{page_file}"
                        
                        # 生成页面内容
                        page_content = page_generator(
                            page['name'], 
                            page['description'], 
                            role['name'], 
                            module['name']
                        )
                        
                        # 写入文件
                        if not self.write_file(file_path, page_content):
                            return False
            
            return True
        except Exception as e:
            print(f"❌ 创建页面文件失败: {e}")
            return False
    
    def get_project_path(self) -> Path:
        """
        获取项目路径
        
        Returns:
            Path: 项目路径对象
        """
        return self.project_path
    
    def check_project_exists(self) -> bool:
        """
        检查项目目录是否已存在
        
        Returns:
            bool: 项目目录是否存在
        """
        return self.project_path.exists()
    
    def print_success_message(self) -> None:
        """打印成功消息"""
        print(f"✅ 项目 '{self.project_name}' 创建成功！")
        print(f"📁 项目路径: {self.project_path.absolute()}")
        print(f"🌐 打开 {self.project_path.absolute()}/index.html 查看原型")