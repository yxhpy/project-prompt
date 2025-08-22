#!/usr/bin/env python3
"""
前端交互工程师 - 业务逻辑生成器
生成通用业务逻辑模板代码，支持自定义配置
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class BusinessLogicGenerator:
    """通用业务逻辑生成器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.business_dir = self.project_root / "business"
        self.business_dir.mkdir(exist_ok=True)
        
        # 通用业务逻辑模板
        self.templates = {
            "base_framework": self._get_base_framework_template,
            "data_storage": self._get_data_storage_template,
            "form_handler": self._get_form_handler_template,
            "navigation": self._get_navigation_template,
            "notification": self._get_notification_template,
            "validation": self._get_validation_template,
            "api_handler": self._get_api_handler_template
        }
    
    def generate_business_logic(self, logic_types: List[str] = None) -> Dict:
        """
        生成业务逻辑代码
        
        Args:
            logic_types: 要生成的逻辑类型列表，None表示生成所有
            
        Returns:
            Dict: 生成结果
        """
        if logic_types is None:
            logic_types = list(self.templates.keys())
        
        print(f"🚀 开始生成业务逻辑模块...")
        
        results = {
            "project_name": self.project_root.name,
            "generation_timestamp": datetime.now().isoformat(),
            "generated_modules": {},
            "integration_guide": []
        }
        
        for logic_type in logic_types:
            if logic_type in self.templates:
                print(f"📝 生成 {logic_type} 模块...")
                module_result = self._generate_module(logic_type)
                results["generated_modules"][logic_type] = module_result
            else:
                print(f"⚠️ 未知的业务逻辑类型: {logic_type}")
        
        # 生成集成文件
        self._generate_integration_file(results)
        
        # 生成使用说明
        self._generate_usage_guide(results)
        
        print(f"✅ 业务逻辑生成完成！共生成 {len(results['generated_modules'])} 个模块")
        
        return results
    
    def _generate_module(self, logic_type: str) -> Dict:
        """生成单个业务逻辑模块"""
        template_func = self.templates[logic_type]
        template_content = template_func()
        
        # 保存到文件
        file_path = self.business_dir / f"{logic_type}.js"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        return {
            "file_path": str(file_path),
            "size": len(template_content),
            "functions_count": template_content.count('function ') + template_content.count('=>'),
            "description": self._get_module_description(logic_type)
        }
    
    def _get_shopping_cart_template(self) -> str:
        """购物车业务逻辑模板"""
        return '''
/**
 * 购物车管理系统
 * 支持添加商品、删除商品、修改数量、计算总价等功能
 */
class ShoppingCartManager {
    constructor() {
        this.cart = this.loadCart();
        this.listeners = [];
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.updateCartDisplay();
    }
    
    // 添加商品到购物车
    addToCart(product) {
        const existingItem = this.cart.find(item => item.id === product.id);
        
        if (existingItem) {
            existingItem.quantity += product.quantity || 1;
        } else {
            this.cart.push({
                id: product.id,
                name: product.name,
                price: product.price,
                quantity: product.quantity || 1,
                image: product.image || '',
                addedAt: new Date().toISOString()
            });
        }
        
        this.saveCart();
        this.updateCartDisplay();
        this.notifyListeners('itemAdded', product);
        this.showNotification(`${product.name} 已添加到购物车`, 'success');
    }
    
    // 从购物车删除商品
    removeFromCart(productId) {
        const itemIndex = this.cart.findIndex(item => item.id === productId);
        if (itemIndex > -1) {
            const removedItem = this.cart.splice(itemIndex, 1)[0];
            this.saveCart();
            this.updateCartDisplay();
            this.notifyListeners('itemRemoved', removedItem);
            this.showNotification(`${removedItem.name} 已从购物车删除`, 'info');
        }
    }
    
    // 更新商品数量
    updateQuantity(productId, quantity) {
        const item = this.cart.find(item => item.id === productId);
        if (item) {
            if (quantity <= 0) {
                this.removeFromCart(productId);
            } else {
                item.quantity = quantity;
                this.saveCart();
                this.updateCartDisplay();
                this.notifyListeners('quantityUpdated', { productId, quantity });
            }
        }
    }
    
    // 清空购物车
    clearCart() {
        this.cart = [];
        this.saveCart();
        this.updateCartDisplay();
        this.notifyListeners('cartCleared');
        this.showNotification('购物车已清空', 'info');
    }
    
    // 获取购物车商品数量
    getItemCount() {
        return this.cart.reduce((total, item) => total + item.quantity, 0);
    }
    
    // 计算总价
    getTotalPrice() {
        return this.cart.reduce((total, item) => total + (item.price * item.quantity), 0);
    }
    
    // 获取购物车内容
    getCartItems() {
        return [...this.cart];
    }
    
    // 绑定事件
    bindEvents() {
        // 添加到购物车按钮
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-add-to-cart]')) {
                e.preventDefault();
                const productData = this.extractProductData(e.target);
                if (productData) {
                    this.addToCart(productData);
                }
            }
        });
        
        // 购物车页面操作
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-cart-remove]')) {
                e.preventDefault();
                const productId = e.target.getAttribute('data-cart-remove');
                this.removeFromCart(productId);
            }
            
            if (e.target.matches('[data-cart-clear]')) {
                e.preventDefault();
                if (confirm('确定要清空购物车吗？')) {
                    this.clearCart();
                }
            }
        });
        
        // 数量调整
        document.addEventListener('change', (e) => {
            if (e.target.matches('[data-cart-quantity]')) {
                const productId = e.target.getAttribute('data-cart-quantity');
                const quantity = parseInt(e.target.value);
                this.updateQuantity(productId, quantity);
            }
        });
    }
    
    // 从DOM元素提取商品数据
    extractProductData(element) {
        const productContainer = element.closest('[data-product]');
        if (!productContainer) return null;
        
        return {
            id: productContainer.getAttribute('data-product-id') || Date.now().toString(),
            name: productContainer.querySelector('[data-product-name]')?.textContent.trim() || '未知商品',
            price: parseFloat(productContainer.querySelector('[data-product-price]')?.textContent.replace(/[^\\d.]/g, '')) || 0,
            image: productContainer.querySelector('[data-product-image]')?.src || '',
            quantity: 1
        };
    }
    
    // 更新购物车显示
    updateCartDisplay() {
        // 更新购物车图标数量
        const cartBadges = document.querySelectorAll('[data-cart-count]');
        const itemCount = this.getItemCount();
        cartBadges.forEach(badge => {
            badge.textContent = itemCount;
            badge.style.display = itemCount > 0 ? 'inline' : 'none';
        });
        
        // 更新购物车列表
        const cartList = document.querySelector('[data-cart-list]');
        if (cartList) {
            this.renderCartList(cartList);
        }
        
        // 更新总价显示
        const totalElements = document.querySelectorAll('[data-cart-total]');
        const totalPrice = this.getTotalPrice();
        totalElements.forEach(element => {
            element.textContent = `¥${totalPrice.toFixed(2)}`;
        });
    }
    
    // 渲染购物车列表
    renderCartList(container) {
        if (this.cart.length === 0) {
            container.innerHTML = '<div class="text-center text-gray-500 py-8">购物车是空的</div>';
            return;
        }
        
        const cartHTML = this.cart.map(item => `
            <div class="cart-item border-b border-gray-200 py-4" data-product-id="${item.id}">
                <div class="flex items-center space-x-4">
                    ${item.image ? `<img src="${item.image}" alt="${item.name}" class="w-16 h-16 object-cover rounded">` : '<div class="w-16 h-16 bg-gray-200 rounded"></div>'}
                    <div class="flex-1">
                        <h3 class="font-medium text-gray-800">${item.name}</h3>
                        <p class="text-gray-600">¥${item.price.toFixed(2)}</p>
                    </div>
                    <div class="flex items-center space-x-2">
                        <input type="number" value="${item.quantity}" min="1" 
                               class="w-16 px-2 py-1 border rounded text-center" 
                               data-cart-quantity="${item.id}">
                        <button class="text-red-500 hover:text-red-700" 
                                data-cart-remove="${item.id}">删除</button>
                    </div>
                </div>
            </div>
        `).join('');
        
        container.innerHTML = cartHTML;
    }
    
    // 保存购物车到本地存储
    saveCart() {
        localStorage.setItem('shopping_cart', JSON.stringify(this.cart));
    }
    
    // 从本地存储加载购物车
    loadCart() {
        try {
            const saved = localStorage.getItem('shopping_cart');
            return saved ? JSON.parse(saved) : [];
        } catch (error) {
            console.warn('购物车数据加载失败:', error);
            return [];
        }
    }
    
    // 添加事件监听器
    addListener(callback) {
        this.listeners.push(callback);
    }
    
    // 通知监听器
    notifyListeners(event, data) {
        this.listeners.forEach(callback => {
            try {
                callback(event, data);
            } catch (error) {
                console.warn('购物车事件监听器错误:', error);
            }
        });
    }
    
    // 显示通知
    showNotification(message, type = 'info') {
        if (window.notificationManager) {
            window.notificationManager.show(message, type);
        } else {
            // 简单的alert备用方案
            console.log(`[${type.toUpperCase()}] ${message}`);
        }
    }
}

// 自动初始化
document.addEventListener('DOMContentLoaded', () => {
    window.shoppingCart = new ShoppingCartManager();
});
'''.strip()
    
    def _get_user_auth_template(self) -> str:
        """用户认证业务逻辑模板"""
        return '''
/**
 * 用户认证管理系统
 * 支持登录、注册、登出、状态检查等功能
 */
class UserAuthManager {
    constructor() {
        this.currentUser = this.loadUserFromStorage();
        this.authListeners = [];
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.updateAuthDisplay();
    }
    
    // 用户登录
    async login(username, password) {
        try {
            // 模拟登录验证（实际项目中应该调用后端API）
            const mockUsers = this.getMockUsers();
            const user = mockUsers.find(u => u.username === username && u.password === password);
            
            if (user) {
                const authUser = {
                    id: user.id,
                    username: user.username,
                    email: user.email,
                    role: user.role,
                    loginTime: new Date().toISOString()
                };
                
                this.setCurrentUser(authUser);
                this.showNotification('登录成功！', 'success');
                this.notifyAuthListeners('login', authUser);
                return { success: true, user: authUser };
            } else {
                this.showNotification('用户名或密码错误', 'error');
                return { success: false, error: '用户名或密码错误' };
            }
        } catch (error) {
            console.error('登录错误:', error);
            this.showNotification('登录失败，请稍后重试', 'error');
            return { success: false, error: error.message };
        }
    }
    
    // 用户注册
    async register(userData) {
        try {
            // 验证输入数据
            const validation = this.validateRegistrationData(userData);
            if (!validation.valid) {
                this.showNotification(validation.error, 'error');
                return { success: false, error: validation.error };
            }
            
            // 检查用户名是否已存在
            const mockUsers = this.getMockUsers();
            const existingUser = mockUsers.find(u => u.username === userData.username || u.email === userData.email);
            
            if (existingUser) {
                this.showNotification('用户名或邮箱已存在', 'error');
                return { success: false, error: '用户名或邮箱已存在' };
            }
            
            // 创建新用户
            const newUser = {
                id: Date.now().toString(),
                username: userData.username,
                email: userData.email,
                password: userData.password, // 实际项目中应该加密
                role: 'user',
                createdAt: new Date().toISOString()
            };
            
            // 保存到模拟数据库
            this.saveMockUser(newUser);
            
            // 自动登录
            const authUser = {
                id: newUser.id,
                username: newUser.username,
                email: newUser.email,
                role: newUser.role,
                loginTime: new Date().toISOString()
            };
            
            this.setCurrentUser(authUser);
            this.showNotification('注册成功！', 'success');
            this.notifyAuthListeners('register', authUser);
            
            return { success: true, user: authUser };
        } catch (error) {
            console.error('注册错误:', error);
            this.showNotification('注册失败，请稍后重试', 'error');
            return { success: false, error: error.message };
        }
    }
    
    // 用户登出
    logout() {
        const user = this.currentUser;
        this.currentUser = null;
        this.clearUserFromStorage();
        this.updateAuthDisplay();
        this.showNotification('已安全登出', 'info');
        this.notifyAuthListeners('logout', user);
    }
    
    // 检查是否已登录
    isLoggedIn() {
        return this.currentUser !== null;
    }
    
    // 获取当前用户
    getCurrentUser() {
        return this.currentUser;
    }
    
    // 设置当前用户
    setCurrentUser(user) {
        this.currentUser = user;
        this.saveUserToStorage(user);
        this.updateAuthDisplay();
    }
    
    // 验证注册数据
    validateRegistrationData(data) {
        if (!data.username || data.username.length < 3) {
            return { valid: false, error: '用户名至少需要3个字符' };
        }
        
        if (!data.email || !this.isValidEmail(data.email)) {
            return { valid: false, error: '请输入有效的邮箱地址' };
        }
        
        if (!data.password || data.password.length < 6) {
            return { valid: false, error: '密码至少需要6个字符' };
        }
        
        if (data.password !== data.confirmPassword) {
            return { valid: false, error: '两次输入的密码不一致' };
        }
        
        return { valid: true };
    }
    
    // 验证邮箱格式
    isValidEmail(email) {
        const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
        return emailRegex.test(email);
    }
    
    // 绑定认证相关事件
    bindEvents() {
        // 登录表单提交
        document.addEventListener('submit', (e) => {
            if (e.target.matches('[data-login-form]')) {
                e.preventDefault();
                this.handleLoginForm(e.target);
            }
            
            if (e.target.matches('[data-register-form]')) {
                e.preventDefault();
                this.handleRegisterForm(e.target);
            }
        });
        
        // 登出按钮
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-logout]')) {
                e.preventDefault();
                if (confirm('确定要登出吗？')) {
                    this.logout();
                }
            }
        });
    }
    
    // 处理登录表单
    async handleLoginForm(form) {
        const formData = new FormData(form);
        const username = formData.get('username');
        const password = formData.get('password');
        
        if (!username || !password) {
            this.showNotification('请填写用户名和密码', 'error');
            return;
        }
        
        // 显示加载状态
        const submitBtn = form.querySelector('[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = '登录中...';
        submitBtn.disabled = true;
        
        try {
            const result = await this.login(username, password);
            if (result.success) {
                // 登录成功，可以跳转到其他页面
                setTimeout(() => {
                    if (window.router) {
                        window.router.navigateTo('/dashboard');
                    }
                }, 1000);
            }
        } finally {
            // 恢复按钮状态
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    }
    
    // 处理注册表单
    async handleRegisterForm(form) {
        const formData = new FormData(form);
        const userData = {
            username: formData.get('username'),
            email: formData.get('email'),
            password: formData.get('password'),
            confirmPassword: formData.get('confirmPassword')
        };
        
        // 显示加载状态
        const submitBtn = form.querySelector('[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = '注册中...';
        submitBtn.disabled = true;
        
        try {
            const result = await this.register(userData);
            if (result.success) {
                // 注册成功，可以跳转到其他页面
                setTimeout(() => {
                    if (window.router) {
                        window.router.navigateTo('/dashboard');
                    }
                }, 1000);
            }
        } finally {
            // 恢复按钮状态
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    }
    
    // 更新认证相关的UI显示
    updateAuthDisplay() {
        const isLoggedIn = this.isLoggedIn();
        
        // 显示/隐藏登录相关元素
        document.querySelectorAll('[data-show-when-logged-in]').forEach(element => {
            element.style.display = isLoggedIn ? '' : 'none';
        });
        
        document.querySelectorAll('[data-show-when-logged-out]').forEach(element => {
            element.style.display = isLoggedIn ? 'none' : '';
        });
        
        // 更新用户信息显示
        if (isLoggedIn && this.currentUser) {
            document.querySelectorAll('[data-user-name]').forEach(element => {
                element.textContent = this.currentUser.username;
            });
            
            document.querySelectorAll('[data-user-email]').forEach(element => {
                element.textContent = this.currentUser.email;
            });
        }
    }
    
    // 本地存储操作
    saveUserToStorage(user) {
        localStorage.setItem('current_user', JSON.stringify(user));
    }
    
    loadUserFromStorage() {
        try {
            const saved = localStorage.getItem('current_user');
            return saved ? JSON.parse(saved) : null;
        } catch (error) {
            console.warn('用户数据加载失败:', error);
            return null;
        }
    }
    
    clearUserFromStorage() {
        localStorage.removeItem('current_user');
    }
    
    // 模拟用户数据
    getMockUsers() {
        try {
            const saved = localStorage.getItem('mock_users');
            const defaultUsers = [
                {
                    id: '1',
                    username: 'admin',
                    email: 'admin@example.com',
                    password: 'admin123',
                    role: 'admin'
                },
                {
                    id: '2',
                    username: 'user',
                    email: 'user@example.com',
                    password: 'user123',
                    role: 'user'
                }
            ];
            
            return saved ? JSON.parse(saved) : defaultUsers;
        } catch (error) {
            console.warn('模拟用户数据加载失败:', error);
            return [];
        }
    }
    
    saveMockUser(user) {
        const users = this.getMockUsers();
        users.push(user);
        localStorage.setItem('mock_users', JSON.stringify(users));
    }
    
    // 事件监听器管理
    addAuthListener(callback) {
        this.authListeners.push(callback);
    }
    
    notifyAuthListeners(event, data) {
        this.authListeners.forEach(callback => {
            try {
                callback(event, data);
            } catch (error) {
                console.warn('认证事件监听器错误:', error);
            }
        });
    }
    
    // 显示通知
    showNotification(message, type = 'info') {
        if (window.notificationManager) {
            window.notificationManager.show(message, type);
        } else {
            console.log(`[${type.toUpperCase()}] ${message}`);
        }
    }
}

// 自动初始化
document.addEventListener('DOMContentLoaded', () => {
    window.userAuth = new UserAuthManager();
});
'''.strip()
    
    def _get_search_template(self) -> str:
        """搜索功能业务逻辑模板"""
        return '''
/**
 * 搜索功能管理系统
 * 支持实时搜索、搜索历史、热门搜索等功能
 */
class SearchManager {
    constructor() {
        this.searchHistory = this.loadSearchHistory();
        this.searchListeners = [];
        this.debounceTimer = null;
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadMockData();
    }
    
    // 执行搜索
    async performSearch(query, options = {}) {
        if (!query || query.trim().length === 0) {
            return { results: [], query: '' };
        }
        
        const normalizedQuery = query.trim().toLowerCase();
        
        // 保存搜索历史
        this.addToHistory(normalizedQuery);
        
        try {
            // 模拟搜索延迟
            await this.delay(300);
            
            // 在模拟数据中搜索
            const results = this.searchInMockData(normalizedQuery, options);
            
            // 通知监听器
            this.notifyListeners('searchCompleted', { query: normalizedQuery, results });
            
            return { results, query: normalizedQuery };
        } catch (error) {
            console.error('搜索错误:', error);
            this.notifyListeners('searchError', { query: normalizedQuery, error });
            return { results: [], query: normalizedQuery, error: error.message };
        }
    }
    
    // 实时搜索（带防抖）
    performLiveSearch(query, inputElement, options = {}) {
        // 清除之前的定时器
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        
        // 设置新的防抖定时器
        this.debounceTimer = setTimeout(async () => {
            if (query.length >= (options.minLength || 2)) {
                const results = await this.performSearch(query, options);
                this.showSearchSuggestions(inputElement, results.results, query);
            } else {
                this.hideSearchSuggestions(inputElement);
            }
        }, options.debounceTime || 300);
    }
    
    // 在模拟数据中搜索
    searchInMockData(query, options = {}) {
        const mockData = this.getMockData();
        const maxResults = options.maxResults || 20;
        
        const results = mockData.filter(item => {
            const searchableText = [
                item.title,
                item.description,
                item.category,
                ...(item.tags || [])
            ].join(' ').toLowerCase();
            
            return searchableText.includes(query);
        });
        
        // 按相关性排序
        const sortedResults = results.sort((a, b) => {
            const aRelevance = this.calculateRelevance(a, query);
            const bRelevance = this.calculateRelevance(b, query);
            return bRelevance - aRelevance;
        });
        
        return sortedResults.slice(0, maxResults);
    }
    
    // 计算搜索相关性
    calculateRelevance(item, query) {
        let score = 0;
        const queryWords = query.split(' ');
        
        queryWords.forEach(word => {
            if (item.title.toLowerCase().includes(word)) score += 10;
            if (item.description.toLowerCase().includes(word)) score += 5;
            if (item.category.toLowerCase().includes(word)) score += 3;
            if (item.tags && item.tags.some(tag => tag.toLowerCase().includes(word))) score += 2;
        });
        
        return score;
    }
    
    // 显示搜索建议
    showSearchSuggestions(inputElement, results, query) {
        // 移除现有的建议框
        this.hideSearchSuggestions(inputElement);
        
        if (results.length === 0) return;
        
        // 创建建议框
        const suggestionBox = document.createElement('div');
        suggestionBox.className = 'search-suggestions absolute z-50 w-full bg-white border border-gray-300 rounded-b shadow-lg max-h-64 overflow-y-auto';
        suggestionBox.setAttribute('data-search-suggestions', '');
        
        // 生成建议项
        const suggestionsHTML = results.slice(0, 8).map(item => `
            <div class="search-suggestion-item px-4 py-2 hover:bg-gray-100 cursor-pointer border-b border-gray-100" 
                 data-search-select="${item.id}">
                <div class="font-medium text-gray-800">${this.highlightMatch(item.title, query)}</div>
                <div class="text-sm text-gray-600">${this.highlightMatch(item.description.substring(0, 100), query)}...</div>
            </div>
        `).join('');
        
        suggestionBox.innerHTML = suggestionsHTML;
        
        // 定位建议框
        const inputRect = inputElement.getBoundingClientRect();
        const container = inputElement.closest('.relative') || inputElement.parentElement;
        container.style.position = 'relative';
        container.appendChild(suggestionBox);
        
        // 绑定选择事件
        suggestionBox.addEventListener('click', (e) => {
            const suggestionItem = e.target.closest('[data-search-select]');
            if (suggestionItem) {
                const itemId = suggestionItem.getAttribute('data-search-select');
                const selectedItem = results.find(item => item.id === itemId);
                this.selectSearchResult(selectedItem, inputElement);
            }
        });
    }
    
    // 隐藏搜索建议
    hideSearchSuggestions(inputElement) {
        const container = inputElement.closest('.relative') || inputElement.parentElement;
        const existingSuggestions = container.querySelector('[data-search-suggestions]');
        if (existingSuggestions) {
            existingSuggestions.remove();
        }
    }
    
    // 选择搜索结果
    selectSearchResult(item, inputElement) {
        inputElement.value = item.title;
        this.hideSearchSuggestions(inputElement);
        this.notifyListeners('resultSelected', item);
        
        // 如果有跳转URL，执行跳转
        if (item.url && window.router) {
            window.router.navigateTo(item.url);
        }
    }
    
    // 高亮匹配文本
    highlightMatch(text, query) {
        if (!query) return text;
        
        const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&')})`, 'gi');
        return text.replace(regex, '<mark class="bg-yellow-200">$1</mark>');
    }
    
    // 搜索历史管理
    addToHistory(query) {
        // 移除重复项
        this.searchHistory = this.searchHistory.filter(item => item.query !== query);
        
        // 添加到开头
        this.searchHistory.unshift({
            query,
            timestamp: new Date().toISOString()
        });
        
        // 限制历史记录数量
        if (this.searchHistory.length > 50) {
            this.searchHistory = this.searchHistory.slice(0, 50);
        }
        
        this.saveSearchHistory();
    }
    
    getSearchHistory(limit = 10) {
        return this.searchHistory.slice(0, limit);
    }
    
    clearSearchHistory() {
        this.searchHistory = [];
        this.saveSearchHistory();
    }
    
    // 绑定搜索事件
    bindEvents() {
        // 搜索输入框事件
        document.addEventListener('input', (e) => {
            if (e.target.matches('[data-search-input]')) {
                const query = e.target.value;
                const liveSearch = e.target.getAttribute('data-live-search') !== 'false';
                
                if (liveSearch) {
                    this.performLiveSearch(query, e.target);
                }
            }
        });
        
        // 搜索表单提交
        document.addEventListener('submit', (e) => {
            if (e.target.matches('[data-search-form]')) {
                e.preventDefault();
                const input = e.target.querySelector('[data-search-input]');
                if (input) {
                    this.handleSearchSubmit(input.value, e.target);
                }
            }
        });
        
        // 点击外部隐藏建议
        document.addEventListener('click', (e) => {
            if (!e.target.closest('[data-search-input]') && !e.target.closest('[data-search-suggestions]')) {
                document.querySelectorAll('[data-search-suggestions]').forEach(suggestions => {
                    suggestions.remove();
                });
            }
        });
        
        // 键盘导航
        document.addEventListener('keydown', (e) => {
            if (e.target.matches('[data-search-input]')) {
                this.handleKeyboardNavigation(e);
            }
        });
    }
    
    // 处理搜索提交
    async handleSearchSubmit(query, form) {
        if (!query.trim()) return;
        
        // 显示加载状态
        const submitBtn = form.querySelector('[type="submit"]');
        const originalText = submitBtn ? submitBtn.textContent : '';
        if (submitBtn) {
            submitBtn.textContent = '搜索中...';
            submitBtn.disabled = true;
        }
        
        try {
            const results = await this.performSearch(query);
            this.displaySearchResults(results.results, query);
        } finally {
            // 恢复按钮状态
            if (submitBtn) {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }
        }
    }
    
    // 显示搜索结果
    displaySearchResults(results, query) {
        const resultsContainer = document.querySelector('[data-search-results]');
        if (!resultsContainer) return;
        
        if (results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="text-center py-8 text-gray-500">
                    <p>未找到与"${query}"相关的结果</p>
                    <p class="text-sm mt-2">请尝试其他关键词</p>
                </div>
            `;
            return;
        }
        
        const resultsHTML = `
            <div class="search-results-header mb-4">
                <p class="text-gray-600">找到 ${results.length} 个结果（搜索："${query}"）</p>
            </div>
            <div class="search-results-list space-y-4">
                ${results.map(item => `
                    <div class="search-result-item border border-gray-200 rounded p-4 hover:shadow-md transition-shadow">
                        <h3 class="font-bold text-lg mb-2">
                            <a href="${item.url || '#'}" class="text-blue-600 hover:text-blue-800">
                                ${this.highlightMatch(item.title, query)}
                            </a>
                        </h3>
                        <p class="text-gray-600 mb-2">${this.highlightMatch(item.description, query)}</p>
                        <div class="flex items-center text-sm text-gray-500">
                            <span class="bg-gray-100 px-2 py-1 rounded">${item.category}</span>
                            ${item.tags ? item.tags.map(tag => `<span class="ml-2 text-blue-500">#${tag}</span>`).join('') : ''}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        resultsContainer.innerHTML = resultsHTML;
    }
    
    // 键盘导航处理
    handleKeyboardNavigation(e) {
        const suggestions = document.querySelector('[data-search-suggestions]');
        if (!suggestions) return;
        
        const items = suggestions.querySelectorAll('[data-search-select]');
        if (items.length === 0) return;
        
        let currentIndex = Array.from(items).findIndex(item => item.classList.contains('selected'));
        
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                currentIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0;
                this.updateSelectedSuggestion(items, currentIndex);
                break;
            case 'ArrowUp':
                e.preventDefault();
                currentIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
                this.updateSelectedSuggestion(items, currentIndex);
                break;
            case 'Enter':
                e.preventDefault();
                if (currentIndex >= 0) {
                    items[currentIndex].click();
                }
                break;
            case 'Escape':
                this.hideSearchSuggestions(e.target);
                break;
        }
    }
    
    updateSelectedSuggestion(items, selectedIndex) {
        items.forEach((item, index) => {
            if (index === selectedIndex) {
                item.classList.add('selected', 'bg-blue-100');
            } else {
                item.classList.remove('selected', 'bg-blue-100');
            }
        });
    }
    
    // 数据管理
    loadMockData() {
        // 如果没有模拟数据，创建一些示例数据
        if (!localStorage.getItem('search_mock_data')) {
            const mockData = [
                {
                    id: '1',
                    title: 'iPhone 15 Pro',
                    description: '最新款iPhone，配备A17 Pro芯片，支持Action Button',
                    category: '手机',
                    tags: ['苹果', 'iOS', '5G'],
                    url: '/products/iphone-15-pro'
                },
                {
                    id: '2',
                    title: 'MacBook Pro M3',
                    description: '搭载M3芯片的专业级笔记本电脑，性能强劲',
                    category: '电脑',
                    tags: ['苹果', 'macOS', '笔记本'],
                    url: '/products/macbook-pro-m3'
                },
                {
                    id: '3',
                    title: 'AirPods Pro 2',
                    description: '第二代AirPods Pro，主动降噪升级',
                    category: '耳机',
                    tags: ['苹果', '蓝牙', '降噪'],
                    url: '/products/airpods-pro-2'
                }
            ];
            localStorage.setItem('search_mock_data', JSON.stringify(mockData));
        }
    }
    
    getMockData() {
        try {
            const saved = localStorage.getItem('search_mock_data');
            return saved ? JSON.parse(saved) : [];
        } catch (error) {
            console.warn('搜索模拟数据加载失败:', error);
            return [];
        }
    }
    
    // 本地存储操作
    saveSearchHistory() {
        localStorage.setItem('search_history', JSON.stringify(this.searchHistory));
    }
    
    loadSearchHistory() {
        try {
            const saved = localStorage.getItem('search_history');
            return saved ? JSON.parse(saved) : [];
        } catch (error) {
            console.warn('搜索历史加载失败:', error);
            return [];
        }
    }
    
    // 工具方法
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    // 事件监听器管理
    addListener(callback) {
        this.searchListeners.push(callback);
    }
    
    notifyListeners(event, data) {
        this.searchListeners.forEach(callback => {
            try {
                callback(event, data);
            } catch (error) {
                console.warn('搜索事件监听器错误:', error);
            }
        });
    }
}

// 自动初始化
document.addEventListener('DOMContentLoaded', () => {
    window.searchManager = new SearchManager();
});
'''.strip()
    
    def _get_form_validation_template(self) -> str:
        """表单验证模板"""
        return '''
/**
 * 表单验证管理系统
 * 支持实时验证、自定义规则、错误提示等功能
 */
class FormValidationManager {
    constructor() {
        this.validators = {};
        this.validationRules = this.getDefaultRules();
        this.init();
    }
    
    init() {
        this.bindEvents();
    }
    
    // 默认验证规则
    getDefaultRules() {
        return {
            required: {
                validate: (value) => value !== null && value !== undefined && value.toString().trim() !== '',
                message: '此字段为必填项'
            },
            email: {
                validate: (value) => /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(value),
                message: '请输入有效的邮箱地址'
            },
            phone: {
                validate: (value) => /^1[3-9]\\d{9}$/.test(value),
                message: '请输入有效的手机号码'
            },
            minLength: {
                validate: (value, param) => value.length >= parseInt(param),
                message: (param) => `至少需要${param}个字符`
            },
            maxLength: {
                validate: (value, param) => value.length <= parseInt(param),
                message: (param) => `最多${param}个字符`
            },
            min: {
                validate: (value, param) => parseFloat(value) >= parseFloat(param),
                message: (param) => `值不能小于${param}`
            },
            max: {
                validate: (value, param) => parseFloat(value) <= parseFloat(param),
                message: (param) => `值不能大于${param}`
            },
            pattern: {
                validate: (value, param) => new RegExp(param).test(value),
                message: '格式不正确'
            },
            confirm: {
                validate: (value, param, form) => {
                    const confirmField = form.querySelector(`[name="${param}"]`);
                    return confirmField ? value === confirmField.value : false;
                },
                message: (param) => `与${param}字段不一致`
            },
            url: {
                validate: (value) => {
                    try {
                        new URL(value);
                        return true;
                    } catch {
                        return false;
                    }
                },
                message: '请输入有效的URL地址'
            },
            number: {
                validate: (value) => !isNaN(value) && !isNaN(parseFloat(value)),
                message: '请输入有效的数字'
            },
            integer: {
                validate: (value) => Number.isInteger(parseFloat(value)),
                message: '请输入整数'
            },
            date: {
                validate: (value) => !isNaN(Date.parse(value)),
                message: '请输入有效的日期'
            }
        };
    }
    
    // 绑定表单验证事件
    bindEvents() {
        // 实时验证
        document.addEventListener('input', (e) => {
            if (e.target.matches('[data-validate]')) {
                this.validateField(e.target);
            }
        });
        
        document.addEventListener('blur', (e) => {
            if (e.target.matches('[data-validate]')) {
                this.validateField(e.target);
            }
        });
        
        // 表单提交验证
        document.addEventListener('submit', (e) => {
            if (e.target.matches('[data-validate-form]')) {
                const isValid = this.validateForm(e.target);
                if (!isValid) {
                    e.preventDefault();
                    this.showFormError(e.target, '请修正表单中的错误后重新提交');
                }
            }
        });
    }
    
    // 验证单个字段
    validateField(field) {
        const rules = this.parseValidationRules(field.getAttribute('data-validate'));
        const value = field.value;
        const fieldName = field.name || field.id;
        const form = field.closest('form');
        
        // 清除之前的错误
        this.clearFieldError(field);
        
        // 执行验证
        for (const rule of rules) {
            const ruleConfig = this.validationRules[rule.name];
            if (!ruleConfig) {
                console.warn(`未知的验证规则: ${rule.name}`);
                continue;
            }
            
            // 如果字段为空且不是必填项，跳过验证
            if (!value && rule.name !== 'required') {
                continue;
            }
            
            let isValid;
            if (rule.name === 'confirm') {
                isValid = ruleConfig.validate(value, rule.param, form);
            } else {
                isValid = ruleConfig.validate(value, rule.param);
            }
            
            if (!isValid) {
                let message;
                if (typeof ruleConfig.message === 'function') {
                    message = ruleConfig.message(rule.param);
                } else {
                    message = ruleConfig.message;
                }
                
                this.showFieldError(field, message);
                return false;
            }
        }
        
        // 验证通过
        this.showFieldSuccess(field);
        return true;
    }
    
    // 验证整个表单
    validateForm(form) {
        const fields = form.querySelectorAll('[data-validate]');
        let isValid = true;
        let firstInvalidField = null;
        
        fields.forEach(field => {
            const fieldValid = this.validateField(field);
            if (!fieldValid) {
                isValid = false;
                if (!firstInvalidField) {
                    firstInvalidField = field;
                }
            }
        });
        
        // 滚动到第一个错误字段
        if (firstInvalidField) {
            firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
            firstInvalidField.focus();
        }
        
        return isValid;
    }
    
    // 解析验证规则
    parseValidationRules(rulesString) {
        if (!rulesString) return [];
        
        const rules = [];
        const ruleStrings = rulesString.split('|');
        
        ruleStrings.forEach(ruleString => {
            const [name, param] = ruleString.split(':');
            rules.push({ name: name.trim(), param: param ? param.trim() : null });
        });
        
        return rules;
    }
    
    // 显示字段错误
    showFieldError(field, message) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
        
        // 添加错误样式
        field.style.borderColor = '#ef4444';
        
        // 显示错误消息
        let errorElement = field.parentElement.querySelector('.validation-error');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'validation-error text-red-500 text-sm mt-1';
            field.parentElement.appendChild(errorElement);
        }
        
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
    
    // 显示字段成功状态
    showFieldSuccess(field) {
        field.classList.add('is-valid');
        field.classList.remove('is-invalid');
        
        // 添加成功样式
        field.style.borderColor = '#10b981';
        
        // 隐藏错误消息
        const errorElement = field.parentElement.querySelector('.validation-error');
        if (errorElement) {
            errorElement.style.display = 'none';
        }
    }
    
    // 清除字段错误
    clearFieldError(field) {
        field.classList.remove('is-invalid', 'is-valid');
        field.style.borderColor = '';
        
        const errorElement = field.parentElement.querySelector('.validation-error');
        if (errorElement) {
            errorElement.style.display = 'none';
        }
    }
    
    // 显示表单级错误
    showFormError(form, message) {
        let errorElement = form.querySelector('.form-error');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'form-error bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4';
            form.insertBefore(errorElement, form.firstChild);
        }
        
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        
        // 显示通知
        if (window.notificationManager) {
            window.notificationManager.show(message, 'error');
        }
    }
    
    // 清除表单错误
    clearFormError(form) {
        const errorElement = form.querySelector('.form-error');
        if (errorElement) {
            errorElement.style.display = 'none';
        }
    }
    
    // 添加自定义验证规则
    addValidationRule(name, validator) {
        this.validationRules[name] = validator;
    }
    
    // 程序化验证字段
    validate(fieldSelector, rules) {
        const field = document.querySelector(fieldSelector);
        if (!field) {
            console.warn(`字段不存在: ${fieldSelector}`);
            return false;
        }
        
        field.setAttribute('data-validate', rules);
        return this.validateField(field);
    }
    
    // 获取表单数据（已验证）
    getValidatedFormData(form) {
        const isValid = this.validateForm(form);
        if (!isValid) {
            return null;
        }
        
        const formData = new FormData(form);
        const data = {};
        
        for (const [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        return data;
    }
    
    // 重置表单验证状态
    resetForm(form) {
        const fields = form.querySelectorAll('[data-validate]');
        fields.forEach(field => {
            this.clearFieldError(field);
        });
        
        this.clearFormError(form);
    }
}

// 自动初始化
document.addEventListener('DOMContentLoaded', () => {
    window.formValidator = new FormValidationManager();
});
'''.strip()
    
    def _get_routing_template(self) -> str:
        """路由管理模板"""
        return '''
/**
 * 单页应用路由管理系统
 * 支持页面导航、历史管理、参数传递等功能
 */
class RouterManager {
    constructor() {
        this.routes = new Map();
        this.currentRoute = null;
        this.beforeRouteHooks = [];
        this.afterRouteHooks = [];
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.handleInitialRoute();
    }
    
    // 注册路由
    addRoute(path, handler, options = {}) {
        this.routes.set(path, {
            handler,
            title: options.title || '',
            requiresAuth: options.requiresAuth || false,
            meta: options.meta || {}
        });
    }
    
    // 批量注册路由
    addRoutes(routeConfig) {
        Object.entries(routeConfig).forEach(([path, config]) => {
            this.addRoute(path, config.handler, config);
        });
    }
    
    // 导航到指定路由
    navigateTo(path, params = {}) {
        const fullPath = this.buildPath(path, params);
        
        // 执行before hooks
        for (const hook of this.beforeRouteHooks) {
            const result = hook(fullPath, this.currentRoute);
            if (result === false) {
                return false; // 阻止导航
            }
        }
        
        // 更新浏览器历史
        history.pushState({ path: fullPath, params }, '', fullPath);
        
        // 执行路由处理
        this.handleRoute(fullPath, params);
        
        return true;
    }
    
    // 替换当前路由（不添加历史记录）
    replaceTo(path, params = {}) {
        const fullPath = this.buildPath(path, params);
        history.replaceState({ path: fullPath, params }, '', fullPath);
        this.handleRoute(fullPath, params);
    }
    
    // 返回上一页
    goBack() {
        history.back();
    }
    
    // 前进到下一页
    goForward() {
        history.forward();
    }
    
    // 处理路由
    handleRoute(path, params = {}) {
        const route = this.matchRoute(path);
        
        if (!route) {
            this.handle404(path);
            return;
        }
        
        // 检查认证要求
        if (route.config.requiresAuth && !this.isAuthenticated()) {
            this.redirectToLogin(path);
            return;
        }
        
        // 执行路由处理器
        try {
            const routeContext = {
                path,
                params,
                query: this.parseQuery(),
                meta: route.config.meta
            };
            
            this.currentRoute = routeContext;
            
            // 更新页面标题
            if (route.config.title) {
                document.title = route.config.title;
            }
            
            // 执行处理器
            route.config.handler(routeContext);
            
            // 执行after hooks
            this.afterRouteHooks.forEach(hook => {
                hook(routeContext, this.currentRoute);
            });
            
        } catch (error) {
            console.error('路由处理错误:', error);
            this.handleError(error, path);
        }
    }
    
    // 匹配路由
    matchRoute(path) {
        // 清理路径
        const cleanPath = path.split('?')[0].replace(/\\/$/, '') || '/';
        
        // 精确匹配
        if (this.routes.has(cleanPath)) {
            return {
                path: cleanPath,
                config: this.routes.get(cleanPath),
                params: {}
            };
        }
        
        // 参数匹配
        for (const [routePath, config] of this.routes) {
            const params = this.matchParams(routePath, cleanPath);
            if (params !== null) {
                return {
                    path: routePath,
                    config,
                    params
                };
            }
        }
        
        return null;
    }
    
    // 匹配路径参数
    matchParams(routePath, actualPath) {
        const routeParts = routePath.split('/');
        const actualParts = actualPath.split('/');
        
        if (routeParts.length !== actualParts.length) {
            return null;
        }
        
        const params = {};
        
        for (let i = 0; i < routeParts.length; i++) {
            const routePart = routeParts[i];
            const actualPart = actualParts[i];
            
            if (routePart.startsWith(':')) {
                // 参数匹配
                const paramName = routePart.substring(1);
                params[paramName] = decodeURIComponent(actualPart);
            } else if (routePart !== actualPart) {
                // 静态部分不匹配
                return null;
            }
        }
        
        return params;
    }
    
    // 构建路径
    buildPath(path, params = {}) {
        let builtPath = path;
        
        // 替换路径参数
        Object.entries(params).forEach(([key, value]) => {
            builtPath = builtPath.replace(`:${key}`, encodeURIComponent(value));
        });
        
        return builtPath;
    }
    
    // 解析查询参数
    parseQuery() {
        const query = {};
        const searchParams = new URLSearchParams(window.location.search);
        
        for (const [key, value] of searchParams) {
            query[key] = value;
        }
        
        return query;
    }
    
    // 绑定事件
    bindEvents() {
        // 处理浏览器前进后退
        window.addEventListener('popstate', (e) => {
            if (e.state) {
                this.handleRoute(e.state.path, e.state.params || {});
            } else {
                this.handleRoute(window.location.pathname);
            }
        });
        
        // 拦截链接点击
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]');
            if (!link) return;
            
            const href = link.getAttribute('href');
            
            // 忽略外部链接和特殊链接
            if (this.shouldIgnoreLink(href, link)) return;
            
            e.preventDefault();
            this.navigateTo(href);
        });
    }
    
    // 判断是否应该忽略链接
    shouldIgnoreLink(href, link) {
        // 外部链接
        if (href.startsWith('http://') || href.startsWith('https://')) {
            return true;
        }
        
        // 邮件和电话链接
        if (href.startsWith('mailto:') || href.startsWith('tel:')) {
            return true;
        }
        
        // 锚点链接（同页面）
        if (href.startsWith('#')) {
            return true;
        }
        
        // 明确标记为外部链接
        if (link.hasAttribute('target') && link.getAttribute('target') === '_blank') {
            return true;
        }
        
        // 标记为不使用路由
        if (link.hasAttribute('data-no-route')) {
            return true;
        }
        
        return false;
    }
    
    // 处理初始路由
    handleInitialRoute() {
        const path = window.location.pathname;
        this.handleRoute(path);
    }
    
    // 处理404错误
    handle404(path) {
        console.warn(`路由不存在: ${path}`);
        
        // 查找404处理器
        if (this.routes.has('/404')) {
            const notFoundConfig = this.routes.get('/404');
            notFoundConfig.handler({ path, error: 'Not Found' });
        } else {
            // 默认404处理
            this.showDefaultError('页面不存在', `找不到页面：${path}`);
        }
    }
    
    // 处理路由错误
    handleError(error, path) {
        console.error('路由错误:', error);
        
        if (this.routes.has('/error')) {
            const errorConfig = this.routes.get('/error');
            errorConfig.handler({ path, error });
        } else {
            this.showDefaultError('页面加载失败', error.message);
        }
    }
    
    // 显示默认错误页面
    showDefaultError(title, message) {
        const contentArea = document.querySelector('[data-router-view]') || document.body;
        contentArea.innerHTML = `
            <div class="error-page text-center py-16">
                <h1 class="text-4xl font-bold text-gray-800 mb-4">${title}</h1>
                <p class="text-gray-600 mb-8">${message}</p>
                <button onclick="window.router.goBack()" 
                        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                    返回上页
                </button>
            </div>
        `;
    }
    
    // 认证检查
    isAuthenticated() {
        // 简单的认证检查，实际项目中应该更完善
        return window.userAuth && window.userAuth.isLoggedIn();
    }
    
    // 重定向到登录页
    redirectToLogin(returnUrl) {
        const loginPath = '/login';
        if (returnUrl) {
            this.navigateTo(`${loginPath}?return=${encodeURIComponent(returnUrl)}`);
        } else {
            this.navigateTo(loginPath);
        }
    }
    
    // 添加路由钩子
    beforeRoute(hook) {
        this.beforeRouteHooks.push(hook);
    }
    
    afterRoute(hook) {
        this.afterRouteHooks.push(hook);
    }
    
    // 获取当前路由信息
    getCurrentRoute() {
        return this.currentRoute;
    }
    
    // 获取所有注册的路由
    getRoutes() {
        return Array.from(this.routes.keys());
    }
}

// 自动初始化
document.addEventListener('DOMContentLoaded', () => {
    window.router = new RouterManager();
});
'''.strip()
    
    def _get_data_manager_template(self) -> str:
        """数据管理模板"""
        return '''
/**
 * 数据管理系统
 * 支持本地存储、状态管理、数据同步等功能
 */
class DataManager {
    constructor() {
        this.storage = new Map();
        this.listeners = new Map();
        this.config = {
            storagePrefix: 'app_',
            enableAutoSave: true,
            autoSaveInterval: 30000, // 30秒
            enableCompression: false
        };
        this.init();
    }
    
    init() {
        this.loadFromLocalStorage();
        this.setupAutoSave();
    }
    
    // 设置数据
    set(key, value, options = {}) {
        const oldValue = this.storage.get(key);
        this.storage.set(key, value);
        
        // 持久化到localStorage
        if (options.persist !== false) {
            this.saveToLocalStorage(key, value);
        }
        
        // 触发变化事件
        this.notifyListeners(key, value, oldValue);
        
        return this;
    }
    
    // 获取数据
    get(key, defaultValue = null) {
        return this.storage.has(key) ? this.storage.get(key) : defaultValue;
    }
    
    // 检查数据是否存在
    has(key) {
        return this.storage.has(key);
    }
    
    // 删除数据
    remove(key) {
        const oldValue = this.storage.get(key);
        this.storage.delete(key);
        this.removeFromLocalStorage(key);
        this.notifyListeners(key, undefined, oldValue);
        return this;
    }
    
    // 清空所有数据
    clear() {
        const keys = Array.from(this.storage.keys());
        this.storage.clear();
        this.clearLocalStorage();
        
        keys.forEach(key => {
            this.notifyListeners(key, undefined, undefined);
        });
        
        return this;
    }
    
    // 批量设置数据
    setMany(data, options = {}) {
        Object.entries(data).forEach(([key, value]) => {
            this.set(key, value, options);
        });
        return this;
    }
    
    // 批量获取数据
    getMany(keys) {
        const result = {};
        keys.forEach(key => {
            result[key] = this.get(key);
        });
        return result;
    }
    
    // 更新数据（合并对象）
    update(key, updater) {
        const currentValue = this.get(key);
        
        let newValue;
        if (typeof updater === 'function') {
            newValue = updater(currentValue);
        } else if (typeof updater === 'object' && updater !== null) {
            newValue = { ...currentValue, ...updater };
        } else {
            newValue = updater;
        }
        
        return this.set(key, newValue);
    }
    
    // 监听数据变化
    subscribe(key, callback) {
        if (!this.listeners.has(key)) {
            this.listeners.set(key, new Set());
        }
        
        this.listeners.get(key).add(callback);
        
        // 返回取消订阅函数
        return () => {
            this.unsubscribe(key, callback);
        };
    }
    
    // 取消监听
    unsubscribe(key, callback) {
        if (this.listeners.has(key)) {
            this.listeners.get(key).delete(callback);
        }
    }
    
    // 通知监听器
    notifyListeners(key, newValue, oldValue) {
        if (this.listeners.has(key)) {
            this.listeners.get(key).forEach(callback => {
                try {
                    callback(newValue, oldValue, key);
                } catch (error) {
                    console.warn('数据监听器错误:', error);
                }
            });
        }
        
        // 通知全局监听器
        if (this.listeners.has('*')) {
            this.listeners.get('*').forEach(callback => {
                try {
                    callback(key, newValue, oldValue);
                } catch (error) {
                    console.warn('全局数据监听器错误:', error);
                }
            });
        }
    }
    
    // 本地存储操作
    saveToLocalStorage(key, value) {
        try {
            const storageKey = this.config.storagePrefix + key;
            const data = {
                value,
                timestamp: Date.now(),
                version: '1.0'
            };
            
            let serialized = JSON.stringify(data);
            
            if (this.config.enableCompression && serialized.length > 1000) {
                // 简单的压缩（实际项目中可以使用专门的压缩库）
                serialized = this.compress(serialized);
                data.compressed = true;
            }
            
            localStorage.setItem(storageKey, serialized);
        } catch (error) {
            console.warn(`保存数据到localStorage失败 (${key}):`, error);
        }
    }
    
    loadFromLocalStorage() {
        try {
            const prefix = this.config.storagePrefix;
            const prefixLength = prefix.length;
            
            for (let i = 0; i < localStorage.length; i++) {
                const storageKey = localStorage.key(i);
                if (storageKey && storageKey.startsWith(prefix)) {
                    const key = storageKey.substring(prefixLength);
                    const value = this.loadFromLocalStorageKey(key);
                    if (value !== null) {
                        this.storage.set(key, value);
                    }
                }
            }
        } catch (error) {
            console.warn('从localStorage加载数据失败:', error);
        }
    }
    
    loadFromLocalStorageKey(key) {
        try {
            const storageKey = this.config.storagePrefix + key;
            let serialized = localStorage.getItem(storageKey);
            
            if (!serialized) return null;
            
            const data = JSON.parse(serialized);
            
            if (data.compressed) {
                serialized = this.decompress(serialized);
                return JSON.parse(serialized).value;
            }
            
            return data.value;
        } catch (error) {
            console.warn(`从localStorage加载数据失败 (${key}):`, error);
            return null;
        }
    }
    
    removeFromLocalStorage(key) {
        try {
            const storageKey = this.config.storagePrefix + key;
            localStorage.removeItem(storageKey);
        } catch (error) {
            console.warn(`从localStorage删除数据失败 (${key}):`, error);
        }
    }
    
    clearLocalStorage() {
        try {
            const prefix = this.config.storagePrefix;
            const keysToRemove = [];
            
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key && key.startsWith(prefix)) {
                    keysToRemove.push(key);
                }
            }
            
            keysToRemove.forEach(key => {
                localStorage.removeItem(key);
            });
        } catch (error) {
            console.warn('清空localStorage失败:', error);
        }
    }
    
    // 自动保存设置
    setupAutoSave() {
        if (this.config.enableAutoSave) {
            setInterval(() => {
                this.saveAll();
            }, this.config.autoSaveInterval);
        }
    }
    
    // 保存所有数据
    saveAll() {
        this.storage.forEach((value, key) => {
            this.saveToLocalStorage(key, value);
        });
    }
    
    // 数据导出
    export(keys = null) {
        const data = {};
        const exportKeys = keys || Array.from(this.storage.keys());
        
        exportKeys.forEach(key => {
            if (this.storage.has(key)) {
                data[key] = this.storage.get(key);
            }
        });
        
        return {
            data,
            timestamp: new Date().toISOString(),
            version: '1.0'
        };
    }
    
    // 数据导入
    import(exportData, options = {}) {
        if (!exportData || !exportData.data) {
            throw new Error('无效的导入数据');
        }
        
        const { merge = false, validate = true } = options;
        
        if (!merge) {
            this.clear();
        }
        
        Object.entries(exportData.data).forEach(([key, value]) => {
            if (validate && !this.validateData(key, value)) {
                console.warn(`跳过无效数据: ${key}`);
                return;
            }
            
            this.set(key, value);
        });
        
        return this;
    }
    
    // 数据验证
    validateData(key, value) {
        try {
            // 基本验证：检查是否可以序列化
            JSON.stringify(value);
            return true;
        } catch (error) {
            return false;
        }
    }
    
    // 简单压缩（实际项目中建议使用专门的压缩库）
    compress(str) {
        // 这里只是一个简单的示例，实际应该使用LZString等库
        return btoa(str);
    }
    
    decompress(str) {
        return atob(str);
    }
    
    // 获取存储统计信息
    getStats() {
        const stats = {
            totalKeys: this.storage.size,
            memorySize: 0,
            localStorageSize: 0,
            keys: Array.from(this.storage.keys())
        };
        
        // 计算内存使用
        this.storage.forEach((value, key) => {
            stats.memorySize += JSON.stringify({ key, value }).length;
        });
        
        // 计算localStorage使用
        const prefix = this.config.storagePrefix;
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(prefix)) {
                const value = localStorage.getItem(key);
                stats.localStorageSize += (key + value).length;
            }
        }
        
        return stats;
    }
    
    // 配置管理
    configure(options) {
        this.config = { ...this.config, ...options };
        return this;
    }
    
    getConfig() {
        return { ...this.config };
    }
}

// 自动初始化
document.addEventListener('DOMContentLoaded', () => {
    window.dataManager = new DataManager();
});
'''.strip()
    
    def _get_notification_template(self) -> str:
        """通知系统模板"""
        return '''
/**
 * 通知系统
 * 支持多种类型的通知、自定义样式、位置控制等功能
 */
class NotificationManager {
    constructor() {
        this.notifications = [];
        this.container = null;
        this.defaultConfig = {
            duration: 3000,
            position: 'top-right',
            maxNotifications: 5,
            enableSound: false,
            animation: 'slide'
        };
        this.init();
    }
    
    init() {
        this.createContainer();
        this.injectStyles();
    }
    
    // 显示通知
    show(message, type = 'info', options = {}) {
        const config = { ...this.defaultConfig, ...options };
        
        const notification = {
            id: this.generateId(),
            message,
            type,
            config,
            timestamp: Date.now()
        };
        
        this.notifications.push(notification);
        
        // 限制通知数量
        if (this.notifications.length > config.maxNotifications) {
            const oldNotification = this.notifications.shift();
            this.removeNotificationElement(oldNotification.id);
        }
        
        this.renderNotification(notification);
        
        // 自动关闭
        if (config.duration > 0) {
            setTimeout(() => {
                this.hide(notification.id);
            }, config.duration);
        }
        
        // 播放声音
        if (config.enableSound) {
            this.playNotificationSound(type);
        }
        
        return notification.id;
    }
    
    // 隐藏通知
    hide(notificationId) {
        const index = this.notifications.findIndex(n => n.id === notificationId);
        if (index > -1) {
            this.notifications.splice(index, 1);
            this.removeNotificationElement(notificationId);
        }
    }
    
    // 隐藏所有通知
    hideAll() {
        this.notifications.forEach(notification => {
            this.removeNotificationElement(notification.id);
        });
        this.notifications = [];
    }
    
    // 成功通知
    success(message, options = {}) {
        return this.show(message, 'success', options);
    }
    
    // 错误通知
    error(message, options = {}) {
        return this.show(message, 'error', { duration: 5000, ...options });
    }
    
    // 警告通知
    warning(message, options = {}) {
        return this.show(message, 'warning', options);
    }
    
    // 信息通知
    info(message, options = {}) {
        return this.show(message, 'info', options);
    }
    
    // 加载通知
    loading(message, options = {}) {
        return this.show(message, 'loading', { duration: 0, ...options });
    }
    
    // 确认通知
    confirm(message, onConfirm, onCancel, options = {}) {
        const config = {
            duration: 0,
            showButtons: true,
            ...options
        };
        
        const notificationId = this.show(message, 'confirm', config);
        
        // 添加按钮事件监听
        setTimeout(() => {
            const element = document.getElementById(`notification-${notificationId}`);
            if (element) {
                const confirmBtn = element.querySelector('.btn-confirm');
                const cancelBtn = element.querySelector('.btn-cancel');
                
                if (confirmBtn) {
                    confirmBtn.addEventListener('click', () => {
                        this.hide(notificationId);
                        if (onConfirm) onConfirm();
                    });
                }
                
                if (cancelBtn) {
                    cancelBtn.addEventListener('click', () => {
                        this.hide(notificationId);
                        if (onCancel) onCancel();
                    });
                }
            }
        }, 100);
        
        return notificationId;
    }
    
    // 创建容器
    createContainer() {
        this.container = document.createElement('div');
        this.container.id = 'notification-container';
        this.container.className = 'notification-container';
        document.body.appendChild(this.container);
    }
    
    // 渲染通知
    renderNotification(notification) {
        const element = this.createNotificationElement(notification);
        this.container.appendChild(element);
        
        // 触发动画
        setTimeout(() => {
            element.classList.add('notification-show');
        }, 10);
    }
    
    // 创建通知元素
    createNotificationElement(notification) {
        const element = document.createElement('div');
        element.id = `notification-${notification.id}`;
        element.className = `notification notification-${notification.type} notification-${notification.config.animation}`;
        
        const icon = this.getTypeIcon(notification.type);
        const closeButton = notification.config.duration === 0 ? 
            '<button class="notification-close">&times;</button>' : '';
        
        let buttonsHTML = '';
        if (notification.config.showButtons) {
            buttonsHTML = `
                <div class="notification-buttons">
                    <button class="btn-confirm">确认</button>
                    <button class="btn-cancel">取消</button>
                </div>
            `;
        }
        
        element.innerHTML = `
            <div class="notification-content">
                <div class="notification-icon">${icon}</div>
                <div class="notification-message">${notification.message}</div>
                ${closeButton}
            </div>
            ${buttonsHTML}
        `;
        
        // 绑定关闭事件
        const closeBtn = element.querySelector('.notification-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                this.hide(notification.id);
            });
        }
        
        return element;
    }
    
    // 移除通知元素
    removeNotificationElement(notificationId) {
        const element = document.getElementById(`notification-${notificationId}`);
        if (element) {
            element.classList.add('notification-hide');
            setTimeout(() => {
                if (element.parentNode) {
                    element.parentNode.removeChild(element);
                }
            }, 300);
        }
    }
    
    // 获取类型图标
    getTypeIcon(type) {
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ',
            loading: '⟳',
            confirm: '?'
        };
        
        return icons[type] || icons.info;
    }
    
    // 播放通知声音
    playNotificationSound(type) {
        try {
            // 创建音频上下文（如果支持）
            if ('AudioContext' in window || 'webkitAudioContext' in window) {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                const audioContext = new AudioContext();
                
                // 生成简单的提示音
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                // 根据类型设置不同频率
                const frequencies = {
                    success: 800,
                    error: 400,
                    warning: 600,
                    info: 500,
                    loading: 450,
                    confirm: 700
                };
                
                oscillator.frequency.value = frequencies[type] || 500;
                oscillator.type = 'sine';
                
                gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
                
                oscillator.start(audioContext.currentTime);
                oscillator.stop(audioContext.currentTime + 0.5);
            }
        } catch (error) {
            console.warn('播放通知声音失败:', error);
        }
    }
    
    // 注入样式
    injectStyles() {
        const styles = `
            .notification-container {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                pointer-events: none;
            }
            
            .notification {
                background: white;
                border: 1px solid #e5e5e5;
                border-radius: 6px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                margin-bottom: 10px;
                min-width: 300px;
                max-width: 400px;
                opacity: 0;
                transform: translateX(100%);
                transition: all 0.3s ease;
                pointer-events: auto;
            }
            
            .notification-show {
                opacity: 1;
                transform: translateX(0);
            }
            
            .notification-hide {
                opacity: 0;
                transform: translateX(100%);
            }
            
            .notification-content {
                display: flex;
                align-items: flex-start;
                padding: 12px 16px;
            }
            
            .notification-icon {
                font-size: 18px;
                margin-right: 12px;
                flex-shrink: 0;
                margin-top: 2px;
            }
            
            .notification-message {
                flex: 1;
                line-height: 1.4;
                color: #333;
            }
            
            .notification-close {
                background: none;
                border: none;
                font-size: 18px;
                cursor: pointer;
                color: #999;
                margin-left: 12px;
                padding: 0;
                line-height: 1;
            }
            
            .notification-close:hover {
                color: #666;
            }
            
            .notification-buttons {
                padding: 0 16px 12px;
                text-align: right;
            }
            
            .notification-buttons button {
                margin-left: 8px;
                padding: 4px 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background: white;
                cursor: pointer;
                font-size: 12px;
            }
            
            .btn-confirm {
                background: #007bff !important;
                color: white !important;
                border-color: #007bff !important;
            }
            
            .btn-confirm:hover {
                background: #0056b3 !important;
            }
            
            .notification-success {
                border-left: 4px solid #28a745;
            }
            
            .notification-success .notification-icon {
                color: #28a745;
            }
            
            .notification-error {
                border-left: 4px solid #dc3545;
            }
            
            .notification-error .notification-icon {
                color: #dc3545;
            }
            
            .notification-warning {
                border-left: 4px solid #ffc107;
            }
            
            .notification-warning .notification-icon {
                color: #ffc107;
            }
            
            .notification-info {
                border-left: 4px solid #17a2b8;
            }
            
            .notification-info .notification-icon {
                color: #17a2b8;
            }
            
            .notification-loading .notification-icon {
                color: #6c757d;
                animation: spin 1s linear infinite;
            }
            
            .notification-confirm {
                border-left: 4px solid #6f42c1;
            }
            
            .notification-confirm .notification-icon {
                color: #6f42c1;
            }
            
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            @media (max-width: 480px) {
                .notification-container {
                    left: 10px;
                    right: 10px;
                    top: 10px;
                }
                
                .notification {
                    min-width: auto;
                    max-width: none;
                }
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }
    
    // 生成唯一ID
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
    
    // 获取通知列表
    getNotifications() {
        return [...this.notifications];
    }
    
    // 配置管理
    configure(options) {
        this.defaultConfig = { ...this.defaultConfig, ...options };
    }
}

// 自动初始化
document.addEventListener('DOMContentLoaded', () => {
    window.notificationManager = new NotificationManager();
});
'''.strip()
    
    def _generate_integration_file(self, results: Dict) -> None:
        """生成集成文件"""
        integration_content = f'''
/**
 * 业务逻辑集成文件
 * 统一加载和初始化所有业务模块
 * 生成时间: {results["generation_timestamp"]}
 */

class BusinessLogicIntegrator {{
    constructor() {{
        this.modules = new Map();
        this.loadOrder = [
            'notification',
            'data_manager', 
            'form_validation',
            'user_auth',
            'search',
            'shopping_cart',
            'routing'
        ];
        this.init();
    }}
    
    async init() {{
        console.log('🚀 开始加载业务逻辑模块...');
        
        // 按顺序加载模块
        for (const moduleName of this.loadOrder) {{
            if (this.shouldLoadModule(moduleName)) {{
                await this.loadModule(moduleName);
            }}
        }}
        
        // 模块间依赖设置
        this.setupModuleDependencies();
        
        console.log('✅ 所有业务逻辑模块加载完成');
    }}
    
    shouldLoadModule(moduleName) {{
        // 检查页面是否需要该模块
        const moduleIndicators = {{
            'shopping_cart': '[data-add-to-cart], [data-cart-list]',
            'user_auth': '[data-login-form], [data-register-form]', 
            'search': '[data-search-input], [data-search-form]',
            'form_validation': '[data-validate]',
            'routing': '[data-router-view]'
        }};
        
        const indicator = moduleIndicators[moduleName];
        return !indicator || document.querySelector(indicator);
    }}
    
    async loadModule(moduleName) {{
        try {{
            const script = document.createElement('script');
            script.src = `business/${{moduleName}}.js`;
            script.onload = () => {{
                this.modules.set(moduleName, true);
                console.log(`📦 模块 ${{moduleName}} 加载完成`);
            }};
            script.onerror = () => {{
                console.warn(`⚠️ 模块 ${{moduleName}} 加载失败`);
            }};
            
            document.head.appendChild(script);
            
            // 等待加载完成
            return new Promise((resolve) => {{
                script.onload = resolve;
                script.onerror = resolve;
            }});
        }} catch (error) {{
            console.warn(`模块 ${{moduleName}} 加载错误:`, error);
        }}
    }}
    
    setupModuleDependencies() {{
        // 购物车与用户认证集成
        if (window.shoppingCart && window.userAuth) {{
            window.shoppingCart.addListener((event, data) => {{
                if (!window.userAuth.isLoggedIn() && event === 'itemAdded') {{
                    window.notificationManager?.show('登录后可保存购物车', 'info');
                }}
            }});
        }}
        
        // 搜索与路由集成
        if (window.searchManager && window.router) {{
            window.searchManager.addListener((event, data) => {{
                if (event === 'resultSelected' && data.url) {{
                    window.router.navigateTo(data.url);
                }}
            }});
        }}
        
        // 表单验证与通知集成
        if (window.formValidator && window.notificationManager) {{
            // 表单验证失败时显示通知
            const originalShowFieldError = window.formValidator.showFieldError;
            window.formValidator.showFieldError = function(field, message) {{
                originalShowFieldError.call(this, field, message);
                if (window.notificationManager) {{
                    window.notificationManager.show(message, 'error', {{ duration: 2000 }});
                }}
            }};
        }}
    }}
    
    getLoadedModules() {{
        return Array.from(this.modules.keys());
    }}
}}

// 自动初始化
document.addEventListener('DOMContentLoaded', () => {{
    window.businessLogicIntegrator = new BusinessLogicIntegrator();
}});
'''.strip()
        
        integration_file = self.business_dir / "integration.js"
        with open(integration_file, 'w', encoding='utf-8') as f:
            f.write(integration_content)
        
        results["integration_guide"].append(f"集成文件已生成: {integration_file}")
    
    def _generate_usage_guide(self, results: Dict) -> None:
        """生成使用说明"""
        guide_content = f"""# 业务逻辑模块使用说明

生成时间: {results["generation_timestamp"]}
项目: {results["project_name"]}

## 已生成模块

{chr(10).join([f"- **{module}**: {info['description']}" for module, info in results["generated_modules"].items()])}

## 使用方法

### 1. 在HTML页面中引入

```html
<!-- 在页面底部，body标签结束前引入 -->
<script src="business/integration.js"></script>
```

### 2. 各模块的HTML标记

#### 购物车功能
```html
<!-- 商品容器 -->
<div data-product data-product-id="1">
    <span data-product-name>iPhone 15</span>
    <span data-product-price>¥5999</span>
    <img data-product-image src="iphone.jpg" alt="iPhone 15">
    <button data-add-to-cart>加入购物车</button>
</div>

<!-- 购物车显示 -->
<span data-cart-count>0</span>
<div data-cart-list></div>
<span data-cart-total>¥0.00</span>
```

#### 用户认证
```html
<!-- 登录表单 -->
<form data-login-form>
    <input name="username" required>
    <input name="password" type="password" required>
    <button type="submit">登录</button>
</form>

<!-- 用户信息显示 -->
<span data-user-name></span>
<span data-user-email></span>
<button data-logout>登出</button>

<!-- 条件显示 -->
<div data-show-when-logged-in>已登录内容</div>
<div data-show-when-logged-out>未登录内容</div>
```

#### 搜索功能
```html
<!-- 搜索表单 -->
<form data-search-form>
    <input data-search-input data-live-search="true" placeholder="搜索...">
    <button type="submit">搜索</button>
</form>

<!-- 搜索结果 -->
<div data-search-results></div>
```

#### 表单验证
```html
<!-- 带验证的表单 -->
<form data-validate-form>
    <input name="email" data-validate="required|email">
    <input name="password" data-validate="required|minLength:6">
    <input name="confirmPassword" data-validate="required|confirm:password">
    <button type="submit">提交</button>
</form>
```

#### 路由导航
```html
<!-- 页面容器 -->
<div data-router-view></div>

<!-- 导航链接 -->
<a href="/products">商品页面</a>
<a href="/cart">购物车</a>
```

## 编程接口

### 购物车
```javascript
// 添加商品
window.shoppingCart.addToCart({
    id: '1',
    name: 'iPhone 15',
    price: 5999,
    quantity: 1
});

// 获取购物车内容
const items = window.shoppingCart.getCartItems();
const total = window.shoppingCart.getTotalPrice();
```

### 用户认证
```javascript
// 登录
const result = await window.userAuth.login('username', 'password');

// 检查登录状态
const isLoggedIn = window.userAuth.isLoggedIn();
const currentUser = window.userAuth.getCurrentUser();
```

### 搜索
```javascript
// 执行搜索
const results = await window.searchManager.performSearch('关键词');

// 监听搜索事件
window.searchManager.addListener((event, data) => {
    console.log('搜索事件:', event, data);
});
```

### 表单验证
```javascript
// 验证表单
const isValid = window.formValidator.validateForm(formElement);

// 获取验证后的数据
const data = window.formValidator.getValidatedFormData(formElement);
```

### 路由导航
```javascript
// 注册路由
window.router.addRoute('/products', (context) => {
    // 显示商品页面
});

// 导航到页面
window.router.navigateTo('/products');
```

### 数据管理
```javascript
// 存储数据
window.dataManager.set('user_preferences', { theme: 'dark' });

// 获取数据
const preferences = window.dataManager.get('user_preferences');

// 监听数据变化
window.dataManager.subscribe('user_preferences', (newValue, oldValue) => {
    console.log('用户偏好更新:', newValue);
});
```

### 通知系统
```javascript
// 显示通知
window.notificationManager.success('操作成功！');
window.notificationManager.error('操作失败！');
window.notificationManager.warning('注意事项');

// 确认对话框
window.notificationManager.confirm('确定删除？', () => {
    // 确认操作
}, () => {
    // 取消操作
});
```

## 注意事项

1. **模块加载**: 模块会根据页面内容自动按需加载
2. **依赖关系**: 通知系统会优先加载，其他模块依赖它显示消息
3. **数据持久化**: 购物车、用户信息、搜索历史等会自动保存到localStorage
4. **移动端适配**: 所有功能都支持移动端触摸操作
5. **错误处理**: 模块包含完善的错误处理和降级方案

## 自定义配置

每个模块都支持配置，在模块初始化后可以进行自定义：

```javascript
// 配置通知系统
window.notificationManager.configure({
    duration: 5000,
    position: 'top-left',
    enableSound: true
});

// 配置数据管理器
window.dataManager.configure({
    storagePrefix: 'myapp_',
    enableAutoSave: true
});
```
"""
        
        guide_file = self.business_dir / "README.md"
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        results["integration_guide"].append(f"使用说明已生成: {guide_file}")
    
    def _get_module_description(self, logic_type: str) -> str:
        """获取模块描述"""
        descriptions = {
            "shopping_cart": "购物车管理：商品添加、删除、数量调整、总价计算",
            "user_auth": "用户认证：登录、注册、登出、状态管理",
            "search": "搜索功能：实时搜索、搜索建议、历史记录",
            "form_validation": "表单验证：实时验证、自定义规则、错误提示",
            "routing": "路由管理：页面导航、历史管理、参数传递",
            "data_manager": "数据管理：本地存储、状态管理、数据同步",
            "notification": "通知系统：消息提示、确认对话框、声音提醒"
        }
        return descriptions.get(logic_type, "业务逻辑模块")


def main():
    """命令行界面"""
    import argparse
    
    parser = argparse.ArgumentParser(description="前端交互工程师 - 业务逻辑生成器")
    parser.add_argument("project_path", help="项目路径")
    parser.add_argument("--types", "-t", help="要生成的业务逻辑类型，用逗号分隔（如：shopping_cart,user_auth）")
    parser.add_argument("--list", "-l", action='store_true', help="列出所有可用的业务逻辑类型")
    
    args = parser.parse_args()
    
    generator = BusinessLogicGenerator(args.project_path)
    
    if args.list:
        print("📋 可用的业务逻辑类型:")
        for logic_type in generator.templates.keys():
            description = generator._get_module_description(logic_type)
            print(f"  • {logic_type}: {description}")
        return
    
    logic_types = None
    if args.types:
        logic_types = [t.strip() for t in args.types.split(',')]
    
    result = generator.generate_business_logic(logic_types)
    
    print(f"\n🎯 生成完成！")
    for guide in result.get("integration_guide", []):
        print(f"  📄 {guide}")


if __name__ == "__main__":
    main()