/**
 * 导航管理器 - 处理链接点击跟踪和热门链接展示
 */
class NavManager {
    constructor() {
        this.clickData = {};
        this.saveTimeout = null;
        this.init();
    }

    /**
     * 初始化管理器
     */
    init() {
        this.loadClickData();
        this.updateAllBadges();
        this.updateHotLinks();
        this.setupEventListeners();
    }

    /**
     * 从本地存储加载点击数据
     */
    loadClickData() {
        try {
            const savedData = localStorage.getItem('nav_clicks_data');
            this.clickData = savedData ? JSON.parse(savedData) : {};
            console.log('点击数据加载成功');
        } catch (e) {
            console.error('解析点击数据失败:', e);
            this.clickData = {};
        }
    }

    /**
     * 保存点击数据到本地存储（延迟执行）
     */
    saveClickData() {
        try {
            localStorage.setItem('nav_clicks_data', JSON.stringify(this.clickData));
            console.log('点击数据已保存');
        } catch (e) {
            console.error('保存点击数据失败:', e);
        }
    }

    /**
     * 跟踪链接点击
     * @param {string} linkId - 链接唯一标识
     * @param {string} linkName - 链接名称
     */
    trackClick(linkId, linkName) {
        if (!this.clickData[linkId]) {
            this.clickData[linkId] = {
                name: linkName,
                count: 0,
                lastClicked: new Date().toISOString()
            };
        }

        // 更新点击数据
        this.clickData[linkId].count++;
        this.clickData[linkId].lastClicked = new Date().toISOString();

        // 更新UI
        this.updateBadge(linkId, this.clickData[linkId].count);
        this.updateHotLinks();

        // 延迟保存避免频繁IO操作
        this.debounceSave();
    }

    /**
     * 防抖处理保存操作
     */
    debounceSave() {
        if (this.saveTimeout) {
            clearTimeout(this.saveTimeout);
        }
        this.saveTimeout = setTimeout(() => this.saveClickData(), 1000);
    }

    /**
     * 更新单个链接的点击徽章
     * @param {string} linkId - 链接唯一标识
     * @param {number} count - 点击次数
     */
    updateBadge(linkId, count) {
        const badge = document.getElementById(`badge-${linkId}`);
        if (badge) {
            badge.style.display = count > 0 ? 'inline-block' : 'none';
            badge.textContent = count;
        }
    }

    /**
     * 更新所有链接的点击徽章
     */
    updateAllBadges() {
        Object.entries(this.clickData).forEach(([linkId, data]) => {
            this.updateBadge(linkId, data.count);
        });
    }

    /**
     * 获取热门链接
     * @param {number} limit - 限制数量
     * @returns {Array} 排序后的热门链接
     */
    getHotLinks(limit = 4) {
        return Object.values(this.clickData)
            .sort((a, b) => b.count - a.count || new Date(b.lastClicked) - new Date(a.lastClicked))
            .slice(0, limit);
    }

    /**
     * 更新热门链接展示区域
     */
    updateHotLinks() {
        const hotLinks = this.getHotLinks(4);
        const container = document.getElementById('hotLinksContainer');

        if (hotLinks.length > 0) {
            container.innerHTML = hotLinks.map(link => this.createHotLinkElement(link)).join('');
        } else {
            this.showDefaultHotLinks();
        }
    }

    /**
     * 创建热门链接元素
     * @param {Object} link - 链接数据
     * @returns {string} HTML字符串
     */
    createHotLinkElement(link) {
        const linkId = Object.keys(this.clickData).find(key => this.clickData[key].name === link.name);
        const linkElement = linkId ? document.querySelector(`[data-link-id="${linkId}"]`) : null;

        const url = linkElement?.href || '#';
        const iconClass = linkElement?.querySelector('.link-icon i')?.className.match(/fa-[a-z-]+/)?.[0] || 'fa-external-link-alt';
        const desc = linkElement?.querySelector('.link-desc')?.textContent || '';

        return `
      <a href="${url}" 
         target="_blank" 
         rel="noopener noreferrer" 
         class="hot-link-card"
         onclick="navManager.trackClick('${linkId}', '${link.name}')">
        <div class="hot-link-header">
          <div class="hot-link-icon">
            <i class="fas ${iconClass}"></i>
          </div>
          <div class="hot-link-name">${link.name}</div>
        </div>
        <div class="hot-link-desc" title="${desc}">${desc}</div>
      </a>
    `;
    }

    /**
     * 显示默认热门链接
     */
    showDefaultHotLinks() {
        const container = document.getElementById('hotLinksContainer');
        const recommendedLinks = Array.from(document.querySelectorAll('.link-card'))
            .filter(card => card.querySelector('.recommend-badge'))
            .slice(0, 4);

        if (recommendedLinks.length > 0) {
            container.innerHTML = recommendedLinks.map(card => this.createDefaultHotLink(card)).join('');
        } else {
            // 显示通用默认链接
            container.innerHTML = `
        <a href="https://github.com/" class="hot-link-card" onclick="navManager.trackClick('default-github', 'GitHub')">
          <div class="hot-link-header">
            <div class="hot-link-icon"><i class="fab fa-github"></i></div>
            <div class="hot-link-name">GitHub</div>
          </div>
          <div class="hot-link-desc">代码托管平台</div>
        </a>
        <a href="https://developer.mozilla.org/" class="hot-link-card" onclick="navManager.trackClick('default-mdn', 'MDN Web Docs')">
          <div class="hot-link-header">
            <div class="hot-link-icon"><i class="fas fa-book"></i></div>
            <div class="hot-link-name">MDN Web Docs</div>
          </div>
          <div class="hot-link-desc">Web 技术文档</div>
        </a>
      `;
        }
    }

    /**
     * 创建默认热门链接元素
     * @param {HTMLElement} card - 链接卡片元素
     * @returns {string} HTML字符串
     */
    createDefaultHotLink(card) {
        const name = card.querySelector('.link-name').textContent;
        const desc = card.querySelector('.link-desc').textContent;
        const url = card.href;
        const iconClass = card.querySelector('.link-icon i').className.match(/fa-[a-z-]+/)[0];
        const linkId = card.getAttribute('data-link-id');

        return `
      <a href="${url}" 
         target="_blank" 
         rel="noopener noreferrer" 
         class="hot-link-card"
         onclick="navManager.trackClick('${linkId}', '${name}')">
        <div class="hot-link-header">
          <div class="hot-link-icon"><i class="fas ${iconClass}"></i></div>
          <div class="hot-link-name">${name}</div>
        </div>
        <div class="hot-link-desc" title="${desc}">${desc}</div>
      </a>
    `;
    }

    /**
     * 设置事件监听器
     */
    setupEventListeners() {
        document.querySelectorAll('.link-card').forEach(link => {
            const linkId = link.getAttribute('data-link-id');
            const name = link.querySelector('.link-name').textContent;

            link.addEventListener('click', () => {
                // 延迟跟踪以确保跳转正常执行
                setTimeout(() => this.trackClick(linkId, name), 100);
            });
        });
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    window.navManager = new NavManager();
});