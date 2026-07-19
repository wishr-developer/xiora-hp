/* =====================================================
   Xiora - Main JS
   Minimal, dependency-free, lightweight
   ===================================================== */

(function () {
  'use strict';

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- i18n (auto language detection + toggle) ---------- */
  const LANG_KEY = 'xiora.lang';
  const SUPPORTED = ['ja', 'en'];

  function detectLang() {
    // 1) URL ?lang=
    const url = new URLSearchParams(window.location.search).get('lang');
    if (url && SUPPORTED.includes(url)) return url;
    // 2) stored choice
    const stored = localStorage.getItem(LANG_KEY);
    if (stored && SUPPORTED.includes(stored)) return stored;
    // 3) browser
    const nav = (navigator.language || navigator.userLanguage || 'ja').toLowerCase();
    return nav.startsWith('en') ? 'en' : 'ja';
  }

  function applyDict(dict, lang) {
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.getAttribute('data-i18n');
      if (dict[key] != null) el.innerHTML = dict[key];
    });
    document.querySelectorAll('[data-i18n-attr]').forEach((el) => {
      // value format: "attr1=key1;attr2=key2"
      const spec = el.getAttribute('data-i18n-attr') || '';
      spec.split(';').forEach((pair) => {
        const [attr, key] = pair.split('=').map((s) => (s || '').trim());
        if (attr && key && dict[key] != null) el.setAttribute(attr, dict[key]);
      });
    });
    // Toggle button label: show *other* language name
    const toggle = document.querySelector('[data-lang-toggle]');
    if (toggle) toggle.textContent = lang === 'ja' ? 'EN' : 'JA';
  }

  function loadLang(lang) {
    return fetch('/assets/i18n/' + lang + '.json', { cache: 'no-cache' })
      .then((r) => (r.ok ? r.json() : null))
      .catch(() => null);
  }

  const initialLang = detectLang();
  loadLang(initialLang).then((dict) => { if (dict) applyDict(dict, initialLang); });

  // Switch language on toggle click
  document.addEventListener('click', (e) => {
    const trigger = e.target.closest('[data-lang-toggle]');
    if (!trigger) return;
    e.preventDefault();
    const current = document.documentElement.lang === 'en' ? 'en' : 'ja';
    const next = current === 'ja' ? 'en' : 'ja';
    localStorage.setItem(LANG_KEY, next);
    loadLang(next).then((dict) => { if (dict) applyDict(dict, next); });
  });

  /* ---------- Header scroll state ---------- */
  const header = document.getElementById('siteHeader');
  if (header) {
    let lastY = -1;
    const onScroll = () => {
      const y = window.scrollY;
      if ((y > 16) !== (lastY > 16)) {
        header.classList.toggle('is-scrolled', y > 16);
      }
      lastY = y;
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Mobile nav toggle ---------- */
  const toggle = document.getElementById('navToggle');
  const nav = document.getElementById('siteNav');
  if (toggle && nav) {
    const close = () => {
      toggle.classList.remove('is-open');
      nav.classList.remove('is-open');
      document.body.classList.remove('nav-open');
      toggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    };
    toggle.addEventListener('click', () => {
      const open = !toggle.classList.contains('is-open');
      toggle.classList.toggle('is-open', open);
      nav.classList.toggle('is-open', open);
      document.body.classList.toggle('nav-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.querySelectorAll('a').forEach((a) => a.addEventListener('click', close));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) close();
    });
    window.addEventListener('resize', () => {
      if (window.innerWidth > 880) close();
    });
  }

  /* ---------- Scroll reveal ---------- */
  const reveals = document.querySelectorAll('.reveal');
  if (reduceMotion) {
    reveals.forEach((el) => el.classList.add('is-visible'));
  } else if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          const parent = el.parentElement;
          if (parent) {
            const siblings = Array.from(parent.children).filter((c) => c.classList.contains('reveal'));
            const idx = siblings.indexOf(el);
            el.style.transitionDelay = Math.min(idx * 70, 420) + 'ms';
          }
          el.classList.add('is-visible');
          io.unobserve(el);
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('is-visible'));
  }

  /* ---------- Number count-up ---------- */
  const counters = document.querySelectorAll('[data-count]');
  if (counters.length && 'IntersectionObserver' in window && !reduceMotion) {
    const easeOut = (t) => 1 - Math.pow(1 - t, 3);
    const co = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          const target = parseFloat(el.getAttribute('data-count'));
          const isDecimal = !Number.isInteger(target);
          const duration = 1600;
          const start = performance.now();
          const step = (now) => {
            const p = Math.min((now - start) / duration, 1);
            const v = target * easeOut(p);
            el.textContent = isDecimal ? v.toFixed(1) : Math.floor(v);
            if (p < 1) requestAnimationFrame(step);
            else el.textContent = isDecimal ? target.toFixed(1) : target;
          };
          requestAnimationFrame(step);
          co.unobserve(el);
        });
      },
      { threshold: 0.4 }
    );
    counters.forEach((el) => co.observe(el));
  } else if (counters.length) {
    counters.forEach((el) => {
      const v = parseFloat(el.getAttribute('data-count'));
      el.textContent = Number.isInteger(v) ? v : v.toFixed(1);
    });
  }

  /* ---------- Smooth scroll with header offset ---------- */
  const HEADER_OFFSET = 72;
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const href = a.getAttribute('href');
      if (!href || href.length <= 1) return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.scrollY - HEADER_OFFSET;
      window.scrollTo({
        top,
        behavior: reduceMotion ? 'auto' : 'smooth'
      });
    });
  });

  /* ---------- Footer year ---------- */
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  /* ---------- Contact form ---------- */
  const form = document.getElementById('contactForm');
  if (form) {
    const TYPE_LABEL = {
      'general':   '30分無料相談',
      'ai-dx':     'AI・DX 導入相談',
      'web':       'Web 改善 AI 診断',
      'product':   'プロダクト導入相談',
      'pricing':   '見積り依頼',
      'x-partner': 'X Partner について',
      'intern':    'Build with us（インターン / アソシエイト）',
      'other':     'その他のご相談',
    };
    const METHOD_LABEL = {
      'online': 'オンライン',
      'email':  'メール',
      'phone':  '電話',
    };
    const TIMING_LABEL = {
      'asap':       'すぐ相談したい',
      '1month':     '1ヶ月以内',
      '3months':    '3ヶ月以内',
      'undecided':  '未定 / 情報収集中',
    };
    const PRODUCT_PREFILL = {
      'kigen':          'Kigenについて相談したい',
      'xcloud-connect': 'Connectについて相談したい',
      'connect':        'Connectについて相談したい',
      'xcloud-flow':    'Flowについて相談したい',
      'flow':           'Flowについて相談したい',
    };

    /* Pre-select radio + prefill textarea based on ?type= / ?product= URL params */
    try {
      const params = new URLSearchParams(window.location.search);
      const type = params.get('type');
      const product = params.get('product');

      // If ?product= is present, imply type=product (unless user set type explicitly)
      const effectiveType = type || (product ? 'product' : null);

      if (effectiveType && TYPE_LABEL[effectiveType]) {
        const radio = form.querySelector(`input[name="type"][value="${effectiveType}"]`);
        if (radio) radio.checked = true;
      }

      if (product && PRODUCT_PREFILL[product]) {
        const issue = document.getElementById('issue');
        if (issue && !issue.value) {
          issue.value = PRODUCT_PREFILL[product];
        }
      }
    } catch (_) {
      /* URLSearchParams missing — ignore */
    }

    /* Build a mailto: link from form values, then open it */
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      // Native validation first
      if (!form.checkValidity()) {
        form.reportValidity();
        // Scroll to first invalid field
        const first = form.querySelector(':invalid');
        if (first && 'scrollIntoView' in first) {
          first.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'center' });
          if (typeof first.focus === 'function') first.focus({ preventScroll: true });
        }
        return;
      }

      const data = new FormData(form);
      const get = (k) => (data.get(k) || '').toString().trim();

      const typeKey      = get('type');
      const methodKey    = get('contactMethod');
      const timingKey    = get('timing');
      const typeLabel    = TYPE_LABEL[typeKey] || 'お問い合わせ';
      const methodLabel  = METHOD_LABEL[methodKey] || '';
      const timingLabel  = TIMING_LABEL[timingKey] || '';

      const subject = `【${typeLabel}】${get('company') || ''} ${get('name') || ''}`.trim();

      const lines = [
        `■ 相談内容:    ${typeLabel}`,
        `■ 会社名:      ${get('company')}`,
        `■ お名前:      ${get('name')}`,
        `■ メール:      ${get('email')}`,
        `■ 電話番号:    ${get('phone') || '（未入力）'}`,
        `■ Web サイト:  ${get('website') || '（未入力）'}`,
        `■ 相談方法:    ${methodLabel || '（未選択）'}`,
        `■ 希望時期:    ${timingLabel || '（未選択）'}`,
        '',
        '■ 現在の課題・ご相談内容:',
        get('issue') || '（未記入）',
        '',
        '---',
        '送信元: https://xiora-official.com/contact.html',
      ];

      const body = lines.join('\r\n');
      const mailto = 'mailto:info@xiora-official.com'
        + '?subject=' + encodeURIComponent(subject)
        + '&body='    + encodeURIComponent(body);

      // Open user's mail client. Use location.href so behavior is consistent.
      window.location.href = mailto;
    });
  }

  /* ---------- Marquee (auto-flowing horizontal cards) ---------- */
  // 除外: .workflow (01→05 sequential 順序が重要、loop 化で「05 Drive」が先に見えて混乱)
  const MARQUEE_SELECTOR = [
    '.tech-wall', '.trust-cells', '.prod-sub-grid',
    '.cases', '.cases-grid', '.service-list',
    '.issues-list', '.plans', '.pricing-cards', '.learn-list',
    '.trust-grid', '.stack-grid', '.who-grid', '.dept-grid', '.cap-grid'
  ].join(',');

  document.querySelectorAll(MARQUEE_SELECTOR).forEach((el) => {
    if (el.dataset.marquee || !el.children.length) return;
    el.dataset.marquee = '1';

    // Wrap the target in a mask container to clip overflow + edge fade
    const mask = document.createElement('div');
    mask.className = 'marquee-mask';
    el.parentNode.insertBefore(mask, el);
    mask.appendChild(el);

    // Duplicate children for seamless loop
    const originals = Array.from(el.children);
    originals.forEach((child) => {
      const clone = child.cloneNode(true);
      clone.setAttribute('aria-hidden', 'true');
      clone.setAttribute('tabindex', '-1');
      // Force revealed state on clones (IntersectionObserver won't fire in animated track)
      clone.classList.add('is-visible');
      clone.querySelectorAll('.reveal').forEach((r) => r.classList.add('is-visible'));
      el.appendChild(clone);
    });
    // Also force originals visible (marquee track transforms break reveal timing)
    originals.forEach((child) => {
      child.classList.add('is-visible');
      child.querySelectorAll('.reveal').forEach((r) => r.classList.add('is-visible'));
    });
  });
})();
