"""
JavaScript模板定义
包含JavaScript文件的模板
"""


class JSTemplates:
    """JavaScript模板类"""
    
    @staticmethod
    def get_progress_js() -> str:
        """获取progress.js模板"""
        return '''// 智能状态管理系统
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
    if (this.progress[url]) {
      return this.progress[url];
    }
    
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

  // 智能状态切换
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
  element.className = element.className.replace(/status-\\w+/g, '');
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
    if (typeof menuData !== 'undefined' && menuData.length > 0) {
      const currentPage = localStorage.getItem('lastPage');
      
      renderMenu(menuData);
      updateProgress();
      
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
  if (typeof menuData !== 'undefined' && menuData.length > 0) {
    updateProgress();
  }
  
  startAutoRefresh(5000);
});

// 页面卸载时清理定时器
window.addEventListener('beforeunload', function() {
  stopAutoRefresh();
});'''