/* =====================================================
   Xiora — Analytics bootstrap
   - Looks for a <meta name="ga4-id" content="G-XXXXXXXXXX">
     in <head>. If a valid-looking ID is present, loads gtag.js
     and initializes GA4. If not, does nothing (no requests, no cookies).
   - Honors Do-Not-Track and Global Privacy Control.
   - Tracks conversion-adjacent events: hero_cta_click, product_click,
     product_cta_click, contact_submit, phone_click, email_click,
     plus lang_toggle.
   ===================================================== */
(function () {
  'use strict';

  const meta = document.querySelector('meta[name="ga4-id"]');
  const id = meta && meta.getAttribute('content');
  if (!id || !/^G-[A-Z0-9]{6,}$/.test(id)) return;

  // Respect user privacy preferences
  const dnt = navigator.doNotTrack === '1' || window.doNotTrack === '1';
  const gpc = navigator.globalPrivacyControl === true;
  if (dnt || gpc) return;

  // Load gtag.js
  const s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
  document.head.appendChild(s);

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', id, {
    anonymize_ip: true,
    send_page_view: true
  });

  /* ------------------------------------------------------------------
   * Event helpers
   * ---------------------------------------------------------------- */
  function track(name, params) {
    try {
      gtag('event', name, params || {});
    } catch (_) { /* swallow */ }
  }

  function currentProductSlug() {
    // Derive product slug from URL: /products/<slug>.html → <slug>
    const p = window.location.pathname;
    const m = p.match(/\/products\/([\w-]+)\.html$/);
    if (m) return m[1];
    if (p === '/products/' || p === '/products/index.html') return 'hub';
    return null;
  }

  /* ------------------------------------------------------------------
   * Delegated click tracking
   * ---------------------------------------------------------------- */
  document.addEventListener('click', function (e) {
    const el = e.target && e.target.closest ? e.target : null;
    if (!el) return;

    // 1. Hero CTA — only top-page hero (section.hero, not .page-hero)
    const heroCta = el.closest('.hero__actions .btn--primary, .hero__actions .btn--ghost');
    if (heroCta) {
      track('hero_cta_click', {
        page_path: window.location.pathname,
        cta_variant: heroCta.classList.contains('btn--primary') ? 'primary' : 'ghost',
        cta_href: heroCta.getAttribute('href') || ''
      });
      return;
    }

    // 2. Product card — clicks on Kigen / Connect / Flow / Coming Soon cards
    const prodCard = el.closest('.prod-card');
    if (prodCard) {
      const href = prodCard.getAttribute('href') || '';
      let product = 'unknown';
      const m = href.match(/\/products\/([\w-]+)\.html/);
      if (m) product = m[1];
      else if (prodCard.classList.contains('prod-card--soon')) product = 'coming-soon';
      track('product_click', {
        product: product,
        page_path: window.location.pathname,
        link_url: href
      });
      return;
    }

    // 3. Product CTA — CTA buttons on /products/* detail pages
    if (window.location.pathname.startsWith('/products/')) {
      const prodCta = el.closest(
        '.page-hero__actions a.btn, .section--dark a.btn'
      );
      if (prodCta) {
        const slug = currentProductSlug() || 'hub';
        track('product_cta_click', {
          product: slug,
          cta_variant: prodCta.classList.contains('btn--primary') ? 'primary' : 'ghost',
          cta_href: prodCta.getAttribute('href') || ''
        });
        return;
      }
    }

    // 4. Phone click
    const phoneLink = el.closest('a[href^="tel:"]');
    if (phoneLink) {
      track('phone_click', {
        page_path: window.location.pathname,
        link_url: phoneLink.getAttribute('href') || ''
      });
      return;
    }

    // 5. Email click
    const emailLink = el.closest('a[href^="mailto:"]');
    if (emailLink) {
      track('email_click', {
        page_path: window.location.pathname,
        link_url: emailLink.getAttribute('href') || ''
      });
      return;
    }

    // 6. Language toggle (retained)
    if (el.closest('[data-lang-toggle]')) {
      track('lang_toggle', {
        from: document.documentElement.lang || 'ja'
      });
    }
  }, { passive: true });

  /* ------------------------------------------------------------------
   * Contact form submission tracking
   * ---------------------------------------------------------------- */
  document.addEventListener('submit', function (e) {
    const form = e.target;
    if (!form || form.id !== 'contactForm') return;
    const typeInput = form.querySelector('input[name="type"]:checked');
    const params = new URLSearchParams(window.location.search);
    track('contact_submit', {
      inquiry_type: typeInput ? typeInput.value : 'unknown',
      product: params.get('product') || 'none',
      page_path: window.location.pathname
    });
  }, true /* capture so we fire before the mailto redirect */);
})();
