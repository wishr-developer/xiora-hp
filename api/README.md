# Xiora HP — Vercel Serverless Functions

Zero-dep Node.js 20 serverless functions deployed alongside the static site.

## Functions

### `r.js` — Rakuten CVR redirect
- Endpoint: `/r?a=<article_slug>&l=<link_id>`
- Purpose: 302 redirect to Rakuten affiliate URLs + structured single-line log
- Config: `_links.json` sibling file (link_id → target_url mapping)

### `dl.js` — Post-purchase digital delivery verifier (multi-product)
- Endpoint: `/api/dl?session_id=<stripe_checkout_session_id>`
- Purpose: Verify Stripe Checkout Session → serve packaged digital content
- On success: 200 with content (HTML inline, ZIP/MD attachment)
- On failure: 302 redirect to product LP with `?err=<code>`

#### Product map (SoT lives in `api/dl.js` `PRODUCT_MAP`)

| Slug | Price (JPY) | Type | On-disk filename | Download name |
|------|-------------|------|------------------|----------------|
| `xiora-aos-guide-2026` | 1980 | HTML inline | `xiora-aos-guide-2026.html` | (inline view) |
| `xiora-aos-toolkit-2026` | 4980 | ZIP attach | `aos-toolkit-2026-08f759.zip` | `xiora-aos-toolkit-2026.zip` |
| `xiora-handler-prompt-pack-2026` | 2980 | MD attach | `xiora-handler-prompt-pack-2026-a9e412.md` | `xiora-handler-prompt-pack-2026.md` |
| `xiora-rakuten-template-pack-2026` | 1980 | ZIP attach | `rakuten-template-pack-2026-37b2c9.zip` | `xiora-rakuten-template-pack-2026.zip` |

On-disk filenames carry a random 6-hex suffix so a direct request to
`/dl/*.zip` cannot be guessed from the public slug alone.

#### Product resolution priority (in order)

1. `session.metadata.product_slug` (set by Payment Link metadata)
2. `session.line_items[0].price.metadata.xiora_product` (set at Price creation)
3. Amount-only fallback — only if the amount uniquely identifies a product.
   (Note: AOS Guide and Rakuten Template Pack both cost ¥1,980, so the amount
   fallback rejects with `product_mismatch` for that amount — metadata is
   required to disambiguate.)

## Environment variables (Vercel Project Settings → Environment Variables)

### `STRIPE_SECRET_KEY` (required for `dl.js`)
- Scope: **Production** (also Preview if you want preview testing)
- Format: Stripe secret key or restricted key
  - Live: `sk_live_...` OR restricted key `rk_live_...`
  - Test: `sk_test_...` OR restricted key `rk_test_...`
- Minimum permissions if using restricted key:
  - `Checkout Sessions` — Read
  - `Prices` — Read (needed for expanded `line_items.data.price`)

**Reo action** (one-time, ~2 min):
```
1. Open https://dashboard.stripe.com/apikeys (Xiora account)
2. Create restricted key:
   - Name: xiora-hp-dl-verifier
   - Permissions: Checkout Sessions = Read, Prices = Read (all others = None)
3. Copy the rk_live_... value
4. Vercel dashboard → xiora-hp project → Settings → Environment Variables
5. Add: Key=STRIPE_SECRET_KEY, Value=<the rk_live_...>, Env=Production
6. Redeploy (or wait for next auto-deploy from push)
```

## Testing the download flow (Stripe test mode)

Prerequisite: `STRIPE_SECRET_KEY` env var set to a test key (`sk_test_...`).

1. Open the test-mode Payment Link for a product (from Stripe dashboard).
2. Complete checkout with test card: `4242 4242 4242 4242`.
3. Stripe redirects back to `https://xiora-official.com/api/dl?session_id={CHECKOUT_SESSION_ID}`.
4. The verifier serves the correct file for that product.
5. Error codes (via `?err=<code>` on the LP redirect):
   - `bad_session` — session_id malformed / missing
   - `server_config` — env var `STRIPE_SECRET_KEY` not set
   - `verify_failed` — Stripe API returned non-200 (invalid key / wrong account)
   - `not_paid` — payment_status !== "paid"
   - `product_mismatch` — no metadata slug + amount ambiguous
   - `content_missing` — the on-disk file is missing from `dl/`

## Adding a new direct-sale product

1. Zip / write the content into `Xiora_HP/dl/<slug>-<random-suffix>.zip`.
2. Add an entry to `PRODUCT_MAP` in `api/dl.js`.
3. Create the Stripe Product / Price / Payment Link with
   `metadata.xiora_product=<slug>` on all three, and set the Payment Link
   after-completion redirect to `https://xiora-official.com/api/dl?session_id={CHECKOUT_SESSION_ID}`.
4. Update `content/products.json` and rebuild.
