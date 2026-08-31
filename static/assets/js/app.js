/* ============================================================
   RD WEBDESIGN — app.js
   Interações e animações. Vanilla JS, sem dependências.
   ============================================================ */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- Preloader ---------- */
  var preloader = $('#preloader');
  document.body.classList.add('is-loading');
  function finishLoad() {
    var bar = $('.preloader__bar i');
    if (bar) bar.style.width = '100%';
    setTimeout(function () {
      if (preloader) preloader.classList.add('is-done');
      document.body.classList.remove('is-loading');
      var title = $('.hero__title');
      if (title) title.classList.add('is-in');
    }, reduced ? 0 : 380);
  }
  if (document.readyState === 'complete') finishLoad();
  else window.addEventListener('load', finishLoad);
  // fallback
  setTimeout(finishLoad, 2500);

  /* ---------- Cursor customizado ---------- */
  if (fine && !reduced) {
    var cursor = $('#cursor');
    var dot = $('.cursor__dot');
    var ring = $('.cursor__ring');
    var rx = 0, ry = 0, mx = 0, my = 0;
    document.body.classList.add('cursor-ready');
    window.addEventListener('mousemove', function (e) {
      mx = e.clientX; my = e.clientY;
      if (dot) { dot.style.left = mx + 'px'; dot.style.top = my + 'px'; }
    });
    (function loop() {
      rx += (mx - rx) * 0.18; ry += (my - ry) * 0.18;
      if (ring) { ring.style.left = rx + 'px'; ring.style.top = ry + 'px'; }
      requestAnimationFrame(loop);
    })();
    document.addEventListener('mouseover', function (e) {
      if (e.target.closest('a, button, [data-tilt], summary, input, select, textarea, .pf-filters__btn')) {
        cursor.classList.add('is-hover');
      }
    });
    document.addEventListener('mouseout', function (e) {
      if (e.target.closest('a, button, [data-tilt], summary, input, select, textarea, .pf-filters__btn')) {
        cursor.classList.remove('is-hover');
      }
    });
    window.addEventListener('mousedown', function () { cursor.classList.add('is-down'); });
    window.addEventListener('mouseup', function () { cursor.classList.remove('is-down'); });
  }

  /* ---------- Nav: scroll state + hide on scroll down ---------- */
  var nav = $('#nav');
  var progress = $('#scrollProgress');
  var lastY = window.scrollY;
  function onScroll() {
    var y = window.scrollY;
    if (nav) {
      nav.classList.toggle('is-scrolled', y > 30);
      if (y > 400 && y > lastY) nav.classList.add('is-hidden');
      else nav.classList.remove('is-hidden');
    }
    if (progress) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
    }
    lastY = y;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Menu mobile ---------- */
  var toggle = $('#navToggle');
  var links = $('#navLinks');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    });
    $$('a', links).forEach(function (a) {
      a.addEventListener('click', function () {
        document.body.classList.remove('menu-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- Reveal on scroll ---------- */
  var reveals = $$('[data-reveal]');
  if (reduced) {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  } else if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---------- Contador animado ---------- */
  $$('[data-count]').forEach(function (el) {
    var target = parseInt(el.getAttribute('data-count'), 10) || 0;
    if (reduced) { el.textContent = target; return; }
    var started = false;
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && !started) {
          started = true;
          var start = performance.now(), dur = 1400;
          (function tick(now) {
            var p = Math.min((now - start) / dur, 1);
            var eased = 1 - Math.pow(1 - p, 3);
            el.textContent = Math.round(target * eased);
            if (p < 1) requestAnimationFrame(tick);
          })(start);
          obs.disconnect();
        }
      });
    }, { threshold: 0.6 });
    obs.observe(el);
  });

  /* ---------- Botões magnéticos ---------- */
  if (fine && !reduced) {
    $$('[data-magnetic]').forEach(function (el) {
      var strength = 0.35;
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var x = e.clientX - r.left - r.width / 2;
        var y = e.clientY - r.top - r.height / 2;
        el.style.transform = 'translate(' + x * strength + 'px,' + y * strength + 'px)';
      });
      el.addEventListener('mouseleave', function () { el.style.transform = ''; });
    });
  }

  /* ---------- Tilt 3D nos cards ---------- */
  if (fine && !reduced) {
    $$('[data-tilt]').forEach(function (el) {
      var max = 7;
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width;
        var py = (e.clientY - r.top) / r.height;
        el.style.transform = 'perspective(900px) rotateY(' + (px - 0.5) * max * 2 + 'deg) rotateX(' + (0.5 - py) * max * 2 + 'deg) translateY(-4px)';
        el.style.setProperty('--mx', px * 100 + '%');
        el.style.setProperty('--my', py * 100 + '%');
      });
      el.addEventListener('mouseleave', function () { el.style.transform = ''; });
    });
  }

  /* ---------- Parallax leve ---------- */
  if (!reduced) {
    var parallaxEls = $$('[data-parallax]');
    if (parallaxEls.length) {
      window.addEventListener('scroll', function () {
        var y = window.scrollY;
        parallaxEls.forEach(function (el) {
          var speed = parseFloat(el.getAttribute('data-parallax')) || 0.1;
          el.style.transform = 'translateY(' + y * speed + 'px)';
        });
      }, { passive: true });
    }
  }

  /* ---------- Nav: seção ativa ---------- */
  var sectionLinks = $$('#navLinks a[href*="#"]').filter(function (a) {
    return a.getAttribute('href').indexOf(location.pathname.split('/').pop() || 'index.html') !== -1 || a.getAttribute('href').charAt(0) === '#';
  });
  var idMap = {};
  $$('section[id]').forEach(function (s) { idMap[s.id] = s; });
  if (Object.keys(idMap).length && 'IntersectionObserver' in window) {
    var navIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          $$('#navLinks a').forEach(function (a) {
            a.classList.toggle('is-active', a.getAttribute('href').indexOf('#' + en.target.id) !== -1);
          });
        }
      });
    }, { threshold: 0.5 });
    Object.keys(idMap).forEach(function (id) { navIo.observe(idMap[id]); });
  }

  /* ---------- Escala dos iframes do portfólio ---------- */
  function scaleFrames() {
    $$('.proj__frame').forEach(function (frame) {
      var scaler = frame.querySelector('.proj__scaler');
      if (!scaler) return;
      var scale = frame.offsetWidth / 1440;
      scaler.style.transform = 'scale(' + scale + ')';
      frame.style.height = Math.ceil(900 * scale) + 'px';
    });
  }
  scaleFrames();
  window.addEventListener('resize', scaleFrames);
  window.addEventListener('load', scaleFrames);

  /* ---------- Filtro do portfólio ---------- */
  var filterBtns = $$('.pf-filters__btn');
  if (filterBtns.length) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        filterBtns.forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');
        var f = btn.getAttribute('data-filter');
        $$('.proj').forEach(function (card) {
          var show = f === 'all' || card.getAttribute('data-cat') === f;
          card.classList.toggle('is-hidden', !show);
        });
        scaleFrames();
      });
    });
  }

  /* ---------- Formulário -> WhatsApp ---------- */
  var form = $('#contactForm');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var nome = (data.get('nome') || '').trim();
      var tel = (data.get('telefone') || '').trim();
      var email = (data.get('email') || '').trim();
      var servico = data.get('servico') || '';
      var msg = (data.get('mensagem') || '').trim();
      var txt = 'Olá! Vim pelo site da RD Webdesign e gostaria de um orçamento.';
      if (nome) txt += '\n\n*Nome:* ' + nome;
      if (tel) txt += '\n*WhatsApp:* ' + tel;
      if (email) txt += '\n*E-mail:* ' + email;
      if (servico) txt += '\n*Serviço:* ' + servico;
      if (msg) txt += '\n*Mensagem:* ' + msg;
      var wa = document.body.getAttribute('data-wa') || '5511919948528';
      window.open('https://wa.me/' + wa + '?text=' + encodeURIComponent(txt), '_blank');
    });
  }

  /* ---------- Transição entre páginas ---------- */
  var pt = $('#pageTransition');
  if (pt && !reduced) {
    // revela ao carregar
    pt.classList.add('is-covering');
    requestAnimationFrame(function () {
      pt.classList.remove('is-covering');
      pt.classList.add('is-revealing');
      setTimeout(function () { pt.classList.remove('is-revealing'); }, 700);
    });

    $$('a[data-transition]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var href = a.getAttribute('href');
        if (!href || href.charAt(0) === '#' || a.target === '_blank' || e.metaKey || e.ctrlKey) return;
        e.preventDefault();
        pt.classList.remove('is-revealing');
        pt.classList.add('is-covering');
        setTimeout(function () { window.location.href = href; }, 520);
      });
    });
  }
})();
