/* =====================================================
   Xiora — Analytics bootstrap
   - Looks for a <meta name="ga4-id" content="G-XXXXXXXXXX">
     in <head>. If a valid-looking ID is present, loads gtag.js
     and initializes GA4. If not, does nothing (no requests, no cookies).
   - Honors Do-Not-Track and Global Privacy Control.
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

  // Optional: track language toggle events
  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-lang-toggle]')) {
      gtag('event', 'lang_toggle', {
        from: document.documentElement.lang || 'ja'
      });
    }
  });
})();
