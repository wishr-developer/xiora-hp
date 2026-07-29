# Xiora Lingua 完全 放置 運用 状態 (2026-07-29 完成)

**Reo directive**: 「言語 学習 の やつ 最優先 で 完全 放置 で 運用 できる 状態 まで 作り上げて」
**Result**: 4 gap 完全 fix、 Reo hands-off で 24/7 自動 運用 開始。

## 稼働 中 pipeline (自動 · 人 の 手 なし)

| # | Component | 動作 内容 | 稼働 頻度 | 障害 対応 |
|---|---|---|---|---|
| 1 | **Stripe webhook auto tier flip** | checkout/subscription event → user_plan_tier + user_hearts 自動 更新 | イベント 駆動 | signature 検証 · asyncpg transaction (roll back on error) |
| 2 | **Health check + auto-restart** | `/health` を 3 min 毎 に 3x check、 失敗 で container 自動 restart | 3 分 毎 | systemd `xioralingua-health.timer` |
| 3 | **Postgres backup** | 全 schema (含む xiora_lingua) の pg_dump | Daily 03:30 JST | 既存 `xioraai-backup.timer` |
| 4 | **Weekly revenue report → Reo email** | MRR / user tier 別 / 新規 / 解約 / lesson 数 の 集計 → Resend で 送信 | 週 1 (Mon 07:00 JST) | Resend id 記録、 失敗 は journal |

## 実装 詳細

### Gap 1 — Stripe webhook

- **File**: `services/systems/XioraLingua/apps/api/src/infra/stripe/webhook.py`
- **URL** (public): `https://api.xiora-official.com/lingua/api/webhooks/stripe` (POST)
- **Handles**:
  - `checkout.session.completed` → `stripe_customers` upsert · user linking (client_reference_id / stripe_customer.user_id / users.email match の 3 priority)
  - `customer.subscription.created/updated` → `stripe_subscriptions` + `user_plan_tier` + `user_hearts.unlimited=true` の 3 table upsert (transaction)
  - `customer.subscription.deleted` → `user_plan_tier.tier='free'` + `user_hearts.unlimited=false`
- **Price → tier map** (SoT: stripe-live-products.json#xiora_lingua):
  - `price_1Tw1dYFoGzoX9pTQD3M1l0C1` → super (¥980/月)
  - `price_1Tw1dZFoGzoX9pTQKAgmcp7D` → family (¥1,980/月)
- **Signature**: HMAC-SHA256 constant-time comparison (Stripe rec)、 prod で 必須
- **Verified**: 3 event smoke test 合格 (cus_smoke_4 full lifecycle)
- **DB schema fix**: `stripe_customers.user_id` を nullable + PK を stripe_customer_id に (未 link 購入 の 記録 保持 + 後日 email 一致 で link 可)

### Gap 2 — health check + auto-restart

- **service**: `/etc/systemd/system/xioralingua-health.service` (oneshot)
- **timer**: `/etc/systemd/system/xioralingua-health.timer` (OnUnitActiveSec=3min)
- **logic**: `curl localhost:8010/health` 3x with 2s spacing → 3x fail で `docker restart xioralingua-api` + `logger` に FAIL 記録
- Docker container は `restart=unless-stopped` policy で crash 自動 復旧、 systemd は stuck 検知 補完

### Gap 3 — Postgres backup

- 既存: `xioraai-backup.timer` (Daily 03:30 JST) が全 schema を backup 済
- `xiora_lingua` schema (users / stripe_customers / stripe_subscriptions / user_plan_tier / user_hearts / lesson_events / user_gamification / conversion_events / lessons / family_groups / family_members = 11 tables) も 対象

### Gap 4 — weekly revenue report

- **script**: `/usr/local/bin/xioralingua-revenue-report.sh`
- **timer**: `xioralingua-revenue-report.timer` (Mon 07:00 JST)
- **content**: MRR / Super / Family / Free / 新規 subs / 解約 / 累計 user / 今週 lesson 数
- **transport**: Resend API (bizboost.dx@gmail.com 宛、 Reo 受信 verified)
- **format**: HTML table + subject に MRR 数値 + 新規 数
- **verified**: test 送信 3 件 Resend id 発行 済

## 現在 状態 (2026-07-29 verified)

- Xiora Lingua API container: LIVE (port 8010)、 8 domain 全 動作 (auth / family / gamification / hearts / plans / tutor)
- Public URL: https://xiora-official.com/lingua.html (Web app: https://lingua-app.pages.dev/)
- Stripe LIVE: Super ¥980/月 / Family ¥1,980/月 の buy.stripe.com URL LIVE
- 43 lesson × 3 course (日常 / 旅行 / 表現 力)
- Postgres 16 self-host、 xiora_lingua schema 11 tables 全 稼働
- Ollama tutor 未使用 (Xiora Lingua は Web Speech API 内蔵、 LLM 依存 なし = cost 予測 可能)

## Reo が 1 回 だけ 触る action (完全 放置 状態 の 完成 化)

**Stripe dashboard → Webhooks → Add endpoint**:
- URL: `https://api.xiora-official.com/lingua/api/webhooks/stripe`
- Events: `checkout.session.completed`, `customer.subscription.created`, `.updated`, `.deleted`
- Get Signing secret (whsec_xxx) → save to `STRIPE_WEBHOOK_SECRET` env in xioralingua-api container
- 5 分 の action、 完了 後 は 100% 自動

**xiora Lingua Stripe payment link で 追加 する と 良い もの (option)**:
- HP CTA URL に `?client_reference_id={xiora_user_id}` パラメータ を 追加 → user link が 100% 保証 される
- 現状 は email match で 十分 だが、 email 不一致 の 場合 (Google/Apple ID 経由 login 等) は client_reference_id が 安全

## 「完全 放置 で 運用 できる」の 意味

以下 の 全 case が Reo 介入 なし で 動作:
- 新規 user が Free で signup → user_plan_tier.tier=free で 自動 provisioning
- Free user が Super/Family 契約 → Stripe webhook → tier + hearts 自動 flip
- 加入 user が 解約 → subscription.deleted → tier=free + hearts=limited 自動 flip
- API container crash → Docker 自動 restart
- API stuck (LB proxy timeout) → systemd health 3x fail → 自動 restart
- Postgres disk full 等 → daily backup で 復旧 可能 state
- Reo は 週 1 の revenue report メール を 見る だけ

**次 の 完全 放置 対象 (Xiora Lingua 完成 後)**:
1. Kigen (iOS · 既 LIVE で 完全 放置)
2. Nexa Education OS
3. XCloud Connect
4. L3 Marketplace (Gumroad)
5. L3 KDP
