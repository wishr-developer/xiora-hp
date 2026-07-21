# Xiora HP — Vercel Serverless Functions

Zero-dep Node.js 20 serverless functions deployed alongside the static site.

## Functions

### `r.js` — Rakuten CVR redirect
- Endpoint: `/r?a=<article_slug>&l=<link_id>`
- Purpose: 302 redirect to Rakuten affiliate URLs + structured single-line log
- Config: `_links.json` sibling file (link_id → target_url mapping)

### `dl.js` — Post-purchase digital delivery verifier
- Endpoint: `/api/dl?session_id=<stripe_checkout_session_id>`
- Purpose: Verify Stripe Checkout Session → serve packaged HTML content
- Product: `xiora-aos-guide-2026` (Xiora Autonomous Company OS 実践ガイド 2026)
- Content source: `dl/xiora-aos-guide-2026.html`
- On success: 200 HTML + `Cache-Control: private, no-store`
- On failure: 302 redirect to `/products/xiora-aos-guide-2026.html?err=<code>`

## Environment variables (Vercel Project Settings → Environment Variables)

### `STRIPE_SECRET_KEY` (required for `dl.js`)
- Scope: **Production** (also Preview if you want preview testing)
- Format: Stripe secret key or restricted key
  - Live: `sk_live_...` OR restricted key `rk_live_...`
  - Test: `sk_test_...` OR restricted key `rk_test_...`
- Minimum permissions if using restricted key:
  - `Checkout Sessions` — Read
  - (nothing else needed; we only GET sessions, never mutate)
- Where to get it: https://dashboard.stripe.com/apikeys
  - Recommendation: create a **restricted key** limited to Checkout Sessions Read
    so a leak cannot drain funds or mutate customer data.

**Reo action** (one-time, ~2 min):
```
1. Open https://dashboard.stripe.com/apikeys (Xiora account: acct_1RcC1HFoGzoX9pTQ)
2. Create restricted key:
   - Name: xiora-hp-dl-verifier
   - Permissions: Checkout Sessions = Read (all others = None)
3. Copy the rk_live_... value
4. Vercel dashboard → xiora-hp project → Settings → Environment Variables
5. Add: Key=STRIPE_SECRET_KEY, Value=<the rk_live_...>, Env=Production
6. Redeploy (or wait for next auto-deploy from push)
```

## Product verification logic (`dl.js`)

The function accepts a purchase as valid when EITHER:

1. `session.metadata.product_slug === "xiora-aos-guide-2026"`, OR
2. `session.amount_total === 1980 AND session.currency === "jpy"`

(Belt-and-suspenders — Stripe Payment Links may or may not carry metadata
depending on how they were created. Amount match is the fallback so the flow
still delivers on legitimate ¥1,980 JPY payments.)

## Testing the download flow (Stripe test mode)

Prerequisite: `STRIPE_SECRET_KEY` env var set to a test key (`sk_test_...`).

1. Open the test-mode Payment Link for the product (from Stripe dashboard).
2. Complete checkout with test card: `4242 4242 4242 4242`, any future date,
   any 3-digit CVC, any postal code.
3. Stripe redirects back to the success URL (should be
   `https://xiora-official.com/api/dl?session_id={CHECKOUT_SESSION_ID}`).
4. The `dl.js` function verifies with Stripe, serves the packaged HTML.
5. If anything fails, you'll land on the product LP with an `?err=<code>` query
   parameter — check the code to diagnose:
   - `bad_session` — session_id malformed / missing
   - `server_config` — env var `STRIPE_SECRET_KEY` not set
   - `verify_failed` — Stripe API returned non-200 (invalid key / wrong account)
   - `not_paid` — payment_status !== "paid"
   - `product_mismatch` — neither metadata.product_slug nor amount matched
   - `content_missing` — `dl/xiora-aos-guide-2026.html` not deployed

## Stripe Payment Link success URL configuration

When creating the Payment Link in Stripe dashboard, set the After-payment
success URL to:

```
https://xiora-official.com/api/dl?session_id={CHECKOUT_SESSION_ID}
```

Stripe substitutes `{CHECKOUT_SESSION_ID}` at redirect time.
