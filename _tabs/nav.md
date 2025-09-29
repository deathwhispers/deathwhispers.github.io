---
layout: page
title: 导航
icon: fas fa-compass
order: 3
---

<div class="nav-container">
  <header class="nav-header">
    <h1 class="nav-title">{{ page.title }}</h1>
    <p class="nav-subtitle">精心整理的实用网站合集</p>
  </header>

  <!-- 动态热门链接区域 -->
  <section class="hot-links-section">
    <h2 class="hot-links-title">
      <i class="fas fa-fire"></i>
      热门推荐
    </h2>
    <div class="hot-links-grid" id="hotLinksContainer">
      <div class="loading">加载中...</div>
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
         data-link-id="{{ link.name | slugify }}">
         
        <div class="link-header">
          <div class="link-icon">
            <i class="fas {{ link.icon | default: 'fa-external-link-alt' }}"></i>
          </div>
          <div class="link-name">{{ link.name }}</div>
        </div>
        
        <div class="link-desc" title="{{ link.desc }}">{{ link.desc }}</div>
        
        {% if link.hot %}
        <span class="recommend-badge">推荐</span>
        {% endif %}
        
        <span class="click-badge" id="badge-{{ link.name | slugify }}" style="display: none;"></span>
      </a>
      {% endfor %}
    </div>
  </section>
  {% endfor %}
</div>

<!-- 引入外部资源 -->
<script src="/assets/js/nav.js"></script>