#!/usr/bin/env python3
"""
产品原型生成工具 - 主入口脚本（模块化重构版本）

这是原template.py的重构版本，将1730行的大型脚本拆分为多个专注的模块。

模块说明：
- config/: 配置管理相关模块
- generators/: 内容生成器模块  
- templates/: 模板定义模块
- utils/: 工具函数模块

主要改进：
1. 代码模块化，提高可维护性
2. 职责分离，每个模块专注单一功能
3. 保持所有原有功能完整性
4. 提升代码复用性和扩展性
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径，确保可以导入自定义模块
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from config.config_manager import ConfigManager
from generators.template_generator import TemplateGenerator
from generators.style_manager import StyleManager
from generators.script_manager import ScriptManager
from utils.file_manager import FileManager
from utils.cli_parser import CLIParser


class PrototypeGenerator:
    """产品原型生成器主类"""
    
    def __init__(self):
        self.cli_parser = CLIParser()
        self.config_manager = ConfigManager()
    
    def run(self):
        """运行主程序"""
        try:
            # 解析命令行参数
            args = self.cli_parser.parse_args()
            
            # 验证参数
            if not self.cli_parser.validate_args(args):
                return
            
            # 判断运行模式
            if hasattr(args, 'update_page') and args.update_page:
                # 页面更新模式
                if not self._update_page(args):
                    return
                self._print_update_success_info(args)
            else:
                # 项目创建模式
                # 加载配置
                if not self._load_config(args):
                    return
                
                # 创建项目
                if not self._create_project(args):
                    return
                
                # 输出成功信息
                self._print_success_info(args)
            
        except KeyboardInterrupt:
            print("\n❌ 用户中断操作")
        except Exception as e:
            print(f"❌ 运行出错: {e}")
    
    def _load_config(self, args) -> bool:
        """加载配置"""
        # 从文件加载配置（如果指定了）
        if args.config:
            if not self.config_manager.load_from_file(args.config):
                return False
        
        # 从命令行参数更新配置
        self.config_manager.update_from_args(args.title, args.description)
        
        # 验证配置
        if not self.config_manager.validate_config():
            return False
        
        return True
    
    def _create_project(self, args) -> bool:
        """创建项目"""
        # 获取配置
        config = self.config_manager.get_config()
        
        # 创建文件管理器
        file_manager = FileManager(args.name)
        
        # 创建目录结构
        if not file_manager.create_project_structure(config):
            return False
        
        # 创建生成器
        template_generator = TemplateGenerator(config, args.platform)
        style_manager = StyleManager(args.platform)
        script_manager = ScriptManager()
        
        # 生成并写入各种文件
        files_to_create = [
            ("index.html", template_generator.generate_index_html()),
            ("style.css", style_manager.generate_style_css()),
            ("progress.js", script_manager.generate_progress_js()),
            ("menu.json", self.config_manager.generate_menu_json()),
            ("design-standards.md", template_generator.generate_design_standards()),
            ("README.md", template_generator.generate_readme()),
        ]
        
        # 写入所有文件
        for filename, content in files_to_create:
            if not file_manager.write_file(filename, content):
                return False
        
        # 创建页面文件
        if not file_manager.create_page_files(
            config, 
            template_generator.generate_page_html
        ):
            return False
        
        return True
    
    def _update_page(self, args) -> bool:
        """更新页面"""
        from datetime import datetime
        
        # 创建文件管理器
        file_manager = FileManager(args.name)
        
        # 加载现有的menu.json配置
        if not self.config_manager.load_menu_json(args.name):
            return False
        
        # 查找页面
        page_info = self.config_manager.find_page_by_name(args.update_page)
        if not page_info:
            print(f"❌ 未找到页面: {args.update_page}")
            return False
        
        # 更新页面状态
        if hasattr(args, 'status') and args.status:
            page_info['status'] = args.status
            if args.status == 'completed':
                page_info['completed_at'] = datetime.now().isoformat()
            print(f"✅ 页面 '{args.update_page}' 状态已更新为: {args.status}")
        
        # 更新页面内容
        if hasattr(args, 'page_content') and args.page_content:
            # 获取平台类型，默认为mobile
            platform_type = getattr(args, 'platform', 'mobile')
            
            # 获取页面信息
            page_name = args.update_page
            page_desc = f"{page_name}页面"
            role_name = "角色"  # 可以从page_info中获取更详细信息
            module_name = "模块"
            
            # 获取是否保留源文件的设置
            keep_source = getattr(args, 'keep_source', False)
            
            if not file_manager.update_page_content(
                page_info['url'], 
                args.page_content,
                platform_type,
                page_name,
                page_desc,
                role_name,
                module_name,
                keep_source
            ):
                return False
            print(f"✅ 页面 '{args.update_page}' 内容已更新（{platform_type}模式）")
        
        # 保存更新后的menu.json
        if not self.config_manager.save_menu_json(args.name):
            return False
        
        return True
    
    def _print_update_success_info(self, args):
        """打印页面更新成功信息"""
        print(f"\n🎉 页面更新完成!")
        print(f"📄 项目: {args.name}")
        print(f"📝 页面: {args.update_page}")
        
        if hasattr(args, 'status') and args.status:
            print(f"📊 状态: {args.status}")
        
        if hasattr(args, 'page_content') and args.page_content:
            print(f"📁 内容文件: {args.page_content}")
    
    def _print_success_info(self, args):
        """打印成功信息"""
        file_manager = FileManager(args.name)
        file_manager.print_success_message()
        
        print(f"📱 平台类型: {'手机端' if args.platform == 'mobile' else 'PC端'}")
        if args.platform == 'mobile':
            print("📱 已包含iPhone手机壳模板")
        
        print("\n🎉 重构版本特性:")
        print("   ✅ 模块化架构，代码更清晰易维护")
        print("   ✅ 保留所有原有功能")
        print("   ✅ 提升代码复用性和扩展性")
        print("   ✅ 更好的错误处理和用户体验")


def main():
    """主函数"""
    generator = PrototypeGenerator()
    generator.run()


if __name__ == '__main__':
    main()