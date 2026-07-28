# Reo Action — Gumroad JP signup + 5 SKU upload (2026-07-28)

**Owner**: Reo (Xiora 単独 founder)
**Executed by (代理人)**: Body Claude (Opus 4.7)
**Purpose**: Stream C (Digital template marketplace) の time-to-first-yen 3-7 日 を 達成 する ため の Reo 明示 action 一覧。
**Total Reo hands-on time**: 約 5-10 分 (signup) + 各 SKU upload は 代理人 draft を Reo が copy-paste 実行 (計 15-20 分)

---

## 0. 事前 準備 — 用意 する もの (Reo)

| 項目 | 内容 | 場所 |
|---|---|---|
| Business email | `xiora00000@gmail.com` (会社 main) | 既存 |
| 事業 名 | `xiora` (lowercase 統一) | brand rule |
| 事業 住所 | 〒150-0043 東京都 渋谷区 道玄坂 1-10-8 渋谷道玄坂東急ビル 2F-C | memory |
| 電話 番号 | 070-9165-0203 | memory |
| 銀行 口座 | 既存 Xiora 用 口座 (Bizboost.dx 名義 or 個人 名義) | Vault 参照 |
| マイナンバー | JP tax reporting 用 (Gumroad JP 要求 の 場合) | Reo 保管 |
| profile 画像 | xiora logo 512x512 | `/Users/kutsuzawareo/Desktop/XAI/Xiora_HP/assets/img/icon-512.png` |
| cover 画像 | xiora Marketplace hero 1200x630 | 代理人 が Canva MCP で 生成 済 の OGP を 流用 可 |

---

## 1. Gumroad JP account signup (5 分)

### 1.1 URL

```
https://gumroad.com/signup
```

※ Gumroad は US Delaware 本社 だが、 日本 居住 · JP 銀行 口座 で 販売 可能 (Stripe Connect + PayPal 経由 で 円 → 円 payout)。

### 1.2 signup form 入力

| Field | 入力 値 |
|---|---|
| Email | `xiora00000@gmail.com` |
| Password | Vault `xiora:gumroad:password` に 登録 (代理人 が 事後 export) |
| Country | Japan |
| I agree to Terms | チェック |

→ email 認証 リンク (受信箱 で click)

### 1.3 profile 設定

| Field | 入力 値 |
|---|---|
| Store name | `xiora` |
| Store URL | `xiora.gumroad.com` (SKU URL の 前提) |
| Bio | `xiora は AI Infrastructure を 事業 に 実装 する 会社。 内部 で 動いて いる code · pipeline · asset を そのまま template 化 して 販売 して います。` |
| Profile picture | `/Users/kutsuzawareo/Desktop/XAI/Xiora_HP/assets/img/icon-512.png` |
| Cover image | 代理人 が 後日 supply |

### 1.4 Payout 設定 — Bank info

| Field | 入力 値 |
|---|---|
| Account type | Business |
| Business name | `xiora` (英字) |
| Business address | `Shibuya-ku Dogenzaka 1-10-8 Shibuya Dogenzaka Tokyu Bldg 2F-C, Tokyo 150-0043, Japan` |
| Payout method | Bank transfer (JP 銀行 口座) or PayPal |
| Bank name / SWIFT / IBAN | Reo 既存 Xiora 口座 参照 |

※ Gumroad は 月末 payout (最低 $10 相当 から)、 手数料 は 販売 額 の 10% + Stripe 手数料 3.6%。

### 1.5 Tax settings

| Field | 入力 値 |
|---|---|
| Tax country | Japan |
| Tax ID | (法人 化 前 は skip、 個人 事業主 で マイナンバー 記載) |
| VAT | Not applicable (JP) |

---

## 2. 商品 タグ · カテゴリ 選択 (最初 の 商品 登録 時 に 選ぶ)

| SKU | Gumroad Category | Tags (up to 5) |
|---|---|---|
| Solo SaaS Postgres 16 boilerplate | Software Development / Web Development | `nextjs`, `fastapi`, `postgres`, `stripe`, `boilerplate` |
| Xiora Cold Email Pipeline | Business & Money / Sales | `cold-email`, `playwright`, `smtp`, `automation`, `outreach` |
| AI 秘書 Persistent Memory Kit | Software Development / AI | `ai-agent`, `ollama`, `postgres`, `persistent-memory`, `secretary` |
| Xiora Autonomous QA 4-stage cascade | Software Development / Testing | `qa`, `claude-code`, `cursor`, `aider`, `prompt-engineering` |
| Japanese SMB 500-target list | Business & Money / Sales | `smb`, `japan`, `cold-outreach`, `research`, `csv` |

---

## 3. 5 SKU upload flow (各 3-4 分 × 5 = 15-20 分)

代理人 が draft する 4 asset を Reo が copy-paste → upload:

1. **Title** (Gumroad 用 · 60 字 以内)
2. **Short description** (150 字 以内、 store list 表示)
3. **Description** (Markdown 3,000-5,000 字、 Xiora HP SKU page から 転載)
4. **Cover image** (1280x720 png)
5. **Product file** (zip, 実 asset · 代理人 が supply)

### 3.1 各 SKU の Custom URL (slug)

Xiora HP の SKU page CTA URL と 一致 させる:

| SKU | Custom URL slug |
|---|---|
| Solo SaaS Postgres 16 boilerplate | `solo-saas-postgres-16-boilerplate` |
| Xiora Cold Email Pipeline | `xiora-cold-email-pipeline` |
| AI 秘書 Persistent Memory Kit | `ai-persistent-memory-kit` |
| Xiora Autonomous QA 4-stage cascade | `xiora-qa-4-stage-cascade` |
| Japanese SMB 500-target list | `jp-smb-500-target-list` |

→ 完成形 URL 例: `https://xiora.gumroad.com/l/solo-saas-postgres-16-boilerplate`

### 3.2 各 SKU の 価格

| SKU | Price (JPY) | Currency |
|---|---|---|
| Solo SaaS Postgres 16 boilerplate | 19800 | JPY |
| Xiora Cold Email Pipeline | 9800 | JPY |
| AI 秘書 Persistent Memory Kit | 14800 | JPY |
| Xiora Autonomous QA 4-stage cascade | 7800 | JPY |
| Japanese SMB 500-target list | 4980 | JPY |

※ Gumroad で JPY 直接 表示 する 場合 は Store settings > Payments で `Show prices in JPY` を ON。

### 3.3 各 SKU の legal 追記

各 SKU の Description 末尾 に 以下 を 追加:

```
--
販売 者: xiora
所在 地: 〒150-0043 東京都 渋谷区 道玄坂 1-10-8 渋谷道玄坂東急ビル 2F-C
連絡: info@xiora-official.com
特定商取引法 に基づく表記: https://xiora-official.com/legal/tokusho.html
デジタル コンテンツ の 性質 上、 購入 後 の 返品 · 返金 は 原則 として お受け しかね ます。
```

---

## 4. 販売 開始 後 の 動作 確認 (代理人 実行)

- [ ] 5 SKU の Gumroad URL が LIVE (公開) status
- [ ] Xiora HP `/marketplace/templates/` の 5 CTA が Gumroad に 正しく 遷移
- [ ] test 決済 (Gumroad の view mode で dry-run 可)
- [ ] 販売 発生 時 の email 通知 (`xiora00000@gmail.com` に 届く)
- [ ] Xiora HP sitemap.xml に 6 URL 登録 済

---

## 5. Reo 側 の 完了 定義

- [ ] Gumroad account LIVE (`https://xiora.gumroad.com/` に アクセス 可)
- [ ] 5 SKU 公開 (各 slug URL が 404 で ない)
- [ ] Payout 口座 登録 完了 (「payment method needed」 warning が 消えて いる)
- [ ] 代理人 に signup 完了 report (Vault に password 登録 fwd 用)

---

## 6. 潜在 blocker

| 事象 | 対応 |
|---|---|
| Gumroad JP で JPY 直接 販売 不可 (USD forced) | USD 換算 (¥100 = $0.67 目安) で 再登録、 Xiora HP の 円 表示 は そのまま (Gumroad checkout で 自動 換算) |
| 銀行 口座 rejection | PayPal Business account で 代替 (Reo 既存 の Bizboost 名義) |
| Store URL `xiora` 既に 取られて いる | `xiora-marketplace` or `xiora-templates` で 代替 (SKU page CTA URL 側 も 一括 update) |
| Tax ID 要求 | 個人 事業主 で マイナンバー 記載 (Gumroad 内部 保管 · 外部 開示 なし) |

---

## 7. 完了 後 の 代理人 fw 事項

- [ ] `services/systems/XioraBI/` に Gumroad revenue tracker 追加 (Gumroad API key 発行 が 必要、 Reo Vault へ)
- [ ] Xiora HP insights に「xiora Marketplace 開始 (2026-07-28)」記事 draft
- [ ] X post draft (marketing pipeline)
- [ ] SKU 実 asset (zip 5 個) の 準備 (Nexa / Lingua / Rei / QA cascade / SMB list の 抽出 · 秘匿 除去 · README 作成)

---

## 8. Reo hands-on 合計 見積 (再掲)

- Signup + profile: 5 分
- Payout 銀行 情報 登録: 3 分
- 5 SKU upload (代理人 draft copy-paste): 15-20 分
- **合計 25-30 分** で time-to-first-yen 3-7 日 phase に 突入

---

**Owner**: Reo · **Executed by (代理人)**: Body Claude (Opus 4.7) · **Created**: 2026-07-28
