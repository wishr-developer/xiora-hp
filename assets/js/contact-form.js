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

    // Normalize: contact form uses "issue" textarea + "type"/"contactMethod"/"timing" fields
    const issueText = (payload.issue || payload.message || payload.detail || payload.body || '').toString();
    const contextParts = [];
    if (payload.contactMethod) contextParts.push('連絡希望: ' + payload.contactMethod);
    if (payload.timing) contextParts.push('タイミング: ' + payload.timing);
    const fullMessage = [issueText, contextParts.join(' / ')].filter(Boolean).join('\n\n---\n');

    const apiPayload = {
      product: payload.product || (['product'].includes(payload.type) ? 'general' : payload.type) || 'general',
      name: payload.name || '',
      email: payload.email || '',
      company: payload.company || '',
      phone: payload.phone || '',
      message: fullMessage,
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
      // 通信エラー時: メーラーを強制起動せず、 message + email 案内 のみ表示 (Web メール利用者への配慮)
      console.warn('contact-form POST failed:', err);
      showStatus('err', '送信に失敗しました。 通信環境をご確認の上、 再度お試しください。 継続する場合は info@xiora-official.com まで直接ご連絡ください。');
    } finally {
      if (submitBtn) { submitBtn.disabled = false; if (submitBtn.dataset._originalText) submitBtn.textContent = submitBtn.dataset._originalText; }
    }
  });
})();
