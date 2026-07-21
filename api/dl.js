// Xiora HP — Post-purchase digital delivery verifier (multi-product)
// Vercel Serverless Function (Node.js 20 runtime, zero external deps).
//
// Request:  GET /api/dl?session_id=<stripe_checkout_session_id>
// Behavior:
//   1. Verify the Stripe Checkout Session via GET /v1/checkout/sessions/<id>
//      (with line_items expanded so we can inspect the purchased Price/Product).
//   2. Require payment_status === "paid"
//   3. Resolve which product was bought (via metadata.product_slug on session,
//      line_items[0].price.metadata.xiora_product, or amount fallback)
//   4. Look up product config in PRODUCT_MAP and serve the packaged file:
//        - HTML  -> serve inline text/html (Content-Disposition: inline)
//        - ZIP   -> stream application/zip (Content-Disposition: attachment)
//        - MD    -> text/markdown (attachment)
//   5. On any failure -> 302 redirect to product LP with ?err=<code>
//
// Env vars (set on Vercel):
//   STRIPE_SECRET_KEY - Stripe restricted key with read access to Checkout
//                       Sessions (rk_..., sk_live_..., sk_test_...).
//                       Minimum permissions: Checkout Sessions Read + Prices
//                       Read (needed for line_items[].price expansion).

const fs = require("fs");
const path = require("path");

// ---------------------------------------------------------------------------
// Product map — SoT for all direct-sale digital products.
// filename fields use the on-disk name INCLUDING the random suffix so that the
// dl/*.zip file cannot be guessed from the public product slug.
// ---------------------------------------------------------------------------
const PRODUCT_MAP = {
  // 1. AOS Guide (¥1,980) — the original HTML guide
  "xiora-aos-guide-2026": {
    lp: "/products/xiora-aos-guide-2026.html",
    filename: "xiora-aos-guide-2026.html",
    mime: "text/html; charset=utf-8",
    disposition: "inline",
    expectedAmount: 1980,
  },
  // 2. AOS Toolkit (¥4,980) — zip package
  "xiora-aos-toolkit-2026": {
    lp: "/products/xiora-aos-toolkit-2026.html",
    filename: "aos-toolkit-2026-08f759.zip",
    mime: "application/zip",
    disposition: "attachment",
    downloadName: "xiora-aos-toolkit-2026.zip",
    expectedAmount: 4980,
  },
  // 3. Handler Prompt Pack (¥2,980) — markdown
  "xiora-handler-prompt-pack-2026": {
    lp: "/products/xiora-handler-prompt-pack-2026.html",
    filename: "xiora-handler-prompt-pack-2026-a9e412.md",
    mime: "text/markdown; charset=utf-8",
    disposition: "attachment",
    downloadName: "xiora-handler-prompt-pack-2026.md",
    expectedAmount: 2980,
  },
  // 4. Rakuten Template Pack (¥1,980) — zip package
  "xiora-rakuten-template-pack-2026": {
    lp: "/products/xiora-rakuten-template-pack-2026.html",
    filename: "rakuten-template-pack-2026-37b2c9.zip",
    mime: "application/zip",
    disposition: "attachment",
    downloadName: "xiora-rakuten-template-pack-2026.zip",
    expectedAmount: 1980,
  },
  // 5. Cold Email Template Pack (¥980) — markdown
  "xiora-cold-email-pack-2026": {
    lp: "/products/xiora-cold-email-pack-2026.html",
    filename: "xiora-cold-email-pack-2026-8d6ec2.md",
    mime: "text/markdown; charset=utf-8",
    disposition: "attachment",
    downloadName: "xiora-cold-email-pack-2026.md",
    expectedAmount: 980,
  },
  // 6. Vault Setup Guide (¥1,480) — markdown
  "xiora-vault-setup-guide-2026": {
    lp: "/products/xiora-vault-setup-guide-2026.html",
    filename: "xiora-vault-setup-guide-2026-fdf6ed.md",
    mime: "text/markdown; charset=utf-8",
    disposition: "attachment",
    downloadName: "xiora-vault-setup-guide-2026.md",
    expectedAmount: 1480,
  },
  // 7. Founder Pack Bundle (¥14,800) — redirect to /founder-pack-thanks.html (not direct download)
  "xiora-founder-pack-bundle-2026": {
    lp: "/products/xiora-founder-pack-bundle-2026.html",
    bundleRedirect: "/founder-pack-thanks.html",
    expectedAmount: 14800,
  },
};

// Amount-only fallback map (used when metadata is missing). If two products
// share the same amount (AOS Guide ¥1,980 vs Rakuten Template Pack ¥1,980),
// this falls back to product_mismatch — metadata is mandatory in that case.
function amountFallbackSlug(amount) {
  const matches = Object.entries(PRODUCT_MAP).filter(([, cfg]) => cfg.expectedAmount === amount);
  if (matches.length === 1) return matches[0][0];
  return null;
}

// ---------------------------------------------------------------------------
// Content loader with a small in-memory cache (per cold start).
// ---------------------------------------------------------------------------
const CACHE = new Map();
function loadContent(filename) {
  if (CACHE.has(filename)) return CACHE.get(filename);
  try {
    const p = path.join(__dirname, "..", "dl", filename);
    const buf = fs.readFileSync(p);
    CACHE.set(filename, buf);
    return buf;
  } catch (e) {
    console.log(JSON.stringify({
      ts: new Date().toISOString(),
      event: "dl.load_error",
      filename,
      error: String(e && e.message || e),
    }));
    return null;
  }
}

function redirectErr(res, lp, code) {
  const location = `${lp || "/products/"}?err=${encodeURIComponent(code)}`;
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("Referrer-Policy", "no-referrer");
  res.writeHead(302, { Location: location });
  res.end();
}

function truncate(s, n) {
  if (!s) return "";
  return String(s).slice(0, n);
}

async function verifySession(sessionId, secretKey) {
  const auth = Buffer.from(`${secretKey}:`).toString("base64");
  // Expand line_items so we can read price.metadata.xiora_product.
  const url = `https://api.stripe.com/v1/checkout/sessions/${encodeURIComponent(sessionId)}?expand[]=line_items.data.price`;
  try {
    const resp = await fetch(url, {
      method: "GET",
      headers: {
        "Authorization": `Basic ${auth}`,
        "Accept": "application/json",
      },
    });
    if (!resp.ok) {
      return { ok: false, reason: `stripe_status_${resp.status}` };
    }
    const body = await resp.json();
    return { ok: true, session: body };
  } catch (e) {
    return { ok: false, reason: `stripe_fetch_error: ${String(e && e.message || e).slice(0, 120)}` };
  }
}

// Resolve which product was purchased. Priority:
//   1. session.metadata.product_slug (Payment Link with metadata)
//   2. line_items[0].price.metadata.xiora_product
//   3. Amount fallback (only if unambiguous)
function resolveProductSlug(session) {
  const meta = session.metadata || {};
  if (meta.product_slug && PRODUCT_MAP[meta.product_slug]) {
    return { slug: meta.product_slug, source: "session_metadata" };
  }
  const li = (session.line_items && session.line_items.data) || [];
  for (const item of li) {
    const pmeta = (item.price && item.price.metadata) || {};
    if (pmeta.xiora_product && PRODUCT_MAP[pmeta.xiora_product]) {
      return { slug: pmeta.xiora_product, source: "price_metadata" };
    }
  }
  const amount = session.amount_total;
  const currency = (session.currency || "").toLowerCase();
  if (currency === "jpy") {
    const fallback = amountFallbackSlug(amount);
    if (fallback) return { slug: fallback, source: "amount_fallback" };
  }
  return { slug: null, source: "none" };
}

module.exports = async (req, res) => {
  const url = new URL(req.url, "https://xiora-official.com");
  const sessionId = url.searchParams.get("session_id") || "";
  const ua = req.headers["user-agent"] || "";

  // 0) Basic session_id shape check.
  if (!sessionId || !/^cs_[A-Za-z0-9_]{10,}$/.test(sessionId)) {
    console.log(JSON.stringify({
      ts: new Date().toISOString(),
      event: "dl.reject",
      reason: "bad_session_id_shape",
      ua: truncate(ua, 128),
    }));
    return redirectErr(res, "/products/", "bad_session");
  }

  // 1) Env var check.
  const secretKey = process.env.STRIPE_SECRET_KEY;
  if (!secretKey) {
    console.log(JSON.stringify({
      ts: new Date().toISOString(),
      event: "dl.reject",
      reason: "no_env_stripe_key",
    }));
    return redirectErr(res, "/products/", "server_config");
  }

  // 2) Verify with Stripe.
  const v = await verifySession(sessionId, secretKey);
  if (!v.ok) {
    console.log(JSON.stringify({
      ts: new Date().toISOString(),
      event: "dl.reject",
      reason: v.reason,
      session_id_prefix: truncate(sessionId, 12),
    }));
    return redirectErr(res, "/products/", "verify_failed");
  }

  const s = v.session;

  // 3) Payment status must be paid.
  if (s.payment_status !== "paid") {
    console.log(JSON.stringify({
      ts: new Date().toISOString(),
      event: "dl.reject",
      reason: "not_paid",
      payment_status: truncate(s.payment_status || "", 32),
      session_id_prefix: truncate(sessionId, 12),
    }));
    return redirectErr(res, "/products/", "not_paid");
  }

  // 4) Resolve product slug.
  const { slug, source } = resolveProductSlug(s);
  if (!slug) {
    console.log(JSON.stringify({
      ts: new Date().toISOString(),
      event: "dl.reject",
      reason: "product_mismatch",
      amount_total: s.amount_total,
      currency: truncate(s.currency || "", 8),
      session_id_prefix: truncate(sessionId, 12),
    }));
    return redirectErr(res, "/products/", "product_mismatch");
  }
  const cfg = PRODUCT_MAP[slug];

  // 4b) Bundle redirect handling — no direct file; forward to the download
  //     center HTML page which reveals individual asset links after re-verify.
  if (cfg.bundleRedirect) {
    const target = `${cfg.bundleRedirect}?session_id=${encodeURIComponent(sessionId)}`;
    console.log(JSON.stringify({
      ts: new Date().toISOString(),
      event: "dl.bundle_redirect",
      product_slug: slug,
      resolve_source: source,
      session_id_prefix: truncate(sessionId, 12),
    }));
    res.setHeader("Cache-Control", "private, no-store");
    res.setHeader("Referrer-Policy", "no-referrer");
    res.setHeader("X-Robots-Tag", "noindex, nofollow");
    res.writeHead(302, { Location: target });
    res.end();
    return;
  }

  // 5) Load packaged content.
  const content = loadContent(cfg.filename);
  if (!content) {
    console.log(JSON.stringify({
      ts: new Date().toISOString(),
      event: "dl.reject",
      reason: "content_missing",
      product_slug: slug,
    }));
    return redirectErr(res, cfg.lp, "content_missing");
  }

  // 6) Serve.
  console.log(JSON.stringify({
    ts: new Date().toISOString(),
    event: "dl.serve",
    product_slug: slug,
    resolve_source: source,
    session_id_prefix: truncate(sessionId, 12),
    ua_family: /mobile|iphone|android/i.test(ua) ? "mobile" : "desktop",
    bytes: content.length,
  }));

  res.setHeader("Cache-Control", "private, no-store, no-cache, must-revalidate");
  res.setHeader("Referrer-Policy", "no-referrer");
  res.setHeader("X-Robots-Tag", "noindex, nofollow");
  res.setHeader("Content-Type", cfg.mime);
  if (cfg.disposition === "attachment") {
    const name = cfg.downloadName || cfg.filename;
    res.setHeader("Content-Disposition", `attachment; filename="${name}"`);
  } else {
    res.setHeader("Content-Disposition", "inline");
  }
  res.setHeader("Content-Length", content.length);
  res.writeHead(200);
  res.end(content);
};
