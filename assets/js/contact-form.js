/* Xiora contact form — mailto:fallback → POST /api/contact 昇格
 *
 * 動作:
 *   1. form submit を intercept
 *   2. JSON payload を api.xiora-official.com/api/contact に POST
 *   3. 成功 → 「送信完了」表示
 *   4. 失敗 or endpoint 未稼働 → 既存 mailto: に fallback (form.submit())
 */
(function () {
  'use strict';

  const CONTACT_API_URL = 'https://api.xiora-official.com/api/contact';  // DNS 追加後に有効
  const FALLBACK_MAILTO = 'info@xiora-official.com';

  const form = document.getElementById('contactForm');
  if (!form) return;

  // URL query params → prefill (revenue funnel: 商品ページ CTA `/contact.html?type=X&product=Y` を受ける)
  const params = new URLSearchParams(location.search);
  const typeParam = params.get('type');
  const productParam = params.get('product');
  const VALID_TYPES = ['general','ai-dx','web','product','pricing','x-partner','intern','other'];
  const VALID_PRODUCTS = ['aiverse','gourmie','tradeos','xcloud-connect','xcloud-flow','kigen','general','other'];

  if (typeParam && VALID_TYPES.includes(typeParam)) {
    const radio = form.querySelector(`input[name="type"][value="${typeParam}"]`);
    if (radio) radio.checked = true;
  }
  // Hidden product field so /api/contact receives the correct product tag
  if (productParam && VALID_PRODUCTS.includes(productParam)) {
    const hiddenProduct = document.createElement('input');
    hiddenProduct.type = 'hidden';
    hiddenProduct.name = 'product';
    hiddenProduct.value = productParam;
    form.appendChild(hiddenProduct);
  }
  // Hidden source field for attribution
  const hiddenSource = document.createElement('input');
  hiddenSource.type = 'hidden';
  hiddenSource.name = 'source';
  hiddenSource.value = 'xiora-official.com/contact.html' + (location.search || '');
  form.appendChild(hiddenSource);

  // hidden honeypot field (bot filter). CSS で display:none.
  const honeypot = document.createElement('input');
  honeypot.type = 'text';
  honeypot.name = 'website';
  honeypot.tabIndex = -1;
  honeypot.autocomplete = 'off';
  honeypot.style.position = 'absolute';
  honeypot.style.left = '-9999px';
  honeypot.setAttribute('aria-hidden', 'true');
  form.appendChild(honeypot);

  function serialize(f) {
    const data = new FormData(f);
    const obj = {};
    for (const [k, v] of data.entries()) {
      if (obj[k] !== undefined) {
        obj[k] = Array.isArray(obj[k]) ? obj[k].concat(v) : [obj[k], v];
      } else obj[k] = v;
    }
    return obj;
  }

  function showStatus(kind, text) {
    let el = document.getElementById('contact-form-status');
    if (!el) {
      el = document.createElement('div');
      el.id = 'contact-form-status';
      el.style.marginTop = '16px';
      el.style.padding = '12px 16px';
      el.style.borderRadius = '8px';
      el.style.fontSize = '14px';
      form.parentNode.insertBefore(el, form.nextSibling);
    }
    el.style.background = kind === 'ok' ? '#e6f9ee' : '#fee2e2';
    el.style.color = kind === 'ok' ? '#065f46' : '#991b1b';
    el.textContent = text;
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  form.addEventListener('submit', async function (ev) {
    ev.preventDefault();

    // Basic validation
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    const payload = serialize(form);

    // Normalize: contact form uses "type" for inquiry-type; API prefers "product" and "message"
    const apiPayload = {
      product: payload.product || (['product'].includes(payload.type) ? 'general' : payload.type) || 'general',
      name: payload.name || '',
      email: payload.email || '',
      company: payload.company || '',
      phone: payload.phone || '',
      message: (payload.message || payload.detail || payload.body || '').toString(),
      source: location.pathname,
      // 追加コンテキスト
      inquiry_type: payload.type || '',
      website: payload.website || '',  // honeypot
    };

    // Disable submit button while sending
    const submitBtn = form.querySelector('[type="submit"]');
    if (submitBtn) { submitBtn.disabled = true; submitBtn.dataset._originalText = submitBtn.textContent; submitBtn.textContent = '送信中…'; }

    try {
      const resp = await fetch(CONTACT_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(apiPayload),
      });

      const data = await resp.json().catch(() => ({}));

      if (resp.ok && data.ok) {
        showStatus('ok', `送信完了しました。24 時間以内にご連絡いたします (受付 ID: ${data.id})`);
        form.reset();
      } else if (resp.status === 429) {
        showStatus('err', '短時間に複数回送信されました。しばらく空けて再度お試しください。');
      } else if (data.error === 'validation_failed') {
        showStatus('err', `入力に不備があります: ${(data.fields || []).join(', ')}`);
      } else {
        throw new Error('server error');
      }
    } catch (err) {
      // Fallback: 既存 mailto:
      console.warn('contact-form POST failed, falling back to mailto:', err);
      const bodyText = Object.entries(apiPayload)
        .filter(([k, v]) => v && k !== 'website')
        .map(([k, v]) => `${k}: ${v}`)
        .join('\n');
      const mailto = `mailto:${FALLBACK_MAILTO}?subject=${encodeURIComponent('【お問い合わせ】Xiora HP')}&body=${encodeURIComponent(bodyText)}`;
      showStatus('err', 'API 送信に失敗したため、メーラーを起動します。うまく起動しない場合は info@xiora-official.com に直接ご連絡ください。');
      setTimeout(() => { window.location.href = mailto; }, 1500);
    } finally {
      if (submitBtn) { submitBtn.disabled = false; if (submitBtn.dataset._originalText) submitBtn.textContent = submitBtn.dataset._originalText; }
    }
  });
})();
