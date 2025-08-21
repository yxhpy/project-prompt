#!/usr/bin/env python3
"""
交互功能生成器
为现有原型快速添加常用交互功能
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional

class InteractionGenerator:
    """交互功能生成器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.interactive_dir = self.project_root / "interactive"
        self.interactive_dir.mkdir(exist_ok=True)
        
        # 创建子目录
        (self.interactive_dir / "js").mkdir(exist_ok=True)
        (self.interactive_dir / "css").mkdir(exist_ok=True)
    
    def generate_navigation_system(self) -> str:
        """生成导航系统"""
        js_content = '''
/**
 * 智能导航系统
 * 支持页面切换、面包屑导航、历史记录管理
 */
class SmartNavigation {
    constructor() {
        this.currentPage = null;
        this.navigationHistory = [];
        this.maxHistoryLength = 10;
        this.init();
    }
    
    init() {
        this.bindNavigationEvents();
        this.initializeCurrentPage();
        this.generateBreadcrumb();
    }
    
    bindNavigationEvents() {
        // 绑定所有导航链接
        document.querySelectorAll('[data-nav]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = e.target.getAttribute('data-nav');
                const title = e.target.textContent.trim();
                this.navigateTo(target, title);
            });
        });
        
        // 绑定返回按钮
        document.querySelectorAll('[data-nav-back]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.goBack();
            });
        });
    }
    
    navigateTo(pageId, title = '') {
        const targetPage = document.getElementById(pageId);
        if (!targetPage) {
            console.warn(`页面不存在: ${pageId}`);
            return;
        }
        
        // 记录导航历史
        if (this.currentPage) {
            this.addToHistory(this.currentPage.id, this.getCurrentPageTitle());
        }
        
        // 执行页面切换
        this.hideCurrentPage();
        this.showPage(targetPage, title);
        
        // 更新面包屑
        this.updateBreadcrumb();
        
        // 触发自定义事件
        this.triggerNavigationEvent(pageId, title);
    }
    
    hideCurrentPage() {
        if (this.currentPage) {
            this.currentPage.classList.add('page-hidden');
            this.currentPage.classList.remove('page-visible');
        }
    }
    
    showPage(page, title = '') {
        page.classList.remove('page-hidden');
        page.classList.add('page-visible');
        this.currentPage = page;
        
        // 更新页面标题
        if (title) {
            document.title = `${title} - 产品原型`;
        }
        
        // 滚动到顶部
        page.scrollTop = 0;
    }
    
    goBack() {
        if (this.navigationHistory.length === 0) {
            console.warn('没有可返回的页面');
            return;
        }
        
        const lastPage = this.navigationHistory.pop();
        const targetPage = document.getElementById(lastPage.pageId);
        
        if (targetPage) {
            this.hideCurrentPage();
            this.showPage(targetPage, lastPage.title);
            this.updateBreadcrumb();
        }
    }
    
    addToHistory(pageId, title) {
        this.navigationHistory.push({ pageId, title, timestamp: Date.now() });
        
        // 限制历史记录长度
        if (this.navigationHistory.length > this.maxHistoryLength) {
            this.navigationHistory.shift();
        }
    }
    
    initializeCurrentPage() {
        // 查找当前显示的页面
        const visiblePage = document.querySelector('.page-visible') || 
                           document.querySelector('[data-page]:not(.page-hidden)');
        
        if (visiblePage) {
            this.currentPage = visiblePage;
        }
    }
    
    getCurrentPageTitle() {
        if (!this.currentPage) return '';
        
        const titleElement = this.currentPage.querySelector('h1, h2, [data-page-title]');
        return titleElement ? titleElement.textContent.trim() : this.currentPage.id;
    }
    
    generateBreadcrumb() {
        const breadcrumbContainer = document.getElementById('breadcrumb');
        if (!breadcrumbContainer) return;
        
        this.updateBreadcrumb();
    }
    
    updateBreadcrumb() {
        const breadcrumbContainer = document.getElementById('breadcrumb');
        if (!breadcrumbContainer) return;
        
        let breadcrumbHTML = '<a href="#" data-nav="home">首页</a>';
        
        // 添加历史路径
        this.navigationHistory.slice(-3).forEach(item => {
            breadcrumbHTML += ` <span class="breadcrumb-separator">></span> `;
            breadcrumbHTML += `<a href="#" data-nav="${item.pageId}">${item.title}</a>`;
        });
        
        // 添加当前页面
        if (this.currentPage) {
            breadcrumbHTML += ` <span class="breadcrumb-separator">></span> `;
            breadcrumbHTML += `<span class="current-page">${this.getCurrentPageTitle()}</span>`;
        }
        
        breadcrumbContainer.innerHTML = breadcrumbHTML;
    }
    
    triggerNavigationEvent(pageId, title) {
        const event = new CustomEvent('pageNavigated', {
            detail: { pageId, title, timestamp: Date.now() }
        });
        document.dispatchEvent(event);
    }
}

// 页面切换动画CSS
const navigationCSS = `
.page-visible {
    display: block;
    opacity: 1;
    transform: translateX(0);
    transition: all 0.3s ease-in-out;
}

.page-hidden {
    display: none;
    opacity: 0;
    transform: translateX(-100%);
    transition: all 0.3s ease-in-out;
}

.breadcrumb-separator {
    margin: 0 8px;
    color: #666;
}

.current-page {
    color: #333;
    font-weight: bold;
}
`;

// 注入CSS
const style = document.createElement('style');
style.textContent = navigationCSS;
document.head.appendChild(style);

// 初始化导航系统
document.addEventListener('DOMContentLoaded', () => {
    window.smartNavigation = new SmartNavigation();
});
'''
        
        js_file = self.interactive_dir / "js" / "navigation.js"
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        return str(js_file)
    
    def generate_form_enhancements(self) -> str:
        """生成表单增强功能"""
        js_content = '''
/**
 * 智能表单增强系统
 * 提供实时验证、自动保存、智能提示等功能
 */
class FormEnhancer {
    constructor() {
        this.autoSaveInterval = 30000; // 30秒自动保存
        this.validationRules = {};
        this.autoSaveTimers = new Map();
        this.init();
    }
    
    init() {
        this.enhanceAllForms();
        this.bindGlobalEvents();
    }
    
    enhanceAllForms() {
        document.querySelectorAll('form').forEach(form => {
            this.enhanceForm(form);
        });
    }
    
    enhanceForm(form) {
        // 添加表单标识
        if (!form.id) {
            form.id = `form_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        }
        
        // 增强所有表单字段
        form.querySelectorAll('input, textarea, select').forEach(field => {
            this.enhanceField(field);
        });
        
        // 添加表单提交处理
        form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        
        // 启用自动保存
        this.enableAutoSave(form);
    }
    
    enhanceField(field) {
        // 添加实时验证
        field.addEventListener('blur', () => this.validateField(field));
        field.addEventListener('input', () => this.handleFieldInput(field));
        
        // 添加字段标识
        if (!field.id) {
            field.id = `field_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        }
        
        // 创建错误提示容器
        this.createErrorContainer(field);
        
        // 添加字符计数（针对文本区域）
        if (field.tagName === 'TEXTAREA' && field.maxLength) {
            this.addCharacterCounter(field);
        }
    }
    
    validateField(field) {
        const value = field.value.trim();
        const fieldType = field.type;
        const isRequired = field.required;
        
        let isValid = true;
        let message = '';
        
        // 必填验证
        if (isRequired && !value) {
            isValid = false;
            message = '此字段为必填项';
        }
        // 邮箱验证
        else if (fieldType === 'email' && value && !this.isValidEmail(value)) {
            isValid = false;
            message = '请输入有效的邮箱地址';
        }
        // 电话号码验证
        else if (fieldType === 'tel' && value && !this.isValidPhone(value)) {
            isValid = false;
            message = '请输入有效的手机号码';
        }
        // 自定义验证规则
        else if (this.validationRules[field.id]) {
            const customResult = this.validationRules[field.id](value);
            if (!customResult.isValid) {
                isValid = false;
                message = customResult.message;
            }
        }
        
        this.showValidationResult(field, isValid, message);
        return isValid;
    }
    
    handleFieldInput(field) {
        // 清除错误状态
        this.clearFieldError(field);
        
        // 更新字符计数
        this.updateCharacterCounter(field);
        
        // 触发自动保存
        this.triggerAutoSave(field.form);
    }
    
    showValidationResult(field, isValid, message) {
        const errorContainer = this.getErrorContainer(field);
        
        if (isValid) {
            field.classList.remove('border-red-500', 'border-red-300');
            field.classList.add('border-green-500');
            errorContainer.textContent = '';
            errorContainer.classList.add('hidden');
        } else {
            field.classList.remove('border-green-500');
            field.classList.add('border-red-500');
            errorContainer.textContent = message;
            errorContainer.classList.remove('hidden');
        }
    }
    
    clearFieldError(field) {
        field.classList.remove('border-red-500', 'border-red-300');
        const errorContainer = this.getErrorContainer(field);
        errorContainer.classList.add('hidden');
    }
    
    createErrorContainer(field) {
        const existingError = this.getErrorContainer(field);
        if (existingError) return;
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error text-red-500 text-sm mt-1 hidden';
        errorDiv.id = `error_${field.id}`;
        
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    }
    
    getErrorContainer(field) {
        return document.getElementById(`error_${field.id}`);
    }
    
    addCharacterCounter(field) {
        const counter = document.createElement('div');
        counter.className = 'character-counter text-gray-500 text-sm mt-1';
        counter.id = `counter_${field.id}`;
        
        field.parentNode.insertBefore(counter, field.nextSibling);
        this.updateCharacterCounter(field);
    }
    
    updateCharacterCounter(field) {
        const counter = document.getElementById(`counter_${field.id}`);
        if (!counter || !field.maxLength) return;
        
        const current = field.value.length;
        const max = field.maxLength;
        const remaining = max - current;
        
        counter.textContent = `${current}/${max} 字符`;
        
        if (remaining < 10) {
            counter.className = 'character-counter text-red-500 text-sm mt-1';
        } else if (remaining < 50) {
            counter.className = 'character-counter text-yellow-500 text-sm mt-1';
        } else {
            counter.className = 'character-counter text-gray-500 text-sm mt-1';
        }
    }
    
    enableAutoSave(form) {
        const formId = form.id;
        
        // 清除之前的定时器
        if (this.autoSaveTimers.has(formId)) {
            clearTimeout(this.autoSaveTimers.get(formId));
        }
        
        // 设置新的自动保存定时器
        const timer = setTimeout(() => {
            this.autoSaveForm(form);
        }, this.autoSaveInterval);
        
        this.autoSaveTimers.set(formId, timer);
    }
    
    triggerAutoSave(form) {
        if (!form) return;
        
        // 重置自动保存定时器
        this.enableAutoSave(form);
    }
    
    autoSaveForm(form) {
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        // 保存到本地存储
        localStorage.setItem(`autosave_${form.id}`, JSON.stringify({
            data: data,
            timestamp: Date.now()
        }));
        
        console.log(`表单 ${form.id} 已自动保存`);
    }
    
    loadAutoSavedData(form) {
        const saved = localStorage.getItem(`autosave_${form.id}`);
        if (!saved) return false;
        
        try {
            const { data, timestamp } = JSON.parse(saved);
            
            // 检查数据是否过期（24小时）
            if (Date.now() - timestamp > 24 * 60 * 60 * 1000) {
                localStorage.removeItem(`autosave_${form.id}`);
                return false;
            }
            
            // 恢复表单数据
            Object.keys(data).forEach(name => {
                const field = form.querySelector(`[name="${name}"]`);
                if (field) {
                    field.value = data[name];
                }
            });
            
            return true;
        } catch (error) {
            console.error('加载自动保存数据失败:', error);
            return false;
        }
    }
    
    handleFormSubmit(event) {
        const form = event.target;
        let isFormValid = true;
        
        // 验证所有字段
        form.querySelectorAll('input, textarea, select').forEach(field => {
            if (!this.validateField(field)) {
                isFormValid = false;
            }
        });
        
        if (!isFormValid) {
            event.preventDefault();
            this.showFormError(form, '请修正表单中的错误后重试');
            return false;
        }
        
        // 清除自动保存数据
        localStorage.removeItem(`autosave_${form.id}`);
        
        return true;
    }
    
    showFormError(form, message) {
        // 显示表单级错误信息
        let errorDiv = form.querySelector('.form-error');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'form-error bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4';
            form.insertBefore(errorDiv, form.firstChild);
        }
        
        errorDiv.textContent = message;
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    bindGlobalEvents() {
        // 页面卸载前保存所有表单
        window.addEventListener('beforeunload', () => {
            document.querySelectorAll('form').forEach(form => {
                this.autoSaveForm(form);
            });
        });
    }
    
    // 工具方法
    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
    
    isValidPhone(phone) {
        return /^1[3-9]\d{9}$/.test(phone.replace(/\D/g, ''));
    }
    
    // 添加自定义验证规则
    addValidationRule(fieldId, validator) {
        this.validationRules[fieldId] = validator;
    }
}

// 初始化表单增强器
document.addEventListener('DOMContentLoaded', () => {
    window.formEnhancer = new FormEnhancer();
});
'''
        
        js_file = self.interactive_dir / "js" / "form-enhancer.js"
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        return str(js_file)
    
    def generate_mobile_enhancements(self) -> str:
        """生成移动端交互增强"""
        js_content = '''
/**
 * 移动端交互增强系统
 * 优化触摸交互、手势支持、响应式行为
 */
class MobileEnhancer {
    constructor() {
        this.touchStartY = 0;
        this.touchStartX = 0;
        this.isScrolling = false;
        this.swipeThreshold = 50;
        this.init();
    }
    
    init() {
        this.detectMobileDevice();
        this.optimizeTouchTargets();
        this.enableSwipeGestures();
        this.improveScrolling();
        this.handleOrientationChange();
    }
    
    detectMobileDevice() {
        const isMobile = /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        document.body.classList.toggle('mobile-device', isMobile);
        
        if (isMobile) {
            this.enableMobileOptimizations();
        }
    }
    
    enableMobileOptimizations() {
        // 禁用双击缩放
        document.addEventListener('touchstart', (e) => {
            if (e.touches.length > 1) {
                e.preventDefault();
            }
        });
        
        let lastTouchEnd = 0;
        document.addEventListener('touchend', (e) => {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                e.preventDefault();
            }
            lastTouchEnd = now;
        }, false);
        
        // 优化点击延迟
        document.addEventListener('touchstart', () => {}, true);
    }
    
    optimizeTouchTargets() {
        // 确保触摸目标足够大
        const minTouchSize = 44; // 44px最小触摸目标
        
        document.querySelectorAll('button, a, input, [data-clickable]').forEach(element => {
            const rect = element.getBoundingClientRect();
            
            if (rect.width < minTouchSize || rect.height < minTouchSize) {
                element.style.minWidth = `${minTouchSize}px`;
                element.style.minHeight = `${minTouchSize}px`;
                element.style.display = 'inline-flex';
                element.style.alignItems = 'center';
                element.style.justifyContent = 'center';
            }
        });
    }
    
    enableSwipeGestures() {
        document.addEventListener('touchstart', (e) => {
            this.touchStartY = e.touches[0].clientY;
            this.touchStartX = e.touches[0].clientX;
            this.isScrolling = false;
        });
        
        document.addEventListener('touchmove', (e) => {
            if (!this.touchStartY || !this.touchStartX) return;
            
            const touchY = e.touches[0].clientY;
            const touchX = e.touches[0].clientX;
            
            const diffY = Math.abs(this.touchStartY - touchY);
            const diffX = Math.abs(this.touchStartX - touchX);
            
            if (diffY > diffX) {
                this.isScrolling = true;
            }
        });
        
        document.addEventListener('touchend', (e) => {
            if (!this.touchStartY || !this.touchStartX || this.isScrolling) {
                this.touchStartY = 0;
                this.touchStartX = 0;
                return;
            }
            
            const touchEndY = e.changedTouches[0].clientY;
            const touchEndX = e.changedTouches[0].clientX;
            
            const diffY = this.touchStartY - touchEndY;
            const diffX = this.touchStartX - touchEndX;
            
            // 左右滑动
            if (Math.abs(diffX) > this.swipeThreshold && Math.abs(diffY) < this.swipeThreshold) {
                if (diffX > 0) {
                    this.handleSwipeLeft();
                } else {
                    this.handleSwipeRight();
                }
            }
            
            // 上下滑动
            if (Math.abs(diffY) > this.swipeThreshold && Math.abs(diffX) < this.swipeThreshold) {
                if (diffY > 0) {
                    this.handleSwipeUp();
                } else {
                    this.handleSwipeDown();
                }
            }
            
            this.touchStartY = 0;
            this.touchStartX = 0;
        });
    }
    
    handleSwipeLeft() {
        // 左滑事件 - 可以用于返回或显示侧边栏
        const event = new CustomEvent('swipeLeft');
        document.dispatchEvent(event);
    }
    
    handleSwipeRight() {
        // 右滑事件 - 可以用于前进或隐藏侧边栏
        const event = new CustomEvent('swipeRight');
        document.dispatchEvent(event);
    }
    
    handleSwipeUp() {
        // 上滑事件 - 可以用于刷新
        const event = new CustomEvent('swipeUp');
        document.dispatchEvent(event);
    }
    
    handleSwipeDown() {
        // 下滑事件 - 可以用于关闭
        const event = new CustomEvent('swipeDown');
        document.dispatchEvent(event);
    }
    
    improveScrolling() {
        // 启用平滑滚动
        document.documentElement.style.scrollBehavior = 'smooth';
        
        // 优化滚动性能
        document.addEventListener('scroll', this.throttle(() => {
            // 滚动时的优化处理
            this.handleScroll();
        }, 16)); // 60fps
    }
    
    handleScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // 滚动时隐藏/显示元素
        document.querySelectorAll('[data-scroll-hide]').forEach(element => {
            if (scrollTop > 100) {
                element.classList.add('scroll-hidden');
            } else {
                element.classList.remove('scroll-hidden');
            }
        });
        
        // 触发自定义滚动事件
        const event = new CustomEvent('optimizedScroll', {
            detail: { scrollTop }
        });
        document.dispatchEvent(event);
    }
    
    handleOrientationChange() {
        window.addEventListener('orientationchange', () => {
            // 延迟处理方向改变，等待布局稳定
            setTimeout(() => {
                this.adjustForOrientation();
            }, 100);
        });
    }
    
    adjustForOrientation() {
        const isLandscape = window.orientation === 90 || window.orientation === -90;
        document.body.classList.toggle('landscape', isLandscape);
        document.body.classList.toggle('portrait', !isLandscape);
        
        // 重新计算布局
        window.dispatchEvent(new Event('resize'));
    }
    
    // 工具方法：节流函数
    throttle(func, delay) {
        let timeoutId;
        let lastExecTime = 0;
        
        return function (...args) {
            const currentTime = Date.now();
            
            if (currentTime - lastExecTime > delay) {
                func.apply(this, args);
                lastExecTime = currentTime;
            } else {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => {
                    func.apply(this, args);
                    lastExecTime = Date.now();
                }, delay - (currentTime - lastExecTime));
            }
        };
    }
}

// 移动端优化CSS
const mobileCSS = `
.mobile-device {
    -webkit-text-size-adjust: 100%;
    -webkit-tap-highlight-color: transparent;
}

.scroll-hidden {
    transform: translateY(-100%);
    transition: transform 0.3s ease-in-out;
}

.landscape .iphone-frame {
    transform: rotate(90deg) scale(0.7);
    transform-origin: center center;
}

@media (max-width: 480px) {
    .mobile-optimized {
        padding: 8px;
        font-size: 16px; /* 防止iOS缩放 */
    }
    
    input, textarea, select {
        font-size: 16px; /* 防止iOS缩放 */
    }
}
`;

// 注入移动端优化CSS
const style = document.createElement('style');
style.textContent = mobileCSS;
document.head.appendChild(style);

// 初始化移动端增强器
document.addEventListener('DOMContentLoaded', () => {
    window.mobileEnhancer = new MobileEnhancer();
});
'''
        
        js_file = self.interactive_dir / "js" / "mobile-enhancer.js"
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        return str(js_file)
    
    def generate_integration_script(self) -> str:
        """生成集成脚本，用于在现有页面中引入交互功能"""
        js_content = '''
/**
 * 交互功能集成脚本
 * 自动检测并引入所需的交互功能模块
 */
class InteractionIntegrator {
    constructor() {
        this.scriptsLoaded = new Set();
        this.requiredScripts = [
            'interactive/js/navigation.js',
            'interactive/js/form-enhancer.js',
            'interactive/js/mobile-enhancer.js'
        ];
        this.init();
    }
    
    init() {
        this.loadRequiredScripts();
        this.injectNavigationElements();
        this.enhanceExistingElements();
    }
    
    async loadRequiredScripts() {
        for (const scriptPath of this.requiredScripts) {
            await this.loadScript(scriptPath);
        }
        
        console.log('✅ 所有交互功能模块已加载');
    }
    
    loadScript(src) {
        return new Promise((resolve, reject) => {
            if (this.scriptsLoaded.has(src)) {
                resolve();
                return;
            }
            
            const script = document.createElement('script');
            script.src = src;
            script.onload = () => {
                this.scriptsLoaded.add(src);
                resolve();
            };
            script.onerror = () => {
                console.warn(`无法加载脚本: ${src}`);
                resolve(); // 不阻断其他脚本加载
            };
            
            document.head.appendChild(script);
        });
    }
    
    injectNavigationElements() {
        // 添加面包屑导航容器
        if (!document.getElementById('breadcrumb')) {
            const breadcrumb = document.createElement('nav');
            breadcrumb.id = 'breadcrumb';
            breadcrumb.className = 'breadcrumb p-2 text-sm text-gray-600';
            
            const pageContent = document.querySelector('.page-content');
            if (pageContent) {
                pageContent.insertBefore(breadcrumb, pageContent.firstChild);
            }
        }
        
        // 为现有链接添加导航属性
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            const href = link.getAttribute('href').substring(1);
            if (href && document.getElementById(href)) {
                link.setAttribute('data-nav', href);
            }
        });
    }
    
    enhanceExistingElements() {
        // 为按钮添加点击效果
        document.querySelectorAll('button, .btn').forEach(button => {
            if (!button.classList.contains('enhanced')) {
                this.addRippleEffect(button);
                button.classList.add('enhanced');
            }
        });
        
        // 为输入框添加聚焦效果
        document.querySelectorAll('input, textarea').forEach(input => {
            if (!input.classList.contains('enhanced')) {
                this.addFocusEffect(input);
                input.classList.add('enhanced');
            }
        });
        
        // 为页面添加切换属性
        document.querySelectorAll('[id]').forEach(element => {
            if (element.offsetParent === null && element.id) {
                element.setAttribute('data-page', element.id);
                element.classList.add('page-hidden');
            }
        });
        
        // 显示第一个页面
        const firstPage = document.querySelector('[data-page]');
        if (firstPage) {
            firstPage.classList.remove('page-hidden');
            firstPage.classList.add('page-visible');
        }
    }
    
    addRippleEffect(element) {
        element.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s linear;
                pointer-events: none;
            `;
            
            // 确保父元素有相对定位
            if (getComputedStyle(this).position === 'static') {
                this.style.position = 'relative';
            }
            this.style.overflow = 'hidden';
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    }
    
    addFocusEffect(input) {
        const wrapper = document.createElement('div');
        wrapper.className = 'input-wrapper';
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);
        
        input.addEventListener('focus', () => {
            wrapper.classList.add('focused');
        });
        
        input.addEventListener('blur', () => {
            wrapper.classList.remove('focused');
        });
    }
}

// 添加必要的CSS动画
const interactionCSS = `
@keyframes ripple {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

.input-wrapper {
    position: relative;
    transition: all 0.3s ease;
}

.input-wrapper.focused {
    transform: scale(1.02);
}

.enhanced {
    transition: all 0.2s ease;
}

.enhanced:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.enhanced:active {
    transform: translateY(0);
}
`;

// 注入CSS
const style = document.createElement('style');
style.textContent = interactionCSS;
document.head.appendChild(style);

// 自动初始化
document.addEventListener('DOMContentLoaded', () => {
    window.interactionIntegrator = new InteractionIntegrator();
});
'''
        
        js_file = self.interactive_dir / "js" / "integration.js"
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        return str(js_file)
    
    def create_sample_enhanced_page(self) -> str:
        """创建示例增强页面"""
        html_content = '''<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>交互增强示例页面</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="../style.css">
</head>
<body class="bg-gray-100">
    <div class="iphone-frame">
        <div class="iphone-screen">
            <!-- 状态栏 -->
            <div class="status-bar">
                <div class="status-left">
                    <span class="carrier">中国移动</span>
                    <i class="fas fa-wifi"></i>
                </div>
                <div class="status-center">
                    <span class="time">9:41</span>
                </div>
                <div class="status-right">
                    <span class="battery">100%</span>
                </div>
            </div>
            
            <!-- 页面内容 -->
            <div class="page-content">
                <!-- 面包屑导航 -->
                <nav id="breadcrumb" class="p-4 text-sm text-gray-600 border-b"></nav>
                
                <!-- 首页 -->
                <div id="home" data-page="home" class="p-4">
                    <h1 class="text-xl font-bold mb-4">交互增强示例</h1>
                    
                    <div class="space-y-4">
                        <div class="bg-white p-4 rounded border">
                            <h2 class="font-semibold mb-2">导航测试</h2>
                            <button data-nav="form-page" class="bg-blue-500 text-white px-4 py-2 rounded mr-2">
                                前往表单页面
                            </button>
                            <button data-nav="list-page" class="bg-green-500 text-white px-4 py-2 rounded">
                                前往列表页面
                            </button>
                        </div>
                        
                        <div class="bg-white p-4 rounded border">
                            <h2 class="font-semibold mb-2">手势测试</h2>
                            <p class="text-gray-600">在移动设备上尝试左右滑动</p>
                            <div id="swipe-result" class="mt-2 p-2 bg-gray-100 rounded text-sm"></div>
                        </div>
                    </div>
                </div>
                
                <!-- 表单页面 -->
                <div id="form-page" data-page="form-page" class="p-4 page-hidden">
                    <div class="flex items-center mb-4">
                        <button data-nav-back class="mr-2 text-gray-600">← 返回</button>
                        <h1 class="text-xl font-bold">表单增强示例</h1>
                    </div>
                    
                    <form class="bg-white p-4 rounded border space-y-4">
                        <div>
                            <label class="block text-sm font-medium mb-1">姓名 *</label>
                            <input type="text" name="name" required 
                                   class="w-full border border-gray-300 rounded px-3 py-2">
                            <div class="field-error"></div>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium mb-1">邮箱 *</label>
                            <input type="email" name="email" required 
                                   class="w-full border border-gray-300 rounded px-3 py-2">
                            <div class="field-error"></div>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium mb-1">手机号码</label>
                            <input type="tel" name="phone" 
                                   class="w-full border border-gray-300 rounded px-3 py-2">
                            <div class="field-error"></div>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium mb-1">备注</label>
                            <textarea name="note" maxlength="200" rows="3"
                                      class="w-full border border-gray-300 rounded px-3 py-2"></textarea>
                        </div>
                        
                        <button type="submit" class="bg-blue-500 text-white px-6 py-2 rounded">
                            提交表单
                        </button>
                    </form>
                </div>
                
                <!-- 列表页面 -->
                <div id="list-page" data-page="list-page" class="p-4 page-hidden">
                    <div class="flex items-center mb-4">
                        <button data-nav-back class="mr-2 text-gray-600">← 返回</button>
                        <h1 class="text-xl font-bold">列表示例</h1>
                    </div>
                    
                    <div class="space-y-2">
                        <div class="bg-white p-3 rounded border" data-clickable>
                            <h3 class="font-medium">列表项 1</h3>
                            <p class="text-sm text-gray-600">这是一个可点击的列表项</p>
                        </div>
                        <div class="bg-white p-3 rounded border" data-clickable>
                            <h3 class="font-medium">列表项 2</h3>
                            <p class="text-sm text-gray-600">包含更多交互功能</p>
                        </div>
                        <div class="bg-white p-3 rounded border" data-clickable>
                            <h3 class="font-medium">列表项 3</h3>
                            <p class="text-sm text-gray-600">优化了触摸体验</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 加载交互功能 -->
    <script src="interactive/js/integration.js"></script>
    
    <script>
        // 手势事件监听示例
        document.addEventListener('swipeLeft', () => {
            document.getElementById('swipe-result').textContent = '检测到左滑手势';
        });
        
        document.addEventListener('swipeRight', () => {
            document.getElementById('swipe-result').textContent = '检测到右滑手势';
        });
        
        // 页面导航事件监听
        document.addEventListener('pageNavigated', (e) => {
            console.log('导航到页面:', e.detail);
        });
    </script>
</body>
</html>'''
        
        html_file = self.interactive_dir / "sample-enhanced.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_file)
    
    def generate_all_interactions(self) -> Dict[str, str]:
        """生成所有交互功能文件"""
        generated_files = {}
        
        print("🚀 开始生成交互功能文件...")
        
        generated_files['navigation'] = self.generate_navigation_system()
        print("✅ 导航系统已生成")
        
        generated_files['forms'] = self.generate_form_enhancements()
        print("✅ 表单增强已生成")
        
        generated_files['mobile'] = self.generate_mobile_enhancements()
        print("✅ 移动端优化已生成")
        
        generated_files['integration'] = self.generate_integration_script()
        print("✅ 集成脚本已生成")
        
        generated_files['sample'] = self.create_sample_enhanced_page()
        print("✅ 示例页面已生成")
        
        print(f"\n🎉 所有交互功能文件已生成到: {self.interactive_dir}")
        return generated_files


def main():
    """命令行界面"""
    import argparse
    
    parser = argparse.ArgumentParser(description="交互功能生成器")
    parser.add_argument("project_path", help="项目路径")
    parser.add_argument("--type", choices=['all', 'navigation', 'forms', 'mobile', 'integration'], 
                       default='all', help="生成类型")
    
    args = parser.parse_args()
    
    generator = InteractionGenerator(args.project_path)
    
    if args.type == 'all':
        generator.generate_all_interactions()
    elif args.type == 'navigation':
        file_path = generator.generate_navigation_system()
        print(f"✅ 导航系统已生成: {file_path}")
    elif args.type == 'forms':
        file_path = generator.generate_form_enhancements()
        print(f"✅ 表单增强已生成: {file_path}")
    elif args.type == 'mobile':
        file_path = generator.generate_mobile_enhancements()
        print(f"✅ 移动端优化已生成: {file_path}")
    elif args.type == 'integration':
        file_path = generator.generate_integration_script()
        print(f"✅ 集成脚本已生成: {file_path}")


if __name__ == "__main__":
    main()