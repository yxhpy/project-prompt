"""
命令行参数解析器
负责处理命令行参数的解析和验证
"""

import argparse
from pathlib import Path


class CLIParser:
    """命令行参数解析器类"""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """创建参数解析器"""
        parser = argparse.ArgumentParser(
            description='通用产品原型生成工具（模块化版本）',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""使用示例:
  python main.py -n my-project                    # 使用默认配置（手机端）
  python main.py -n my-project -c config.json    # 使用自定义配置
  python main.py -n my-project --title "我的产品"  # 自定义项目标题
  python main.py -n my-project --platform pc     # 创建PC端项目
  python main.py -n my-project --platform mobile # 创建手机端项目（默认）

配置文件格式请参考默认配置示例。

页面更新示例:
  python main.py -n my-project --update-page "用户登录" --status completed
  python main.py -n my-project --update-page "用户登录" --page-content login.html
  python main.py -n my-project --update-page "用户登录" --status completed --page-content login.html
            """
        )
        
        parser.add_argument('-n', '--name', required=True, 
                           help='项目名称（将作为目录名）')
        parser.add_argument('-c', '--config', 
                           help='自定义配置文件路径（JSON格式）')
        parser.add_argument('--title', 
                           help='项目标题（显示名称）')
        parser.add_argument('--description', 
                           help='项目描述')
        parser.add_argument('--platform', choices=['mobile', 'pc'], default='mobile',
                           help='平台类型：mobile（手机端，默认）或 pc（PC端）')
        parser.add_argument('--force', action='store_true',
                           help='强制覆盖已存在的项目目录')
        
        # 页面更新相关参数
        parser.add_argument('--update-page', 
                           help='更新指定页面（页面名称）')
        parser.add_argument('--status', 
                           choices=['pending', 'in_progress', 'pending_review', 'optimizing', 'completed'],
                           help='设置页面状态')
        parser.add_argument('--page-content', 
                           help='页面内容文件路径（HTML文件）')
        parser.add_argument('--keep-source', action='store_true',
                           help='保留源HTML文件（默认会自动删除）')
        
        # 新增页面/模块/角色相关参数
        parser.add_argument('--add-page', action='store_true',
                           help='新增页面到现有结构')
        parser.add_argument('--add-module', action='store_true', 
                           help='新增模块到现有角色')
        parser.add_argument('--add-role', action='store_true',
                           help='新增角色')
        parser.add_argument('--role', 
                           help='目标角色名称')
        parser.add_argument('--module',
                           help='目标模块名称')
        parser.add_argument('--page-name',
                           help='新页面名称')
        parser.add_argument('--page-desc',
                           help='新页面描述')
        parser.add_argument('--module-name',
                           help='新模块名称')
        parser.add_argument('--module-desc', 
                           help='新模块描述')
        parser.add_argument('--role-name',
                           help='新角色名称')
        parser.add_argument('--role-desc',
                           help='新角色描述')
        parser.add_argument('--pages',
                           help='页面列表（逗号分隔）')
        
        return parser
    
    def parse_args(self):
        """
        解析命令行参数
        
        Returns:
            argparse.Namespace: 解析后的参数
        """
        return self.parser.parse_args()
    
    def validate_args(self, args) -> bool:
        """
        验证参数的有效性
        
        Args:
            args: 解析后的参数对象
            
        Returns:
            bool: 参数是否有效
        """
        # 新增功能模式的验证
        if hasattr(args, 'add_page') and args.add_page:
            # 新增页面模式：项目目录必须存在
            if not Path(args.name).exists():
                print(f"❌ 项目目录 '{args.name}' 不存在，无法新增页面")
                return False
            
            # 检查必需参数
            if not all([args.role, args.module, args.page_name]):
                print("❌ 新增页面模式必须指定 --role、--module、--page-name 参数")
                return False
                
        elif hasattr(args, 'add_module') and args.add_module:
            # 新增模块模式：项目目录必须存在
            if not Path(args.name).exists():
                print(f"❌ 项目目录 '{args.name}' 不存在，无法新增模块")
                return False
            
            # 检查必需参数
            if not all([args.role, args.module_name]):
                print("❌ 新增模块模式必须指定 --role、--module-name 参数")
                return False
                
        elif hasattr(args, 'add_role') and args.add_role:
            # 新增角色模式：项目目录必须存在
            if not Path(args.name).exists():
                print(f"❌ 项目目录 '{args.name}' 不存在，无法新增角色")
                return False
            
            # 检查必需参数
            if not args.role_name:
                print("❌ 新增角色模式必须指定 --role-name 参数")
                return False
        
        # 页面更新模式的验证
        elif hasattr(args, 'update_page') and args.update_page:
            # 页面更新模式：项目目录必须存在
            if not Path(args.name).exists():
                print(f"❌ 项目目录 '{args.name}' 不存在，无法更新页面")
                return False
            
            # 检查menu.json是否存在
            menu_file = Path(args.name) / 'menu.json'
            if not menu_file.exists():
                print(f"❌ 项目配置文件 '{menu_file}' 不存在")
                return False
            
            # 检查页面内容文件是否存在（如果指定了的话）
            if hasattr(args, 'page_content') and args.page_content:
                if not Path(args.page_content).exists():
                    print(f"❌ 页面内容文件 '{args.page_content}' 不存在")
                    return False
            
            # 页面更新模式必须指定状态或内容
            if not (hasattr(args, 'status') and args.status) and not (hasattr(args, 'page_content') and args.page_content):
                print("❌ 页面更新模式必须指定 --status 或 --page-content 参数")
                return False
        else:
            # 项目创建模式的验证
            # 检查项目目录是否已存在
            if Path(args.name).exists() and not args.force:
                print(f"❌ 项目目录 '{args.name}' 已存在，使用 --force 参数强制覆盖")
                return False
        
        # 检查配置文件是否存在（如果指定了的话）
        if args.config and not Path(args.config).exists():
            print(f"❌ 配置文件 '{args.config}' 不存在")
            return False
        
        return True