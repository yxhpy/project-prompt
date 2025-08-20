"""
HTML模板生成器
负责生成各种HTML文件
"""

import sys
from pathlib import Path
from typing import Dict, Any

# 添加父目录到路径以支持导入
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from templates.html_templates import HTMLTemplates


class TemplateGenerator:
    """HTML模板生成器类"""
    
    def __init__(self, config: Dict[str, Any], platform_type: str = "mobile"):
        self.config = config
        self.platform_type = platform_type
        self.html_templates = HTMLTemplates()
    
    def generate_index_html(self) -> str:
        """
        生成index.html文件内容
        
        Returns:
            str: index.html文件内容
        """
        index_content = self.html_templates.get_index_template()
        return index_content.replace("原型导航", f"{self.config['project_name']} - 原型导航")
    
    def generate_page_html(self, page_name: str, page_description: str, 
                          role_name: str, module_name: str) -> str:
        """
        生成页面HTML文件内容
        
        Args:
            page_name: 页面名称
            page_description: 页面描述
            role_name: 角色名称
            module_name: 模块名称
            
        Returns:
            str: 页面HTML内容
        """
        if self.platform_type == "mobile":
            return self.html_templates.get_mobile_page_template(
                page_name, page_description, role_name, module_name
            )
        else:
            return self.html_templates.get_pc_page_template(
                page_name, page_description, role_name, module_name
            )
    
    def generate_page_content_only(self, page_name: str, page_description: str, 
                                  role_name: str, module_name: str) -> str:
        """
        仅生成页面内容部分（用于手机模式的内容替换）
        
        Args:
            page_name: 页面名称
            page_description: 页面描述
            role_name: 角色名称
            module_name: 模块名称
            
        Returns:
            str: 页面内容HTML
        """
        if self.platform_type == "mobile":
            return self.html_templates.get_mobile_page_content(
                page_name, page_description, role_name, module_name
            )
        else:
            # PC模式依然返回完整页面，因为需要替换整个body
            return self.html_templates.get_pc_page_template(
                page_name, page_description, role_name, module_name
            )
    
    def generate_design_standards(self) -> str:
        """
        生成设计规范文档内容
        
        Returns:
            str: 设计规范文档内容
        """
        platform_text = "手机端" if self.platform_type == "mobile" else "PC端"
        title_size = "18px" if self.platform_type == "mobile" else "24px"
        body_size = "14px" if self.platform_type == "mobile" else "16px"
        small_size = "12px" if self.platform_type == "mobile" else "14px"
        page_margin = "15px" if self.platform_type == "mobile" else "20px"
        component_spacing = "10px" if self.platform_type == "mobile" else "15px"
        content_spacing = "20px" if self.platform_type == "mobile" else "30px"
        btn_padding = "10px 20px" if self.platform_type == "mobile" else "12px 24px"
        input_padding = "10px" if self.platform_type == "mobile" else "12px"
        card_padding = "15px" if self.platform_type == "mobile" else "20px"
        container_width = "375px" if self.platform_type == "mobile" else "1200px"
        grid_system = "单列布局" if self.platform_type == "mobile" else "双列网格"
        responsive = "固定宽度" if self.platform_type == "mobile" else "自适应"
        mobile_requirement = "5. **手机壳要求**: 手机端页面必须包含iPhone手机壳外框" if self.platform_type == "mobile" else ""
        mobile_check = "- [ ] 手机端是否包含iPhone手机壳" if self.platform_type == "mobile" else ""
        
        iphone_template = '''
<!-- iPhone手机壳模板 -->
<div class="iphone-frame">
  <div class="iphone-screen">
    <!-- 状态栏 -->
    <div class="status-bar">
      <div class="status-left">
        <span class="signal">●●●</span>
        <span class="carrier">中国移动</span>
        <span class="wifi">📶</span>
      </div>
      <div class="status-center">
        <span class="time">9:41</span>
      </div>
      <div class="status-right">
        <span class="battery">🔋100%</span>
      </div>
    </div>
    
    <!-- 页面内容区域 -->
    <div class="page-content">
      <!-- 在这里放置页面内容 -->
    </div>
  </div>
</div>''' if self.platform_type == "mobile" else ""
        
        page_template = self.html_templates.get_mobile_page_template(
            "页面标题", "页面功能描述", "角色名称", "模块名称"
        ) if self.platform_type == "mobile" else self.html_templates.get_pc_page_template(
            "页面标题", "页面功能描述", "角色名称", "模块名称"
        )
        
        js_config = '''```javascript
tailwind.config = {
  theme: {
    extend: {
      colors: {
        'gray-custom': '#f5f5f5',
        'border-custom': '#cccccc',
        'text-primary': '#333333',
        'text-secondary': '#666666'
      }
    }
  }
}
```'''
        
        return f'''# 设计规范文档

## 项目基本信息
- **项目名称**: {self.config['project_name']}
- **项目描述**: {self.config['project_description']}
- **平台类型**: {platform_text}
- **设计风格**: 严格低保真线稿

## 颜色规范（严格低保真）
- **主色调**: #333333 (深灰)
- **次要色**: #666666 (中灰)
- **背景色**: #ffffff (白色)
- **边框色**: #cccccc (浅灰)
- **辅助色**: #f5f5f5 (极浅灰)
- **禁用颜色**: 严禁使用任何彩色，只允许灰度色彩

## 字体规范
- **主字体**: Arial, sans-serif
- **标题字号**: {title_size} (粗体)
- **正文字号**: {body_size}
- **小字字号**: {small_size}

## 间距规范
- **页面边距**: {page_margin}
- **组件间距**: {component_spacing}
- **内容间距**: {content_spacing}

## 组件规范

### 按钮
- 边框: 2px solid #333
- 内边距: {btn_padding}
- 背景: #fff
- 文字: #333

### 输入框
- 边框: 2px solid #ccc
- 内边距: {input_padding}
- 宽度: 100%

### 卡片
- 边框: 2px solid #ddd
- 内边距: {card_padding}
- 背景: #fff

## 布局规范

### {platform_text}布局
- **容器宽度**: {container_width}
- **网格系统**: {grid_system}
- **响应式**: {responsive}

{f"## iPhone手机壳模板{iphone_template}" if self.platform_type == "mobile" else ""}

## 标准页面模板

### {platform_text}页面模板

```html
{page_template[:1000]}...
```

## TailwindCSS 配置
{js_config}

## 使用规范

### 工作流程
1. **设计前必读**: 每次设计新页面前，必须先阅读本规范文件
2. **严格遵循**: 所有页面必须严格按照本规范执行
3. **保持一致**: 确保所有页面风格统一
4. **低保真原则**: 严禁使用彩色，只能使用灰度色彩
{mobile_requirement}

### 质量检查
- [ ] 页面是否使用了规范中的颜色
- [ ] 字体和字号是否符合规范
- [ ] 间距是否按照规范设置
- [ ] 组件样式是否统一
- [ ] 是否严格保持低保真风格
{mobile_check}
'''
    
    def generate_readme(self) -> str:
        """
        生成README.md文件内容
        
        Returns:
            str: README.md文件内容
        """
        project_name = self.config['project_name']
        
        readme_content = f"""# {project_name}

## 项目描述
{self.config['project_description']}

## 使用说明
1. 在浏览器中打开 `index.html` 文件
2. 使用左侧导航菜单浏览不同的页面
3. 支持搜索功能，可快速定位页面

## 项目结构
```
{project_name.replace(' ', '-')}/
├── index.html          # 主页面（导航+预览）
├── menu.json           # 菜单配置文件
├── style.css           # 公共样式文件
├── progress.js         # 进度跟踪系统
├── design-standards.md # 设计规范文档
├── README.md           # 项目说明文档
└── pages/              # 所有原型页面
    ├── role1/          # 用户角色1的页面
    ├── role2/          # 用户角色2的页面
    └── ...
```

## 进度跟踪功能
- **实时进度条**: 页面顶部显示整体完成进度
- **完成标识**: 已完成页面显示绿色 ✅ 标记
- **智能展开**: 包含已完成页面的节点自动展开
- **右键操作**: 右键点击页面可切换完成状态
- **状态持久化**: 完成状态自动保存到本地存储

## 角色和模块说明
"""
        
        for role_index, role in enumerate(self.config['roles']):
            readme_content += f"\n### {role['name']}\n"
            readme_content += f"{role['description']}\n\n"
            
            for module in role['modules']:
                readme_content += f"- **{module['name']}**: {module['description']}\n"
                for page in module['pages']:
                    readme_content += f"  - {page['name']}: {page['description']}\n"
            readme_content += "\n"
        
        readme_content += """## 自定义说明
本原型系统基于通用模板生成，可根据实际项目需求进行以下自定义：

1. **修改页面内容**: 编辑 `pages/` 目录下的HTML文件
2. **调整菜单结构**: 修改 `menu.json` 文件
3. **更新样式**: 编辑 `style.css` 文件
4. **添加新页面**: 按照现有结构添加新的HTML文件，并更新menu.json

## 注意事项
- 这是低保真原型，主要用于展示页面结构和功能布局
- 实际开发时需要根据具体需求进行详细设计和功能实现
- 建议配合产品需求文档使用，确保原型符合业务需求
"""
        
        return readme_content