/*
 * Motion for northpineapps.com.
 *   1. Opening: the hero headline rises in word by word, then the text and the label sheet settle in.
 *   2. Header: becomes frosted glass once you scroll.
 *   3. Depth: the label sheet (or app panel) and the moon drift at different speeds as you scroll.
 *   4. Reveals: sections slide up and come into focus as they reach the screen, with grids staggered.
 * Without JavaScript, or with "reduce motion" on, everything simply shows, still.
 */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var root = document.documentElement;
  if (reduce || !('IntersectionObserver' in window)) return;
  root.classList.add('motion');

  function ready(fn) { if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn); else fn(); }

  ready(function () {
    /* 1. Opening sequence */
    var h1 = document.querySelector('.hero h1');
    if (h1 && !h1.dataset.split) {
      h1.dataset.split = '1';
      var words = h1.textContent.trim().split(/\s+/);
      h1.setAttribute('aria-label', h1.textContent.trim());
      h1.innerHTML = words.map(function (w, i) {
        return '<span class="w" aria-hidden="true"><span style="transition-delay:' + (120 + i * 55) + 'ms">' + w.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span></span>';
      }).join(' ');
    }
    requestAnimationFrame(function () { requestAnimationFrame(function () { root.classList.add('loaded'); }); });

    /* 2. Frosted header */
    var head = document.querySelector('.site-head');
    var onScroll = function () {
      var y = window.scrollY || 0;
      if (head) head.classList.toggle('scrolled', y > 12);
      depth(y);
    };

    /* 3. Depth */
    var sheet = document.querySelector('.sheet-stage, .app-shot, .icon-stack');
    var hero = document.querySelector('.hero');
    var ticking = false;
    function depth(y) {
      if (!hero || ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        ticking = false;
        var h = hero.offsetHeight || 1;
        var p = Math.max(0, Math.min(1, y / h));
        if (sheet) sheet.style.setProperty('--lift', (-p * 70).toFixed(1) + 'px');
        if (sheet) sheet.style.setProperty('--tilt', (p * 1.5).toFixed(2) + 'deg');
        var moon = hero.querySelector('.moon');
        if (moon) moon.style.transform = 'translateY(' + (p * 60).toFixed(1) + 'px)';
        hero.style.setProperty('--fade', (1 - p * 0.35).toFixed(3));
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    /* 4. Reveals */
    var groups = ['.steps', '.plans', '.extras', '.more-apps', '.guide-list', '.app-grid'];
    var singles = ['.section-head', '.shot', '.wide-shot', '.table-scroll', '.data', '.contact', '.envelopes', '.sheets-note', '.fine', '.doc h1', '.doc .intro', '.doc section'];
    var targets = [];
    groups.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (g) {
        Array.prototype.forEach.call(g.children, function (c, i) { c.classList.add('rv'); c.style.setProperty('--i', i); targets.push(c); });
      });
    });
    singles.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el) { if (!el.closest('.hero') && !el.classList.contains('rv')) { el.classList.add('rv'); targets.push(el); } });
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var t = e.target;
        t.classList.add('in');
        io.unobserve(t);
        // Once it has arrived, hand the element back to its normal styles (hover effects etc.).
        setTimeout(function () { t.classList.remove('rv', 'in'); t.style.removeProperty('--i'); }, 1300 + 90 * (parseInt(t.style.getPropertyValue('--i'), 10) || 0));
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    targets.forEach(function (t) { io.observe(t); });
  });
})();
