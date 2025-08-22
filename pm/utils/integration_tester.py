#!/usr/bin/env python3
"""
前端交互工程师 - 集成测试工具
自动测试页面功能和交互是否正常工作
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import re

class IntegrationTester:
    """集成测试器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "project": self.project_root.name,
            "tests": {}
        }
    
    def run_tests(self, test_types: List[str] = None) -> Dict:
        """运行集成测试"""
        if not test_types:
            test_types = ["html_validation", "js_syntax", "css_validation", "accessibility", "performance"]
        
        print("🧪 开始运行集成测试...")
        
        for test_type in test_types:
            print(f"🔍 运行 {test_type} 测试...")
            
            if test_type == "html_validation":
                self.test_results["tests"]["html"] = self._test_html_validation()
            elif test_type == "js_syntax":
                self.test_results["tests"]["javascript"] = self._test_js_syntax()
            elif test_type == "css_validation":
                self.test_results["tests"]["css"] = self._test_css_validation()
            elif test_type == "accessibility":
                self.test_results["tests"]["accessibility"] = self._test_accessibility()
            elif test_type == "performance":
                self.test_results["tests"]["performance"] = self._test_performance()
        
        # 保存测试结果
        self._save_test_results()
        
        # 生成测试报告
        self._generate_report()
        
        print("✅ 集成测试完成！")
        return self.test_results
    
    def _test_html_validation(self) -> Dict:
        """测试HTML验证"""
        results = {"passed": [], "failed": [], "warnings": []}
        
        html_files = list(self.project_root.rglob("*.html"))
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 基本HTML结构检查
                issues = []
                
                # 检查DOCTYPE
                if not content.strip().startswith('<!DOCTYPE'):
                    issues.append("缺少DOCTYPE声明")
                
                # 检查基本结构
                if '<html' not in content:
                    issues.append("缺少<html>标签")
                if '<head>' not in content:
                    issues.append("缺少<head>标签")
                if '<body>' not in content:
                    issues.append("缺少<body>标签")
                
                # 检查标签闭合
                unclosed_tags = self._check_unclosed_tags(content)
                if unclosed_tags:
                    issues.extend([f"未闭合标签: {tag}" for tag in unclosed_tags])
                
                # 检查meta标签
                if 'charset=' not in content:
                    issues.append("缺少字符编码声明")
                if 'viewport' not in content:
                    issues.append("缺少viewport meta标签")
                
                if issues:
                    results["failed"].append({
                        "file": str(html_file.relative_to(self.project_root)),
                        "issues": issues
                    })
                else:
                    results["passed"].append(str(html_file.relative_to(self.project_root)))
                    
            except Exception as e:
                results["failed"].append({
                    "file": str(html_file.relative_to(self.project_root)),
                    "issues": [f"文件读取错误: {str(e)}"]
                })
        
        return results
    
    def _test_js_syntax(self) -> Dict:
        """测试JavaScript语法"""
        results = {"passed": [], "failed": [], "warnings": []}
        
        js_files = list(self.project_root.rglob("*.js"))
        
        for js_file in js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                issues = []
                warnings = []
                
                # 基本语法检查
                syntax_issues = self._check_js_syntax(content)
                if syntax_issues:
                    issues.extend(syntax_issues)
                
                # 最佳实践检查
                best_practices = self._check_js_best_practices(content)
                if best_practices:
                    warnings.extend(best_practices)
                
                if issues:
                    results["failed"].append({
                        "file": str(js_file.relative_to(self.project_root)),
                        "issues": issues
                    })
                elif warnings:
                    results["warnings"].append({
                        "file": str(js_file.relative_to(self.project_root)),
                        "warnings": warnings
                    })
                else:
                    results["passed"].append(str(js_file.relative_to(self.project_root)))
                    
            except Exception as e:
                results["failed"].append({
                    "file": str(js_file.relative_to(self.project_root)),
                    "issues": [f"文件读取错误: {str(e)}"]
                })
        
        return results
    
    def _test_css_validation(self) -> Dict:
        """测试CSS验证"""
        results = {"passed": [], "failed": [], "warnings": []}
        
        css_files = list(self.project_root.rglob("*.css"))
        
        for css_file in css_files:
            try:
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                issues = []
                warnings = []
                
                # 基本CSS语法检查
                css_issues = self._check_css_syntax(content)
                if css_issues:
                    issues.extend(css_issues)
                
                # CSS最佳实践检查
                css_warnings = self._check_css_best_practices(content)
                if css_warnings:
                    warnings.extend(css_warnings)
                
                if issues:
                    results["failed"].append({
                        "file": str(css_file.relative_to(self.project_root)),
                        "issues": issues
                    })
                elif warnings:
                    results["warnings"].append({
                        "file": str(css_file.relative_to(self.project_root)),
                        "warnings": warnings
                    })
                else:
                    results["passed"].append(str(css_file.relative_to(self.project_root)))
                    
            except Exception as e:
                results["failed"].append({
                    "file": str(css_file.relative_to(self.project_root)),
                    "issues": [f"文件读取错误: {str(e)}"]
                })
        
        return results
    
    def _test_accessibility(self) -> Dict:
        """测试可访问性"""
        results = {"passed": [], "failed": [], "suggestions": []}
        
        html_files = list(self.project_root.rglob("*.html"))
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                issues = []
                suggestions = []
                
                # 可访问性检查
                accessibility_issues = self._check_accessibility(content)
                if accessibility_issues["errors"]:
                    issues.extend(accessibility_issues["errors"])
                if accessibility_issues["suggestions"]:
                    suggestions.extend(accessibility_issues["suggestions"])
                
                if issues:
                    results["failed"].append({
                        "file": str(html_file.relative_to(self.project_root)),
                        "issues": issues
                    })
                elif suggestions:
                    results["suggestions"].append({
                        "file": str(html_file.relative_to(self.project_root)),
                        "suggestions": suggestions
                    })
                else:
                    results["passed"].append(str(html_file.relative_to(self.project_root)))
                    
            except Exception as e:
                results["failed"].append({
                    "file": str(html_file.relative_to(self.project_root)),
                    "issues": [f"文件读取错误: {str(e)}"]
                })
        
        return results
    
    def _test_performance(self) -> Dict:
        """测试性能"""
        results = {"metrics": {}, "suggestions": []}
        
        # 文件大小分析
        total_size = 0
        file_sizes = {"html": 0, "css": 0, "js": 0, "images": 0}
        
        for file_type, pattern in [("html", "*.html"), ("css", "*.css"), ("js", "*.js")]:
            for file_path in self.project_root.rglob(pattern):
                size = file_path.stat().st_size
                file_sizes[file_type] += size
                total_size += size
        
        # 图片文件
        image_patterns = ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg", "*.webp"]
        for pattern in image_patterns:
            for file_path in self.project_root.rglob(pattern):
                size = file_path.stat().st_size
                file_sizes["images"] += size
                total_size += size
        
        results["metrics"] = {
            "total_size_kb": round(total_size / 1024, 2),
            "html_size_kb": round(file_sizes["html"] / 1024, 2),
            "css_size_kb": round(file_sizes["css"] / 1024, 2),
            "js_size_kb": round(file_sizes["js"] / 1024, 2),
            "images_size_kb": round(file_sizes["images"] / 1024, 2)
        }
        
        # 性能建议
        if file_sizes["images"] > 500 * 1024:  # 500KB
            results["suggestions"].append("图片文件较大，建议压缩")
        
        if file_sizes["js"] > 200 * 1024:  # 200KB
            results["suggestions"].append("JavaScript文件较大，建议代码分割")
        
        if file_sizes["css"] > 100 * 1024:  # 100KB
            results["suggestions"].append("CSS文件较大，建议优化")
        
        return results
    
    def _check_unclosed_tags(self, content: str) -> List[str]:
        """检查未闭合的HTML标签"""
        # 简单的标签配对检查
        self_closing_tags = {'img', 'br', 'hr', 'input', 'meta', 'link', 'area', 'base', 'embed', 'source'}
        
        # 提取所有标签
        tags = re.findall(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)[^>]*?(/?)>', content)
        
        tag_stack = []
        unclosed = []
        
        for is_closing, tag_name, is_self_closing in tags:
            tag_name = tag_name.lower()
            
            if tag_name in self_closing_tags or is_self_closing:
                continue
            
            if is_closing:  # 闭合标签
                if tag_stack and tag_stack[-1] == tag_name:
                    tag_stack.pop()
                else:
                    unclosed.append(tag_name)
            else:  # 开始标签
                tag_stack.append(tag_name)
        
        # 栈中剩余的都是未闭合的
        unclosed.extend(tag_stack)
        
        return list(set(unclosed))
    
    def _check_js_syntax(self, content: str) -> List[str]:
        """检查JavaScript语法"""
        issues = []
        
        # 检查括号配对
        brackets = {'(': ')', '[': ']', '{': '}'}
        stack = []
        
        for char in content:
            if char in brackets:
                stack.append(brackets[char])
            elif char in brackets.values():
                if not stack or stack.pop() != char:
                    issues.append("括号不匹配")
                    break
        
        if stack:
            issues.append("存在未闭合的括号")
        
        # 检查常见语法错误
        if 'function(' in content and 'function (' not in content.replace('function(', 'function ('):
            pass  # 允许function()语法
        
        # 检查分号
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if (line.endswith('{') or line.endswith('}') or 
                line.startswith('//') or line.startswith('/*') or
                line.startswith('*') or line.endswith('*/') or
                not line):
                continue
            
            if (line and not line.endswith(';') and not line.endswith(',') and 
                not line.endswith('{') and not line.endswith('}') and
                not line.endswith(':') and 'return' not in line):
                # 这是一个警告而不是错误
                pass
        
        return issues
    
    def _check_js_best_practices(self, content: str) -> List[str]:
        """检查JavaScript最佳实践"""
        warnings = []
        
        # 检查var使用
        if 'var ' in content:
            warnings.append("建议使用let/const代替var")
        
        # 检查console.log
        if 'console.log(' in content:
            warnings.append("生产环境应移除console.log")
        
        # 检查全局变量
        if 'window.' in content:
            warnings.append("避免使用过多全局变量")
        
        return warnings
    
    def _check_css_syntax(self, content: str) -> List[str]:
        """检查CSS语法"""
        issues = []
        
        # 检查括号配对
        open_braces = content.count('{')
        close_braces = content.count('}')
        
        if open_braces != close_braces:
            issues.append(f"大括号不匹配: {open_braces} vs {close_braces}")
        
        # 检查分号
        rules = re.findall(r'{([^}]*)}', content)
        for rule in rules:
            properties = [p.strip() for p in rule.split('\n') if p.strip()]
            for prop in properties:
                if prop and not prop.endswith(';') and not prop.startswith('/*'):
                    issues.append(f"CSS属性缺少分号: {prop[:50]}...")
                    break
        
        return issues
    
    def _check_css_best_practices(self, content: str) -> List[str]:
        """检查CSS最佳实践"""
        warnings = []
        
        # 检查!important使用
        if '!important' in content:
            warnings.append("避免过度使用!important")
        
        # 检查ID选择器
        id_selectors = len(re.findall(r'#[a-zA-Z]', content))
        if id_selectors > 5:
            warnings.append("ID选择器使用过多，建议使用class")
        
        return warnings
    
    def _check_accessibility(self, content: str) -> Dict:
        """检查可访问性"""
        errors = []
        suggestions = []
        
        # 检查img标签的alt属性
        img_tags = re.findall(r'<img[^>]*>', content)
        for img in img_tags:
            if 'alt=' not in img:
                errors.append("img标签缺少alt属性")
        
        # 检查表单标签
        input_tags = re.findall(r'<input[^>]*>', content)
        for input_tag in input_tags:
            if 'id=' in input_tag:
                input_id = re.search(r'id=["\']([^"\']*)["\']', input_tag)
                if input_id:
                    label_pattern = f'for=["\']?{input_id.group(1)}["\']?'
                    if not re.search(label_pattern, content):
                        suggestions.append(f"input元素应该有对应的label")
        
        # 检查标题层次
        headings = re.findall(r'<h([1-6])', content)
        if headings:
            prev_level = 0
            for heading in headings:
                level = int(heading)
                if level > prev_level + 1:
                    suggestions.append("标题层次跳跃过大")
                    break
                prev_level = level
        
        # 检查颜色对比度（基本检查）
        if 'color:' in content and 'background' in content:
            suggestions.append("请确保颜色对比度符合WCAG标准")
        
        return {"errors": errors, "suggestions": suggestions}
    
    def _save_test_results(self):
        """保存测试结果"""
        results_file = self.project_root / "test-results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
    
    def _generate_report(self):
        """生成测试报告"""
        report_content = self._create_html_report()
        
        report_file = self.project_root / "test-report.html"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📋 测试报告已生成: {report_file}")
    
    def _create_html_report(self) -> str:
        """创建HTML测试报告"""
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        
        # 统计测试结果
        for test_name, test_result in self.test_results["tests"].items():
            if isinstance(test_result, dict):
                if "passed" in test_result:
                    passed = len(test_result.get("passed", []))
                    failed = len(test_result.get("failed", []))
                    total_tests += passed + failed
                    passed_tests += passed
                    failed_tests += failed
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 100
        
        return f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>集成测试报告 - {self.test_results["project"]}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .success {{ background-color: #d1f2eb; color: #27ae60; }}
        .error {{ background-color: #fadbd8; color: #e74c3c; }}
        .warning {{ background-color: #fef9e7; color: #f39c12; }}
    </style>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <h1 class="text-3xl font-bold text-gray-800 mb-4">集成测试报告</h1>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div class="bg-blue-100 p-4 rounded">
                    <h3 class="font-bold">项目</h3>
                    <p>{self.test_results["project"]}</p>
                </div>
                <div class="bg-green-100 p-4 rounded">
                    <h3 class="font-bold">通过率</h3>
                    <p>{success_rate:.1f}%</p>
                </div>
                <div class="bg-yellow-100 p-4 rounded">
                    <h3 class="font-bold">总测试数</h3>
                    <p>{total_tests}</p>
                </div>
                <div class="bg-red-100 p-4 rounded">
                    <h3 class="font-bold">失败数</h3>
                    <p>{failed_tests}</p>
                </div>
            </div>
        </div>
        
        {self._generate_test_sections()}
    </div>
</body>
</html>
'''.strip()
    
    def _generate_test_sections(self) -> str:
        """生成测试部分HTML"""
        sections = []
        
        for test_name, test_result in self.test_results["tests"].items():
            if isinstance(test_result, dict):
                sections.append(f'''
                <div class="bg-white rounded-lg shadow-md p-6 mb-6">
                    <h2 class="text-2xl font-bold mb-4">{test_name.replace("_", " ").title()}</h2>
                    {self._generate_test_details(test_result)}
                </div>
                ''')
        
        return '\n'.join(sections)
    
    def _generate_test_details(self, test_result: Dict) -> str:
        """生成测试详情HTML"""
        details = []
        
        # 通过的测试
        if "passed" in test_result and test_result["passed"]:
            details.append(f'''
            <div class="mb-4">
                <h3 class="text-lg font-bold text-green-600 mb-2">✅ 通过 ({len(test_result["passed"])})</h3>
                <ul class="list-disc list-inside">
                    {"".join([f"<li class='text-green-700'>{item}</li>" for item in test_result["passed"]])}
                </ul>
            </div>
            ''')
        
        # 失败的测试
        if "failed" in test_result and test_result["failed"]:
            details.append(f'''
            <div class="mb-4">
                <h3 class="text-lg font-bold text-red-600 mb-2">❌ 失败 ({len(test_result["failed"])})</h3>
                {self._generate_failed_details(test_result["failed"])}
            </div>
            ''')
        
        # 警告
        if "warnings" in test_result and test_result["warnings"]:
            details.append(f'''
            <div class="mb-4">
                <h3 class="text-lg font-bold text-yellow-600 mb-2">⚠️ 警告 ({len(test_result["warnings"])})</h3>
                {self._generate_warning_details(test_result["warnings"])}
            </div>
            ''')
        
        return '\n'.join(details)
    
    def _generate_failed_details(self, failed_items: List[Dict]) -> str:
        """生成失败详情"""
        items = []
        for item in failed_items:
            issues = "<br>".join([f"• {issue}" for issue in item.get("issues", [])])
            items.append(f'''
            <div class="bg-red-50 border border-red-200 rounded p-3 mb-2">
                <strong class="text-red-800">{item.get("file", "Unknown")}</strong><br>
                <span class="text-red-700">{issues}</span>
            </div>
            ''')
        return '\n'.join(items)
    
    def _generate_warning_details(self, warning_items: List[Dict]) -> str:
        """生成警告详情"""
        items = []
        for item in warning_items:
            warnings = "<br>".join([f"• {warning}" for warning in item.get("warnings", [])])
            items.append(f'''
            <div class="bg-yellow-50 border border-yellow-200 rounded p-3 mb-2">
                <strong class="text-yellow-800">{item.get("file", "Unknown")}</strong><br>
                <span class="text-yellow-700">{warnings}</span>
            </div>
            ''')
        return '\n'.join(items)


def main():
    """命令行界面"""
    import argparse
    
    parser = argparse.ArgumentParser(description="前端交互工程师 - 集成测试工具")
    parser.add_argument("project_path", help="项目路径")
    parser.add_argument("--tests", "-t", help="测试类型（逗号分隔）")
    parser.add_argument("--report", "-r", action='store_true', help="生成HTML报告")
    
    args = parser.parse_args()
    tester = IntegrationTester(args.project_path)
    
    test_types = [t.strip() for t in args.tests.split(',')] if args.tests else None
    results = tester.run_tests(test_types)
    
    # 显示简要结果
    total_files = 0
    passed_files = 0
    failed_files = 0
    
    for test_name, test_result in results["tests"].items():
        if isinstance(test_result, dict):
            passed = len(test_result.get("passed", []))
            failed = len(test_result.get("failed", []))
            
            total_files += passed + failed
            passed_files += passed
            failed_files += failed
            
            print(f"\n{test_name}: {passed} 通过, {failed} 失败")
    
    if total_files > 0:
        success_rate = (passed_files / total_files) * 100
        print(f"\n📊 总体结果: {success_rate:.1f}% 通过率 ({passed_files}/{total_files})")
    
    print(f"\n📋 详细报告: {tester.project_root}/test-report.html")


if __name__ == "__main__":
    main()