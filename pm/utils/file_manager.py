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
    
    def update_page_content(self, page_url: str, content_file: str, platform_type: str = "mobile", 
                           page_name: str = "", page_desc: str = "", 
                           role_name: str = "", module_name: str = "", 
                           keep_source: bool = False) -> bool:
        """
        更新页面内容 - 支持业务代码自动包装
        
        Args:
            page_url: 页面URL路径（相对于项目根目录）
            content_file: 新内容文件路径（业务代码）
            platform_type: 平台类型（mobile/pc）
            page_name: 页面名称
            page_desc: 页面描述  
            role_name: 角色名称
            module_name: 模块名称
            keep_source: 是否保留源文件（默认False，自动删除）
            
        Returns:
            bool: 更新是否成功
        """
        try:
            # 读取业务代码内容
            content_path = Path(content_file)
            if not content_path.exists():
                print(f"❌ 内容文件 {content_file} 不存在")
                return False
            
            business_content = content_path.read_text(encoding='utf-8')
            
            # 目标页面文件路径
            target_file = self.project_path / page_url
            if not target_file.exists():
                print(f"❌ 目标页面文件 {target_file} 不存在")
                return False
            
            # 导入模板生成器
            import sys
            current_dir = Path(__file__).parent.parent
            sys.path.insert(0, str(current_dir))
            from templates.html_templates import HTMLTemplates
            
            # 根据平台类型生成完整页面
            if platform_type == "mobile":
                # 手机模式：使用手机框架包装业务内容
                full_page = self._wrap_mobile_content(business_content, page_name, page_desc, role_name, module_name)
            else:
                # PC模式：生成完整页面，业务内容替换默认内容
                full_page = self._wrap_pc_content(business_content, page_name, page_desc, role_name, module_name)
            
            # 更新页面内容
            target_file.write_text(full_page, encoding='utf-8')
            
            # 成功更新后删除源HTML文件（除非用户指定保留）
            if not keep_source:
                try:
                    content_path.unlink()
                    print(f"✅ 已删除源文件: {content_file}")
                except Exception as e:
                    print(f"⚠️  删除源文件失败: {e}")
            else:
                print(f"📁 保留源文件: {content_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ 更新页面内容失败: {e}")
            return False
    
    def _wrap_mobile_content(self, business_content: str, page_name: str, 
                           page_desc: str, role_name: str, module_name: str) -> str:
        """
        包装手机端业务内容
        
        Args:
            business_content: 业务代码内容
            page_name: 页面名称
            page_desc: 页面描述
            role_name: 角色名称
            module_name: 模块名称
            
        Returns:
            str: 完整的手机端页面HTML
        """
        from templates.html_templates import HTMLTemplates
        
        # 获取手机框架模板
        frame_template = HTMLTemplates.get_mobile_frame_template()
        
        # 替换页面内容占位符
        full_page = frame_template.replace('<!-- 页面内容将在这里替换 -->', business_content)
        
        # 更新标题
        if page_name:
            full_page = full_page.replace('手机页面框架', f'{page_name} - {role_name}')
        
        return full_page
    
    def _wrap_pc_content(self, business_content: str, page_name: str, 
                        page_desc: str, role_name: str, module_name: str) -> str:
        """
        包装PC端业务内容
        
        Args:
            business_content: 业务代码内容
            page_name: 页面名称
            page_desc: 页面描述
            role_name: 角色名称
            module_name: 模块名称
            
        Returns:
            str: 完整的PC端页面HTML
        """
        from templates.html_templates import HTMLTemplates
        
        # PC模式：生成完整页面模板，然后替换body内容
        if not page_name:
            page_name = "页面标题"
        if not page_desc:
            page_desc = "页面描述"
        if not role_name:
            role_name = "角色"
        if not module_name:
            module_name = "模块"
            
        # 获取PC页面模板
        pc_template = HTMLTemplates.get_pc_page_template(page_name, page_desc, role_name, module_name)
        
        # 提取body标签内的内容，替换为业务内容
        import re
        body_pattern = r'<body[^>]*>(.*?)</body>'
        match = re.search(body_pattern, pc_template, re.DOTALL)
        
        if match:
            # 保留body标签属性，替换内容
            body_start = pc_template.find('<body')
            body_end = pc_template.find('>', body_start) + 1
            body_close = pc_template.rfind('</body>')
            
            body_tag = pc_template[body_start:body_end]
            result = pc_template[:body_end] + '\n' + business_content + '\n' + pc_template[body_close:]
            return result
        else:
            # 如果没有找到body标签，直接返回业务内容包装在基本HTML结构中
            return f'''<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <title>{page_name} - {role_name}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="../../../style.css">
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            'gray-custom': '#f5f5f5',
            'border-custom': '#cccccc',
            'text-primary': '#333333',
            'text-secondary': '#666666'
          }}
        }}
      }}
    }}
  </script>
</head>
<body class="font-sans bg-gray-custom">
{business_content}
</body>
</html>'''
    
    def backup_page(self, page_url: str) -> bool:
        """
        备份页面文件
        
        Args:
            page_url: 页面URL路径（相对于项目根目录）
            
        Returns:
            bool: 备份是否成功
        """
        try:
            from datetime import datetime
            
            source_file = self.project_path / page_url
            if not source_file.exists():
                print(f"❌ 源页面文件 {source_file} 不存在")
                return False
            
            # 生成备份文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{source_file.stem}_backup_{timestamp}{source_file.suffix}"
            backup_file = source_file.parent / backup_name
            
            # 复制文件
            import shutil
            shutil.copy2(source_file, backup_file)
            
            print(f"✅ 页面已备份到: {backup_file}")
            return True
            
        except Exception as e:
            print(f"❌ 备份页面失败: {e}")
            return False
    
    def create_new_page_file(self, role_name: str, module_name: str, 
                            page_name: str, page_desc: str, platform_type: str = "mobile") -> bool:
        """
        为新增的页面创建HTML文件
        
        Args:
            role_name: 角色名称
            module_name: 模块名称
            page_name: 页面名称
            page_desc: 页面描述
            platform_type: 平台类型
            
        Returns:
            bool: 创建是否成功
        """
        try:
            # 导入模板生成器
            import sys
            current_dir = Path(__file__).parent.parent
            sys.path.insert(0, str(current_dir))
            from generators.template_generator import TemplateGenerator
            
            # 创建目录结构
            role_dir = self.project_path / "pages" / self._safe_filename(role_name)
            module_dir = role_dir / self._safe_filename(module_name)
            module_dir.mkdir(parents=True, exist_ok=True)
            
            # 生成页面文件名（查找现有页面数量，生成新的编号）
            existing_pages = list(module_dir.glob("*.html"))
            page_num = len(existing_pages) + 1
            page_filename = f"page{page_num}.html"
            page_file = module_dir / page_filename
            
            # 创建虚拟配置
            temp_config = {
                "project_name": self.project_name,
                "project_description": f"{self.project_name}项目"
            }
            
            # 生成页面内容
            template_generator = TemplateGenerator(temp_config, platform_type)
            page_content = template_generator.generate_page_html(
                page_name, page_desc, role_name, module_name
            )
            
            # 写入文件
            page_file.write_text(page_content, encoding='utf-8')
            
            print(f"✅ 成功创建页面文件: {page_file}")
            return True
            
        except Exception as e:
            print(f"❌ 创建页面文件失败: {e}")
            return False
    
    def create_new_module_directory(self, role_name: str, module_name: str) -> bool:
        """
        为新增的模块创建目录
        
        Args:
            role_name: 角色名称
            module_name: 模块名称
            
        Returns:
            bool: 创建是否成功
        """
        try:
            role_dir = self.project_path / "pages" / self._safe_filename(role_name)
            module_dir = role_dir / self._safe_filename(module_name)
            module_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"✅ 成功创建模块目录: {module_dir}")
            return True
            
        except Exception as e:
            print(f"❌ 创建模块目录失败: {e}")
            return False
    
    def create_new_role_directory(self, role_name: str) -> bool:
        """
        为新增的角色创建目录
        
        Args:
            role_name: 角色名称
            
        Returns:
            bool: 创建是否成功
        """
        try:
            role_dir = self.project_path / "pages" / self._safe_filename(role_name)
            role_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"✅ 成功创建角色目录: {role_dir}")
            return True
            
        except Exception as e:
            print(f"❌ 创建角色目录失败: {e}")
            return False
    
    def _safe_filename(self, name: str) -> str:
        """
        将名称转换为安全的文件名
        
        Args:
            name: 原始名称
            
        Returns:
            str: 安全的文件名
        """
        import re
        # 移除特殊字符，保留中文字符、字母、数字和连字符
        safe_name = re.sub(r'[^\w\u4e00-\u9fff\-]', '_', name)
        return safe_name
    
    def print_success_message(self) -> None:
        """打印成功消息"""
        print(f"✅ 项目 '{self.project_name}' 创建成功！")
        print(f"📁 项目路径: {self.project_path.absolute()}")
        print(f"🌐 打开 {self.project_path.absolute()}/index.html 查看原型")