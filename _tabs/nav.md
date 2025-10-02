---
title: 导航
icon: fas fa-compass
order: 3
---

<style>
/* 容器与通用样式 */
.nav-container {
  max-width: 1200px;
  padding: 0;
  margin: 0 auto;
}

.nav-header {
  text-align: center;
  margin-bottom: 2.5rem;
  padding: 0 1.5rem;
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
  padding: 0 1.5rem;
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
  gap: 0.8rem 1.5rem;
  line-height: 1.6;
}

.hot-link-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  color: var(--link-color);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s ease;
}

.hot-link-tag:hover {
  color: var(--link-hover-color, #0056b3);
  text-decoration: underline;
}

.hot-link-count {
  color: var(--text-muted);
  font-size: 0.8rem;
  margin-left: 0.3rem;
}

/* 分类链接区域 - 核心优化：卡片边框与阴影 */
.category-section {
  margin-bottom: 2.5rem;
  padding: 0 1.5rem;
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

.link-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

/* 卡片样式优化：虚化边框+分层阴影，增强质感 */
.link-card {
  background: var(--card-bg);
  /* 虚化边框：用rgba降低不透明度，避免生硬实线 */
  border: 1px solid rgba(var(--card-border-rgb), 0.5);
  /* 轻微圆角增加柔和感 */
  border-radius: 8px;
  padding: 0.8rem 1rem;
  /* 过渡包含边框+阴影，确保交互流畅 */
  transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
  text-decoration: none;
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  height: auto;
  /* 正常状态：淡阴影增加悬浮感，不扁平 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}

/* hover状态：边框提亮+阴影加深，增强交互反馈 */
.link-card:hover {
  /* 边框关联链接色，增加关联性，同时保留虚化质感 */
  border-color: rgba(var(--link-color-rgb), 0.6);
  background: var(--card-bg);
  text-decoration: none;
  /* 阴影分层：内阴影增加通透感，外阴影增强立体感 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05), inset 0 0 0 1px rgba(var(--link-color-rgb), 0.1);
  transform: translateY(-1px);
}

.link-card:hover .link-name {
  color: var(--link-color);
}

.link-icon {
  font-size: 1.1rem;
  color: var(--link-color);
  transition: all 0.2s ease;
  flex-shrink: 0;
  margin-top: 0.2rem;
}

.link-content {
  flex: 1;
  min-width: 0;
}

.link-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--heading-color);
  margin: 0 0 0.5rem 0;
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
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .link-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .link-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .nav-header,
  .hot-links-section,
  .category-section {
    padding: 0 1rem;
  }
  
  .nav-title {
    font-size: 1.8rem;
  }
  
  .hot-links-container {
    gap: 0.6rem 1rem;
  }
}

@media (max-width: 480px) {
  .link-grid {
    grid-template-columns: 1fr;
  }
  
  .hot-links-container {
    gap: 0.5rem 0.8rem;
  }
}

/* 卡片动画：保持轻盈过渡 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.link-card {
  animation: fadeIn 0.3s ease forwards;
  opacity: 0;
}

.link-card:nth-child(1) { animation-delay: 0.05s; }
.link-card:nth-child(2) { animation-delay: 0.1s; }
.link-card:nth-child(3) { animation-delay: 0.15s; }
.link-card:nth-child(4) { animation-delay: 0.2s; }
.link-card:nth-child(5) { animation-delay: 0.25s; }
.link-card:nth-child(6) { animation-delay: 0.3s; }
</style>

<div class="nav-container">
  <!-- 热门链接区域 -->
  <section class="hot-links-section">
    <h2 class="hot-links-title">
      <i class="fas fa-fire"></i>
      热门推荐
    </h2>
    <div class="hot-links-container" id="hotLinksContainer">
      <!-- 动态填充 -->
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
         data-is-hot="{{ link.hot | default: 'false' }}"
         onclick="trackClick('{{ link.name | slugify }}')">
        
        <i class="fas link-icon {{ link.icon | default: 'fa-external-link-alt' }}"></i>
        <div class="link-content">
          <div class="link-name">{{ link.name }}</div>
          <div class="link-desc">{{ link.desc }}</div>
        </div>
      </a>
      {% endfor %}
    </div>
  </section>
  {% endfor %}
</div>

<script>
const HOT_LINKS_MAX = 8;

// 跟踪链接点击
function trackClick(linkId) {
  let clicks = localStorage.getItem(`nav_clicks_${linkId}`) || 0;
  clicks = parseInt(clicks) + 1;
  localStorage.setItem(`nav_clicks_${linkId}`, clicks);
  updateHotLinks();
}

// 更新热门链接显示
function updateHotLinks() {
  const container = document.getElementById('hotLinksContainer');
  const allLinks = [];

  // 从site.data.links中收集所有链接数据
  site.data.links.forEach(group => {
    group.links.forEach(link => {
      const linkId = link.name.toLowerCase().replace(/\s+/g, '-');
      allLinks.push({
        id: linkId,
        isHot: link.hot || false,
        name: link.name,
        url: link.url,
        icon: link.icon || 'fa-external-link-alt',
        clicks: parseInt(localStorage.getItem(`nav_clicks_${linkId}`)) || 0
      });
    });
  });

  // 筛选hot标签链接和高点击链接
  const hotTaggedLinks = allLinks.filter(link => link.isHot);
  const sortedNormalLinks = allLinks.filter(link => !link.isHot).sort((a, b) => b.clicks - a.clicks);
  const finalHotLinks = [...hotTaggedLinks, ...sortedNormalLinks].slice(0, HOT_LINKS_MAX);

  // 渲染热门链接
  if (finalHotLinks.length > 0) {
    container.innerHTML = finalHotLinks.map(link => `
      <a 
        href="${link.url}" 
        target="_blank" 
        rel="noopener noreferrer" 
        class="hot-link-tag"
        onclick="trackClick('${link.id}')"
      >
        <i class="fas ${link.icon}"></i>
        ${link.name}
        ${link.clicks > 0 ? `<span class="hot-link-count">(${link.clicks})</span>` : ''}
      </a>
    `).join('');
  } else {
    container.innerHTML = '<span class="text-muted">暂无热门链接数据</span>';
  }
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', () => {
  updateHotLinks();
});
</script>