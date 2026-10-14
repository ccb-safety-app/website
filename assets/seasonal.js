/*
 * Seasonal decorations for northpineapps.com. Halloween: a harvest moon and a few bats over
 * the green hero, and a spider on a thread under the header.
 * Shown from October 1 to October 31 only, then switches itself off. To remove it for good,
 * delete this file and its <script> tag in build.py.
 * Decoration only: it never blocks clicks, and it holds still for people who prefer reduced motion.
 */
(function () {
  var now = new Date();
  var force = /[?&]halloween=1/.test(location.search);
  if (!force && now.getMonth() !== 9) return;   // October only

  var css = [
    '.spooky{position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:0}',
    '.hero{position:relative}.hero>.wrap{position:relative;z-index:1}',
    '.spooky .moon{position:absolute;right:6%;top:8%;width:clamp(110px,14vw,190px);aspect-ratio:1;border-radius:50%;',
    'background:radial-gradient(circle at 38% 36%,#fff6da 0,#f3dc9e 42%,#e3b341 100%);',
    'box-shadow:0 0 60px 18px rgba(243,220,158,.22),0 0 160px 60px rgba(227,179,65,.10);opacity:0;animation:moonIn 2.4s .2s ease-out forwards}',
    '.spooky .moon::before,.spooky .moon::after{content:"";position:absolute;border-radius:50%;background:rgba(190,150,60,.18)}',
    '.spooky .moon::before{width:22%;height:22%;left:22%;top:30%}.spooky .moon::after{width:13%;height:13%;left:58%;top:58%}',
    '@keyframes moonIn{to{opacity:.9}}',
    '.spooky .bat{position:absolute;left:-60px;width:var(--s,34px);color:#06100c;opacity:.95;filter:drop-shadow(0 0 6px rgba(227,179,65,.18));animation:fly var(--d,16s) linear var(--delay,0s) infinite}',
    '.spooky .bat svg{display:block;width:100%;height:auto;transform-origin:50% 40%;animation:flap .26s ease-in-out infinite alternate}',
    '@keyframes flap{from{transform:scaleY(1)}to{transform:scaleY(.5)}}',
    '@keyframes fly{0%{transform:translate(0,0)}25%{transform:translate(28vw,-34px)}50%{transform:translate(56vw,18px)}75%{transform:translate(84vw,-26px)}100%{transform:translate(calc(100vw + 120px),6px)}}',
    '.spider{position:absolute;right:clamp(16px,6vw,96px);top:100%;width:20px;pointer-events:none;z-index:6;transform-origin:50% 0;animation:dangle 5.5s ease-in-out infinite}',
    '.spider .thread{display:block;width:1px;margin:0 auto;height:var(--h,54px);background:linear-gradient(rgba(255,255,255,.55),rgba(255,255,255,.25));animation:drop 5.5s ease-in-out infinite}',
    '.site-head:not(.on-hero) .spider .thread{background:linear-gradient(rgba(27,42,36,.45),rgba(27,42,36,.2))}',
    '.spider svg{display:block;width:20px;height:auto;margin-top:-1px}',
    '@keyframes dangle{0%,100%{transform:rotate(-3deg)}50%{transform:rotate(3deg)}}',
    '@keyframes drop{0%,100%{height:var(--h,54px)}50%{height:calc(var(--h,54px) + 18px)}}',
    '@media (max-width:640px){.spooky .moon{top:3%;right:4%}.spooky .bat:nth-child(n+3){display:none}}',
    '@media (prefers-reduced-motion:reduce){.spooky .bat{animation:none;transform:translate(60vw,40px)}.spooky .bat svg,.spider,.spider .thread{animation:none}.spooky .moon{animation:none;opacity:.9}}'
  ].join('');
  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  var BAT = '<svg viewBox="0 0 64 30" aria-hidden="true"><path fill="currentColor" d="M32 9c1.6-3.4 3-4.6 3.8-4.6.4 1.5.3 2.8-.3 4 4.2-.5 8.3-3.2 11.4-7.6 1 4.3 4.7 7.2 9.6 7.4-1 2.5-1 5.2 0 8.4 2.2-.8 4.6-.8 7.5 0-5.2 2.4-8.6 6.4-10 12.2-3.1-3.2-6.7-4.2-10.8-3-.8-3.3-3.3-5.6-6.8-6.4-.9 1.9-2.4 3.2-4.4 3.8-2-.6-3.5-1.9-4.4-3.8-3.5.8-6 3.1-6.8 6.4-4.1-1.2-7.7-.2-10.8 3C8.6 23.6 5.2 19.6 0 17.2c2.9-.8 5.3-.8 7.5 0 1-3.2 1-5.9 0-8.4 4.9-.2 8.6-3.1 9.6-7.4 3.1 4.4 7.2 7.1 11.4 7.6-.6-1.2-.7-2.5-.3-4C29 4.4 30.4 5.6 32 9z"/></svg>';
  var SPIDER = '<svg viewBox="0 0 40 40" aria-hidden="true"><g fill="none" stroke="#0a1611" stroke-width="2.2" stroke-linecap="round"><path d="M14 17 4 9M14 21 2 20M14 25 4 33M15 28l-6 9M26 17l10-8M26 21l12-1M26 25l10 8M25 28l6 9"/></g><ellipse cx="20" cy="15" rx="5" ry="4.5" fill="#0a1611"/><ellipse cx="20" cy="25" rx="7.5" ry="8.5" fill="#0a1611"/><circle cx="18" cy="14" r="1.1" fill="#e3b341"/><circle cx="22" cy="14" r="1.1" fill="#e3b341"/></svg>';

  function decorate() {
    var hero = document.querySelector('.hero');
    if (hero && !hero.querySelector('.spooky')) {
      var layer = document.createElement('div');
      layer.className = 'spooky';
      layer.setAttribute('aria-hidden', 'true');
      var bats = [
        { top: '14%', s: '58px', d: '18s', delay: '-13s' },
        { top: '30%', s: '40px', d: '23s', delay: '-4s' },
        { top: '8%', s: '30px', d: '27s', delay: '-19s' },
        { top: '55%', s: '46px', d: '20s', delay: '-9s' }
      ];
      layer.innerHTML = '<div class="moon"></div>' + bats.map(function (b) {
        return '<div class="bat" style="top:' + b.top + ';--s:' + b.s + ';--d:' + b.d + ';--delay:' + b.delay + '">' + BAT + '</div>';
      }).join('');
      hero.insertBefore(layer, hero.firstChild);
    }
    var head = document.querySelector('.site-head');
    if (head && !head.querySelector('.spider')) {
      var sp = document.createElement('div');
      sp.className = 'spider';
      sp.setAttribute('aria-hidden', 'true');
      sp.style.setProperty('--h', hero ? '64px' : '42px');
      sp.innerHTML = '<span class="thread"></span>' + SPIDER;
      head.appendChild(sp);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', decorate); else decorate();
})();
