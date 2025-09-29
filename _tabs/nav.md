---
title: 导航
icon: fas fa-compass
order: 3
---

<style>
.nav-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1.5rem;
}

.nav-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.nav-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--heading-color);
}

.nav-subtitle {
  font-size: 1rem;
  color: var(--text-muted);
  line-height: 1.5;
}

/* 热门链接区域 */
.hot-links-section {
  margin-bottom: 2.5rem;
}

.hot-links-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--heading-color);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.hot-links-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
}

.hot-link-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 6px;
  color: var(--text-color);
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.hot-link-tag:hover {
  background: var(--link-color);
  color: white;
  border-color: var(--link-color);
  text-decoration: none;
  transform: translateY(-1px);
}

/* 分类链接区域 */
.category-section {
  margin-bottom: 2.5rem;
}

.category-header {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin-bottom: 1.2rem;
  padding-bottom: 0.7rem;
  border-bottom: 1px solid var(--border-color);
}

.category-icon {
  font-size: 1.1rem;
  color: var(--link-color);
  background: rgba(var(--link-color-rgb), 0.1);
  width: 2.2rem;
  height: 2.2rem;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.category-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--heading-color);
  margin: 0;
}

/* 4列网格布局 */
.link-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

/* 扁平化卡片样式 */
.link-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 5px;
  padding: 1rem;
  transition: all 0.2s ease;
  text-decoration: none;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  height: auto;
  position: relative;
}

.link-card:hover {
  border-color: var(--link-color);
  background: var(--card-bg);
  text-decoration: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.link-card:hover .link-name {
  color: var(--link-color);
}

.link-icon {
  font-size: 1.1rem;
  color: var(--link-color);
  transition: all 0.2s ease;
  flex-shrink: 0;
  margin-top: 0.1rem;
}

.link-content {
  flex: 1;
  min-width: 0;
}

.link-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--heading-color);
  margin: 0 0 0.3rem 0;
  line-height: 1.3;
  transition: color 0.2s ease;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.link-desc {
  font-size: 0.82rem;
  color: var(--text-muted);
  line-height: 1.4;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 点击计数徽章 */
.click-badge {
  background: var(--link-color);
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 0.6rem;
  font-size: 0.7rem;
  font-weight: 600;
  position: absolute;
  top: 0.7rem;
  right: 0.7rem;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .link-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .link-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .nav-container {
    padding: 0 1rem;
  }
  
  .nav-title {
    font-size: 1.8rem;
  }
}

@media (max-width: 480px) {
  .link-grid {
    grid-template-columns: 1fr;
  }
  
  .hot-links-container {
    flex-direction: column;
  }
  
  .hot-link-tag {
    justify-content: center;
  }
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.link-card {
  animation: fadeIn 0.3s ease forwards;
  opacity: 0;
}

/* 为每个卡片设置延迟动画 */
.link-card:nth-child(1) { animation-delay: 0.05s; }
.link-card:nth-child(2) { animation-delay: 0.1s; }
.link-card:nth-child(3) { animation-delay: 0.15s; }
.link-card:nth-child(4) { animation-delay: 0.2s; }
.link-card:nth-child(5) { animation-delay: 0.25s; }
.link-card:nth-child(6) { animation-delay: 0.3s; }
</style>

<div class="nav-container">
  <header class="nav-header">
    <h1 class="nav-title">网址导航</h1>
    <p class="nav-subtitle">精心整理的实用网站合集</p>
  </header>

  <!-- 动态热门链接区域 -->
  <section class="hot-links-section">
    <h2 class="hot-links-title">
      <i class="fas fa-fire"></i>
      热门推荐
    </h2>
    <div class="hot-links-container" id="hotLinksContainer">
      <!-- 动态内容将由JavaScript填充 -->
    </div>
  </section>

  <!-- 分类链接区域 -->
{% for group in site.data.links %}
  <section class="category-section">
    <div class="category-header">
      <div class="category-icon">
        <i class="fas {{ group.icon | default: 'fa-link' }}"></i>
      </div>
      <h2 class="category-title">{{ group.category }}</h2>
    </div>

    <div class="link-grid">
      {% for link in group.links %}
      <a href="{{ link.url }}" 
         target="_blank" 
         rel="noopener noreferrer" 
         class="link-card" 
         data-link-id="{{ link.name | slugify }}"
         onclick="trackClick('{{ link.name | slugify }}')">
        
        <i class="fas link-icon {{ link.icon | default: 'fa-external-link-alt' }}"></i>
        <div class="link-content">
          <div class="link-name">{{ link.name }}</div>
          <div class="link-desc">{{ link.desc }}</div>
        </div>
        <span class="click-badge" id="badge-{{ link.name | slugify }}" style="display: none;"></span>
      </a>
      {% endfor %}
    </div>
  </section>
  {% endfor %}
</div>

<script>
// 链接点击跟踪功能
function trackClick(linkId) {
  let clicks = localStorage.getItem(`nav_clicks_${linkId}`) || 0;
  clicks = parseInt(clicks) + 1;
  localStorage.setItem(`nav_clicks_${linkId}`, clicks);
  
  // 更新徽章显示
  updateBadge(linkId, clicks);
  
  // 更新热门链接
  updateHotLinks();
}

// 更新单个链接的点击徽章
function updateBadge(linkId, clicks) {
  const badge = document.getElementById(`badge-${linkId}`);
  if (badge && clicks > 0) {
    badge.style.display = 'inline-block';
    badge.textContent = clicks;
  }
}

// 获取所有链接的点击数据
function getLinkClickData() {
  const links = document.querySelectorAll('.link-card');
  const linkData = [];
  
  links.forEach(link => {
    const linkId = link.getAttribute('data-link-id');
    const name = link.querySelector('.link-name').textContent;
    const desc = link.querySelector('.link-desc').textContent;
    const url = link.getAttribute('href');
    const icon = link.querySelector('.link-icon').className.match(/fa-[a-z-]+/)[0];
    const clicks = parseInt(localStorage.getItem(`nav_clicks_${linkId}`)) || 0;
    
    linkData.push({
      id: linkId,
      name: name,
      desc: desc,
      url: url,
      icon: icon,
      clicks: clicks
    });
  });
  
  return linkData;
}

// 更新热门链接显示
function updateHotLinks() {
  const linkData = getLinkClickData();
  
  // 按点击量排序，取前8个
  const hotLinks = linkData
    .filter(link => link.clicks > 0)
    .sort((a, b) => b.clicks - a.clicks)
    .slice(0, 8);
  
  const hotLinksContainer = document.getElementById('hotLinksContainer');
  
  if (hotLinks.length > 0) {
    hotLinksContainer.innerHTML = hotLinks.map(link => `
      <a href="${link.url}" 
         target="_blank" 
         rel="noopener noreferrer" 
         class="hot-link-tag"
         onclick="trackClick('${link.id}')">
        <i class="fas ${link.icon}"></i>
        ${link.name}
        <span>(${link.clicks})</span>
      </a>
    `).join('');
  } else {
    // 如果没有点击数据，显示默认的热门链接
    showDefaultHotLinks();
  }
}

// 显示默认热门链接
function showDefaultHotLinks() {
  // 从数据中获取标记为hot的链接
  const hotLinksContainer = document.getElementById('hotLinksContainer');
  
  // 这里使用Jekyll数据，但需要确保数据文件中有hot标记
  // 如果没有，可以手动创建一些默认热门链接
  hotLinksContainer.innerHTML = `
    <a href="https://github.com/" class="hot-link-tag">
      <i class="fab fa-github"></i> GitHub
    </a>
    <a href="https://developer.mozilla.org/" class="hot-link-tag">
      <i class="fas fa-book"></i> MDN Web Docs
    </a>
    <a href="https://stackoverflow.com/" class="hot-link-tag">
      <i class="fab fa-stack-overflow"></i> Stack Overflow
    </a>
    <a href="https://www.google.com/" class="hot-link-tag">
      <i class="fab fa-google"></i> Google
    </a>
  `;
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
  // 初始化所有链接的点击徽章
  const links = document.querySelectorAll('.link-card');
  links.forEach(link => {
    const linkId = link.getAttribute('data-link-id');
    const clicks = localStorage.getItem(`nav_clicks_${linkId}`) || 0;
    
    if (clicks > 0) {
      updateBadge(linkId, parseInt(clicks));
    }
  });
  
  // 更新热门链接
  updateHotLinks();
});
</script>