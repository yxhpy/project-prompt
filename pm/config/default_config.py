"""
默认配置定义
包含项目的默认配置模板
"""

DEFAULT_CONFIG = {
    "project_name": "产品原型系统",
    "project_description": "基于需求文档生成的产品低保真原型",
    "roles": [
        {
            "name": "用户角色A",
            "description": "主要用户群体",
            "modules": [
                {
                    "name": "核心功能模块",
                    "description": "主要业务功能",
                    "pages": [
                        {"name": "功能页面1", "description": "页面功能描述"},
                        {"name": "功能页面2", "description": "页面功能描述"}
                    ]
                },
                {
                    "name": "辅助功能模块",
                    "description": "辅助业务功能",
                    "pages": [
                        {"name": "辅助页面1", "description": "页面功能描述"},
                        {"name": "辅助页面2", "description": "页面功能描述"}
                    ]
                }
            ]
        },
        {
            "name": "用户角色B",
            "description": "次要用户群体",
            "modules": [
                {
                    "name": "管理功能模块",
                    "description": "管理相关功能",
                    "pages": [
                        {"name": "管理页面1", "description": "页面功能描述"},
                        {"name": "管理页面2", "description": "页面功能描述"}
                    ]
                }
            ]
        }
    ]
}