#!/usr/bin/env python3
"""
前端交互工程师 - 功能分析工具
分析页面中需要添加功能的元素，生成功能清单
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re

class FunctionAnalyzer:
    """页面功能分析器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.analysis_results = {}
        self.function_patterns = {
            'buttons': {
                'pattern': r'<button[^>]*>(.*?)</button>',
                'selector': 'button',
                'analysis': self._analyze_button
            },
            'forms': {
                'pattern': r'<form[^>]*>.*?</form>',
                'selector': 'form',
                'analysis': self._analyze_form
            },
            'inputs': {
                'pattern': r'<input[^>]*>',
                'selector': 'input',
                'analysis': self._analyze_input
            },
            'links': {
                'pattern': r'<a[^>]*href=["\'][^"\']*["\'][^>]*>(.*?)</a>',
                'selector': 'a[href]',
                'analysis': self._analyze_link
            },
            'search_boxes': {
                'pattern': r'placeholder=["\'][^"\']*搜索[^"\']*["\']',
                'selector': 'input[placeholder*="搜索"]',
                'analysis': self._analyze_search
            }
        }
    
    def analyze_project(self) -> Dict:
        """
        分析整个项目的功能需求
        
        Returns:
            Dict: 分析结果
        """
        print("🔍 开始分析项目功能需求...")
        
        # 读取项目菜单结构
        menu_file = self.project_root / "menu.json"
        if not menu_file.exists():
            print("❌ 未找到menu.json文件")
            return {}
        
        with open(menu_file, 'r', encoding='utf-8') as f:
            menu_data = json.load(f)
        
        # 分析所有页面
        pages_dir = self.project_root / "pages"
        if not pages_dir.exists():
            print("❌ 未找到pages目录")
            return {}
        
        analysis_result = {
            "project_name": self.project_root.name,
            "analysis_timestamp": self._get_timestamp(),
            "total_pages": 0,
            "pages_analysis": {},
            "function_summary": {
                "buttons": 0,
                "forms": 0,
                "inputs": 0,
                "links": 0,
                "search_boxes": 0
            },
            "recommendations": []
        }
        
        # 遍历所有HTML文件
        for html_file in pages_dir.rglob("*.html"):
            page_analysis = self._analyze_page(html_file)
            relative_path = str(html_file.relative_to(self.project_root))
            analysis_result["pages_analysis"][relative_path] = page_analysis
            analysis_result["total_pages"] += 1
            
            # 累计统计
            for func_type, count in page_analysis["function_counts"].items():
                analysis_result["function_summary"][func_type] += count
        
        # 生成建议
        analysis_result["recommendations"] = self._generate_recommendations(analysis_result)
        
        # 保存分析结果
        self._save_analysis(analysis_result)
        
        print(f"✅ 项目分析完成！共分析 {analysis_result['total_pages']} 个页面")
        print(f"📊 发现功能点：按钮 {analysis_result['function_summary']['buttons']} 个，表单 {analysis_result['function_summary']['forms']} 个")
        
        return analysis_result
    
    def _analyze_page(self, html_file: Path) -> Dict:
        """分析单个页面"""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            page_analysis = {
                "file_path": str(html_file),
                "page_title": self._extract_page_title(soup),
                "function_counts": {
                    "buttons": 0,
                    "forms": 0,
                    "inputs": 0,
                    "links": 0,
                    "search_boxes": 0
                },
                "functions_found": [],
                "priority": "normal"
            }
            
            # 分析各种功能元素
            for func_type, config in self.function_patterns.items():
                elements = soup.select(config['selector'])
                page_analysis["function_counts"][func_type] = len(elements)
                
                for element in elements:
                    function_info = config['analysis'](element, content)
                    if function_info:
                        function_info["type"] = func_type
                        page_analysis["functions_found"].append(function_info)
            
            # 设置优先级
            page_analysis["priority"] = self._calculate_priority(page_analysis)
            
            return page_analysis
            
        except Exception as e:
            print(f"⚠️ 分析页面 {html_file} 时出错: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_button(self, element, content: str) -> Optional[Dict]:
        """分析按钮功能"""
        text = element.get_text().strip()
        classes = element.get('class', [])
        
        # 识别按钮类型
        button_type = "generic"
        suggested_action = "showAlert"
        
        if any(keyword in text.lower() for keyword in ['购物车', '加入', '添加']):
            button_type = "add_to_cart"
            suggested_action = "addToCart"
        elif any(keyword in text.lower() for keyword in ['搜索', 'search']):
            button_type = "search"
            suggested_action = "performSearch"
        elif any(keyword in text.lower() for keyword in ['登录', 'login']):
            button_type = "login"
            suggested_action = "handleLogin"
        elif any(keyword in text.lower() for keyword in ['提交', 'submit']):
            button_type = "submit"
            suggested_action = "handleSubmit"
        elif any(keyword in text.lower() for keyword in ['返回', 'back']):
            button_type = "navigation"
            suggested_action = "goBack"
        
        return {
            "text": text,
            "button_type": button_type,
            "classes": classes,
            "suggested_action": suggested_action,
            "implementation_priority": "high" if button_type != "generic" else "medium"
        }
    
    def _analyze_form(self, element, content: str) -> Optional[Dict]:
        """分析表单功能"""
        inputs = element.find_all('input')
        textareas = element.find_all('textarea')
        selects = element.find_all('select')
        
        form_type = "generic"
        if any(inp.get('type') == 'password' for inp in inputs):
            form_type = "login"
        elif any('email' in inp.get('type', '') or 'email' in inp.get('name', '') for inp in inputs):
            form_type = "contact"
        elif any('search' in inp.get('type', '') or 'search' in inp.get('name', '') for inp in inputs):
            form_type = "search"
        
        return {
            "form_type": form_type,
            "input_count": len(inputs),
            "textarea_count": len(textareas),
            "select_count": len(selects),
            "suggested_handler": f"handle{form_type.title()}Form",
            "implementation_priority": "high"
        }
    
    def _analyze_input(self, element, content: str) -> Optional[Dict]:
        """分析输入框功能"""
        input_type = element.get('type', 'text')
        placeholder = element.get('placeholder', '')
        name = element.get('name', '')
        
        suggested_features = []
        if 'search' in placeholder.lower() or 'search' in name.lower():
            suggested_features.append('实时搜索')
        if input_type == 'email':
            suggested_features.append('邮箱验证')
        if input_type == 'password':
            suggested_features.append('密码强度检查')
        if input_type == 'number':
            suggested_features.append('数值验证')
        
        return {
            "input_type": input_type,
            "placeholder": placeholder,
            "name": name,
            "suggested_features": suggested_features,
            "implementation_priority": "medium"
        }
    
    def _analyze_link(self, element, content: str) -> Optional[Dict]:
        """分析链接功能"""
        href = element.get('href', '')
        text = element.get_text().strip()
        
        if href.startswith('#'):
            link_type = "internal"
            suggested_action = "navigateToSection"
        elif href.startswith('http'):
            link_type = "external"
            suggested_action = "openExternalLink"
        else:
            link_type = "page"
            suggested_action = "navigateToPage"
        
        return {
            "href": href,
            "text": text,
            "link_type": link_type,
            "suggested_action": suggested_action,
            "implementation_priority": "medium"
        }
    
    def _analyze_search(self, element, content: str) -> Optional[Dict]:
        """分析搜索功能"""
        placeholder = element.get('placeholder', '')
        
        return {
            "placeholder": placeholder,
            "suggested_features": [
                "实时搜索提示",
                "搜索历史",
                "热门搜索",
                "搜索结果高亮"
            ],
            "implementation_priority": "high"
        }
    
    def _extract_page_title(self, soup) -> str:
        """提取页面标题"""
        # 尝试多种方式获取页面标题
        title_element = soup.find('title')
        if title_element:
            return title_element.get_text().strip()
        
        h1_element = soup.find('h1')
        if h1_element:
            return h1_element.get_text().strip()
        
        h2_element = soup.find('h2')
        if h2_element:
            return h2_element.get_text().strip()
        
        return "未知页面"
    
    def _calculate_priority(self, page_analysis: Dict) -> str:
        """计算页面优先级"""
        total_functions = sum(page_analysis["function_counts"].values())
        
        if total_functions >= 10:
            return "high"
        elif total_functions >= 5:
            return "medium"
        else:
            return "low"
    
    def _generate_recommendations(self, analysis_result: Dict) -> List[str]:
        """生成实现建议"""
        recommendations = []
        summary = analysis_result["function_summary"]
        
        if summary["buttons"] > 0:
            recommendations.append(f"发现 {summary['buttons']} 个按钮，建议优先实现购物车、搜索等核心功能按钮")
        
        if summary["forms"] > 0:
            recommendations.append(f"发现 {summary['forms']} 个表单，建议添加表单验证和提交处理")
        
        if summary["search_boxes"] > 0:
            recommendations.append(f"发现 {summary['search_boxes']} 个搜索框，建议实现实时搜索功能")
        
        if summary["links"] > 0:
            recommendations.append(f"发现 {summary['links']} 个链接，建议实现页面路由和导航功能")
        
        # 优先级建议
        high_priority_pages = [
            path for path, analysis in analysis_result["pages_analysis"].items()
            if analysis.get("priority") == "high"
        ]
        
        if high_priority_pages:
            recommendations.append(f"建议优先处理以下高优先级页面：{', '.join(high_priority_pages[:3])}")
        
        return recommendations
    
    def _save_analysis(self, analysis_result: Dict) -> None:
        """保存分析结果"""
        output_file = self.project_root / "function_analysis.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        print(f"📄 分析结果已保存到: {output_file}")
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    """命令行界面"""
    import argparse
    
    parser = argparse.ArgumentParser(description="前端交互工程师 - 功能分析工具")
    parser.add_argument("project_path", help="项目路径")
    parser.add_argument("--output", "-o", help="输出文件路径（可选）")
    parser.add_argument("--verbose", "-v", action='store_true', help="详细输出")
    
    args = parser.parse_args()
    
    analyzer = FunctionAnalyzer(args.project_path)
    result = analyzer.analyze_project()
    
    if args.verbose:
        print("\n📊 详细分析结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print(f"\n🎯 推荐实现顺序:")
    for i, recommendation in enumerate(result.get("recommendations", []), 1):
        print(f"  {i}. {recommendation}")


if __name__ == "__main__":
    main()