# Xiora 5+ 収入源 拡張 計画 (2026-07-28)

**Owner**: Reo (Xiora 単独 founder) / **Executed by**: Body Claude (Opus 4.7)
**North Star**: time-to-first-yen 昇順 で 5+ 独立 revenue stream を 確立
**Constraint**: 無資格 事業 のみ / 対面 NG / Reo outgoing money NG / fact-only

---

## 1. Concept explainer — 7 streams framework と なぜ 5+ が 効くのか

### 1.1 古典 「7 streams of income」 分類 (IRS ベース)

米国 では 個人 の 所得 を 税務 上 7 種類 に 分類 する 慣習 が あり、 これ が 「7 income streams」 の 語源。

| # | Stream (英) | Stream (日) | 性質 | 例 |
|---|---|---|---|---|
| 1 | Earned income | 給与 · 労働 所得 | active | 雇用 · consulting · 時間 拘束 |
| 2 | Profit / Business income | 事業 所得 | active | SaaS 販売 · digital product · サービス |
| 3 | Interest income | 利子 所得 | passive | 預金 · 債券 · P2P lending |
| 4 | Dividend income | 配当 所得 | passive | 株式 · ETF · REIT |
| 5 | Rental income | 賃貸 所得 | semi-passive | 不動産 · Airbnb · 機材 rental |
| 6 | Capital gains | 譲渡 所得 | event-driven | 株式 · 不動産 · asset 売却 |
| 7 | Royalty income | 著作権 · 使用料 | passive | 印税 · 特許 · license · music |

### 1.2 Tom Corley "Rich Habits" study の 実 データ

Tom Corley が 233 名 の self-made millionaire を 5 年 追跡 した 結果:

- **65%** が first million を 稼ぐ 前 に **3 種類 以上** の income stream を 持っていた
- **45%** が **4 種類 以上**
- **29%** が **5 種類 以上**

つまり 「7 streams 全部 持て」 ではなく、 **「3-5 stream で 十分 圧倒的 少数 派 に なる」** が 実像。

### 1.3 2024-2026 の refinement — creator economy 統合

近年 の solopreneur 統計 (Goal Group 2026 report, 847 verified income reports) では:
- Median 年商 $94k、 top 10% で $380k+、 top 1% で $1.2M+
- Top 25% は **passive 割合 35-55%**、 その 大半 が **digital products + affiliate**
- **Affiliate が 2026 最速 成長 stream**、 全 他 stream と stack 可能
- Creator with **3+ stream** = single source の **5-6x** 収益

### 1.4 なぜ 5+ が xiora に とって 重要 か

1. **Diversification** — SaaS 単一 依存 は Stripe account ban / platform 依存 で 一夜 消滅 リスク
2. **Resilience** — 1 stream の 下振れ を 他 stream が cover、 精神 的 平静
3. **Compounding** — SaaS で 作った asset を そのまま digital product / affiliate / API に 再利用 = 追加 build 労力 少
4. **Autonomous execution 適性** — Reo hands-off で 24/7 稼働 する stream ほど 単独 founder に 適合

---

## 2. Xiora 現状 — 7 streams の どこ に 位置 するか

| Stream | 現状 | 該当 asset | 月商 概算 |
|---|---|---|---|
| Earned income | **なし** (Reo 意図 的 に 雇用 拒否) | — | ¥0 |
| **Business (SaaS)** | **稼働** | Kigen / Xiora Lingua / Nexa / XCloud Connect (Stripe LIVE) | ¥600-19,800/月 subscription |
| **Business (retail SKU)** | **稼働** | 7 digital SKU (¥980-9,800、 Stripe direct link) | 単発 決済 |
| Interest income | **なし** | — | ¥0 |
| Dividend income | **なし** | — | ¥0 |
| Rental income | 対象 外 (不動産 なし、 対面 NG) | — | ¥0 |
| Capital gains | 対象 外 (投資 助言 業 回避、 event-driven) | — | ¥0 |
| **Royalty / Affiliate (2026-07-28 開始)** | **launched** | Rakuten ROOM LIVE / Amazon Associates pending / A8.net pending | ¥0 (初日) |

**Xiora が 現在 稼働 している 分類**: 2/7 (Business の 2 sub-form + Royalty の launched-not-yielding)

**Reo directive 「5+ 収入 源」 達成 に は あと 3 stream 追加 必要**。

---

## 3. 5+ 新 stream 拡張 plan (each with concrete implementation)

### Stream A — **API monetization (RapidAPI / 自社 gateway)**

- **Category**: Royalty income (usage-based license)
- **Concrete implementation**: `services/systems/XAIPublicAPIs/` 既存 asset を base に、 3 API を RapidAPI Hub に list
  1. **JP Business Registry API** — 帝国 database 相当 の 会社 情報 lookup (法人 番号 API を wrapper) → freemium ¥0 / ¥1,980/月 / ¥9,800/月
  2. **Japanese Text Normalization API** — 全角 半角 / 送り仮名 / 住所 正規化 (Xiora Lingua の 副産物) → $0.005/request
  3. **Xiora Contact Extraction API** — HP から 会社 情報 抽出 (`XioraContactAPI` 既存 asset) → $0.01/request
- **Time-to-first-yen**: **14-30 日** (RapidAPI list 承認 3-7 日 + traffic 獲得)
- **Reo action**: **RapidAPI Provider signup + Stripe Connect (5 分 KYC)**、 以降 hands-off
- **Phase 1 projection**: Month 1 = ¥0-3,000 / Month 2 = ¥5,000-30,000 / Month 3 = ¥20,000-100,000
- **Body Claude 可 execute now**: (1) 3 API の OpenAPI spec 作成 (2) RapidAPI 用 Docker package (3) pricing tier config (4) Xiora HP に API 商品 page 追加

### Stream B — **KDP 電子書籍 (印税)**

- **Category**: Royalty income (印税)
- **Concrete implementation**: Xiora 既存 コンテンツ を 電子書籍 化
  1. 「AI で 完全 無人 SaaS を 12 個 立ち上げた 記録」 (Xiora HP insights + docs 統合、 4-6 万字)
  2. 「Japanese Solo Founder の Zero-spend Playbook」 (英語 版、 海外 市場)
  3. 「AI エージェント 20 名 を Postgres で 動かす」 (Rei + Xiora AI Org spec の 実務 版)
- **Time-to-first-yen**: **7-30 日** (KDP 審査 24-72h + 販売 開始)
- **Reo action**: **KDP account signup + 銀行 口座 + マイナンバー 登録 (10 分 KYC)** 、 以降 hands-off
- **Phase 1 projection**: 1 冊 ¥500 × 70% royalty × 20-100 部/月 = ¥7,000-35,000/月/冊。 3 冊 で ¥21,000-105,000/月
- **Body Claude 可 execute now**: (1) 3 冊 分 の 原稿 生成 (既存 docs から reorganize) (2) 表紙 (Canva MCP) (3) キーワード SEO 最適化 (4) KDP metadata (title/subtitle/description/A+ content)

### Stream C — **Digital template / boilerplate marketplace (Gumroad + Xiora HP 直販)**

- **Category**: Business income (digital product、 但し low-touch = 実質 royalty 的)
- **Concrete implementation**: Xiora の 内部 code / spec / template を SKU 化
  1. **「Solo SaaS Postgres 16 boilerplate」** (Next.js + FastAPI + Stripe webhook、 Nexa/Lingua base) — ¥19,800 一括
  2. **「Xiora Cold Email Pipeline」** (Playwright + Gmail SMTP + 4 段 follow-up、 XAIOutreach 抽出) — ¥9,800
  3. **「AI 秘書 Persistent Memory Kit」** (Rei 基盤 の 汎用 版) — ¥14,800
  4. **「Xiora Autonomous QA 4-stage cascade」** (build/fact/UX/browser MCP) — ¥7,800
  5. **「Japanese SMB Cold Outreach 500-target list」** (research 済 リスト、 CSV) — ¥4,980
- **Time-to-first-yen**: **3-7 日** (Gumroad 即日 approve + Xiora HP に 商品 page)
- **Reo action**: **Gumroad JP account 開設 (5 分 KYC)**、 以降 hands-off
- **Phase 1 projection**: 5 SKU × avg ¥12,000 × 2-8 sales/月 = ¥24,000-96,000/月 (Month 2-3 で SEO traffic 立ち上げ 後)
- **Body Claude 可 execute now**: (1) 5 SKU の README + demo repo (2) Gumroad 商品 page copy (3) Stripe direct link (Gumroad 経由 と dual) (4) Xiora HP `/marketplace/templates/` セクション

### Stream D — **Sponsor / brand deal (note + X + Xiora HP insights)**

- **Category**: Business income (advertising / sponsored content)
- **Concrete implementation**: 既存 SNS + content asset を sponsor 掲載 面 化
  1. note magazine (¥500/月 × N 人) + 単発 有料 記事 (¥980-2,980)
  2. Xiora HP `/insights/` の 週次 記事 に SaaS 企業 tie-up (sponsored 明記、 景表法 遵守)
  3. X (@Xiora_official) の SNS post に PR 案件 (product placement、 stealth NG)
- **Time-to-first-yen**: **21-45 日** (audience 数 が 一定 必要、 note magazine の 月末 決済 まで)
- **Reo action**: **note Pro signup + 銀行 口座 (5 分 KYC)**、 以降 hands-off
- **Phase 1 projection**: note magazine ¥500 × 20-100 人 = ¥10,000-50,000/月 + 単発 記事 ¥1,500 × 3-10 = ¥4,500-15,000/月
- **Body Claude 可 execute now**: (1) note magazine の 3 号 記事 draft (2) sponsor 掲載 面 の kit (rate card) (3) X post schedule (4) 景表法 遵守 [PR] 表記 template

### Stream E — **App Store / iOS in-app purchase (印税 相当)**

- **Category**: Royalty income (Apple が 70% royalty 支払い、 印税 モデル)
- **Concrete implementation**: 既存 iOS app 7 個 (Kigen LIVE + 6 submission-ready) の in-app purchase / subscription 完全 稼働
  1. Kigen Lifetime IAP (MISSING_METADATA を 解消) — ¥4,980 一括
  2. Xiora Lingua iOS の 3 tier (¥490/¥980/¥1,980 月額)
  3. Xiora Pulse / Smart Finance / Vow / Stub / Quil (6 app) の App Store 提出 完了
- **Time-to-first-yen**: **7-45 日** (App Store 審査 1-7 日 + traffic)
- **Reo action**: **Apple Developer $99 支払い (既存)** + **各 app の pricing tier 確定 タップ (10 分 × 6 app)**
- **Phase 1 projection**: Kigen ¥600/月 × 10-50 subs = ¥6,000-30,000/月 + Lifetime × 5-20 = ¥25,000-100,000/月。 他 6 app 立ち上げ で 累積 ¥50,000-200,000/月
- **Body Claude 可 execute now**: (1) Kigen Lifetime IAP metadata 補完 (2) 6 app の App Store screenshot / description / keyword 完成 (3) TestFlight beta 準備

### Stream F — **Bonus: Stock photo / AI generated asset library (印税)**

- **Category**: Royalty income
- **Concrete implementation**: Canva MCP + AI 画像 生成 で Xiora が 既に 作った 画像 (thumbnail / brand asset) を Adobe Stock / Shutterstock Contributor に upload
- **Time-to-first-yen**: **30-60 日** (審査 + traffic)
- **Reo action**: **Adobe Stock Contributor signup (10 分 KYC + マイナンバー)**、 hands-off
- **Phase 1 projection**: 100 asset upload × $0.25-2.00/download × 2-10 downloads/asset/月 = ¥3,000-30,000/月
- **Body Claude 可 execute now**: 既存 全 画像 asset の EXIF / metadata / keyword 整形 → upload queue

---

## 4. Priority order — 収益 影響 大 × Reo action 少

| 順位 | Stream | 収益 potential (Phase 1 上振れ) | Reo action | time-to-first-yen | 判定 |
|---|---|---|---|---|---|
| 🥇 **1st** | **Stream C (Digital template Gumroad)** | ¥96,000/月 | Gumroad signup 5 分 | **3-7 日** | 最速 + Reo 5 分 + 既存 code 転用 |
| 🥈 2nd | **Stream E (iOS IAP 完全 稼働)** | ¥200,000/月 | 各 app pricing タップ 10 分 × 6 | 7-45 日 | 既存 6 app が 眠っている、 収益 上限 高 |
| 🥉 3rd | **Stream B (KDP 電子書籍)** | ¥105,000/月 | KDP signup 10 分 | 7-30 日 | 既存 docs から 3 冊 生成 可能、 印税 永続 |
| 4th | **Stream A (API monetization)** | ¥100,000/月 | RapidAPI signup 5 分 | 14-30 日 | XAIPublicAPIs 既存 asset 転用、 usage-based で 上限 なし |
| 5th | **Stream D (Sponsor / note magazine)** | ¥65,000/月 | note Pro signup 5 分 | 21-45 日 | audience 依存、 立ち上がり 遅い |
| 6th | Stream F (Stock photo) | ¥30,000/月 | Adobe Contributor 10 分 | 30-60 日 | bonus、 手間 対 リターン 低め |

### 4.1 Reo action 合計 = **35 分 (5 KYC signup)** → 5 stream 追加

現状 の Business 2 form + Royalty (affiliate) = 3 分類 に、 上記 5 stream 追加 で **合計 7 stream 分類 に 到達** (Corley 上位 29% ゾーン)。

---

## 5. Body Claude が 今 すぐ 単独 execute 可能 な list

### 5.1 Stream C (Gumroad template) — 今 週 中 完了 可

- [ ] `services/systems/XioraApps/marketplace/` 配下 に 5 SKU の README + demo repo 作成
- [ ] `Xiora_HP/pages/marketplace/templates/index.html` 新規 商品 page (5 SKU list)
- [ ] Gumroad JP の 商品 metadata (title/description/cover) 一式 draft
- [ ] Stripe direct link (Gumroad 併用 / dual channel)
- [ ] Xiora HP hero / navigation に `/marketplace/templates` link 追加
- **Reo blocker**: Gumroad JP account signup 5 分 のみ

### 5.2 Stream B (KDP 電子書籍) — 今 週 中 に 原稿 3 冊 生成

- [ ] `deliverables/kdp/book1_ai_solo_saas_12/manuscript.md` 生成 (既存 Xiora HP insights + docs 統合 40,000 字)
- [ ] `deliverables/kdp/book2_zero_spend_playbook_en/manuscript.md` (英語 版 30,000 words)
- [ ] `deliverables/kdp/book3_ai_agent_postgres/manuscript.md` (Rei + AI Org spec 実務 版)
- [ ] Canva MCP で 各 冊 の 表紙 3 patterns (A/B test 用)
- [ ] KDP metadata (title / subtitle / description / 7 keywords / 2 categories) 一式
- **Reo blocker**: KDP account signup 10 分 + 銀行 口座 情報 (既存 Xiora account 流用) のみ

### 5.3 Stream E (iOS IAP 完全 稼働) — 既存 asset 補完 のみ

- [ ] Kigen Lifetime IAP の MISSING_METADATA 項目 一括 補完 (App Store Connect API)
- [ ] Xiora Lingua iOS の 3 tier pricing config (`ios/XioraLingua/StoreConfig.swift`)
- [ ] 6 app (Pulse/Smart Finance/Vow/Stub/Quil + 1) の App Store screenshot generation (Canva MCP + fastlane)
- [ ] 6 app の description / keyword ASO 最適化
- **Reo blocker**: 各 app pricing tier の 最終 タップ (App Store Connect UI、 10 分 × 6)

### 5.4 Stream A (API monetization) — 3 API を RapidAPI list 準備

- [ ] `services/systems/XAIPublicAPIs/rapidapi/openapi.yaml` 3 API の OpenAPI 3.1 spec
- [ ] Docker image (VPS 稼働、 rate limit + auth + billing metering webhook)
- [ ] RapidAPI provider dashboard 用 の pricing tier JSON
- [ ] Xiora HP `/products/apis/` 商品 page + SDK snippet (Python/JS/Go)
- **Reo blocker**: RapidAPI Provider signup 5 分 + Stripe Connect 連携 のみ

### 5.5 Stream D (note magazine + sponsor) — 記事 draft 前倒し

- [ ] note magazine 3 号 分 (¥500/月) 記事 draft (Xiora AI ops 内部 記録 が ネタ 供給 源)
- [ ] Xiora HP insights 記事 の 末尾 に sponsor 枠 (rate card link)
- [ ] X (@Xiora_official) の PR 案件 kit (rate / audience / [PR] 表記 template)
- **Reo blocker**: note Pro signup 5 分

### 5.6 全 stream 横断

- [ ] Xiora HP `/revenue-streams/` 内部 dashboard (Reo だけ 見える、 XAI Portal 経由) で 5 stream の 日次 revenue 集計
- [ ] Stripe / Gumroad / KDP / RapidAPI / App Store Connect の 全 API を `services/systems/XioraBI/` で 統合 (既存 asset)
- [ ] Reo action queue (`docs/REO_ACTION_QUEUE_2026-07-28.md`) に 「5 KYC signup 35 分」 として 一括 追加

---

## 6. 除外 事業 (memory constraint 遵守)

- **投資 助言 / 金融 商品 取引** (Stream 6 Capital gains 系) — 金商法 違反 リスク、 完全 除外
- **税務 / 法務 相談 系** — 士業 独占 業務、 完全 除外
- **医療 / 薬事 系 (薬機法)** — 完全 除外
- **不動産 賃貸** — 対面 + Reo capital NG、 除外
- **P2P lending / 高利 貸 系 (Stream 3 Interest 一部)** — 貸金 業 免許 不要 range のみ 検討 (現状 除外)

---

## 7. Summary card

- **現状**: 3 分類 (SaaS sub / retail SKU / affiliate)
- **追加 5 stream**: Gumroad template / iOS IAP / KDP / API / sponsor
- **達成 後**: **合計 7 stream 分類** (Corley study 上位 29% ゾーン)
- **Reo action 合計**: **35 分 (5 KYC signup)**
- **Body Claude autonomous execute**: 上記 5.1-5.6 の 全 item (100+ file 作成 / edit)
- **Phase 1 (Month 3) 合計 上振れ projection**: **¥500,000-600,000/月**
- **Time-to-first-yen 最速 stream**: Stream C (Gumroad template、 **3 日**)

---

## Sources

- [Rich Habits Study — Background and Methodology (Tom Corley)](https://richhabits.net/rich-habits-study-background-and-methodology/)
- [7 Streams of Income: How the Average Millionaire Builds Wealth (debtfreedr)](https://www.debtfreedr.com/7-streams-of-income/)
- [7 Streams of Income of Millionaires According to IRS (goodfinancialcents)](https://www.goodfinancialcents.com/7-streams-of-income-of-millionaires-according-to-irs/)
- [Solopreneur Income Report 2026 (Goal Group)](https://goal-group.com/articles/tools-comparisons/solopreneur-income-report-real-revenue-benchmarks-/)
- [10 Passive Income Ideas for Solopreneurs 2026 (Creator OS)](https://creatoros.me/blog/10-lucrative-passive-income-ideas-for-solopreneurs-in-2026)
- [Monetize Your API on RapidAPI in 2026 (1xAPI)](https://1xapi.com/blog/how-to-monetize-api-rapidapi-pricing-strategy-usage-tracking-2026)
- [API Economy: How Developers Make Money with APIs in 2026 (Idlen)](https://www.idlen.io/blog/api-economy-developers-make-money-apis-2026/)
- [Why KDP Authors Should Use Amazon Associates (Just Publishing Advice)](https://justpublishingadvice.com/why-you-need-to-be-an-amazon-affiliate-if-you-are-an-author/)
- [36 Passive Income Ideas 2026 (Shopify)](https://www.shopify.com/blog/passive-income-ideas)
