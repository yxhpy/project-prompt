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
        # 检查项目目录是否已存在
        if Path(args.name).exists() and not args.force:
            print(f"❌ 项目目录 '{args.name}' 已存在，使用 --force 参数强制覆盖")
            return False
        
        # 检查配置文件是否存在（如果指定了的话）
        if args.config and not Path(args.config).exists():
            print(f"❌ 配置文件 '{args.config}' 不存在")
            return False
        
        return True