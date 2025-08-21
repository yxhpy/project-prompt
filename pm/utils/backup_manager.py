#!/usr/bin/env python3
"""
UX工程师备份管理工具
负责原型文件的安全备份和版本管理
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

class BackupManager:
    """原型文件备份管理器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backup_root = self.project_root / "backups"
        self.backup_root.mkdir(exist_ok=True)
        self.backup_index_file = self.backup_root / "backup_index.json"
    
    def create_backup(self, description: str = "") -> str:
        """
        创建项目备份
        
        Args:
            description: 备份描述
            
        Returns:
            str: 备份目录路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_id = f"backup_{timestamp}"
        backup_dir = self.backup_root / backup_id
        backup_dir.mkdir(exist_ok=True)
        
        # 备份关键文件和目录
        backup_items = [
            "pages",
            "index.html", 
            "style.css",
            "progress.js",
            "menu.json",
            "design-standards.md"
        ]
        
        backed_up_files = []
        for item in backup_items:
            item_path = self.project_root / item
            if item_path.exists():
                backup_target = backup_dir / item
                if item_path.is_dir():
                    shutil.copytree(item_path, backup_target)
                else:
                    shutil.copy2(item_path, backup_target)
                backed_up_files.append(str(item))
        
        # 记录备份信息
        backup_info = {
            "backup_id": backup_id,
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "files": backed_up_files,
            "project_root": str(self.project_root)
        }
        
        # 更新备份索引
        self._update_backup_index(backup_info)
        
        # 保存备份信息到备份目录
        with open(backup_dir / "backup_info.json", 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 备份完成: {backup_dir}")
        print(f"📝 备份描述: {description}")
        print(f"📂 备份文件数: {len(backed_up_files)}")
        
        return str(backup_dir)
    
    def list_backups(self) -> List[Dict]:
        """
        列出所有备份
        
        Returns:
            List[Dict]: 备份信息列表
        """
        if not self.backup_index_file.exists():
            return []
        
        with open(self.backup_index_file, 'r', encoding='utf-8') as f:
            backup_index = json.load(f)
        
        return backup_index.get('backups', [])
    
    def restore_backup(self, backup_id: str, confirm: bool = False) -> bool:
        """
        恢复指定备份
        
        Args:
            backup_id: 备份ID
            confirm: 是否确认恢复
            
        Returns:
            bool: 恢复是否成功
        """
        if not confirm:
            print("⚠️  恢复操作将覆盖当前文件，请使用 confirm=True 确认操作")
            return False
        
        backup_dir = self.backup_root / backup_id
        if not backup_dir.exists():
            print(f"❌ 备份不存在: {backup_id}")
            return False
        
        # 读取备份信息
        backup_info_file = backup_dir / "backup_info.json"
        if not backup_info_file.exists():
            print(f"❌ 备份信息文件不存在: {backup_info_file}")
            return False
        
        with open(backup_info_file, 'r', encoding='utf-8') as f:
            backup_info = json.load(f)
        
        # 恢复文件
        restored_files = []
        for file_name in backup_info['files']:
            source_path = backup_dir / file_name
            target_path = self.project_root / file_name
            
            if source_path.exists():
                if source_path.is_dir():
                    if target_path.exists():
                        shutil.rmtree(target_path)
                    shutil.copytree(source_path, target_path)
                else:
                    shutil.copy2(source_path, target_path)
                restored_files.append(file_name)
        
        print(f"✅ 恢复完成: {backup_id}")
        print(f"📂 恢复文件数: {len(restored_files)}")
        
        return True
    
    def cleanup_old_backups(self, keep_count: int = 10) -> None:
        """
        清理旧备份，保留指定数量的最新备份
        
        Args:
            keep_count: 保留的备份数量
        """
        backups = self.list_backups()
        if len(backups) <= keep_count:
            print(f"📦 当前备份数量: {len(backups)}，无需清理")
            return
        
        # 按时间排序，删除旧备份
        backups.sort(key=lambda x: x['timestamp'], reverse=True)
        to_delete = backups[keep_count:]
        
        deleted_count = 0
        for backup_info in to_delete:
            backup_dir = self.backup_root / backup_info['backup_id']
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
                deleted_count += 1
        
        # 更新备份索引
        remaining_backups = backups[:keep_count]
        self._update_backup_index_list(remaining_backups)
        
        print(f"🗑️  清理完成，删除了 {deleted_count} 个旧备份")
    
    def _update_backup_index(self, backup_info: Dict) -> None:
        """更新备份索引"""
        backup_index = {"backups": []}
        
        if self.backup_index_file.exists():
            with open(self.backup_index_file, 'r', encoding='utf-8') as f:
                backup_index = json.load(f)
        
        backup_index['backups'].append(backup_info)
        
        with open(self.backup_index_file, 'w', encoding='utf-8') as f:
            json.dump(backup_index, f, ensure_ascii=False, indent=2)
    
    def _update_backup_index_list(self, backups: List[Dict]) -> None:
        """更新备份索引列表"""
        backup_index = {"backups": backups}
        
        with open(self.backup_index_file, 'w', encoding='utf-8') as f:
            json.dump(backup_index, f, ensure_ascii=False, indent=2)


def main():
    """命令行界面"""
    import argparse
    
    parser = argparse.ArgumentParser(description="UX工程师备份管理工具")
    parser.add_argument("project_path", help="项目路径")
    parser.add_argument("--action", choices=['backup', 'list', 'restore', 'cleanup'], 
                       default='backup', help="操作类型")
    parser.add_argument("--description", "-d", help="备份描述")
    parser.add_argument("--backup-id", help="备份ID（用于恢复）")
    parser.add_argument("--keep", type=int, default=10, help="保留的备份数量")
    parser.add_argument("--confirm", action='store_true', help="确认恢复操作")
    
    args = parser.parse_args()
    
    backup_manager = BackupManager(args.project_path)
    
    if args.action == 'backup':
        description = args.description or f"手动备份 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        backup_manager.create_backup(description)
    
    elif args.action == 'list':
        backups = backup_manager.list_backups()
        if not backups:
            print("📦 暂无备份")
        else:
            print(f"📦 共有 {len(backups)} 个备份:")
            for backup in reversed(backups[-10:]):  # 显示最新10个
                print(f"  🗂️  {backup['backup_id']}")
                print(f"      时间: {backup['timestamp']}")
                print(f"      描述: {backup['description']}")
                print(f"      文件: {len(backup['files'])} 个")
                print()
    
    elif args.action == 'restore':
        if not args.backup_id:
            print("❌ 恢复操作需要指定 --backup-id")
            return
        backup_manager.restore_backup(args.backup_id, args.confirm)
    
    elif args.action == 'cleanup':
        backup_manager.cleanup_old_backups(args.keep)


if __name__ == "__main__":
    main()