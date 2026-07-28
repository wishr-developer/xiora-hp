# RapidAPI Provider Onboarding — xiora API

**Owner**: Reo (Xiora founder) / **Executed by**: Body Claude (deploy) + Reo (signup / KYC)
**Stream**: A (API monetization、 time-to-first-yen 14-30 日)
**Last updated**: 2026-07-28

---

## 0. 前提

- 3 API (business-registry / text-normalize / contact-extract) は `openapi.yaml` で spec 化 済
- Tier config は `pricing_tiers.json` (Freemium / Basic ¥1,980 / Pro ¥9,800 / Enterprise ¥49,800)
- 実 endpoint は Tokyo VPS (`xiora-official.com/api/*`、 Caddy reverse proxy) に deploy 済 前提

---

## 1. Reo action (5 min signup)

### 1.1 RapidAPI Provider account signup

1. https://rapidapi.com/provider にアクセス
2. `Sign up` → GitHub / Google / メール いずれか (推奨: `info@xiora-official.com`)
3. Profile:
   - Company name: `xiora`
   - Website: `https://xiora-official.com`
   - Support email: `info@xiora-official.com`
   - Country: `Japan`
4. 「Add your first API」 → 後述 の Body Claude が spec upload 実行 の 段階 で 触る のみ

### 1.2 Stripe Connect (payout 受取)

1. RapidAPI Provider dashboard → `Settings` → `Payouts`
2. Stripe Connect 「Connect account」 → xiora の 既存 Stripe account (`acct_1RcC1HFoGzoX9pTQ`) を 選択
3. 銀行 口座 は Stripe 側 で 既に 登録 済 前提 (追加 手続 不要)

**Reo action 合計: 5 分**

---

## 2. VPS endpoint 検証 (Body Claude execute)

### 2.1 前提 endpoint

| Path | Method | 実 backend | Cache |
|---|---|---|---|
| `/api/v1/companies/{corporate_number}` | GET | 国税庁 法人 番号 API wrapper + Postgres cache | 30 日 |
| `/api/v1/companies/search` | GET | 同上、 曖昧 検索 mode | 30 日 |
| `/api/v1/normalize/text` | POST | Xiora Lingua 内部 normalizer 転用 | なし |
| `/api/v1/normalize/address` | POST | 郵便 番号 辞書 (KEN_ALL.CSV) + 内部 mapper | 90 日 |
| `/api/v1/normalize/name` | POST | Xiora Lingua furigana mapper | なし |
| `/api/v1/extract/contact` | POST | XioraContactAPI (LLM=Ollama) + regex fallback | 24h (URL) |

### 2.2 Caddy config 追加 (VPS)

```
xiora-official.com {
  handle /api/* {
    reverse_proxy xai-public-apis:3013
  }
}
```

### 2.3 検証 command (Body Claude)

```
curl -s https://xiora-official.com/api/healthz
# → {"status":"ok"}

curl -sH "X-RapidAPI-Key: internal-test-key" \
  "https://xiora-official.com/api/v1/companies/2011101044774"
# → 200 with Company schema
```

---

## 3. OpenAPI spec upload

### 3.1 RapidAPI dashboard 経由

1. Provider dashboard → `Add New API`
2. Name: `xiora JP Business Data & Text Utilities`
3. Category: `Business` / secondary=`Text Analysis`
4. Import from OpenAPI:
   - Upload `services/systems/XAIPublicAPIs/rapidapi/openapi.yaml`
   - Base URL confirm: `https://xiora-official.com/api`
5. Auth: `Custom` → `X-RapidAPI-Key` header は RapidAPI proxy 側 で 自動 付与
6. Save

### 3.2 動作 確認 (Provider dashboard の テスト UI)

- 全 6 endpoint で `Test Endpoint` → 200 応答 確認
- 400 / 401 / 429 の error schema も サンプル confirm

---

## 4. Pricing tier 設定

### 4.1 dashboard 手順

1. Provider dashboard → `<API name>` → `Monetize` タブ
2. `pricing_tiers.json` の 4 tier を 上から 順に 追加:
   - Freemium (¥0, 100 req/day hard cap)
   - Basic (¥1,980/月, 10,000 req/月, overage ¥0.5/req)
   - Pro (¥9,800/月, 100,000 req/月, overage ¥0.3/req)
   - Enterprise (¥49,800/月, 1,000,000 req/月, overage ¥0.15/req)
3. Overage は `Per-request` mode で endpoint 単位 設定 (json の `endpoint_overage_pricing_jpy` 参照)
4. Currency: RapidAPI 標準 は USD、 為替 換算 は dashboard 自動

### 4.2 通貨 の 注意

- 表示 は JPY で 統一 (国内 顧客 前提)
- Stripe 側 の payout は USD で 着金、 為替 差 は月次 で 記帳
- 特商法 表記 上、 Xiora HP `/legal/tokusho.html` に 「RapidAPI Hub 経由 契約、 表示 価格 は 参考、 実 決済 は USD」 と 追記

---

## 5. Public listing 前 checklist

- [ ] `openapi.yaml` upload 完了、 6 endpoint 全て 200 応答
- [ ] 4 tier pricing 設定 完了、 overage 動作 確認 (Freemium で 101 req 目 が 429)
- [ ] API description (RapidAPI 上) に 以下 明記:
  - xiora 自社 SaaS (Nexa / XCloud Connect / Xiora Lingua) で 実 使用 中
  - 除外 領域 (投資 助言 / 士業 独占 / 医療 診断) は 一切 含まない
  - 出典 (国税庁 法人 番号 API) の attribution
- [ ] Xiora HP `/products/apis.html` へ の link を RapidAPI description に 追加
- [ ] Reo が RapidAPI Hub の public 化 ボタン を タップ (最終 承認)

---

## 6. Post-launch monitoring (Body Claude 自動 化)

- 日次: `services/systems/XAIPublicAPIs/scripts/rapidapi_daily.py` で 収益 · req 数 · error rate を fetch → `state.db.rapidapi_daily` に 記帳
- 週次: XAI Portal `/co/finance` に 反映
- Alert: error rate > 5% で Reo Gmail 通知 (既存 XAIOutreach pipeline 転用)

---

## 7. Known blocker

- **Postgres cache table (schema=xai_public_apis) 未 create** — Phase 1 で 未使用 だった ため。 Body Claude が deploy 前 に `CREATE SCHEMA xai_public_apis` + `companies_cache` table を alembic で 追加 必要。
- **`XioraContactAPI` 既存 asset の LLM path** — Ollama VPS `qwen2.5:7b` 前提、 GPU 不要 range で 動作 済 だが 100 req/日 上限 は 実 負荷 検証 未。
- **KEN_ALL.CSV (郵便 番号 辞書) の 月次 更新** — 日本 郵便 サイト から scrape、 launchd cron で 自動 化 必要。

---

## 8. Reo に 依頼 する order 明確 化

1. **今**: 何もしない (Body Claude が spec + pricing + LP 完成 させる)
2. **Body Claude 完了 report 受領 後**: 上記 §1 の RapidAPI signup + Stripe Connect 連携 (5 分)
3. **RapidAPI public 化 タップ**: §5 checklist を Reo が dashboard で 確認 して 「Publish」 (2 分)

**Reo total action: 7 分 (5 分 signup + 2 分 Publish タップ)**
