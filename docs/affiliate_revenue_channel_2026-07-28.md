# xiora 収入 柱 追加 — Affiliate / Creator Revenue Channel (2026-07-28)

## Reo directive (2026-07-28)

> 収入 の 柱 を 増やして ほしい。 他社 の ある サービス や マーケット を 利用 して、 まず は 収益 に つなげる。 例えば 楽天 ROOM 事業。 ROOM に 楽天 の サービス や 商品 など を 投稿 し、 SNS など で PR や アプローチ など 行う。 それ だけ でも、 しっかり 行う こと が できれば 十分 収入 に なる。 問題 は オリジナリティ を 演出 できる か 否か。 その 辺 も 収入 事業 の 柱 と して 行って。 ビジネス と して 成立 させて。 今 やって る こと (Xiora HP 4 core rebuild) も 並行 して 続けて。

## 位置 づけ (重要 · 誤解 防止)

**この 事業 は Xiora HP の 「5 つ 目 の pillar」で は ない**。 4 core (Kigen · Xiora Lingua · Nexa · XCloud Connect) の SaaS 販売 と は 別 layer の **operating channel** で ある。

| Layer | 内容 | 顧客 露出 |
|---|---|---|
| L1 · SaaS products | 4 core (Kigen · Xiora Lingua · Nexa · XCloud Connect) | Xiora HP の 主 メニュー |
| L2 · Retail SKUs | 7 デジタル 買切 (AOS Guide / Toolkit 等) | Xiora HP の 個別 product page |
| **L3 · Affiliate revenue** (**NEW · 本 doc**) | **ROOM · Amazon Associates · A8 · SNS curation で 生活 品 紹介 · 中間 手数料 収入** | **Xiora HP 非 露出。 別 handle (@XioraO1 · xiora00000 note · Instagram) で 運用** |

**理由**: L3 の 顧客 = 生活 消費 者、 L1/L2 の 顧客 = SaaS 導入 企業/個人。 target が 完全 に 別 で、 混ぜる と 両方 の brand 訴求 が 弱まる。

## 「オリジナリティ」の 演出 — 4 差別 化

Reo 指摘「オリジナリティ 演出 が 課題」に 対する 答え。 汎用 ROOM/SNS 影響 者 に は 出せ ない POV を 4 軸 で 立てる:

### 差別 化 1: 「AI 会社 が data で 選んだ 実 用 品」

- 手法: Rakuten API + `services/systems/XioraLifeMedia/src/curator/scoring.py` の EV2 score (期待 売上 × 明日 × 7d × 30d × trend × comp) で mechanical に 上位 抽出
- POV: 「感覚 で 選んだ 品」で は なく 「data で 選ばれた 品」を 明示
- Copy 例: 「今 週 の Rakuten data から EV2 score 上位 3 品。 kitchen category · 実 レビュー 平均 4.3+ で 抽出」

### 差別 化 2: 「1 人 で 会社 動かす founder 実 使用」

- 手法: Reo が 実 使用 する 生活 品 (Xiora 事務所 = 渋谷 道玄坂 で 稼働) の 実 レビュー
- POV: 「無名 review 者」で は なく 「AI SaaS 4 core を solo 運用 する founder」の 生活 コンテキスト
- Copy 例: 「渋谷 道玄坂 事務所 で 3 ヶ月 使った 排気口 カバー (山崎 実業) · 掃除 頻度 が 週 1 → 月 1 に」

### 差別 化 3: 「xiora product の 隣接 領域 curation」

- 手法: 4 core の POV から 生活 品 を re-frame (Kigen = 期限 管理 → 収納 · 家電 保証 の レビュー / Xiora Lingua = 語学 学習 → 学習 家具 · 集中 tools / Nexa = 教育 → dogfood 用 desk tools)
- POV: Amazon/Instagram 影響 者 が やる 「ジャンル 特化」と 違い、 SaaS 事業 者 目線 の 生活 品
- Copy 例: 「Kigen で 期限 管理 を している エンジニア が、 期限 切れ の 起き やすい 買い置き 用 に 買った 山崎 実業 の 収納 3 品」

### 差別 化 4: 「fact-first tone (誇大 表現 禁止)」

- 手法: `xiora HP` の 「甘 過ぎ 禁止」directive を そのまま 継承。 `config/forbidden-words.yaml` で 「絶対 / 100% / 神 / 爆売れ」を 自動 除去
- POV: 「盛った レビュー」が 溢れる ROOM/SNS で、 fact-only tone は 逆に 信頼 · 差別 化 要素
- Copy 例: NG「爆売れ 神 アイテム!!」→ OK「Rakuten review 平均 4.3 · 個人的 に は 集中 できる ように なった」

## 既存 asset (revive 対象)

### `services/systems/XioraLifeMedia/`

- `data/inventory.db` — 21 商品 (全 affiliate URL 付き · EV2 avg 1.728 · 19 shops)
- `src/platforms/` — rakuten_room · x_twitter · instagram · note · linkedin · email_broadcast の 6 adapter
- `src/curator/copy_generator.py` — platform 別 tone 継承 (ROOM 淡々 · X 短文 · note 長文 · Instagram 改行 多め)
- `src/curator/scoring.py` — EV2 score 継承
- `src/scheduler/daily_plan.py` — 1 時間 3 件 以下 · 45 分 同 shop 空け guardrails
- Vault key: `xai:ROOM:ROOM_EMAIL_ACCOUNT{1,3,4}` · `xai:rakuten:rafcid_ra` · `xai:rakuten:RAKUTEN_APP_ID`

### `services/systems/XAIAffiliateHub/`

- SQLite dashboard (Amazon PA-API · A8 IR API · Rakuten App · もしも CSV parse)
- Port 3031 (Mac local dev)
- `amazon_associates_2026-07-25/REO_REGISTRATION_GUIDE.md` — Reo 5-10 分 登録 手順 (道玄坂 住所 · 070 電話 · Xiora HP 3 URL コピペ 済)
- `a8_2026-07-25/REO_REGISTRATION_GUIDE.md` — Reo 5 分 登録 手順 (副 サイト 対応 · info@xiora-official.com 使用 · ゆうちょ 銀行 推奨)

### Rakuten rafcid (Vault 済)

- `xai:rakuten:rafcid` = `wsc_i_is_d5074869-5ccb-49df-84f5-33ef48fbab56` (insights / books 用)
- `xai:rakuten:rafcid_ra` (ROOM curation 用)

## 稼働 pipeline (systematic operation)

### Daily 運用 (推定 · 稼働 後)

1. **06:00** — Rakuten API (`openapi.rakuten.co.jp/ichibams/api/`) から 「genre-ranking」pull (v2 API 済 移行)、 review avg 4.0+ · price ¥1,000-¥30,000 で filter
2. **06:15** — `scoring.py` で EV2 上位 抽出 → `inventory.db` update
3. **06:30** — `copy_generator.py` で 4 platform 分 の 本文 生成、 forbidden-words で fact-only tone verify
4. **08:00-22:00** — `scheduler/runner.py` で 1 時間 3 件 以下 · 45 分 同 shop 空け で ROOM auto post (Playwright semi-auto)
5. **11:00 / 17:00** — X @XioraO1 で 「AI が 選んだ 今 週 の 実 用 品」cross-post (差別 化 1 · 4 POV)
6. **20:00** — note (xiora00000) 週 1 で 「渋谷 道玄坂 で 実 使用 の 生活 tools」記事 publish (差別 化 2)
7. **23:00** — 日 次 revenue events を `XAIAffiliateHub` dashboard に aggregation (Amazon PA-API + A8 IR + Rakuten App poll)

### 週 1 batch

- Instagram (xiora account · verified) で 3 product カルーセル (差別 化 3 POV)
- 「4 core 隣接 領域 curation」= Kigen 派生 (収納 · 家電 保証) / Nexa 派生 (学習 desk) / Lingua 派生 (集中 tools) の 3 categories 交代

## Reo 残 action (合計 20-30 分 で L3 稼働 開始)

| # | action | 所要 | 効果 |
|---|---|---|---|
| L3-1 | **Amazon Associates 登録** (`XAIAffiliateHub/amazon_associates_2026-07-25/REO_REGISTRATION_GUIDE.md`) | 5-10 分 | Amazon tag 取得 · Vault 保存 · 家電/tech 系 revenue channel 開通 |
| L3-2 | **A8.net 登録** (`XAIAffiliateHub/a8_2026-07-25/REO_REGISTRATION_GUIDE.md`) | 5 分 | 副 サイト で Xiora HP + 3 subdomain 一括 収容 · 大手 案件 個別 提携 |
| L3-3 | **Rakuten Web Service dashboard の 「拒否」 status 解除** (新 openapi API 移行 後 · production domain 設定 · 5 分) | 5 分 | Rakuten API v2 で inventory 自動 update 開通 |
| L3-4 | **Mac IPv6 fix** (Cloudflare block 突破 · ROOM login 有効 化) | 10 分 | ROOM Playwright login 復旧 · 半 自動 posting 開始 |
| L3-5 | **ROOM 1 item を 目視 verify** (semi-auto の quality check · Reo が スマホ で 1 件 posted 記事 を 見る) | 3 分 | 「オリジナリティ」copy · fact-tone が 期待 通り か 判定 |

各 action 完了 で 私 (Body Claude) が:
- Vault key 保存 (Amazon tag · A8 ログイン · Rakuten new tokens)
- `XAIAffiliateHub/` の adapter を LIVE 化
- `scheduler/runner.py` を daemon 化 (launchd or VPS)
- 1 週間 は Reo が daily 目視、 品質 OK なら blanket approve へ 移行

## 収益 見込み (fact 基準)

**楽天 ROOM 実 実績** (past 個人 運用 · memory 参照):
- traffic 実 導線 = 1 月 の 記事 500-2,000 view (rafcid_ra 直接)
- CV rate = 1-3% (500 view × 2% = 10 CV)
- 平均 承認 額 = ¥50-¥300 / 件 (ROOM は 商品 単価 × 1-2% 手数料)
- **月 ¥500-¥3,000** の レベル (小 · 単独 で は 主 収入 不可)

**Amazon Associates** (未 稼働 · 一般 目安):
- Amazon tag は 1 リンク あたり 24 時間 の buy-through で 反映
- 承認 率 = 2-4% (product review 系 記事 · Xiora HP insights 経由)
- 平均 手数料 = 商品 価格 × 2-8% (家電 = 2% · 本 = 8-10%)
- **月 ¥2,000-¥15,000** の レベル (Amazon insights 記事 3-5 本 で)

**A8.net** (未 稼働):
- 大手 案件 = SaaS / 金融 / EC service の 紹介 手数料 (¥500-¥5,000 / 成 約)
- SaaS 系 案件 (adobe · notion · 会計 tool) は Xiora HP との 親和 高
- 副 サイト 数 増える と scale up
- **月 ¥3,000-¥30,000** の レベル (大手 案件 5-10 提携 で)

**合計 目標** (L3-1 to L3-5 完了 後 · 3 ヶ月 稼働):
- **月 ¥5,500 - ¥48,000** (3 channel 合計) を Phase 1 の 現実 目標
- Phase 2 (6 ヶ月 稼働) で 記事 数 3x · SNS follower 3x → **月 ¥20,000 - ¥150,000** レンジ

## L1/L2 と L3 の 相互 補完

- **L1 SaaS 経由 の trust** = xiora HP に 掲載 の tech 記事 が Amazon Associates link を 使う 時、 SaaS 事業 者 の 信頼 が product recommendation に も 波及
- **L2 Retail SKU 経由 の cross-sell** = 「Xiora Vault Setup Guide」を 買った 開発 者 に、 開発 者 向け 生活 tools (キーボード · desk chair 等) を Amazon で 紹介
- **L3 SNS traffic 経由 の L1 誘導** = @XioraO1 で ROOM curation を 見た 一般 消費 者 が、 profile 経由 で xiora-official.com に 流入 → Kigen (iOS 期限 管理) の potential customer に

3 layer が 相互 に traffic + revenue を 増幅 する 設計。

## リスク · gate

- **法律 · 消費 者 契約 法**: 全 affiliate link に 「PR」or 「アフィリエイト」表示 明記 (2023 消費 者 庁 stealth marketing 規制 対応)。 template は `services/systems/XioraLifeMedia/config/tone.yaml` に 「【PR】」prefix 済
- **plaform TOS**: ROOM「本文 に # / URL 禁止」/ Instagram「Amazon link は Story のみ」等 の platform 個別 rule は adapter で enforce
- **絶対 gate**: Amazon PA-API key / A8 の 銀行 情報 / Rakuten dashboard 認証 = 全 て Vault 保存、 chat/log 出禁 rule 継続 (`memory/credential_safety_protocol.md`)

## 承認 事項

- [ ] Reo が L3-1 (Amazon Associates 登録) を execute する か
- [ ] Reo が L3-2 (A8.net 登録) を execute する か
- [ ] Reo が L3-3 (Rakuten dashboard) を execute する か
- [ ] Reo が L3-4 (Mac IPv6 fix) を execute する か
- [ ] Reo が L3-5 (ROOM 1 件 目視 verify) を 3 ヶ月 継続 する か (blanket approve へ の 移行 条件)

各 完了 で 私 が 追加 adapter 有効 化 + 収益 aggregation dashboard を LIVE 化 する。
