#!/usr/bin/env python3
"""
前端交互工程师 - 数据管理工具
创建mock数据、管理项目配置、处理数据持久化
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import random

class DataManager:
    """项目数据管理器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        # 数据类型模板
        self.data_templates = {
            "users": self._generate_users,
            "products": self._generate_products,
            "orders": self._generate_orders,
            "categories": self._generate_categories,
            "settings": self._generate_settings
        }
    
    def create_mock_data(self, data_types: List[str] = None, count: int = 10) -> Dict:
        """创建mock数据"""
        if not data_types:
            data_types = list(self.data_templates.keys())
        
        print(f"📊 开始生成mock数据...")
        
        results = {
            "project": self.project_root.name,
            "timestamp": datetime.now().isoformat(),
            "generated_data": {}
        }
        
        for data_type in data_types:
            if data_type in self.data_templates:
                print(f"📝 生成 {data_type} 数据...")
                data = self.data_templates[data_type](count)
                results["generated_data"][data_type] = {
                    "count": len(data),
                    "file": self._save_data(data_type, data)
                }
        
        # 生成数据配置文件
        self._create_data_config(results)
        
        print(f"✅ mock数据生成完成！")
        return results
    
    def _save_data(self, data_type: str, data: List[Dict]) -> str:
        """保存数据到文件"""
        file_path = self.data_dir / f"{data_type}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        return str(file_path)
    
    def _generate_users(self, count: int) -> List[Dict]:
        """生成用户数据"""
        users = []
        names = ["张三", "李四", "王五", "赵六", "陈七", "刘八", "杨九", "黄十"]
        domains = ["example.com", "test.com", "demo.com"]
        
        for i in range(count):
            name = random.choice(names) + str(i+1)
            users.append({
                "id": i + 1,
                "username": f"user{i+1:02d}",
                "name": name,
                "email": f"{name.lower()}@{random.choice(domains)}",
                "phone": f"1{random.randint(30,89):02d}{random.randint(1000,9999):04d}{random.randint(1000,9999):04d}",
                "avatar": f"https://i.pravatar.cc/150?u={i+1}",
                "role": random.choice(["admin", "user", "vip"]),
                "status": random.choice(["active", "inactive"]),
                "created_at": datetime.now().isoformat(),
                "last_login": datetime.now().isoformat()
            })
        
        return users
    
    def _generate_products(self, count: int) -> List[Dict]:
        """生成商品数据"""
        products = []
        categories = ["手机", "电脑", "平板", "耳机", "音响", "相机"]
        brands = ["苹果", "华为", "小米", "三星", "索尼", "佳能"]
        
        for i in range(count):
            category = random.choice(categories)
            brand = random.choice(brands)
            
            products.append({
                "id": i + 1,
                "name": f"{brand} {category} {i+1}",
                "description": f"高品质的{category}产品，性能卓越",
                "price": random.randint(99, 9999),
                "original_price": random.randint(999, 19999),
                "category": category,
                "brand": brand,
                "stock": random.randint(0, 100),
                "rating": round(random.uniform(3.0, 5.0), 1),
                "reviews_count": random.randint(10, 1000),
                "images": [
                    f"https://picsum.photos/400/400?random={i+1}",
                    f"https://picsum.photos/400/400?random={i+100}"
                ],
                "tags": random.sample(["热销", "新品", "推荐", "限时", "包邮"], k=2),
                "specifications": {
                    "颜色": random.choice(["黑色", "白色", "金色", "银色"]),
                    "尺寸": f"{random.randint(5, 15)}.{random.randint(0, 9)}英寸",
                    "重量": f"{random.randint(100, 2000)}g"
                },
                "status": random.choice(["active", "inactive", "out_of_stock"]),
                "created_at": datetime.now().isoformat()
            })
        
        return products
    
    def _generate_orders(self, count: int) -> List[Dict]:
        """生成订单数据"""
        orders = []
        statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
        
        for i in range(count):
            item_count = random.randint(1, 5)
            total_amount = 0
            items = []
            
            for j in range(item_count):
                price = random.randint(99, 999)
                quantity = random.randint(1, 3)
                items.append({
                    "product_id": random.randint(1, 20),
                    "product_name": f"商品{j+1}",
                    "price": price,
                    "quantity": quantity,
                    "subtotal": price * quantity
                })
                total_amount += price * quantity
            
            orders.append({
                "id": f"ORD{datetime.now().strftime('%Y%m%d')}{i+1:04d}",
                "user_id": random.randint(1, 10),
                "status": random.choice(statuses),
                "items": items,
                "total_amount": total_amount,
                "shipping_address": {
                    "name": f"收货人{i+1}",
                    "phone": f"1{random.randint(30,89):02d}{random.randint(1000,9999):08d}",
                    "address": f"北京市朝阳区{random.choice(['建国门', '国贸', '三里屯'])}街道{i+1}号"
                },
                "payment_method": random.choice(["wechat", "alipay", "credit_card"]),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            })
        
        return orders
    
    def _generate_categories(self, count: int) -> List[Dict]:
        """生成分类数据"""
        categories = []
        main_categories = ["电子产品", "服装鞋包", "家居用品", "图书音像", "运动户外"]
        
        for i, main_cat in enumerate(main_categories[:count]):
            sub_categories = []
            for j in range(random.randint(3, 6)):
                sub_categories.append({
                    "id": i * 10 + j + 1,
                    "name": f"{main_cat}子分类{j+1}",
                    "product_count": random.randint(10, 100)
                })
            
            categories.append({
                "id": i + 1,
                "name": main_cat,
                "icon": f"category-{i+1}.svg",
                "description": f"{main_cat}相关的所有商品",
                "sub_categories": sub_categories,
                "sort_order": i + 1,
                "is_active": True,
                "created_at": datetime.now().isoformat()
            })
        
        return categories
    
    def _generate_settings(self, count: int) -> List[Dict]:
        """生成系统设置数据"""
        settings = [
            {"key": "site_name", "value": "演示商城", "type": "string", "description": "网站名称"},
            {"key": "site_logo", "value": "/images/logo.png", "type": "string", "description": "网站logo"},
            {"key": "contact_email", "value": "admin@example.com", "type": "email", "description": "联系邮箱"},
            {"key": "contact_phone", "value": "400-123-4567", "type": "string", "description": "联系电话"},
            {"key": "enable_registration", "value": True, "type": "boolean", "description": "允许用户注册"},
            {"key": "max_cart_items", "value": 20, "type": "number", "description": "购物车最大商品数"},
            {"key": "default_currency", "value": "CNY", "type": "string", "description": "默认货币"},
            {"key": "shipping_fee", "value": 10.00, "type": "number", "description": "配送费用"},
            {"key": "free_shipping_threshold", "value": 199.00, "type": "number", "description": "免邮门槛"},
            {"key": "maintenance_mode", "value": False, "type": "boolean", "description": "维护模式"}
        ]
        
        return settings[:count]
    
    def _create_data_config(self, results: Dict):
        """创建数据配置文件"""
        config = {
            "version": "1.0",
            "description": "项目mock数据配置",
            "generation_info": {
                "timestamp": results["timestamp"],
                "project": results["project"]
            },
            "data_sources": {},
            "api_endpoints": {}
        }
        
        # 配置数据源
        for data_type, info in results["generated_data"].items():
            config["data_sources"][data_type] = {
                "file": info["file"],
                "count": info["count"],
                "description": f"{data_type}相关数据"
            }
            
            # 生成API端点配置
            config["api_endpoints"][data_type] = {
                "list": f"/api/{data_type}",
                "detail": f"/api/{data_type}/:id",
                "create": f"/api/{data_type}",
                "update": f"/api/{data_type}/:id", 
                "delete": f"/api/{data_type}/:id"
            }
        
        config_file = self.data_dir / "config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def load_data(self, data_type: str) -> List[Dict]:
        """加载数据"""
        file_path = self.data_dir / f"{data_type}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def update_data(self, data_type: str, data: List[Dict]):
        """更新数据"""
        self._save_data(data_type, data)
    
    def create_api_mock(self) -> str:
        """创建API mock文件"""
        mock_content = '''
/**
 * API Mock 数据管理器
 * 模拟后端API响应
 */
class APIMock {
    constructor() {
        this.data = {};
        this.loadData();
    }
    
    async loadData() {
        // 加载所有mock数据
        const dataTypes = ['users', 'products', 'orders', 'categories', 'settings'];
        
        for (const type of dataTypes) {
            try {
                const response = await fetch(`data/${type}.json`);
                this.data[type] = await response.json();
            } catch (error) {
                console.warn(`加载 ${type} 数据失败:`, error);
                this.data[type] = [];
            }
        }
    }
    
    // 获取列表数据
    getList(type, params = {}) {
        let data = this.data[type] || [];
        const { page = 1, limit = 10, search = '', sort = 'id' } = params;
        
        // 搜索过滤
        if (search) {
            data = data.filter(item => 
                JSON.stringify(item).toLowerCase().includes(search.toLowerCase())
            );
        }
        
        // 排序
        data.sort((a, b) => {
            if (sort.startsWith('-')) {
                const field = sort.substring(1);
                return b[field] > a[field] ? 1 : -1;
            }
            return a[sort] > b[sort] ? 1 : -1;
        });
        
        // 分页
        const start = (page - 1) * limit;
        const items = data.slice(start, start + limit);
        
        return {
            success: true,
            data: {
                items,
                total: data.length,
                page: parseInt(page),
                limit: parseInt(limit),
                pages: Math.ceil(data.length / limit)
            }
        };
    }
    
    // 获取单个数据
    getDetail(type, id) {
        const data = this.data[type] || [];
        const item = data.find(item => item.id == id);
        
        return item ? 
            { success: true, data: item } : 
            { success: false, error: 'Not found' };
    }
    
    // 创建数据
    create(type, itemData) {
        if (!this.data[type]) this.data[type] = [];
        
        const newItem = {
            id: Math.max(0, ...this.data[type].map(item => item.id || 0)) + 1,
            ...itemData,
            created_at: new Date().toISOString()
        };
        
        this.data[type].push(newItem);
        return { success: true, data: newItem };
    }
    
    // 更新数据
    update(type, id, itemData) {
        const data = this.data[type] || [];
        const index = data.findIndex(item => item.id == id);
        
        if (index === -1) {
            return { success: false, error: 'Not found' };
        }
        
        data[index] = {
            ...data[index],
            ...itemData,
            updated_at: new Date().toISOString()
        };
        
        return { success: true, data: data[index] };
    }
    
    // 删除数据
    delete(type, id) {
        const data = this.data[type] || [];
        const index = data.findIndex(item => item.id == id);
        
        if (index === -1) {
            return { success: false, error: 'Not found' };
        }
        
        const deletedItem = data.splice(index, 1)[0];
        return { success: true, data: deletedItem };
    }
    
    // 模拟网络延迟
    async simulateDelay(ms = 500) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// 全局实例
window.apiMock = new APIMock();

// 模拟API调用函数
window.mockAPI = {
    get: async (url, params = {}) => {
        await window.apiMock.simulateDelay();
        
        const [, , type, id] = url.split('/');
        
        if (id) {
            return window.apiMock.getDetail(type, id);
        } else {
            return window.apiMock.getList(type, params);
        }
    },
    
    post: async (url, data) => {
        await window.apiMock.simulateDelay();
        const [, , type] = url.split('/');
        return window.apiMock.create(type, data);
    },
    
    put: async (url, data) => {
        await window.apiMock.simulateDelay();
        const [, , type, id] = url.split('/');
        return window.apiMock.update(type, id, data);
    },
    
    delete: async (url) => {
        await window.apiMock.simulateDelay();
        const [, , type, id] = url.split('/');
        return window.apiMock.delete(type, id);
    }
};
'''.strip()
        
        mock_file = self.data_dir / "api-mock.js"
        with open(mock_file, 'w', encoding='utf-8') as f:
            f.write(mock_content)
        
        return str(mock_file)
    
    def get_stats(self) -> Dict:
        """获取数据统计"""
        stats = {"total_files": 0, "total_records": 0, "data_types": {}}
        
        for json_file in self.data_dir.glob("*.json"):
            if json_file.name == "config.json":
                continue
                
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                data_type = json_file.stem
                record_count = len(data) if isinstance(data, list) else 1
                
                stats["data_types"][data_type] = {
                    "file": str(json_file),
                    "records": record_count
                }
                stats["total_files"] += 1
                stats["total_records"] += record_count
                
            except Exception as e:
                print(f"读取文件 {json_file} 失败: {e}")
        
        return stats


def main():
    """命令行界面"""
    import argparse
    
    parser = argparse.ArgumentParser(description="前端交互工程师 - 数据管理工具")
    parser.add_argument("project_path", help="项目路径")
    parser.add_argument("--create-mock", action='store_true', help="创建mock数据")
    parser.add_argument("--types", "-t", help="数据类型（逗号分隔）")
    parser.add_argument("--count", "-c", type=int, default=10, help="每种数据的生成数量")
    parser.add_argument("--create-api", action='store_true', help="创建API mock文件")
    parser.add_argument("--stats", action='store_true', help="显示数据统计")
    
    args = parser.parse_args()
    manager = DataManager(args.project_path)
    
    if args.create_mock:
        data_types = [t.strip() for t in args.types.split(',')] if args.types else None
        result = manager.create_mock_data(data_types, args.count)
        print(f"📊 Mock数据已生成到: {manager.data_dir}")
    
    if args.create_api:
        api_file = manager.create_api_mock()
        print(f"🔌 API Mock文件已生成: {api_file}")
    
    if args.stats:
        stats = manager.get_stats()
        print(f"\n📈 数据统计:")
        print(f"  文件数: {stats['total_files']}")
        print(f"  记录数: {stats['total_records']}")
        for data_type, info in stats["data_types"].items():
            print(f"  {data_type}: {info['records']} 条记录")


if __name__ == "__main__":
    main()