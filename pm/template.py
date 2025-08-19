import os
import sys
import json
import argparse
from pathlib import Path

index_html = '''
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <title>原型导航</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="style.css">
  <script>
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
  </script>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; display: flex; flex-direction: column; height: 100vh; }
    .progress-bar { height: 4px; background: #f0f0f0; position: relative; }
    .progress-fill { height: 100%; background: #4CAF50; transition: width 0.3s ease; }
    .progress-text { position: absolute; top: -25px; right: 10px; font-size: 12px; color: #666; }
    .main-container { display: flex; flex: 1; }
    .sidebar { width: 280px; background: #f8f8f8; border-right: 1px solid #ccc; overflow-y: auto; padding: 10px; display: flex; flex-direction: column; }
    .content { flex: 1; }
    iframe { width: 100%; height: 100%; border: none; }
    ul { list-style: none; padding-left: 15px; }
    li { cursor: pointer; margin: 5px 0; position: relative; }
    li span { font-weight: bold; }
    .nested { display: none; }
    .active { display: block; }
    .completed { color: #4CAF50; }
    .completed::after { content: ' ✅'; }
    .search-box { margin-bottom: 10px; padding: 5px; border: 1px solid #ccc; border-radius: 5px; }
    .search-results { list-style: none; margin: 5px 0; padding: 0; max-height: 200px; overflow-y: auto; border-top: 1px solid #ddd; }
    .search-results li { padding: 5px; cursor: pointer; }
    .search-results li:hover { background: #eee; }
  </style>
</head>
<body>
  <div class="fixed top-0 left-0 w-full h-1 bg-gray-200 z-50">
    <div class="h-full bg-green-500 transition-all duration-300 ease-out" id="progressFill" style="width: 0%"></div>
  </div>
  <div class="fixed top-2 right-4 bg-white bg-opacity-90 px-3 py-1 rounded text-xs z-50" id="progressText">0%</div>
  
  <div class="mt-8 h-screen flex flex-col">
    <div class="flex flex-1 overflow-hidden">
      <div class="w-80 bg-gray-custom border-r border-border-custom flex flex-col">
        <div class="p-4 border-b border-border-custom">
          <input type="text" id="search" placeholder="搜索页面/模块/角色..." 
                 class="w-full px-3 py-2 border border-border-custom rounded focus:outline-none focus:border-gray-400">
        </div>
        <nav class="flex-1 overflow-y-auto p-4">
          <ul id="menu" class="space-y-1"></ul>
          <ul id="searchResults" class="mt-4 space-y-1 border-t border-border-custom pt-4"></ul>
        </nav>
      </div>
      <div class="flex-1 bg-white">
        <iframe id="preview" src="" class="w-full h-full border-0"></iframe>
      </div>
    </div>
  </div>

  <script src="progress.js"></script>
  <script>
    let menuData = [];

    async function loadMenu() {
      const res = await fetch('menu.json');
      menuData = await res.json();
      renderMenu(menuData);

      // 先尝试加载上次打开页面
      const lastPage = localStorage.getItem('lastPage');
      if (lastPage) {
        openPage(lastPage);
      } else {
        loadFirstPage(menuData); // 如果没有记录，加载第一个页面
      }
    }

    function renderMenu(data) {
      const menuContainer = document.getElementById('menu');
      menuContainer.innerHTML = "";

      data.forEach(role => {
        const roleLi = document.createElement('li');
        roleLi.className = 'menu-item';
        
        const roleSpan = document.createElement('span');
        roleSpan.textContent = role.name;
        roleSpan.className = 'font-semibold text-text-primary flex items-center';
        roleSpan.innerHTML = `<i class="fas fa-user mr-2 text-text-secondary"></i>${role.name}`;
        roleSpan.onclick = () => toggleMenu(roleSpan);
        roleLi.appendChild(roleSpan);

        const moduleUl = document.createElement('ul');
        moduleUl.className = 'nested pl-4 space-y-1';
        
        // 检查是否有非pending状态的页面，如果有则展开角色节点
        let hasActivePages = false;

        role.modules.forEach(module => {
          const moduleLi = document.createElement('li');
          moduleLi.className = 'menu-item';
          
          const moduleSpan = document.createElement('span');
          moduleSpan.textContent = module.name;
          moduleSpan.className = 'font-medium text-text-primary flex items-center';
          moduleSpan.innerHTML = `<i class="fas fa-folder mr-2 text-text-secondary"></i>${module.name}`;
          moduleSpan.onclick = () => toggleMenu(moduleSpan);
          moduleLi.appendChild(moduleSpan);

          const pageUl = document.createElement('ul');
          pageUl.className = 'nested pl-4 space-y-1';
          
          let moduleHasActive = false;

          module.pages.forEach(page => {
            const pageLi = document.createElement('li');
            pageLi.className = 'menu-item flex items-center justify-between group';
            
            const pageContent = document.createElement('span');
            pageContent.className = 'flex items-center flex-1';
            
            // 获取页面状态
            const pageStatus = getPageStatus(page.url);
            const statusConfig = progressTracker.getStatusConfig(pageStatus);
            
            // 添加状态指示器
            const statusIndicator = document.createElement('span');
            statusIndicator.className = 'status-indicator mr-2';
            statusIndicator.textContent = statusConfig.icon;
            statusIndicator.title = statusConfig.label;
            statusIndicator.style.color = statusConfig.color;
            
            pageContent.innerHTML = `<i class="fas fa-file-alt mr-2 text-text-secondary"></i>${page.name}`;
            pageContent.insertBefore(statusIndicator, pageContent.firstChild);
            pageContent.onclick = () => openPage(page.url);
            
            // 添加右键菜单提示
            const contextHint = document.createElement('span');
            contextHint.className = 'context-menu-hint';
            contextHint.textContent = '右键切换状态';
            
            pageLi.appendChild(pageContent);
            pageLi.appendChild(contextHint);
            
            // 添加状态样式类
            pageLi.classList.add(`status-${pageStatus}`);
            
            // 设置背景色
            pageLi.style.backgroundColor = pageStatus !== 'pending' ? statusConfig.bgColor : '';
            
            // 添加右键菜单功能
            pageLi.oncontextmenu = (e) => {
              e.preventDefault();
              togglePageStatus(page.url, pageLi);
            };
            
            // 检查是否有非pending状态的页面
            if (pageStatus !== 'pending') {
              hasActivePages = true;
              moduleHasActive = true;
            }
            
            pageUl.appendChild(pageLi);
          });
          
          // 如果模块有非pending状态的页面，展开模块节点
          if (moduleHasActive) {
            pageUl.classList.add('active');
          }

          moduleLi.appendChild(pageUl);
          moduleUl.appendChild(moduleLi);
        });
        
        // 如果角色有非pending状态的页面，展开角色节点
        if (hasActivePages) {
          moduleUl.classList.add('active');
        }

        roleLi.appendChild(moduleUl);
        menuContainer.appendChild(roleLi);
      });
      
      // 更新进度条
      updateProgress();
    }

    function toggleMenu(el) {
      const nested = el.nextElementSibling;
      if (nested) nested.classList.toggle("active");
    }

    function openPage(url) {
      document.getElementById('preview').src = url;
      localStorage.setItem('lastPage', url); // ✅ 记住上次打开页面
      
      // 展开当前激活页面的父级节点
      expandActivePageParents(url);
    }
    
    // 展开当前激活页面的父级节点
    function expandActivePageParents(activeUrl) {
      menuData.forEach(role => {
        role.modules.forEach(module => {
          module.pages.forEach(page => {
            if (page.url === activeUrl) {
              // 找到对应的DOM元素并展开
              const menuItems = document.querySelectorAll('.menu-item');
              menuItems.forEach(item => {
                const span = item.querySelector('span');
                if (span && span.textContent.includes(role.name)) {
                  const roleUl = span.nextElementSibling;
                  if (roleUl) roleUl.classList.add('active');
                }
                if (span && span.textContent.includes(module.name)) {
                  const moduleUl = span.nextElementSibling;
                  if (moduleUl) moduleUl.classList.add('active');
                }
              });
            }
          });
        });
      });
    }

    // ✅ 默认加载第一个页面
    function loadFirstPage(data) {
      if (data.length > 0) {
        const firstRole = data[0];
        if (firstRole.modules && firstRole.modules.length > 0) {
          const firstModule = firstRole.modules[0];
          if (firstModule.pages && firstModule.pages.length > 0) {
            openPage(firstModule.pages[0].url);
          }
        }
      }
    }

    // 搜索功能
    document.getElementById('search').addEventListener('input', function() {
      const query = this.value.trim().toLowerCase();
      const results = [];
      if (query) {
        menuData.forEach(role => {
          if (role.name.toLowerCase().includes(query)) {
            results.push({ name: `[角色] ${role.name}`, url: null });
          }
          role.modules.forEach(module => {
            if (module.name.toLowerCase().includes(query)) {
              results.push({ name: `[模块] ${module.name}`, url: null });
            }
            module.pages.forEach(page => {
              if (page.name.toLowerCase().includes(query)) {
                results.push({ name: `[页面] ${page.name}`, url: page.url });
              }
            });
          });
        });
      }
      renderSearchResults(results);
    });

    function renderSearchResults(results) {
      const container = document.getElementById('searchResults');
      container.innerHTML = "";
      
      if (results.length === 0) {
        container.innerHTML = '<li class="text-text-secondary text-sm p-2">无搜索结果</li>';
        return;
      }
      
      results.forEach(item => {
        const li = document.createElement('li');
        li.className = 'search-result-item flex items-center';
        
        // 根据类型添加不同图标
        let icon = 'fas fa-file-alt';
        if (item.name.includes('[角色]')) {
          icon = 'fas fa-user';
        } else if (item.name.includes('[模块]')) {
          icon = 'fas fa-folder';
        }
        
        li.innerHTML = `<i class="${icon} mr-2 text-text-secondary"></i>${item.name}`;
        
        if (item.url) {
          li.onclick = () => openPage(item.url);
          li.classList.add('cursor-pointer');
        } else {
          li.classList.add('cursor-default', 'opacity-60');
        }
        
        container.appendChild(li);
      });
    }

    loadMenu();
  </script>
</body>
</html>
'''
style_css = '''
/* 低保真线框样式 - 使用 TailwindCSS 补充 */
.wireframe {
  @apply w-96 mx-auto my-5 border border-border-custom;
}

.block {
  @apply border border-dashed border-text-secondary p-5 m-2 text-center text-text-secondary;
}

/* 多状态样式 */
.status-pending {
  @apply text-gray-500;
}

.status-in_progress {
  @apply text-blue-600 bg-blue-50;
}

.status-pending_review {
  @apply text-amber-600 bg-amber-50;
}

.status-optimizing {
  @apply text-purple-600 bg-purple-50;
}

.status-completed {
  @apply text-green-600 bg-green-50 font-semibold;
}

/* 状态指示器样式 */
.status-indicator {
  @apply inline-block w-4 text-center;
}

/* 菜单项交互样式 */
.menu-item {
  @apply cursor-pointer my-1 px-2 py-1 rounded transition-colors duration-200;
}

.menu-item:hover {
  @apply bg-gray-100;
}

.menu-item.active {
  @apply bg-blue-50 text-blue-700;
}

/* 嵌套菜单样式 */
.nested {
  @apply hidden pl-4;
}

.nested.active {
  @apply block;
}

/* 搜索结果样式 */
.search-result-item {
  @apply p-2 cursor-pointer rounded transition-colors duration-200;
}

.search-result-item:hover {
  @apply bg-gray-100;
}

/* 右键菜单提示 */
.context-menu-hint {
  @apply absolute bg-gray-800 text-white px-2 py-1 rounded text-xs whitespace-nowrap z-50 -top-8 left-0 opacity-0 transition-opacity duration-200;
}

.menu-item:hover .context-menu-hint {
  @apply opacity-100;
}

/* iPhone 手机壳样式 */
.iphone-frame {
  @apply relative mx-auto bg-black rounded-3xl p-2;
  width: 375px;
  height: 812px;
}

.iphone-screen {
  @apply w-full h-full bg-white rounded-2xl overflow-hidden relative;
}

.iphone-notch {
  @apply absolute top-0 left-1/2 transform -translate-x-1/2 w-32 h-6 bg-black rounded-b-2xl z-10;
}

.iphone-status-bar {
  @apply absolute top-0 left-0 right-0 h-11 bg-white flex items-center justify-between px-6 text-sm font-medium z-20;
}

.iphone-home-indicator {
  @apply absolute bottom-2 left-1/2 transform -translate-x-1/2 w-32 h-1 bg-black rounded-full;
}
'''

progress_js = '''
// 智能状态管理系统
class ProgressTracker {
  constructor() {
    this.storageKey = 'prototype_progress';
    this.statusConfig = {
      'pending': { icon: '⏳', label: '待开始', color: '#9CA3AF', bgColor: '#F3F4F6' },
      'in_progress': { icon: '🔄', label: '进行中', color: '#3B82F6', bgColor: '#DBEAFE' },
      'pending_review': { icon: '⏰', label: '待确认', color: '#F59E0B', bgColor: '#FEF3C7' },
      'optimizing': { icon: '🔧', label: '优化中', color: '#8B5CF6', bgColor: '#EDE9FE' },
      'completed': { icon: '✅', label: '已确认', color: '#10B981', bgColor: '#D1FAE5' }
    };
    this.loadProgress();
  }

  // 加载进度数据
  loadProgress() {
    const saved = localStorage.getItem(this.storageKey);
    this.progress = saved ? JSON.parse(saved) : {};
  }

  // 保存进度数据
  saveProgress() {
    localStorage.setItem(this.storageKey, JSON.stringify(this.progress));
  }

  // 获取页面状态
  getPageStatus(url) {
    // 首先检查localStorage中的状态
    if (this.progress[url]) {
      return this.progress[url];
    }
    
    // 如果localStorage中没有，则从menu.json中读取初始状态
    if (typeof menuData !== 'undefined' && menuData.length > 0) {
      for (const role of menuData) {
        for (const module of role.modules) {
          for (const page of module.pages) {
            if (page.url === url && page.status) {
              return page.status;
            }
          }
        }
      }
    }
    
    // 默认返回pending状态
    return 'pending';
  }

  // 设置页面状态
  setPageStatus(url, status) {
    if (!this.statusConfig[status]) {
      console.warn('Invalid status:', status);
      return;
    }
    this.progress[url] = status;
    this.saveProgress();
  }

  // 智能状态切换：右键菜单循环切换状态
  togglePageStatus(url) {
    const currentStatus = this.getPageStatus(url);
    const statusOrder = ['pending', 'in_progress', 'pending_review', 'optimizing', 'completed'];
    const currentIndex = statusOrder.indexOf(currentStatus);
    const nextIndex = (currentIndex + 1) % statusOrder.length;
    const newStatus = statusOrder[nextIndex];
    
    this.setPageStatus(url, newStatus);
    return newStatus;
  }

  // AI完成页面后自动标记为待确认
  markPageAsCompleted(url) {
    this.setPageStatus(url, 'pending_review');
  }

  // 用户确认页面
  confirmPage(url) {
    this.setPageStatus(url, 'completed');
  }

  // 开始优化页面
  startOptimizing(url) {
    this.setPageStatus(url, 'optimizing');
  }

  // 计算总进度
  calculateProgress(menuData) {
    let totalPages = 0;
    let completedPages = 0;

    menuData.forEach(role => {
      role.modules.forEach(module => {
        module.pages.forEach(page => {
          totalPages++;
          if (this.getPageStatus(page.url) === 'completed') {
            completedPages++;
          }
        });
      });
    });

    return totalPages > 0 ? Math.round((completedPages / totalPages) * 100) : 0;
  }

  // 更新进度条显示
  updateProgressBar(percentage) {
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    
    if (progressFill && progressText) {
      progressFill.style.width = percentage + '%';
      progressText.textContent = percentage + '%';
    }
  }

  // 获取状态配置
  getStatusConfig(status) {
    return this.statusConfig[status] || this.statusConfig['pending'];
  }

  // 检查是否有非pending状态的页面需要展开父级节点
  shouldExpandNode(pages) {
    return pages.some(page => {
      const status = this.getPageStatus(page.url);
      return status !== 'pending';
    });
  }
}

// 全局进度跟踪器实例
const progressTracker = new ProgressTracker();

// 全局函数供 index.html 使用
function getPageStatus(url) {
  return progressTracker.getPageStatus(url);
}

function togglePageStatus(url, element) {
  const newStatus = progressTracker.togglePageStatus(url);
  const config = progressTracker.getStatusConfig(newStatus);
  
  // 更新元素样式
  element.className = element.className.replace(/status-\w+/g, '');
  element.classList.add(`status-${newStatus}`);
  
  // 更新状态显示
  const statusSpan = element.querySelector('.status-indicator');
  if (statusSpan) {
    statusSpan.textContent = config.icon;
    statusSpan.title = config.label;
  }
  
  // 重新渲染菜单以更新节点展开状态
  renderMenu(menuData);
}

function updateProgress() {
  const percentage = progressTracker.calculateProgress(menuData);
  progressTracker.updateProgressBar(percentage);
}

// AI完成页面后调用
function markPageAsCompleted(url) {
  progressTracker.markPageAsCompleted(url);
  // 重新渲染菜单
  renderMenu(menuData);
}

// 用户确认页面
function confirmPage(url) {
  progressTracker.confirmPage(url);
  renderMenu(menuData);
}

// 开始优化页面
function startOptimizing(url) {
  progressTracker.startOptimizing(url);
  renderMenu(menuData);
}

// 定时刷新功能
let refreshInterval;

// 启动定时刷新
function startAutoRefresh(intervalMs = 5000) {
  if (refreshInterval) {
    clearInterval(refreshInterval);
  }
  
  refreshInterval = setInterval(() => {
    // 重新渲染菜单和更新进度
    if (typeof menuData !== 'undefined' && menuData.length > 0) {
      // 保存当前激活的页面
      const currentPage = localStorage.getItem('lastPage');
      
      renderMenu(menuData);
      updateProgress();
      
      // 重新激活当前页面的父级节点
      if (currentPage) {
        expandActivePageParents(currentPage);
      }
    }
  }, intervalMs);
}

// 停止定时刷新
function stopAutoRefresh() {
  if (refreshInterval) {
    clearInterval(refreshInterval);
    refreshInterval = null;
  }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
  // 确保菜单数据加载后更新进度
  if (typeof menuData !== 'undefined' && menuData.length > 0) {
    updateProgress();
  }
  
  // 启动定时刷新（每5秒刷新一次）
  startAutoRefresh(5000);
});

// 页面卸载时清理定时器
window.addEventListener('beforeunload', function() {
  stopAutoRefresh();
});
'''

# 通用配置模板
default_config = {
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

def generate_menu_json(config):
    """根据配置生成menu.json内容"""
    menu_data = []
    
    for role_index, role in enumerate(config['roles']):
        role_data = {
            "name": role['name'],
            "modules": []
        }
        
        for module_index, module in enumerate(role['modules']):
            module_data = {
                "name": module['name'],
                "pages": []
            }
            
            for page_index, page in enumerate(module['pages']):
                # 生成规范的URL路径
                role_dir = f"role{role_index + 1}"
                module_dir = f"module{chr(65 + module_index)}"  # A, B, C...
                page_file = f"page{page_index + 1}.html"
                
                page_data = {
                    "name": page['name'],
                    "url": f"pages/{role_dir}/{module_dir}/{page_file}",
                    "status": page.get('status', 'pending'),
                    "completed_at": page.get('completed_at', None),
                    "priority": page.get('priority', 'normal')
                }
                module_data['pages'].append(page_data)
            
            role_data['modules'].append(module_data)
        
        menu_data.append(role_data)
    
    return json.dumps(menu_data, ensure_ascii=False, indent=2)

def generate_page_template(page_name, page_description, role_name, module_name, platform_type="mobile"):
    """生成页面HTML模板"""
    if platform_type == "mobile":
        return f'''<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_name} - {role_name}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="../../../style.css">
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            'gray-custom': '#f5f5f5',
            'border-custom': '#cccccc',
            'text-primary': '#333333',
            'text-secondary': '#666666'
          }}
        }}
      }}
    }}
  </script>
  <style>
    /* iPhone手机壳样式 */
    .iphone-frame {{
      width: 375px;
      height: 812px;
      background: #000;
      border-radius: 40px;
      padding: 8px;
      margin: 20px auto;
      box-shadow: 0 0 20px rgba(0,0,0,0.3);
    }}
    
    .iphone-screen {{
      width: 100%;
      height: 100%;
      background: #fff;
      border-radius: 32px;
      overflow: hidden;
      position: relative;
    }}
    
    .status-bar {{
      height: 44px;
      background: #fff;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 20px;
      font-size: 14px;
      font-weight: 600;
      color: #000;
      border-bottom: 1px solid #e0e0e0;
    }}
    
    .status-left, .status-right {{
      display: flex;
      align-items: center;
      gap: 5px;
    }}
    
    .page-content {{
      height: calc(100% - 44px);
      overflow-y: auto;
      padding: 0;
    }}
  </style>
</head>
<body class="m-0 p-0 font-sans bg-gray-custom">
  <!-- iPhone手机壳开始 -->
  <div class="iphone-frame">
    <div class="iphone-screen">
      <!-- 状态栏 -->
      <div class="status-bar">
        <div class="status-left">
          <div class="signal-indicator">
            <div class="signal-bar" style="height: 3px;"></div>
            <div class="signal-bar" style="height: 5px;"></div>
            <div class="signal-bar" style="height: 7px;"></div>
            <div class="signal-bar" style="height: 9px;"></div>
          </div>
          <span class="carrier">中国移动</span>
          <i class="fas fa-wifi" style="font-size: 11px; margin: 0 3px;"></i>
        </div>
        <div class="status-center">
          <span class="time">9:41</span>
        </div>
        <div class="status-right">
          <div class="battery-indicator">
            <div class="battery-body">
              <div class="battery-level"></div>
            </div>
            <div class="battery-tip"></div>
          </div>
        </div>
      </div>
      
      <!-- 页面内容 -->
      <div class="page-content">
        <div class="bg-white min-h-full">
          <div class="p-4 border-b border-gray-200 bg-white">
            <div class="text-text-secondary text-xs mb-1">
              <i class="fas fa-home mr-1"></i>{role_name} > {module_name}
            </div>
            <h1 class="text-lg text-text-primary m-0 font-bold">
              <i class="fas fa-file-alt mr-2 text-blue-500"></i>{page_name}
            </h1>
          </div>
          <div class="p-4">
            <div class="border-2 border-dashed border-gray-400 p-4 my-2 bg-gray-50 text-center rounded">
              <h3 class="text-base text-text-primary mb-2 font-semibold">
                <i class="fas fa-cogs mr-2 text-blue-500"></i>主要功能区域
              </h3>
              <p class="text-sm text-text-secondary mb-2">此处展示页面的核心功能内容</p>
              <div class="h-20 border border-dashed border-border-custom my-2 flex items-center justify-center text-text-secondary rounded">
                <i class="fas fa-cube mr-2"></i>功能内容区域
              </div>
            </div>
            
            <div class="border-2 border-dashed border-gray-400 p-4 my-2 bg-gray-50 text-center rounded">
              <h3 class="text-base text-text-primary mb-2 font-semibold">
                <i class="fas fa-tools mr-2 text-green-500"></i>辅助功能区域
              </h3>
              <p class="text-sm text-text-secondary mb-2">此处展示页面的辅助功能内容</p>
              <div class="h-20 border border-dashed border-border-custom my-2 flex items-center justify-center text-text-secondary rounded">
                <i class="fas fa-puzzle-piece mr-2"></i>辅助功能区域
              </div>
            </div>
            
            <div class="border border-border-custom p-4 my-2 rounded bg-white">
              <h3 class="text-base font-semibold mb-2 text-text-primary">
                <i class="fas fa-mouse-pointer mr-2 text-purple-500"></i>操作区域
              </h3>
              <div class="flex flex-wrap gap-2">
                <button class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors">
                  <i class="fas fa-play mr-1"></i>主要操作
                </button>
                <button class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 transition-colors">
                  <i class="fas fa-cog mr-1"></i>次要操作
                </button>
                <button class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition-colors">
                  <i class="fas fa-arrow-left mr-1"></i>返回
                </button>
              </div>
            </div>
          </div>
          
          <div class="mx-4 mb-4 p-4 bg-gray-100 rounded">
            <h4 class="text-sm text-text-primary mb-2 font-semibold">
              <i class="fas fa-info-circle mr-2 text-blue-500"></i>页面说明
            </h4>
            <div class="space-y-1 text-xs">
              <p><i class="fas fa-bullseye mr-2 text-green-500"></i><strong>页面用途：</strong>{page_description}</p>
              <p><i class="fas fa-user mr-2 text-blue-500"></i><strong>目标用户：</strong>{role_name}</p>
              <p><i class="fas fa-folder mr-2 text-yellow-500"></i><strong>所属模块：</strong>{module_name}</p>
              <p><i class="fas fa-lightbulb mr-2 text-orange-500"></i><strong>设计说明：</strong>这是一个低保真线稿页面，展示了页面的基本布局和功能区域划分。</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>'''
    else:
        return f'''<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <title>{page_name} - {role_name}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="../../../style.css">
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            'gray-custom': '#f5f5f5',
            'border-custom': '#cccccc',
            'text-primary': '#333333',
            'text-secondary': '#666666'
          }}
        }}
      }}
    }}
  </script>
</head>
<body class="font-sans bg-gray-custom">
  <div class="max-w-6xl mx-auto p-5">
    <div class="border-b-2 border-text-primary pb-2 mb-5">
      <div class="text-text-secondary text-sm mb-2">
        <i class="fas fa-home mr-1"></i>{role_name} > {module_name}
      </div>
      <h1 class="text-2xl font-bold text-text-primary">
        <i class="fas fa-file-alt mr-2 text-blue-500"></i>{page_name}
      </h1>
      <p class="text-text-secondary mt-2">{page_description}</p>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
      <div class="border-2 border-dashed border-gray-400 p-5 text-center bg-gray-50 rounded">
        <h3 class="text-lg font-semibold mb-2 text-text-primary">
          <i class="fas fa-cogs mr-2 text-blue-500"></i>主要功能区域
        </h3>
        <p class="text-text-secondary mb-3">此处展示页面的核心功能内容</p>
        <div class="h-24 border border-dashed border-border-custom my-2 flex items-center justify-center text-text-secondary rounded">
          <i class="fas fa-cube mr-2"></i>功能内容区域
        </div>
      </div>
      
      <div class="border-2 border-dashed border-gray-400 p-5 text-center bg-gray-50 rounded">
        <h3 class="text-lg font-semibold mb-2 text-text-primary">
          <i class="fas fa-tools mr-2 text-green-500"></i>辅助功能区域
        </h3>
        <p class="text-text-secondary mb-3">此处展示页面的辅助功能内容</p>
        <div class="h-24 border border-dashed border-border-custom my-2 flex items-center justify-center text-text-secondary rounded">
          <i class="fas fa-puzzle-piece mr-2"></i>辅助功能区域
        </div>
      </div>
    </div>
    
    <div class="border border-border-custom p-4 mt-5 rounded bg-white">
      <h3 class="text-lg font-semibold mb-3 text-text-primary">
        <i class="fas fa-mouse-pointer mr-2 text-purple-500"></i>操作区域
      </h3>
      <div class="flex flex-wrap gap-2">
        <button class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors">
          <i class="fas fa-play mr-1"></i>主要操作
        </button>
        <button class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 transition-colors">
          <i class="fas fa-cog mr-1"></i>次要操作
        </button>
        <button class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition-colors">
          <i class="fas fa-arrow-left mr-1"></i>返回
        </button>
      </div>
    </div>
    
    <div class="mt-8 p-4 bg-gray-100 rounded">
      <h4 class="text-base font-semibold mb-3 text-text-primary">
        <i class="fas fa-info-circle mr-2 text-blue-500"></i>页面说明
      </h4>
      <div class="space-y-2 text-sm">
        <p><i class="fas fa-bullseye mr-2 text-green-500"></i><strong>页面用途：</strong>{page_description}</p>
        <p><i class="fas fa-user mr-2 text-blue-500"></i><strong>目标用户：</strong>{role_name}</p>
        <p><i class="fas fa-folder mr-2 text-yellow-500"></i><strong>所属模块：</strong>{module_name}</p>
        <p><i class="fas fa-lightbulb mr-2 text-orange-500"></i><strong>设计说明：</strong>这是一个低保真线稿页面，展示了页面的基本布局和功能区域划分。实际开发时需要根据具体需求进行详细设计。</p>
      </div>
    </div>
  </div>
</body>
</html>'''

def create_directory_structure(base_path, config, platform_type="mobile"):
    """创建目录结构"""
    base_path = Path(base_path)
    base_path.mkdir(exist_ok=True)
    
    # 创建pages目录结构
    pages_dir = base_path / "pages"
    pages_dir.mkdir(exist_ok=True)
    
    for role_index, role in enumerate(config['roles']):
        role_dir = pages_dir / f"role{role_index + 1}"
        role_dir.mkdir(exist_ok=True)
        
        for module_index, module in enumerate(role['modules']):
            module_dir = role_dir / f"module{chr(65 + module_index)}"
            module_dir.mkdir(exist_ok=True)
            
            # 创建页面文件
            for page_index, page in enumerate(module['pages']):
                page_file = module_dir / f"page{page_index + 1}.html"
                page_content = generate_page_template(
                    page['name'], 
                    page['description'], 
                    role['name'], 
                    module['name'],
                    platform_type
                )
                page_file.write_text(page_content, encoding='utf-8')

def generate_design_standards(config, platform_type="mobile"):
    """生成设计规范文件内容"""
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
</div>

<style>
.iphone-frame {
  width: 375px;
  height: 812px;
  background: #000;
  border-radius: 40px;
  padding: 8px;
  margin: 20px auto;
  box-shadow: 0 0 20px rgba(0,0,0,0.3);
}

.iphone-screen {
  width: 100%;
  height: 100%;
  background: #fff;
  border-radius: 32px;
  overflow: hidden;
  position: relative;
}

.status-bar {
  height: 44px;
  background: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  font-size: 14px;
  font-weight: 600;
  color: #000;
  border-bottom: 1px solid #e0e0e0;
}

.status-left, .status-right {
      display: flex;
      align-items: center;
      gap: 5px;
    }
    
    .signal-indicator {
      display: flex;
      align-items: flex-end;
      gap: 1px;
      margin-right: 4px;
    }
    
    .signal-bar {
      width: 2px;
      background: #000;
      border-radius: 0.5px;
    }
    
    .battery-indicator {
      display: flex;
      align-items: center;
      gap: 1px;
    }
    
    .battery-body {
      width: 18px;
      height: 9px;
      border: 1px solid #000;
      border-radius: 1px;
      position: relative;
    }
    
    .battery-level {
      width: 80%;
      height: 100%;
      background: #000;
      border-radius: 0.5px;
    }
    
    .battery-tip {
      width: 1px;
      height: 4px;
      background: #000;
      border-radius: 0 1px 1px 0;
    }

.page-content {
  height: calc(100% - 44px);
  overflow-y: auto;
  padding: 20px;
}
</style>'''
    
    mobile_template = '''<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>页面标题</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            'gray-custom': '#f5f5f5',
            'border-custom': '#cccccc',
            'text-primary': '#333333',
            'text-secondary': '#666666'
          }}
        }}
      }}
    }}
  </script>
  <style>
    /* iPhone手机壳样式 */
    .iphone-frame {{
      width: 375px;
      height: 812px;
      background: #000;
      border-radius: 40px;
      padding: 8px;
      margin: 20px auto;
      box-shadow: 0 0 20px rgba(0,0,0,0.3);
    }}
    
    .iphone-screen {{
      width: 100%;
      height: 100%;
      background: #fff;
      border-radius: 32px;
      overflow: hidden;
      position: relative;
    }}
    
    .status-bar {{
      height: 44px;
      background: #fff;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 20px;
      font-size: 14px;
      font-weight: 600;
      color: #000;
      border-bottom: 1px solid #e0e0e0;
    }}
    
    .status-left, .status-right {
      display: flex;
      align-items: center;
      gap: 5px;
    }
    
    .signal-indicator {
      display: flex;
      align-items: flex-end;
      gap: 1px;
      margin-right: 4px;
    }
    
    .signal-bar {
      width: 2px;
      background: #000;
      border-radius: 0.5px;
    }
    
    .battery-indicator {
      display: flex;
      align-items: center;
      gap: 1px;
    }
    
    .battery-body {
      width: 18px;
      height: 9px;
      border: 1px solid #000;
      border-radius: 1px;
      position: relative;
    }
    
    .battery-level {
      width: 80%;
      height: 100%;
      background: #000;
      border-radius: 0.5px;
    }
    
    .battery-tip {
      width: 1px;
      height: 4px;
      background: #000;
      border-radius: 0 1px 1px 0;
    }
    
    .page-content {
      height: calc(100% - 44px);
      overflow-y: auto;
      padding: 20px;
    }}
  </style>
</head>
<body class="m-0 p-0 font-sans bg-gray-custom">
  <!-- iPhone手机壳开始 -->
  <div class="iphone-frame">
    <div class="iphone-screen">
      <!-- 状态栏 -->
      <div class="status-bar">
        <div class="status-left">
          <div class="signal-indicator">
            <div class="signal-bar" style="height: 3px;"></div>
            <div class="signal-bar" style="height: 5px;"></div>
            <div class="signal-bar" style="height: 7px;"></div>
            <div class="signal-bar" style="height: 9px;"></div>
          </div>
          <span class="carrier">中国移动</span>
          <i class="fas fa-wifi" style="font-size: 11px; margin: 0 3px;"></i>
        </div>
        <div class="status-center">
          <span class="time">9:41</span>
        </div>
        <div class="status-right">
          <div class="battery-indicator">
            <div class="battery-body">
              <div class="battery-level"></div>
            </div>
            <div class="battery-tip"></div>
          </div>
        </div>
      </div>
      
      <!-- 页面内容 -->
      <div class="page-content">
        <div class="max-w-sm mx-auto bg-white min-h-full">
          <div class="p-4 border-b border-gray-200 bg-white">
            <h1 class="text-lg text-text-primary font-bold">
              <i class="fas fa-mobile-alt mr-2 text-blue-500"></i>页面标题
            </h1>
          </div>
          <div class="p-5">
            <!-- 页面具体内容 -->
            <div class="border-2 border-gray-300 p-4 my-2 bg-white rounded">
              <h3 class="text-base font-semibold mb-2 text-text-primary">
                <i class="fas fa-cube mr-2 text-green-500"></i>功能模块标题
              </h3>
              <p class="text-text-secondary mb-3">功能描述文字</p>
              <button class="bg-blue-500 text-white px-6 py-3 rounded hover:bg-blue-600 transition-colors">
                <i class="fas fa-play mr-1"></i>操作按钮
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>'''
    
    pc_template = '''<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>页面标题</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            'gray-custom': '#f5f5f5',
            'border-custom': '#cccccc',
            'text-primary': '#333333',
            'text-secondary': '#666666'
          }}
        }}
      }}
    }}
  </script>
</head>
<body class="font-sans bg-gray-custom">
  <div class="max-w-6xl mx-auto bg-white min-h-screen">
    <div class="p-5 border-b-2 border-text-primary bg-white">
      <h1 class="text-2xl text-text-primary font-bold">
        <i class="fas fa-desktop mr-2 text-blue-500"></i>页面标题
      </h1>
    </div>
    <div class="px-5 py-4 bg-gray-100 border-b border-gray-200">
      <ul class="flex space-x-8 list-none">
        <li><a href="#" class="text-text-primary font-bold hover:text-blue-500 transition-colors">
          <i class="fas fa-home mr-1"></i>导航1
        </a></li>
        <li><a href="#" class="text-text-primary font-bold hover:text-blue-500 transition-colors">
          <i class="fas fa-cog mr-1"></i>导航2
        </a></li>
        <li><a href="#" class="text-text-primary font-bold hover:text-blue-500 transition-colors">
          <i class="fas fa-user mr-1"></i>导航3
        </a></li>
      </ul>
    </div>
    <div class="p-8 grid grid-cols-1 md:grid-cols-2 gap-8">
      <div class="border-2 border-gray-300 p-5 my-4 bg-white rounded">
        <h3 class="text-lg font-semibold mb-2 text-text-primary">
          <i class="fas fa-cube mr-2 text-green-500"></i>功能模块1
        </h3>
        <p class="text-text-secondary mb-3">功能描述文字</p>
        <button class="bg-blue-500 text-white px-6 py-3 rounded hover:bg-blue-600 transition-colors">
          <i class="fas fa-play mr-1"></i>操作按钮
        </button>
      </div>
      <div class="border-2 border-gray-300 p-5 my-4 bg-white rounded">
        <h3 class="text-lg font-semibold mb-2 text-text-primary">
          <i class="fas fa-puzzle-piece mr-2 text-purple-500"></i>功能模块2
        </h3>
        <p class="text-text-secondary mb-3">功能描述文字</p>
        <button class="bg-green-500 text-white px-6 py-3 rounded hover:bg-green-600 transition-colors">
          <i class="fas fa-cog mr-1"></i>操作按钮
        </button>
      </div>
    </div>
  </div>
</body>
</html>'''
    
    platform_text = "手机端" if platform_type == "mobile" else "PC端"
    title_size = "18px" if platform_type == "mobile" else "24px"
    body_size = "14px" if platform_type == "mobile" else "16px"
    small_size = "12px" if platform_type == "mobile" else "14px"
    page_margin = "15px" if platform_type == "mobile" else "20px"
    component_spacing = "10px" if platform_type == "mobile" else "15px"
    content_spacing = "20px" if platform_type == "mobile" else "30px"
    btn_padding = "10px 20px" if platform_type == "mobile" else "12px 24px"
    input_padding = "10px" if platform_type == "mobile" else "12px"
    card_padding = "15px" if platform_type == "mobile" else "20px"
    container_width = "375px" if platform_type == "mobile" else "1200px"
    grid_system = "单列布局" if platform_type == "mobile" else "双列网格"
    responsive = "固定宽度" if platform_type == "mobile" else "自适应"
    mobile_requirement = "5. **手机壳要求**: 手机端页面必须包含iPhone手机壳外框" if platform_type == "mobile" else ""
    mobile_check = "- [ ] 手机端是否包含iPhone手机壳" if platform_type == "mobile" else ""
    iphone_section = "## iPhone手机壳模板\n\n" + iphone_template if platform_type == "mobile" else ""
    page_template = mobile_template if platform_type == "mobile" else pc_template
    
    # 构建 JavaScript 配置代码块
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
- **项目名称**: {config['project_name']}
- **项目描述**: {config['project_description']}
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

{iphone_section}

## 标准页面模板

### {platform_text}页面模板

```html
{page_template}
```

## TailwindCSS 和 FontAwesome 集成

### TailwindCSS 配置
本项目使用 TailwindCSS CDN 版本，并配置了自定义颜色主题：

#### 自定义颜色配置
{js_config}

#### 常用 TailwindCSS 类名
- **布局**: `flex`, `grid`, `w-full`, `h-full`, `mx-auto`, `p-4`, `m-2`
- **颜色**: `bg-gray-custom`, `text-text-primary`, `border-border-custom`
- **间距**: `px-3`, `py-2`, `mt-4`, `mb-2`, `space-y-1`, `space-x-2`
- **边框**: `border`, `border-2`, `rounded`, `rounded-lg`
- **交互**: `hover:bg-gray-100`, `transition-colors`, `duration-200`
- **响应式**: `sm:w-1/2`, `md:w-1/3`, `lg:w-1/4`

### FontAwesome 图标系统
项目集成了 FontAwesome 6.4.0，按功能分类的图标：

#### 导航类图标
- `fas fa-home`: 首页/主页
- `fas fa-arrow-left`: 返回
- `fas fa-arrow-right`: 前进
- `fas fa-chevron-down`: 展开
- `fas fa-chevron-up`: 收起

#### 用户界面图标
- `fas fa-user`: 用户/个人中心
- `fas fa-users`: 用户组/团队
- `fas fa-user-circle`: 用户头像
- `fas fa-user-cog`: 用户设置

#### 文件和文档图标
- `fas fa-folder`: 文件夹/目录
- `fas fa-folder-open`: 打开的文件夹
- `fas fa-file-alt`: 文档/页面
- `fas fa-file-image`: 图片文件
- `fas fa-file-pdf`: PDF文件

#### 功能操作图标
- `fas fa-cogs`: 设置/配置
- `fas fa-tools`: 工具
- `fas fa-edit`: 编辑
- `fas fa-trash`: 删除
- `fas fa-save`: 保存
- `fas fa-download`: 下载
- `fas fa-upload`: 上传

#### 状态指示图标
- `fas fa-check`: 完成/确认
- `fas fa-times`: 关闭/取消
- `fas fa-info-circle`: 信息提示
- `fas fa-exclamation-triangle`: 警告
- `fas fa-question-circle`: 帮助/疑问

#### 业务功能图标
- `fas fa-shopping-cart`: 购物车
- `fas fa-heart`: 收藏/喜欢
- `fas fa-star`: 评分/重要
- `fas fa-search`: 搜索
- `fas fa-filter`: 筛选
- `fas fa-sort`: 排序

#### 图标使用规范
1. **一致性**: 同类功能使用相同图标
2. **语义化**: 图标含义要与功能匹配
3. **大小统一**: 使用 `text-sm`, `text-base`, `text-lg` 控制大小
4. **颜色搭配**: 使用 `text-text-secondary` 作为默认图标颜色
5. **间距控制**: 图标与文字间使用 `mr-2` 或 `ml-2` 间距

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

def create_project_files(project_name, config=None, platform_type="mobile"):
    """创建项目文件"""
    if config is None:
        config = default_config
    
    # 创建项目目录
    project_path = Path(project_name)
    project_path.mkdir(exist_ok=True)
    
    # 创建设计规范文件
    design_standards_file = project_path / "design-standards.md"
    design_standards_content = generate_design_standards(config, platform_type)
    design_standards_file.write_text(design_standards_content, encoding='utf-8')
    
    # 创建index.html
    index_file = project_path / "index.html"
    index_content = index_html.replace("原型导航", f"{config['project_name']} - 原型导航")
    index_file.write_text(index_content, encoding='utf-8')
    
    # 创建style.css
    style_file = project_path / "style.css"
    style_file.write_text(style_css, encoding='utf-8')
    
    # 创建progress.js
    progress_file = project_path / "progress.js"
    progress_file.write_text(progress_js, encoding='utf-8')
    
    # 创建menu.json
    menu_file = project_path / "menu.json"
    menu_content = generate_menu_json(config)
    menu_file.write_text(menu_content, encoding='utf-8')
    
    # 创建目录结构和页面文件
    create_directory_structure(project_path, config, platform_type)
    
    # 创建项目说明文件
    readme_file = project_path / "README.md"
    readme_content = f"""# {config['project_name']}

## 项目描述
{config['project_description']}

## 使用说明
1. 在浏览器中打开 `index.html` 文件
2. 使用左侧导航菜单浏览不同的页面
3. 支持搜索功能，可快速定位页面

## 项目结构
```
{project_name}/
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
    
    for role_index, role in enumerate(config['roles']):
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
    
    readme_file.write_text(readme_content, encoding='utf-8')
    
    print(f"✅ 项目 '{project_name}' 创建成功！")
    print(f"📁 项目路径: {project_path.absolute()}")
    print(f"🌐 打开 {project_path.absolute()}/index.html 查看原型")

def load_config_from_file(config_file):
    """从文件加载配置"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ 配置文件 {config_file} 不存在")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='通用产品原型生成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""使用示例:
  python template.py -n my-project                    # 使用默认配置（手机端）
  python template.py -n my-project -c config.json    # 使用自定义配置
  python template.py -n my-project --title "我的产品"  # 自定义项目标题
  python template.py -n my-project --platform pc     # 创建PC端项目
  python template.py -n my-project --platform mobile # 创建手机端项目（默认）

配置文件格式请参考脚本中的 default_config 示例。
        """
    )
    
    parser.add_argument('-n', '--name', required=True, 
                       help='项目名称（将作为目录名）')
    parser.add_argument('-c', '--config', 
                       help='自定义配置文件路径（JSON格式）')
    parser.add_argument('--title', 
                       help='项目标题（显示名称）')
    parser.add_argument('--description', 
                       help='项目描述')
    parser.add_argument('--platform', choices=['mobile', 'pc'], default='mobile',
                       help='平台类型：mobile（手机端，默认）或 pc（PC端）')
    parser.add_argument('--force', action='store_true',
                       help='强制覆盖已存在的项目目录')
    
    args = parser.parse_args()
    
    # 检查项目目录是否已存在
    if Path(args.name).exists() and not args.force:
        print(f"❌ 项目目录 '{args.name}' 已存在，使用 --force 参数强制覆盖")
        return
    
    # 加载配置
    config = default_config.copy()
    
    if args.config:
        custom_config = load_config_from_file(args.config)
        if custom_config:
            config.update(custom_config)
        else:
            return
    
    # 应用命令行参数
    if args.title:
        config['project_name'] = args.title
    if args.description:
        config['project_description'] = args.description
    
    # 创建项目
    try:
        create_project_files(args.name, config, args.platform)
        print(f"📱 平台类型: {'手机端' if args.platform == 'mobile' else 'PC端'}")
        if args.platform == 'mobile':
            print(f"📱 已包含iPhone手机壳模板")
    except Exception as e:
        print(f"❌ 创建项目失败: {e}")
        return

if __name__ == '__main__':
    main()

