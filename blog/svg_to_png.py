import os
import re

def fix_svg_chinese_fonts_simple(svg_file):
    """简单有效的SVG中文字体修复"""
    print(f"修复SVG字体: {svg_file}")
    
    try:
        # 读取SVG文件
        with open(svg_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 备份原文件
        backup_file = svg_file.replace('.svg', '_original.svg')
        if not os.path.exists(backup_file):
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ 创建备份: {backup_file}")
        
        # 定义中文字体
        chinese_fonts = 'Microsoft YaHei, SimSun, PingFang SC, Hiragino Sans GB, sans-serif'
        
        # 替换所有font-family属性
        # 匹配 font-family="..." 或 font-family='...'
        content = re.sub(r'font-family="[^"]*"', f'font-family="{chinese_fonts}"', content)
        content = re.sub(r"font-family='[^']*'", f'font-family="{chinese_fonts}"', content)
        
        # 如果没有font-family，在每个text元素添加
        if 'font-family' not in content:
            content = re.sub(r'<text([^>]*?)>', f'<text\\1 font-family="{chinese_fonts}">', content)
        
        # 在SVG根元素添加默认样式
        svg_pattern = r'<svg([^>]*?)>'
        def add_style(match):
            attrs = match.group(1)
            if 'style=' not in attrs:
                return f'<svg{attrs} style="font-family: {chinese_fonts};">'
            else:
                # 如果已有style，添加字体设置
                style_match = re.search(r'style="([^"]*)"', attrs)
                if style_match:
                    existing_style = style_match.group(1)
                    if 'font-family' not in existing_style:
                        new_style = f'{existing_style}; font-family: {chinese_fonts};'
                        attrs = attrs.replace(style_match.group(0), f'style="{new_style}"')
                return f'<svg{attrs}>'
        
        content = re.sub(svg_pattern, add_style, content)
        
        # 保存修复后的文件
        with open(svg_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ 字体修复完成")
        return True
        
    except Exception as e:
        print(f"  ✗ 字体修复失败: {e}")
        return False

def convert_with_wand_simple(svg_file, png_file):
    """使用Wand进行简单转换"""
    try:
        from wand.image import Image
        from wand.color import Color
        
        print(f"  转换: {svg_file} -> {png_file}")
        
        # 删除旧的PNG文件
        if os.path.exists(png_file):
            os.remove(png_file)
        
        with Image(filename=svg_file) as img:
            # 设置分辨率
            img.resolution = (300, 300)
            
            # 设置背景色
            img.background_color = Color('white')
            
            # 移除透明通道
            img.alpha_channel = 'remove'
            
            # 设置格式并保存
            img.format = 'png'
            img.save(filename=png_file)
        
        # 验证文件
        if os.path.exists(png_file) and os.path.getsize(png_file) > 0:
            file_size = os.path.getsize(png_file)
            print(f"  ✓ 转换成功: {png_file} ({file_size} bytes)")
            return True
        else:
            print(f"  ✗ 转换失败: 文件未生成")
            return False
            
    except ImportError:
        print(f"  ✗ Wand库未安装")
        return False
    except Exception as e:
        print(f"  ✗ 转换失败: {e}")
        return False

def check_wand_installation():
    """检查Wand安装状态"""
    try:
        from wand.image import Image
        from wand.version import MAGICK_VERSION
        print(f"✓ Wand已安装，ImageMagick版本: {MAGICK_VERSION}")
        return True
    except ImportError:
        print("✗ Wand未安装")
        print("请运行: pip install Wand")
        return False
    except Exception as e:
        print(f"✗ Wand检查失败: {e}")
        return False

def main():
    print("=== 简化版SVG中文字体修复工具 ===")
    
    # 检查Wand
    if not check_wand_installation():
        return
    
    # 获取SVG文件
    svg_files = [f for f in os.listdir('.') if f.endswith('.svg') and f.startswith('IMAGE_CHART_')]
    
    if not svg_files:
        print("未找到IMAGE_CHART_*.svg文件")
        return
    
    print(f"\n找到 {len(svg_files)} 个SVG文件")
    
    success_count = 0
    
    for svg_file in svg_files:
        print(f"\n处理: {svg_file}")
        
        # 修复字体
        if fix_svg_chinese_fonts_simple(svg_file):
            # 转换为PNG
            png_file = svg_file.replace('.svg', '.png')
            if convert_with_wand_simple(svg_file, png_file):
                success_count += 1
            else:
                print(f"  ✗ {svg_file} 转换失败")
        else:
            print(f"  ✗ {svg_file} 字体修复失败")
    
    print(f"\n=== 处理完成 ===")
    print(f"成功处理: {success_count}/{len(svg_files)} 个文件")
    
    # 删除备份文件
    print("\n=== 清理备份文件 ===")
    backup_files = [f for f in os.listdir('.') if f.endswith('_original.svg')]
    deleted_count = 0
    
    for backup_file in backup_files:
        try:
            os.remove(backup_file)
            print(f"✓ 已删除备份文件: {backup_file}")
            deleted_count += 1
        except Exception as e:
            print(f"✗ 删除备份文件失败: {backup_file} - {e}")
    
    if deleted_count > 0:
        print(f"\n✓ 已清理 {deleted_count} 个备份文件")
    else:
        print("\n未找到需要清理的备份文件")
    
    if success_count > 0:
        print("\n✓ 所有文件已重新生成，请检查PNG文件中的中文显示")
        print("\n如果中文仍然显示为方块或乱码，可能的原因:")
        print("1. 系统缺少中文字体")
        print("2. ImageMagick配置问题")
        print("3. SVG文件本身的编码问题")
        
        print("\n建议解决方案:")
        print("1. 确保Windows已安装中文语言包")
        print("2. 重新安装ImageMagick")
        print("3. 检查SVG文件是否为UTF-8编码")
    else:
        print("\n所有文件处理失败，请检查错误信息")

if __name__ == "__main__":
    main()