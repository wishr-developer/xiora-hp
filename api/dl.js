// Xiora HP — Post-purchase digital delivery verifier
// Vercel Serverless Function (Node.js 20 runtime, zero external deps).
//
// Request:  GET /api/dl?session_id=<stripe_checkout_session_id>
// Behavior:
//   1. Verify the Stripe Checkout Session via GET /v1/checkout/sessions/<id>
//   2. Require payment_status === "paid"
//   3. Match session metadata.product_slug (or amount_total) against expected
//   4. Return the packaged HTML content (dl/xiora-aos-guide-2026.html)
//   5. On any failure → 302 redirect to product LP with ?err=<code>
//
// Env vars (set on Vercel):
//   STRIPE_SECRET_KEY — Stripe restricted key with read access to
//                       checkout sessions (rak_... or sk_live_... / sk_test_...).
//                       See docs at Xiora_HP/api/README.md
//
// No external deps. Uses global fetch (Node 20 built-in).

const fs = require("fs");
const path = require("path");

const PRODUCT_SLUG = "xiora-aos-guide-2026";
const PRODUCT_LP = `/products/${PRODUCT_SLUG}.html`;
const EXPECTED_AMOUNT_JPY = 1980; // ¥1,980 (Stripe amount_total for JPY is unit yen)

// Load content once per cold start.
let CONTENT = null;
function loadContent() {
  if (CONTENT) return CONTENT;
  try {
    // dl/ sits next to api/ at repo root → ../dl/<slug>.html from this file.
    const p = path.join(__dirname, "..", "dl", `${PRODUCT_SLUG}.html`);
    CONTENT = fs.readFileSync(p, "utf-8");
  } catch (e) {
    CONTENT = null;
    console.log(JSON.stringify({
      ts: new Date().toISOString(),
      event: "dl.load_error",
      error: String(e && e.message || e),
    }));
  }
  return CONTENT;
}

function redirectErr(res, code) {
  const location = `${PRODUCT_LP}?err=${encodeURIComponent(code)}`;
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
  // Stripe HTTP Basic auth: username=secret_key, password=empty.
  const auth = Buffer.from(`${secretKey}:`).toString("base64");
  const url = `https://api.stripe.com/v1/checkout/sessions/${encodeURIComponent(sessionId)}`;
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

module.exports = async (req, res) => {
  const url = new URL(req.url, "https://xiora-official.com");
  const sessionId = url.searchParams.get("session_id") || "";
  const ua = req.headers["user-agent"] || "";

  // 0) Basic session_id shape check (Stripe session IDs start with cs_ and are
  // longer than 20 chars). Prevents fetch storms on random requests.
  if (!sessionId || !/^cs_[A-Za-z0-9_]{10,}$/.test(sessionId)) {
    console.log(JSON.stringify({
      ts: new Date().toISOString(),
      event: "dl.reject",
      reason: "bad_session_id_shape",
      ua: truncate(ua, 128),
    }));
    return redirectErr(res, "bad_session");
  }

  // 1) Env var check.
  const secretKey = process.env.STRIPE_SECRET_KEY;
  if (!secretKey) {
    console.log(JSON.stringify({
      ts: new Date().toISOString(),
      event: "dl.reject",
      reason: "no_env_stripe_key",
    }));
    return redirectErr(res, "server_config");
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
    return redirectErr(res, "verify_failed");
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
    return redirectErr(res, "not_paid");
  }

  // 4) Product match: prefer metadata.product_slug, fall back to amount_total.
  const meta = s.metadata || {};
  const slugMeta = truncate(meta.product_slug || "", 64);
  const slugOk = slugMeta === PRODUCT_SLUG;
  const amountOk = s.amount_total === EXPECTED_AMOUNT_JPY && (s.currency || "").toLowerCase() === "jpy";
  if (!slugOk && !amountOk) {
    console.log(JSON.stringify({
      ts: new Date().toISOString(),
      event: "dl.reject",
      reason: "product_mismatch",
      slug_meta: slugMeta,
      amount_total: s.amount_total,
      currency: truncate(s.currency || "", 8),
      session_id_prefix: truncate(sessionId, 12),
    }));
    return redirectErr(res, "product_mismatch");
  }

  // 5) Load packaged content.
  const content = loadContent();
  if (!content) {
    console.log(JSON.stringify({
      ts: new Date().toISOString(),
      event: "dl.reject",
      reason: "content_missing",
    }));
    return redirectErr(res, "content_missing");
  }

  // 6) Serve the packaged HTML.
  console.log(JSON.stringify({
    ts: new Date().toISOString(),
    event: "dl.serve",
    product_slug: PRODUCT_SLUG,
    session_id_prefix: truncate(sessionId, 12),
    slug_meta_ok: slugOk,
    amount_ok: amountOk,
    ua_family: /mobile|iphone|android/i.test(ua) ? "mobile" : "desktop",
  }));

  res.setHeader("Cache-Control", "private, no-store, no-cache, must-revalidate");
  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.setHeader("Referrer-Policy", "no-referrer");
  res.setHeader("X-Robots-Tag", "noindex, nofollow");
  res.writeHead(200);
  res.end(content);
};
