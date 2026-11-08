/* Claw Docs · 共享框架渲染与交互，零依赖 */
(function () {
  'use strict';
  var root = document.documentElement;
  var body = document.body;
  var base = body.getAttribute('data-base') || './';
  var page = body.getAttribute('data-page') || 'home';
  var NAV = window.SITE_NAV || [];
  var INDEX = window.SITE_INDEX || [];
  var themeKey = 'claw-docs-theme';

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  var flat = [];
  NAV.forEach(function (g) {
    g.items.forEach(function (it) { if (!it.noPager) flat.push(it); });
  });

  try {
    var saved = localStorage.getItem(themeKey);
    if (saved) root.setAttribute('data-md-color-scheme', saved);
    else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      root.setAttribute('data-md-color-scheme', 'slate');
    }
  } catch (e) {}

  /* 顶栏 */
  var header = document.getElementById('site-header');
  if (header) {
    header.innerHTML =
      '<div class="md-header__inner">' +
        '<a class="md-header__button md-logo" href="' + base + '"><span class="md-logo-mark">C</span><span>Claw Docs</span></a>' +
        '<div class="md-header__title">创作工作台文档</div>' +
        '<div class="md-header__spacer"></div>' +
        '<button class="md-header__button" id="theme-btn" title="切换亮色 / 深色主题" aria-label="切换主题">◐</button>' +
        '<a class="md-header__button po-header-link" href="https://github.com/cyq87999-oss/Claw" target="_blank" rel="noopener">GitHub</a>' +
      '</div>';
  }

  /* 左侧多级折叠导航 */
  var sidebar = document.getElementById('site-sidebar');
  if (sidebar) {
    var sh = '<nav class="md-nav md-nav--primary" aria-label="导航栏"><div class="md-nav__title">CLAW 创作工作台文档</div>';
    NAV.forEach(function (g) {
      sh += g.flatGroup
        ? '<ul class="md-nav__list">'
        : '<details class="md-nav__group" open><summary>' + esc(g.group) + '<span class="md-nav__chev">⌄</span></summary><ul class="md-nav__list md-nav__list--nested">';
      g.items.forEach(function (it) {
        var active = (it.id === page || it.match === page) ? ' md-nav__link--active' : '';
        sh += '<li class="md-nav__item"><a class="md-nav__link' + active + '" href="' + base + it.p + '">' + esc(it.t) + '</a></li>';
      });
      sh += g.flatGroup ? '</ul>' : '</ul></details>';
    });
    sh += '</nav>';
    sidebar.innerHTML = sh;
  }

  /* 右侧本页目录（首页不显示，与参考站一致） */
  var toc = document.getElementById('site-toc');
  if (toc && page !== 'home') {
    var hs = Array.prototype.slice.call(document.querySelectorAll('.md-content__inner h2, .md-content__inner h3'))
      .filter(function (el) { return !el.closest('.po-docs-card, .po-docs-step, .po-docs-index-row, .po-docs-link-tile'); });
    var th = '<nav class="md-nav md-nav--secondary" aria-label="本页目录"><div class="md-nav__title">本页目录</div><ul class="md-nav__list">';
    hs.forEach(function (el, i) {
      if (!el.id) el.id = 'sec-' + i;
      var pad = el.tagName === 'H3' ? ' style="padding-left:1.25rem"' : '';
      th += '<li class="md-nav__item"><a class="md-nav__link" data-target="' + el.id + '"' + pad + ' href="#' + el.id + '">' +
        esc(el.textContent.replace(/[#¶]/g, '').trim()) + '</a></li>';
    });
    th += '</ul></nav>';
    toc.innerHTML = th;

    var tocLinks = Array.prototype.slice.call(toc.querySelectorAll('[data-target]'));
    var ticking = false;
    function syncToc() {
      ticking = false;
      var current = null;
      hs.forEach(function (el) { if (el.getBoundingClientRect().top <= 150) current = el.id; });
      tocLinks.forEach(function (a) {
        a.classList.toggle('md-nav__link--active', a.getAttribute('data-target') === current);
      });
      var top = document.getElementById('site-top');
      if (top) top.classList.toggle('is-visible', window.scrollY > 400);
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(syncToc); }
    }, { passive: true });
    syncToc();
  } else if (toc) {
    toc.innerHTML = '';
  }

  /* 上一页 / 下一页 */
  var pager = document.getElementById('site-pager');
  if (pager) {
    var pos = -1;
    for (var i = 0; i < flat.length; i++) { if (flat[i].id === page) { pos = i; break; } }
    var prev = pos > 0 ? flat[pos - 1] : null;
    var next = pos >= 0 && pos < flat.length - 1 ? flat[pos + 1] : null;
    var ph = '';
    if (prev) ph += '<a class="md-footer-nav__link prev" href="' + base + prev.p + '"><span>上一页</span>' + esc(prev.t) + '</a>';
    if (next) ph += '<a class="md-footer-nav__link next" href="' + base + next.p + '"><span>下一页</span>' + esc(next.t) + '</a>';
    pager.innerHTML = ph;
  }

  /* 本地搜索 */
  var input = document.getElementById('search-input');
  var result = document.getElementById('search-result');
  if (input && result) {
    function render(q) {
      q = (q || '').trim().toLowerCase();
      if (!q) { result.classList.remove('is-open'); result.innerHTML = ''; return; }
      var hits = INDEX.filter(function (it) {
        return (it.t + ' ' + it.k + ' ' + it.d).toLowerCase().indexOf(q) >= 0;
      }).slice(0, 8);
      result.innerHTML = hits.length
        ? hits.map(function (it, i) {
            return '<a class="' + (i === 0 ? 'is-active' : '') + '" href="' + base + it.p + '"><strong>' + esc(it.t) + '</strong><span>' + esc(it.d) + '</span></a>';
          }).join('')
        : '<div class="is-empty">没有匹配的文档</div>';
      result.classList.add('is-open');
    }
    input.addEventListener('input', function () { render(input.value); });
    input.addEventListener('focus', function () { if (input.value.trim()) render(input.value); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { result.classList.remove('is-open'); input.blur(); return; }
      if (e.key === 'Enter') {
        var first = result.querySelector('a');
        if (first) window.location.href = first.getAttribute('href');
      }
    });
    document.addEventListener('click', function (e) {
      if (!e.target.closest('.po-header-search')) result.classList.remove('is-open');
    });
    document.addEventListener('keydown', function (e) {
      var tag = (e.target.tagName || '').toLowerCase();
      if (tag === 'input' || tag === 'textarea') return;
      if (e.key === '/' || ((e.metaKey || e.ctrlKey) && e.key === 'k')) {
        e.preventDefault();
        input.focus();
      }
    });
  }

  /* 主题 / 抽屉 / 回顶 */
  var themeBtn = document.getElementById('theme-btn');
  if (themeBtn) {
    themeBtn.textContent = root.getAttribute('data-md-color-scheme') === 'slate' ? '☀' : '◐';
    themeBtn.addEventListener('click', function () {
      var next = root.getAttribute('data-md-color-scheme') === 'slate' ? 'default' : 'slate';
      root.setAttribute('data-md-color-scheme', next);
      themeBtn.textContent = next === 'slate' ? '☀' : '◐';
      try { localStorage.setItem(themeKey, next); } catch (e) {}
    });
  }
  var drawerBtn = document.getElementById('drawer-btn');
  var mask = document.getElementById('site-mask');
  if (drawerBtn) drawerBtn.addEventListener('click', function () { body.classList.toggle('drawer-open'); });
  if (mask) mask.addEventListener('click', function () { body.classList.remove('drawer-open'); });
  var topBtn = document.getElementById('site-top');
  if (topBtn) topBtn.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
})();
