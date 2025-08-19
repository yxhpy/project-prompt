"""
CSS样式模板定义
包含CSS样式文件的模板
"""


class CSSTemplates:
    """CSS模板类"""
    
    @staticmethod
    def get_style_css() -> str:
        """获取style.css模板"""
        return '''/* 低保真线框样式 - 使用 TailwindCSS 补充 */
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
}'''