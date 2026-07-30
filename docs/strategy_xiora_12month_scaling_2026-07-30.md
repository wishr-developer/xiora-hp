# Xiora 12 ヶ月 scaling + 完全自動化 daemon design (2026-07-30)

**背景**: Reo directive「1 個ずつ完璧にして順番に公開・販売・運用」+ 「完全自動化 phase に持っていかないと収益化できない」

**現状 snapshot (2026-07-30 23:33)**:
- Kigen 1st core: LP + SEO + X post + IAP metadata 全 LIVE、 iOS v1.0.2 archive+upload 進行中
- XCloud Connect 2nd core: 準備 subagent 稼働中
- Nexa Academy 3rd core: 準備 subagent 稼働中
- Xiora Lingua 4th core: Free 一本化 pivot 済 (funnel 装置化)
- 実 revenue: **¥0** (全 core)

---

## Part 1 — 4 core 順次 first-yen 到達 の 現実的 timeline

### Phase 1 (Day 0-14): Kigen first-yen
- Kigen iOS v1.0.2 upload → App Store Review (24-48h) → LIVE update
- Lifetime IAP 「審査用に追加」有効化 → 提出 → Review (24-48h) → 買切 販売 開始
- **first-yen 期待**: SEO 3 記事 indexing 進行 + X post 週次 (7 週) + Xiora HP hero strip 経由 で **Day 7-14 に ¥600 or ¥6,000 (Lifetime) の 初回 課金** を 期待
- 前提: App Store review が 差戻し なし で 通ること

### Phase 2 (Day 14-30): XCloud Connect first-yen
- 越谷 · 草加 20 target の D+3/D+7 follow-up が 進行中、 D+14 · D+21 追撃
- 対面 NG のため demo 動画 (screencast) を LP に埋込
- Stripe webhook 疎通確認 + 内部 Gmail 通知
- **first-yen 期待**: 20 target 中 1 契約 = ¥9,800 MRR (Day 21-30)
- 前提: 越谷/草加 SMB が Web signup できる 顧客層 (若手 経営者 中心)

### Phase 3 (Day 30-60): Nexa Academy first-yen
- course 数 SoT 統一 + 11 payment link 生存 確認 + LP hero 差別化
- 買切 course 1 本 販売 が最も 短期で 到達しやすい (¥8,800-19,800 単発 · signup 障壁 低)
- **first-yen 期待**: SEO cluster + Lingua/Kigen cross-sell → Day 30-60 に 買切 1 件 = ¥8,800
- 前提: Clerk Production keys (Reo 30 分) or Free tier で dev key の まま LIVE 継続

### Phase 4 (Day 30-60): Xiora Lingua 収益 経路 なし (funnel 装置)
- 直接 revenue = ¥0 で 継続、 traffic は Kigen + Nexa に 誘導
- lesson complete modal に cross-sell CTA 追加済 (2026-07-29)
- **収益 貢献**: Kigen/Nexa first-yen の 加速 として 間接 効果

### Phase 5 (Day 60-90): 収益 拡大
- Kigen: X post 週次 auto + SEO indexing 進行 → ¥600 × N users で **MRR ¥6,000-30,000**
- XCloud: 埼玉 SMB 横展開 (100 target 追加) → 2-5 契約 で **MRR ¥19,600-49,000**
- Nexa: LLM 経由 course 量産 pipeline 起動 → 50 courses seed → 買切 5-10 本/月 = **¥44,000-198,000/月**
- **合計 MRR 目標**: Day 90 で **¥70k-280k**、 Reo goals の T+3 ヶ月 ¥300-500k の 下限 触れる

---

## Part 2 — MRR ¥5M/月 (T+12ヶ月) 到達 path

### Kigen (¥600/月 monthly + ¥6,000-9,800 Lifetime 買切)
- SEO 3 記事 → 20 記事 (LLM + 人力 audit)
- App Store SEO (ASO): keyword optimization · localization en/ja/zh-Hans
- Family Sharing 有効化済 → 1 契約 で 家族 6 名 使える → 満足度 高 → LTV 長期化
- **Year 1 目標**: 500 subs (¥300k MRR) + 200 Lifetime 買切 (ARR ¥1.4M pooled)

### XCloud Connect (¥9,800-19,800/月)
- 越谷 · 草加 → 埼玉 (春日部 · 川口 · 大宮) 展開 → 100 target × 3-5% conversion = 3-5 契約/週
- toB 特化 SEO 記事 (「飲食店 QR オーダー 導入 ROI」等 · Google 検索 上位)
- **Year 1 目標**: 50 契約 (Starter 平均 で ¥490k MRR、 Pro 混在 で ¥600-800k MRR)

### Nexa Academy (¥8,800-19,800 買切 + ¥1,980-98,000/月 SaaS)
- LLM 経由 course 量産 pipeline (spec 化 → GPT/Claude で content 生成 → 人力 audit → publish)
- 100+ courses 目標 (資格 · 副業 · 起業 · キャリア)
- toB (社員 研修): Enterprise ¥98,000/月 × 5 社 = ¥490k MRR
- **Year 1 目標**: toC 買切 100 本/月 + toB Enterprise 5 社 = MRR ¥800k-1.2M

### Xiora Lingua (funnel 装置)
- 直接 revenue = ¥0 継続、 だが 月 500-1000 unique visitor → Kigen/Nexa 誘導 で 間接 貢献 20-40 万円/月

### 合計 Year 1 MRR 目標
- Kigen ¥300k + XCloud ¥600k + Nexa ¥800k = **¥1.7M MRR** (Reo goal ¥5M の 34%)
- **¥5M 到達 は Year 2 前半**、 Year 1 は 「基盤 建設」フェーズ

---

## Part 3 — Xiora 5+ 収入源 復活 (北星 memory `north_star_make_money.md`)

Reo 志向 の 5+ streams of income (2026-07-25 memory · A-E の 5 stream):

| # | Stream | 現状 | 12 ヶ月 目標 |
|---|---|---|---|
| A | Rapid API 販売 (kigen-affiliate API 等) | 未起動 | LIVE + 月 10 users × ¥1,980 = ¥19,800 |
| B | KDP 販売 (電子書籍) | 1 冊 執筆中 | 3 冊 出版 · 月 印税 ¥30,000 |
| C | Gumroad Marketplace (デジタル 買切) | 7 種 LIVE | 20 種 · 月 ¥100,000 |
| D | note magazine (月額) | 未起動 | 2 magazine × 100 subs × ¥500 = ¥100,000 |
| E | iOS IAP (Kigen) | 進行 中 | 上記 Kigen MRR ¥300k |
| **合計** | | | **¥550k / 月** (Year 1 目標 の 40%) |

上記 A-E は 4 core と 並行 で 「idle 時 の 副収入」として 少数 継続 execute。

---

## Part 4 — 完全自動化 daemon design (5 個)

Reo directive: 「収益化のため完全自動化 phase に」

### Daemon 1: revenue_check (日次 · 朝 07:00 JST)
- **役割**: 全 revenue source (App Store Connect API · Stripe API · Gumroad API · Amazon Affiliate) の 昨日 売上 を 集計 → Reo 宛 email 送信
- **実装 path**:
  - launchd `com.xiora.revenue-daily-brief.plist`
  - Python script が ASC / Stripe / Gumroad API 経由 で 「昨日 の 売上 · MRR 差分 · churn 数」 を pull
  - 集計 結果 を Reo 宛 メール (`reo44283@gmail.com`) · Body に summary + 詳細 CSV 添付
  - **first-yen 発生 の 即時 認知** = Reo モチベ 維持

### Daemon 2: churn_detection (日次 · 深夜 03:00 JST)
- **役割**: Stripe subscription 解約 event を 監視 → 予兆 (最終 login から 30 日 · 60 日) を alert
- **実装**:
  - Stripe webhook で customer.subscription.deleted 受信
  - 別途 各 product の login DB (Kigen · Nexa · XCloud) と cross-check
  - 「解約 予兆 5 名 · 実 解約 2 名」等 の 集計 を Reo に notify
  - 対応 案 (メール · 割引 offer · 電話 = NG) を 添える

### Daemon 3: auto_content_pipeline (週次 · 火曜 05:00 JST)
- **役割**: 4 core 分 の SEO 記事 · X post · note 記事 を LLM で 自動 生成 → 私 (CLI Claude) が audit → publish
- **実装**:
  - GPT/Claude API で 記事 draft 生成 (fact-only tone template)
  - 憲法 grep (「必ず · 保証」等 0 hit check) 自動 実行
  - 憲法 pass の draft のみ 私 に 通知 → 私 が edit + push
  - **Reo 介在 ゼロ で 週 1 記事/core × 4 core = 4 記事/週 = 208 記事/年**

### Daemon 4: affiliate_seo_poster (週次 · 木曜 09:00 JST)
- **役割**: Rakuten rafcid + Amazon Associates + A8 の 商品 選定 + insights 記事 に link 埋込 + 楽天 ROOM 投稿
- **実装**:
  - 既存 XAIAffiliateHub / ROOM backup を 拡張
  - 週 5 商品 × 4 platform = 20 link/週
  - 「¥0 コスト + ゼロ Reo 介在」で 副収入 発生

### Daemon 5: outreach_watcher (24/7 · 既存 稼働 中 の 拡張)
- **役割**: XCloud + Nexa の 20-100 target cold email + form fill + D+3/D+7 follow-up + IMAP reply 監視
- **現状**: `com.xiora.imap-reply-watcher.plist` + `com.xiora.outreach-followup.plist` 稼働 中
- **拡張**: reply が 発生 したら 私 に immediate 通知 (現在 は 手動 poll)、 conversation thread を DB 化

### daemon 全体 統合 dashboard
- xiora-official.com/co/dashboard (XAI Portal 内部 admin) に daemon 5 個 の 稼働 status + 昨日/今週 の 実 数字 を可視化
- 私 (CLI Claude) が 週 1 で dashboard 確認 → 異常検知 → alert

---

## Part 5 — Xiora 完璧 tempate (4 core 共通 の SoP)

Kigen 1st で 確立 した 「完璧 = LIVE 販売 可能」の 7 項目 template を 4 core 共通 SoP 化:

1. **LP hero 5 秒 テスト**: BC で 5 秒 以内 に 「何 か · 誰 向け か · 価格 · CTA」が 伝わる
2. **CTA 明確 性**: primary CTA が hero + footer + sticky bottom の 3 面 で 反復、 tap target 44×44 met
3. **送客 経路 3+**: Xiora HP top + 他 3 core footer + insights 記事 の 経路 で 内部 traffic circulation
4. **SEO 3 記事** (最低): fact-only tone · 憲法 grep 0 hit · schema.org markup · 内部 link 3+
5. **X post 7 本 + 週次 auto post daemon**: XSocialOS 経由 で ゼロ Reo 介在
6. **決済 経路 verified LIVE**: Stripe/App Store の payment link が active + test 決済 完了 record
7. **first-yen 記録**: 実 決済 1 件 の revenue event を DB 化 + Reo 通知

---

## Part 6 — その先 (12 ヶ月 以降 · Year 2-5)

- Year 2: MRR ¥5M 到達、 4 core が 各 ¥1-1.5M MRR で 均等 に scale
- Year 3: 5 番 目 core (Ocean LLM 公開 対話 AI product) 起動、 MRR ¥15M
- Year 5: T+5 年 goal (memory `xiora_goals_2026_07_19.md`) ¥50M+ MRR、 Ocean LLM が Xiora unique moat に成長 (Path D · 日本語 SMB domain data)
- Year 10-30: 「全 世界 top 企業 を 超える」mission (memory `xiora_ultimate_mission_beat_world_top.md`) — Apple/MS/Google 級 の $3T+ 時価総額 · Path A/B/C/D の 4 pillar で 到達

---

## 今 の Reo action (0 個)

全 4 core は 私 (CLI + subagent + MCP) が 遠隔 実行 中。 Reo の billing/KYC 以外 は 一切 不要。

## 次 の Kigen build 完了 直後 の action (私 側)

1. IAP 提出 完了 (App Store Connect MCP)
2. Kigen 完成 通知 (Reo 宛 email · daemon 経由)
3. XCloud Connect 2nd core (subagent 出力 待ち) の 実 execute 開始
4. Nexa Academy 3rd core 準備 完了 (subagent 出力 受領)

---

**doc SoT**: `docs/strategy_xiora_12month_scaling_2026-07-30.md`
**次回 review**: 週次 (毎 月曜 07:00 JST · daemon 1 の 集計 と 併せて)
