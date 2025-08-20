"""
HTML模板定义
包含各种HTML模板的字符串定义
"""


class HTMLTemplates:
    """HTML模板类"""
    
    @staticmethod
    def get_index_template() -> str:
        """获取index.html模板"""
        return '''<!DOCTYPE html>
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

      const lastPage = localStorage.getItem('lastPage');
      if (lastPage) {
        openPage(lastPage);
      } else {
        loadFirstPage(menuData);
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
            
            const pageStatus = getPageStatus(page.url);
            const statusConfig = progressTracker.getStatusConfig(pageStatus);
            
            const statusIndicator = document.createElement('span');
            statusIndicator.className = 'status-indicator mr-2';
            statusIndicator.textContent = statusConfig.icon;
            statusIndicator.title = statusConfig.label;
            statusIndicator.style.color = statusConfig.color;
            
            pageContent.innerHTML = `<i class="fas fa-file-alt mr-2 text-text-secondary"></i>${page.name}`;
            pageContent.insertBefore(statusIndicator, pageContent.firstChild);
            pageContent.onclick = () => openPage(page.url);
            
            const contextHint = document.createElement('span');
            contextHint.className = 'context-menu-hint';
            contextHint.textContent = '右键切换状态';
            
            pageLi.appendChild(pageContent);
            pageLi.appendChild(contextHint);
            
            pageLi.classList.add(`status-${pageStatus}`);
            pageLi.style.backgroundColor = pageStatus !== 'pending' ? statusConfig.bgColor : '';
            
            pageLi.oncontextmenu = (e) => {
              e.preventDefault();
              togglePageStatus(page.url, pageLi);
            };
            
            if (pageStatus !== 'pending') {
              hasActivePages = true;
              moduleHasActive = true;
            }
            
            pageUl.appendChild(pageLi);
          });
          
          if (moduleHasActive) {
            pageUl.classList.add('active');
          }

          moduleLi.appendChild(pageUl);
          moduleUl.appendChild(moduleLi);
        });
        
        if (hasActivePages) {
          moduleUl.classList.add('active');
        }

        roleLi.appendChild(moduleUl);
        menuContainer.appendChild(roleLi);
      });
      
      updateProgress();
    }

    function toggleMenu(el) {
      const nested = el.nextElementSibling;
      if (nested) nested.classList.toggle("active");
    }

    function openPage(url) {
      document.getElementById('preview').src = url;
      localStorage.setItem('lastPage', url);
      expandActivePageParents(url);
    }
    
    function expandActivePageParents(activeUrl) {
      menuData.forEach(role => {
        role.modules.forEach(module => {
          module.pages.forEach(page => {
            if (page.url === activeUrl) {
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
</html>'''
    
    @staticmethod
    def get_mobile_page_template(page_name: str, page_description: str, 
                                role_name: str, module_name: str) -> str:
        """获取手机端页面模板 - 返回完整HTML结构，包含手机框架"""
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
</head>
<body class="m-0 p-0 font-sans bg-gray-custom">
  <div class="iphone-frame">
    <div class="iphone-screen">
      <div class="status-bar">
        <div class="status-left">
          <span class="carrier">中国移动</span>
          <i class="fas fa-wifi" style="font-size: 11px; margin: 0 3px;"></i>
        </div>
        <div class="status-center">
          <span class="time">9:41</span>
        </div>
        <div class="status-right">
          <span class="battery">100%</span>
        </div>
      </div>
      
      <div class="page-content">
        {HTMLTemplates.get_mobile_page_content(page_name, page_description, role_name, module_name)}
      </div>
    </div>
  </div>
</body>
</html>'''
    
    @staticmethod
    def get_mobile_page_content(page_name: str, page_description: str, 
                               role_name: str, module_name: str) -> str:
        """获取手机端页面内容 - 仅返回页面内容部分"""
        return f'''<div class="bg-white min-h-full">
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
        </div>'''
    
    @staticmethod
    def get_mobile_frame_template() -> str:
        """获取手机框架模板 - 用于提供给用户的空框架"""
        return '''<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>手机页面框架</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="../../../style.css">
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
</head>
<body class="m-0 p-0 font-sans bg-gray-custom">
  <div class="iphone-frame">
    <div class="iphone-screen">
      <div class="status-bar">
        <div class="status-left">
          <span class="carrier">中国移动</span>
          <i class="fas fa-wifi" style="font-size: 11px; margin: 0 3px;"></i>
        </div>
        <div class="status-center">
          <span class="time">9:41</span>
        </div>
        <div class="status-right">
          <span class="battery">100%</span>
        </div>
      </div>
      
      <div class="page-content">
        <!-- 页面内容将在这里替换 -->
      </div>
    </div>
  </div>
</body>
</html>'''
    
    @staticmethod
    def get_pc_page_template(page_name: str, page_description: str, 
                           role_name: str, module_name: str) -> str:
        """获取PC端页面模板"""
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