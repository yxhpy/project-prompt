#!/usr/bin/env python3
"""
前端交互工程师 - 功能分析工具
通用的页面元素和交互功能分析器，不依赖外部库
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

class FunctionAnalyzer:
    """通用页面功能分析器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.analysis_results = {}
        
        # 通用功能模式
        self.patterns = {
            'buttons': {
                'regex': r'<button[^>]*>(.*?)</button>',
                'description': '按钮元素'
            },
            'forms': {
                'regex': r'<form[^>]*>.*?</form>',
                'description': '表单元素'
            },
            'inputs': {
                'regex': r'<input[^>]*>',
                'description': '输入框元素'
            },
            'links': {
                'regex': r'<a[^>]*href[^>]*>(.*?)</a>',
                'description': '链接元素'
            },
            'images': {
                'regex': r'<img[^>]*>',
                'description': '图片元素'
            },
            'data_attributes': {
                'regex': r'data-[a-zA-Z-]+=["\'][^"\']*["\']',
                'description': '数据属性'
            },
            'event_handlers': {
                'regex': r'on[a-zA-Z]+=["\'][^"\']*["\']',
                'description': '事件处理器'
            }
        }
    
    def analyze_project(self) -> Dict:
        """分析整个项目"""
        print("🔍 开始分析项目功能需求...")
        
        analysis_result = {
            "project_name": self.project_root.name,
            "timestamp": datetime.now().isoformat(),
            "total_pages": 0,
            "pages_analysis": {},
            "function_summary": {},
            "recommendations": []
        }
        
        # 初始化功能计数
        for pattern_name in self.patterns:
            analysis_result["function_summary"][pattern_name] = 0
        
        # 查找所有HTML文件
        html_files = list(self.project_root.rglob("*.html"))
        
        for html_file in html_files:
            page_analysis = self._analyze_page(html_file)
            relative_path = str(html_file.relative_to(self.project_root))
            analysis_result["pages_analysis"][relative_path] = page_analysis
            analysis_result["total_pages"] += 1
            
            # 累计统计
            for pattern_name, count in page_analysis["function_counts"].items():
                analysis_result["function_summary"][pattern_name] += count
        
        # 生成建议
        analysis_result["recommendations"] = self._generate_recommendations(analysis_result)
        
        # 保存分析结果
        self._save_analysis(analysis_result)
        
        print(f"✅ 分析完成！共分析 {analysis_result['total_pages']} 个页面")
        self._print_summary(analysis_result)
        
        return analysis_result
    
    def _analyze_page(self, html_file: Path) -> Dict:
        """分析单个页面"""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            page_analysis = {
                "file_path": str(html_file),
                "page_title": self._extract_title(content),
                "function_counts": {},
                "functions_found": [],
                "priority": "normal",
                "file_size": len(content)
            }
            
            # 分析各种功能元素
            for pattern_name, pattern_config in self.patterns.items():
                matches = re.findall(pattern_config['regex'], content, re.IGNORECASE | re.DOTALL)
                page_analysis["function_counts"][pattern_name] = len(matches)
                
                # 分析具体的功能
                if matches:
                    function_details = self._analyze_pattern_matches(pattern_name, matches, content)
                    if function_details:
                        page_analysis["functions_found"].extend(function_details)
            
            # 设置优先级
            page_analysis["priority"] = self._calculate_priority(page_analysis)
            
            return page_analysis
            
        except Exception as e:
            return {"error": str(e), "file_path": str(html_file)}
    
    def _analyze_pattern_matches(self, pattern_name: str, matches: List[str], content: str) -> List[Dict]:
        """分析具体的模式匹配"""
        functions = []
        
        if pattern_name == "buttons":
            for match in matches:
                button_text = self._clean_text(match)
                button_type = self._classify_button(button_text, content)
                functions.append({
                    "type": "button",
                    "text": button_text,
                    "category": button_type,
                    "suggested_action": self._suggest_button_action(button_type),
                    "priority": "high" if button_type in ["submit", "add_to_cart", "login"] else "medium"
                })
        
        elif pattern_name == "forms":
            form_count = len(matches)
            for i in range(form_count):
                functions.append({
                    "type": "form",
                    "form_id": f"form_{i+1}",
                    "suggested_features": ["validation", "submission_handling", "error_display"],
                    "priority": "high"
                })
        
        elif pattern_name == "inputs":
            input_types = self._analyze_input_types(matches)
            for input_type, count in input_types.items():
                functions.append({
                    "type": "input",
                    "input_type": input_type,
                    "count": count,
                    "suggested_features": self._suggest_input_features(input_type),
                    "priority": "medium"
                })
        
        elif pattern_name == "links":
            for match in matches:
                link_text = self._clean_text(match)
                functions.append({
                    "type": "link",
                    "text": link_text,
                    "suggested_action": "navigation",
                    "priority": "medium"
                })
        
        elif pattern_name == "data_attributes":
            unique_attributes = set(re.findall(r'data-([a-zA-Z-]+)', ' '.join(matches)))
            for attr in unique_attributes:
                functions.append({
                    "type": "data_attribute", 
                    "attribute": f"data-{attr}",
                    "suggested_use": self._suggest_data_attribute_use(attr),
                    "priority": "low"
                })
        
        return functions
    
    def _extract_title(self, content: str) -> str:
        """提取页面标题"""
        # 尝试从title标签提取
        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if title_match:
            return self._clean_text(title_match.group(1))
        
        # 尝试从h1标签提取
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        if h1_match:
            return self._clean_text(h1_match.group(1))
        
        # 尝试从h2标签提取
        h2_match = re.search(r'<h2[^>]*>(.*?)</h2>', content, re.IGNORECASE | re.DOTALL)
        if h2_match:
            return self._clean_text(h2_match.group(1))
        
        return "未知页面"
    
    def _clean_text(self, text: str) -> str:
        """清理HTML标签和多余空白"""
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        # 清理空白字符
        text = re.sub(r'\\s+', ' ', text)
        return text.strip()
    
    def _classify_button(self, button_text: str, content: str) -> str:
        """分类按钮类型"""
        text_lower = button_text.lower()
        
        if any(keyword in text_lower for keyword in ['提交', 'submit', '确认', 'confirm']):
            return 'submit'
        elif any(keyword in text_lower for keyword in ['购物车', 'cart', '加入', 'add']):
            return 'add_to_cart'
        elif any(keyword in text_lower for keyword in ['登录', 'login', '登陆']):
            return 'login'
        elif any(keyword in text_lower for keyword in ['注册', 'register', '注册']):
            return 'register'
        elif any(keyword in text_lower for keyword in ['搜索', 'search']):
            return 'search'
        elif any(keyword in text_lower for keyword in ['删除', 'delete', '移除', 'remove']):
            return 'delete'
        elif any(keyword in text_lower for keyword in ['编辑', 'edit', '修改', 'update']):
            return 'edit'
        elif any(keyword in text_lower for keyword in ['返回', 'back', '后退']):
            return 'navigation'
        else:
            return 'generic'
    
    def _suggest_button_action(self, button_type: str) -> str:
        """建议按钮动作"""
        action_map = {
            'submit': 'handleFormSubmit',
            'add_to_cart': 'addToCart',
            'login': 'handleLogin',
            'register': 'handleRegister',
            'search': 'performSearch',
            'delete': 'confirmDelete',
            'edit': 'enableEdit',
            'navigation': 'navigateBack',
            'generic': 'handleButtonClick'
        }
        return action_map.get(button_type, 'handleButtonClick')
    
    def _analyze_input_types(self, matches: List[str]) -> Dict[str, int]:
        """分析输入框类型"""
        input_types = {}
        
        for match in matches:
            # 提取type属性
            type_match = re.search(r'type=["\']?([^"\'\\s>]+)', match, re.IGNORECASE)
            input_type = type_match.group(1).lower() if type_match else 'text'
            
            input_types[input_type] = input_types.get(input_type, 0) + 1
        
        return input_types
    
    def _suggest_input_features(self, input_type: str) -> List[str]:
        """建议输入框功能"""
        feature_map = {
            'email': ['email_validation', 'format_check'],
            'password': ['strength_check', 'visibility_toggle'],
            'number': ['numeric_validation', 'range_check'],
            'tel': ['phone_format', 'country_code'],
            'url': ['url_validation', 'protocol_check'],
            'search': ['live_search', 'suggestions'],
            'text': ['length_validation', 'trim_whitespace'],
            'textarea': ['character_counter', 'auto_resize']
        }
        return feature_map.get(input_type, ['basic_validation'])
    
    def _suggest_data_attribute_use(self, attr: str) -> str:
        """建议数据属性用途"""
        use_map = {
            'toggle': '切换显示/隐藏',
            'target': '目标元素选择',
            'action': '动作触发',
            'validate': '表单验证',
            'bind': '数据绑定',
            'click': '点击事件',
            'submit': '表单提交',
            'load': '延迟加载'
        }
        
        for key, use in use_map.items():
            if key in attr:
                return use
        
        return '自定义数据存储'
    
    def _calculate_priority(self, page_analysis: Dict) -> str:
        """计算页面优先级"""
        total_functions = sum(page_analysis["function_counts"].values())
        
        # 根据功能元素数量判断优先级
        if total_functions >= 15:
            return "high"
        elif total_functions >= 8:
            return "medium"
        else:
            return "low"
    
    def _generate_recommendations(self, analysis_result: Dict) -> List[str]:
        """生成实现建议"""
        recommendations = []
        summary = analysis_result["function_summary"]
        
        # 按钮建议
        if summary.get("buttons", 0) > 0:
            recommendations.append(f"发现 {summary['buttons']} 个按钮，建议添加点击事件处理")
        
        # 表单建议
        if summary.get("forms", 0) > 0:
            recommendations.append(f"发现 {summary['forms']} 个表单，建议添加验证和提交处理")
        
        # 输入框建议
        if summary.get("inputs", 0) > 0:
            recommendations.append(f"发现 {summary['inputs']} 个输入框，建议添加实时验证")
        
        # 链接建议
        if summary.get("links", 0) > 0:
            recommendations.append(f"发现 {summary['links']} 个链接，建议实现路由导航")
        
        # 数据属性建议
        if summary.get("data_attributes", 0) > 0:
            recommendations.append(f"发现 {summary['data_attributes']} 个数据属性，建议实现对应的交互功能")
        
        # 优先级建议
        high_priority_pages = [
            path for path, analysis in analysis_result["pages_analysis"].items()
            if analysis.get("priority") == "high" and "error" not in analysis
        ]
        
        if high_priority_pages:
            recommendations.append(f"建议优先处理高优先级页面：{', '.join(high_priority_pages[:3])}")
        
        # 性能建议
        large_pages = [
            path for path, analysis in analysis_result["pages_analysis"].items()
            if analysis.get("file_size", 0) > 50000  # 50KB
        ]
        
        if large_pages:
            recommendations.append("发现较大的HTML文件，建议考虑代码分割和优化")
        
        return recommendations
    
    def _save_analysis(self, analysis_result: Dict) -> None:
        """保存分析结果"""
        output_file = self.project_root / "function_analysis.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        print(f"📄 分析结果已保存到: {output_file}")
    
    def _print_summary(self, analysis_result: Dict) -> None:
        """打印分析摘要"""
        print(f"\\n📊 功能元素统计:")
        for pattern_name, count in analysis_result["function_summary"].items():
            if count > 0:
                description = self.patterns[pattern_name]["description"]
                print(f"  {description}: {count} 个")
        
        print(f"\\n🎯 实现建议:")
        for i, recommendation in enumerate(analysis_result["recommendations"][:5], 1):
            print(f"  {i}. {recommendation}")
    
    def generate_implementation_plan(self) -> Dict:
        """生成实现计划"""
        # 读取分析结果
        analysis_file = self.project_root / "function_analysis.json"
        if not analysis_file.exists():
            print("❌ 请先运行分析")
            return {}
        
        with open(analysis_file, 'r', encoding='utf-8') as f:
            analysis_result = json.load(f)
        
        plan = {
            "project": analysis_result["project_name"],
            "timestamp": datetime.now().isoformat(),
            "phases": [],
            "estimated_time": "待评估"
        }
        
        # 第一阶段：基础设置
        plan["phases"].append({
            "phase": 1,
            "name": "基础设置",
            "tasks": [
                "生成通用业务逻辑模板",
                "创建数据存储管理",
                "设置事件管理器",
                "配置通知系统"
            ],
            "priority": "high",
            "estimated_days": 1
        })
        
        # 第二阶段：表单处理
        if analysis_result["function_summary"].get("forms", 0) > 0:
            plan["phases"].append({
                "phase": 2,
                "name": "表单功能实现",
                "tasks": [
                    "实现表单验证",
                    "添加提交处理",
                    "错误消息显示",
                    "成功反馈机制"
                ],
                "priority": "high",
                "estimated_days": 2
            })
        
        # 第三阶段：交互功能
        if analysis_result["function_summary"].get("buttons", 0) > 0:
            plan["phases"].append({
                "phase": 3,
                "name": "按钮交互实现",
                "tasks": [
                    "按钮点击事件",
                    "业务逻辑处理",
                    "状态更新",
                    "视觉反馈"
                ],
                "priority": "medium",
                "estimated_days": 2
            })
        
        # 第四阶段：导航系统
        if analysis_result["function_summary"].get("links", 0) > 0:
            plan["phases"].append({
                "phase": 4,
                "name": "导航系统实现",
                "tasks": [
                    "路由配置",
                    "页面切换",
                    "历史管理",
                    "面包屑导航"
                ],
                "priority": "medium",
                "estimated_days": 1
            })
        
        # 保存实现计划
        plan_file = self.project_root / "implementation_plan.json"
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        
        print(f"📋 实现计划已生成: {plan_file}")
        return plan


def main():
    """命令行界面"""
    import argparse
    
    parser = argparse.ArgumentParser(description="前端交互工程师 - 功能分析工具")
    parser.add_argument("project_path", help="项目路径")
    parser.add_argument("--analyze", "-a", action='store_true', help="分析项目功能")
    parser.add_argument("--plan", "-p", action='store_true', help="生成实现计划")
    parser.add_argument("--summary", "-s", action='store_true', help="显示分析摘要")
    
    args = parser.parse_args()
    
    analyzer = FunctionAnalyzer(args.project_path)
    
    if args.analyze or not any([args.plan, args.summary]):
        result = analyzer.analyze_project()
    
    if args.plan:
        plan = analyzer.generate_implementation_plan()
        if plan:
            print(f"\\n📈 实现计划包含 {len(plan['phases'])} 个阶段")
    
    if args.summary:
        analysis_file = Path(args.project_path) / "function_analysis.json"
        if analysis_file.exists():
            with open(analysis_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
            analyzer._print_summary(result)
        else:
            print("❌ 未找到分析结果，请先运行分析")


if __name__ == "__main__":
    main()