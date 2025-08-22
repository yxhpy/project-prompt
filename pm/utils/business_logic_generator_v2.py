#!/usr/bin/env python3
"""
前端交互工程师 - 通用业务逻辑生成器
生成通用的JavaScript模板，而不是特定业务代码
"""

import os
import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime

class BusinessLogicGenerator:
    """通用业务逻辑生成器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.business_dir = self.project_root / "business"
        self.business_dir.mkdir(exist_ok=True)
        
        # 通用模板类型
        self.templates = {
            "base_framework": "应用基础框架",
            "data_storage": "数据存储管理器", 
            "form_handler": "表单处理器",
            "navigation": "导航管理器",
            "notification": "通知系统",
            "validation": "验证管理器",
            "event_manager": "事件管理器"
        }
    
    def generate_templates(self, template_types: List[str] = None) -> Dict:
        """生成通用模板"""
        if not template_types:
            template_types = list(self.templates.keys())
        
        print("🚀 开始生成通用业务逻辑模板...")
        
        results = {
            "project": self.project_root.name,
            "timestamp": datetime.now().isoformat(),
            "generated": {},
            "examples": {}
        }
        
        for template_type in template_types:
            if template_type in self.templates:
                print(f"📝 生成 {template_type} 模板...")
                results["generated"][template_type] = self._create_template(template_type)
                results["examples"][template_type] = self._get_example(template_type)
        
        # 生成集成文件
        self._create_integrator()
        self._create_config()
        
        print(f"✅ 完成！共生成 {len(results['generated'])} 个模板")
        return results
    
    def _create_template(self, template_type: str) -> str:
        """创建单个模板文件"""
        content = self._get_template_content(template_type)
        file_path = self.business_dir / f"{template_type}.js"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(file_path)
    
    def _get_template_content(self, template_type: str) -> str:
        """获取模板内容 - 通用版本"""
        templates = {
            "base_framework": '''
/**
 * 应用基础框架 - 提供模块管理和初始化
 */
class AppFramework {
    constructor(config = {}) {
        this.config = { debug: false, autoInit: true, ...config };
        this.modules = new Map();
        this.hooks = new Map();
        if (this.config.autoInit) this.init();
    }
    
    init() {
        this.log('框架初始化...');
        this.executeHooks('init');
    }
    
    loadModule(name, options = {}) {
        const script = document.createElement('script');
        script.src = `business/${name}.js`;
        script.onload = () => {
            this.modules.set(name, options);
            this.log(`模块 ${name} 已加载`);
        };
        document.head.appendChild(script);
    }
    
    addHook(event, callback) {
        if (!this.hooks.has(event)) this.hooks.set(event, []);
        this.hooks.get(event).push(callback);
    }
    
    executeHooks(event, data = null) {
        if (this.hooks.has(event)) {
            this.hooks.get(event).forEach(callback => callback(data));
        }
    }
    
    log(message) {
        if (this.config.debug) console.log(`[Framework] ${message}`);
    }
}

window.AppFramework = AppFramework;
'''.strip(),
            
            "data_storage": '''
/**
 * 数据存储管理器 - 统一的存储接口
 */
class DataStorage {
    constructor(options = {}) {
        this.options = { prefix: 'app_', storage: 'localStorage', ...options };
        this.cache = new Map();
        this.listeners = new Map();
    }
    
    set(key, value, options = {}) {
        const fullKey = this.options.prefix + key;
        const data = { value, timestamp: Date.now() };
        
        try {
            if (this.options.storage === 'memory') {
                this.cache.set(fullKey, data);
            } else {
                window[this.options.storage].setItem(fullKey, JSON.stringify(data));
            }
            this.notify(key, value);
            return true;
        } catch (error) {
            console.warn('存储失败:', error);
            return false;
        }
    }
    
    get(key, defaultValue = null) {
        const fullKey = this.options.prefix + key;
        
        try {
            let data;
            if (this.options.storage === 'memory') {
                data = this.cache.get(fullKey);
            } else {
                const stored = window[this.options.storage].getItem(fullKey);
                data = stored ? JSON.parse(stored) : null;
            }
            return data ? data.value : defaultValue;
        } catch (error) {
            return defaultValue;
        }
    }
    
    subscribe(key, callback) {
        if (!this.listeners.has(key)) this.listeners.set(key, []);
        this.listeners.get(key).push(callback);
    }
    
    notify(key, value) {
        if (this.listeners.has(key)) {
            this.listeners.get(key).forEach(cb => cb(value));
        }
    }
}

window.DataStorage = DataStorage;
'''.strip(),
            
            "form_handler": '''
/**
 * 表单处理器 - 统一的表单管理
 */
class FormHandler {
    constructor(options = {}) {
        this.options = { validateOnInput: true, ...options };
        this.forms = new Map();
        this.validators = new Map();
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.addValidator('required', (value) => !!value && value.trim() !== '');
        this.addValidator('email', (value) => /^[^@]+@[^@]+\\.[^@]+$/.test(value));
    }
    
    register(selector, config = {}) {
        const form = document.querySelector(selector);
        if (form) {
            this.forms.set(selector, { element: form, ...config });
            this.setupValidation(form);
        }
    }
    
    setupValidation(form) {
        if (!this.options.validateOnInput) return;
        
        form.querySelectorAll('[data-validate]').forEach(field => {
            field.addEventListener('input', () => this.validateField(field));
        });
    }
    
    validateField(field) {
        const rules = field.getAttribute('data-validate').split('|');
        const value = field.value;
        
        for (const rule of rules) {
            const validator = this.validators.get(rule);
            if (validator && !validator(value)) {
                this.showError(field, `${rule} 验证失败`);
                return false;
            }
        }
        
        this.clearError(field);
        return true;
    }
    
    showError(field, message) {
        field.classList.add('error');
        let error = field.parentElement.querySelector('.error-message');
        if (!error) {
            error = document.createElement('div');
            error.className = 'error-message text-red-500 text-sm';
            field.parentElement.appendChild(error);
        }
        error.textContent = message;
    }
    
    clearError(field) {
        field.classList.remove('error');
        const error = field.parentElement.querySelector('.error-message');
        if (error) error.style.display = 'none';
    }
    
    addValidator(name, fn) { this.validators.set(name, fn); }
    
    bindEvents() {
        document.addEventListener('submit', (e) => {
            if (e.target.matches('[data-form-handler]')) {
                e.preventDefault();
                this.handleSubmit(e.target);
            }
        });
    }
    
    async handleSubmit(form) {
        if (!this.validateForm(form)) return;
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        const config = Array.from(this.forms.values()).find(c => c.element === form);
        if (config && config.onSubmit) {
            await config.onSubmit(data);
        }
    }
    
    validateForm(form) {
        const fields = form.querySelectorAll('[data-validate]');
        let valid = true;
        
        fields.forEach(field => {
            if (!this.validateField(field)) valid = false;
        });
        
        return valid;
    }
}

window.FormHandler = FormHandler;
'''.strip(),
            
            "navigation": '''
/**
 * 导航管理器 - SPA路由管理
 */
class NavigationManager {
    constructor(options = {}) {
        this.options = { enableHistory: true, defaultRoute: '/', ...options };
        this.routes = new Map();
        this.currentRoute = null;
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.handleRoute(window.location.pathname || this.options.defaultRoute);
    }
    
    addRoute(path, handler) { this.routes.set(path, handler); }
    
    navigateTo(path) {
        if (this.options.enableHistory) {
            history.pushState({}, '', path);
        }
        this.handleRoute(path);
    }
    
    handleRoute(path) {
        const handler = this.routes.get(path);
        if (handler) {
            this.currentRoute = path;
            handler({ path, query: this.parseQuery() });
        } else {
            this.handleNotFound(path);
        }
    }
    
    handleNotFound(path) {
        const container = document.querySelector('[data-page-container]') || document.body;
        container.innerHTML = `
            <div class="text-center py-16">
                <h1 class="text-4xl mb-4">页面未找到</h1>
                <p class="mb-8">路径 "${path}" 不存在</p>
                <button onclick="history.back()" class="px-4 py-2 bg-blue-500 text-white rounded">
                    返回
                </button>
            </div>
        `;
    }
    
    parseQuery() {
        const params = new URLSearchParams(window.location.search);
        const query = {};
        for (const [key, value] of params) query[key] = value;
        return query;
    }
    
    bindEvents() {
        window.addEventListener('popstate', () => {
            this.handleRoute(window.location.pathname);
        });
        
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]');
            if (link && this.isInternalLink(link.href)) {
                e.preventDefault();
                this.navigateTo(new URL(link.href).pathname);
            }
        });
    }
    
    isInternalLink(href) {
        return href && !href.startsWith('http') && !href.startsWith('#');
    }
}

window.NavigationManager = NavigationManager;
'''.strip(),
            
            "notification": '''
/**
 * 通知系统 - 消息提示管理
 */
class NotificationManager {
    constructor(options = {}) {
        this.options = { position: 'top-right', duration: 3000, ...options };
        this.notifications = [];
        this.container = null;
        this.init();
    }
    
    init() {
        this.createContainer();
        this.injectStyles();
    }
    
    show(message, type = 'info', duration = null) {
        const notification = {
            id: Date.now(),
            message,
            type,
            duration: duration || this.options.duration
        };
        
        this.notifications.push(notification);
        this.render(notification);
        
        if (notification.duration > 0) {
            setTimeout(() => this.remove(notification.id), notification.duration);
        }
        
        return notification.id;
    }
    
    success(message) { return this.show(message, 'success'); }
    error(message) { return this.show(message, 'error', 5000); }
    warning(message) { return this.show(message, 'warning'); }
    
    remove(id) {
        const index = this.notifications.findIndex(n => n.id === id);
        if (index > -1) {
            const notification = this.notifications[index];
            this.notifications.splice(index, 1);
            
            const element = document.getElementById(`notification-${id}`);
            if (element) element.remove();
        }
    }
    
    render(notification) {
        const element = document.createElement('div');
        element.id = `notification-${notification.id}`;
        element.className = `notification notification-${notification.type}`;
        
        const icon = { success: '✓', error: '✕', warning: '⚠', info: 'ℹ' }[notification.type] || 'ℹ';
        
        element.innerHTML = `
            <div class="flex items-center p-4">
                <span class="icon mr-3">${icon}</span>
                <span class="message flex-1">${notification.message}</span>
                <button class="close ml-3" onclick="window.notificationManager.remove(${notification.id})">&times;</button>
            </div>
        `;
        
        this.container.appendChild(element);
        setTimeout(() => element.classList.add('show'), 10);
    }
    
    createContainer() {
        this.container = document.createElement('div');
        this.container.className = `notification-container ${this.options.position}`;
        document.body.appendChild(this.container);
    }
    
    injectStyles() {
        const css = `
            .notification-container { position: fixed; z-index: 9999; }
            .notification-container.top-right { top: 20px; right: 20px; }
            .notification { 
                background: white; border-radius: 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                margin-bottom: 10px; min-width: 300px; opacity: 0; transform: translateX(100%);
                transition: all 0.3s ease;
            }
            .notification.show { opacity: 1; transform: translateX(0); }
            .notification-success { border-left: 4px solid #10b981; }
            .notification-error { border-left: 4px solid #ef4444; }
            .notification-warning { border-left: 4px solid #f59e0b; }
            .notification-info { border-left: 4px solid #3b82f6; }
            .notification .close { background: none; border: none; font-size: 18px; cursor: pointer; }
        `;
        const style = document.createElement('style');
        style.textContent = css;
        document.head.appendChild(style);
    }
}

window.NotificationManager = NotificationManager;
'''.strip(),
            
            "validation": '''
/**
 * 验证管理器 - 通用数据验证
 */
class ValidationManager {
    constructor() {
        this.rules = new Map();
        this.init();
    }
    
    init() {
        // 注册默认规则
        this.addRule('required', (value) => value != null && value.toString().trim() !== '');
        this.addRule('email', (value) => /^[^@]+@[^@]+\\.[^@]+$/.test(value || ''));
        this.addRule('min', (value, param) => (value || '').length >= parseInt(param));
        this.addRule('max', (value, param) => (value || '').length <= parseInt(param));
        this.addRule('numeric', (value) => !isNaN(value) && !isNaN(parseFloat(value)));
        this.addRule('url', (value) => {
            try { return !value || Boolean(new URL(value)); } 
            catch { return false; }
        });
    }
    
    validate(value, rules) {
        const ruleArray = typeof rules === 'string' ? rules.split('|') : rules;
        const errors = [];
        
        for (const rule of ruleArray) {
            const [name, param] = rule.split(':');
            const validator = this.rules.get(name.trim());
            
            if (validator && !validator(value, param)) {
                errors.push({ rule: name, message: this.getMessage(name, param) });
            }
        }
        
        return { valid: errors.length === 0, errors };
    }
    
    validateObject(data, schema) {
        const results = {};
        let allValid = true;
        
        Object.entries(schema).forEach(([key, rules]) => {
            const result = this.validate(data[key], rules);
            results[key] = result;
            if (!result.valid) allValid = false;
        });
        
        return { valid: allValid, results };
    }
    
    addRule(name, validator) { this.rules.set(name, validator); }
    
    getMessage(rule, param) {
        const messages = {
            required: '此字段为必填项',
            email: '请输入有效的邮箱地址',
            min: `至少需要 ${param} 个字符`,
            max: `最多允许 ${param} 个字符`,
            numeric: '请输入有效的数字',
            url: '请输入有效的URL'
        };
        return messages[rule] || `${rule} 验证失败`;
    }
}

window.ValidationManager = ValidationManager;
'''.strip(),
            
            "event_manager": '''
/**
 * 事件管理器 - 自定义事件系统
 */
class EventManager {
    constructor() {
        this.listeners = new Map();
        this.delegated = new Map();
        this.init();
    }
    
    init() { this.setupDelegation(); }
    
    on(event, handler) {
        if (!this.listeners.has(event)) this.listeners.set(event, []);
        const id = Date.now() + Math.random();
        this.listeners.get(event).push({ handler, id });
        return id;
    }
    
    once(event, handler) {
        const id = this.on(event, (data) => {
            handler(data);
            this.off(event, id);
        });
        return id;
    }
    
    off(event, id) {
        if (this.listeners.has(event)) {
            const listeners = this.listeners.get(event);
            const index = listeners.findIndex(l => l.id === id);
            if (index > -1) listeners.splice(index, 1);
        }
    }
    
    emit(event, data = null) {
        if (this.listeners.has(event)) {
            this.listeners.get(event).forEach(({ handler }) => {
                try { handler(data); } 
                catch (error) { console.error('事件处理错误:', error); }
            });
        }
    }
    
    delegate(selector, event, handler) {
        const id = Date.now() + Math.random();
        if (!this.delegated.has(event)) {
            this.delegated.set(event, []);
            document.addEventListener(event, (e) => this.handleDelegated(event, e));
        }
        
        this.delegated.get(event).push({ selector, handler, id });
        return id;
    }
    
    handleDelegated(eventType, nativeEvent) {
        const delegates = this.delegated.get(eventType);
        if (!delegates) return;
        
        delegates.forEach(({ selector, handler }) => {
            const element = nativeEvent.target.closest(selector);
            if (element) {
                try { handler(nativeEvent, element); } 
                catch (error) { console.error('委托事件错误:', error); }
            }
        });
    }
    
    setupDelegation() {
        // 预设常用委托
        this.delegate('[data-click]', 'click', (e, el) => {
            const action = el.getAttribute('data-click');
            this.emit('action:' + action, { element: el, event: e });
        });
    }
    
    clear() { 
        this.listeners.clear(); 
        this.delegated.clear(); 
    }
}

window.EventManager = EventManager;
'''.strip()
        }
        
        return templates.get(template_type, f'// {template_type} 模板')
    
    def _create_integrator(self):
        """创建集成器"""
        content = '''
/**
 * 业务逻辑集成器 - 统一初始化管理
 */
class BusinessIntegrator {
    constructor() {
        this.modules = {};
        this.loadOrder = ['notification', 'data_storage', 'validation', 'event_manager', 'form_handler', 'navigation', 'base_framework'];
        this.init();
    }
    
    async init() {
        console.log('🚀 初始化业务模块...');
        
        for (const name of this.loadOrder) {
            await this.loadModule(name);
        }
        
        console.log('✅ 模块初始化完成');
    }
    
    async loadModule(name) {
        try {
            const className = name.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join('');
            const ModuleClass = window[className];
            
            if (ModuleClass) {
                this.modules[name] = new ModuleClass();
                console.log(`📦 ${name} 模块已加载`);
            }
        } catch (error) {
            console.warn(`模块 ${name} 加载失败:`, error);
        }
    }
    
    get(name) { return this.modules[name]; }
    list() { return Object.keys(this.modules); }
}

document.addEventListener('DOMContentLoaded', () => {
    window.businessIntegrator = new BusinessIntegrator();
});
'''.strip()
        
        file_path = self.business_dir / "integrator.js"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_config(self):
        """创建配置文件"""
        config = {
            "version": "1.0",
            "description": "通用业务逻辑模块配置",
            "modules": {name: {"enabled": True, "description": desc} for name, desc in self.templates.items()}
        }
        
        file_path = self.business_dir / "config.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def _get_example(self, template_type: str) -> str:
        """获取使用示例"""
        examples = {
            "base_framework": "const app = new AppFramework({ debug: true }); app.loadModule('my-module');",
            "data_storage": "const storage = new DataStorage(); storage.set('user', {name: 'John'});",
            "form_handler": "const forms = new FormHandler(); forms.register('#myForm');",
            "navigation": "const nav = new NavigationManager(); nav.addRoute('/home', showHome);",
            "notification": "const notify = new NotificationManager(); notify.success('成功！');",
            "validation": "const v = new ValidationManager(); v.validate('test@email.com', 'required|email');",
            "event_manager": "const events = new EventManager(); events.on('user:login', handleLogin);"
        }
        return examples.get(template_type, "// 使用示例")


def main():
    """命令行界面"""
    import argparse
    
    parser = argparse.ArgumentParser(description="通用业务逻辑生成器")
    parser.add_argument("project_path", help="项目路径")
    parser.add_argument("--types", "-t", help="模板类型（逗号分隔）")
    parser.add_argument("--list", "-l", action='store_true', help="列出所有模板")
    
    args = parser.parse_args()
    generator = BusinessLogicGenerator(args.project_path)
    
    if args.list:
        print("📋 可用模板:")
        for name, desc in generator.templates.items():
            print(f"  • {name}: {desc}")
        return
    
    types = [t.strip() for t in args.types.split(',')] if args.types else None
    result = generator.generate_templates(types)
    
    print(f"\n✅ 完成！文件位置: {generator.business_dir}")


if __name__ == "__main__":
    main()