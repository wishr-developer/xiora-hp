# xiora Operational State — 2026-07-27 (集中 4 core rebuild 後)

## 1. 4 core の LIVE 状態

| 事業 | 状態 | 収益 経路 | 課題 (Reo action) |
|---|---|---|---|
| **Kigen (iOS)** | ✅ App Store LIVE | ¥600/月 monthly (APPROVED) | KigenX → Kigen rename (新 version 提出 · Reo 30 分) / Lifetime IAP MISSING_METADATA |
| **Xiora Lingua v1.0** | ✅ Web LIVE (Free 一般 公開) | 43 lesson × 3 course、 有料 tier ¥690/¥1,180 は 準備 中 | Stripe metadata 追加 · daemon load |
| **Nexa Education OS** | ✅ academy.xiora-official.com LIVE | 36 courses、 個別 購入 ¥8,800〜¥19,800 (Stripe 直リンク 埋込 済) | traffic 未流入 |
| **XCloud Connect** | ✅ LP LIVE | ¥5,980/月 B2B (問い合わせ → onboarding) | 越谷/草加 飲食 40 target outreach 継続 |

**8 URL 全 HTTP 200 verified** (2026-07-27 confirmed):
- xiora-official.com / /products/ / /lingua.html / /pricing.html
- /products/kigen.html / /products/xcloud-connect.html
- kigen.xiora-official.com / academy.xiora-official.com

## 2. 撤退 pillar (18 事業) — 見直し 中 状態 に 収束

### HP 上 の 露出 停止 済 (2026-07-27 batch)

- **products/*.html 16 file → short redirect** (noindex + 3 秒 refresh → /products/)
  - agent-factory / content-engine / restaurant-os / ocean-chat / ocean-llm / aiverse / tradeos / xiora-ec / xiora-suite / xcloud-flow / xiora-life-media / shigyo-agents / xiora-hire / xiora-salon / xiora-predict / xiora-trader
  - shigyo-agents / xiora-predict / xiora-trader の 3 file は 「資格 独占 業務 · 金融 商品 取引 業 は 一切 行わない」旨 追記
- **footer + sitemap.xml 自動 除外** (products.json flag + build.py 再生成、 24 file 更新)
- **insights 15 記事 + comparisons 2 記事 + news 2 記事** に 「事業 見直し 中」amber banner 追記 (SEO 資産 保持)
- **xiora-apps.html rewrite** (iOS 事業 Kigen 集中 + 他 6 iOS app 事業 見直し 中 明示)

### 未処理 (低 優先)

- 25+ 過去 insights 記事 の 中 に 撤退 pillar 単発 言及 (banner 対応 済 の 記事 経由 で users は 4 core に 誘導 される 前提)
- 個別 撤退 pillar の Stripe checkout link (現状 存在 しない、 全 SaaS pillar は Stripe 未 発行)

## 3. 収益 pipeline (retail SKU) — 稼働 中

7 retail digital product (¥1,980-¥29,800) が Stripe checkout 直リンク で LIVE:
- Xiora AOS 実践ガイド 2026 / Toolkit / Handler Prompt Pack / Rakuten Article Template Pack
- Xiora Founder Pack Bundle / Cold Email Template Pack / Vault Setup Guide

Nexa Academy 11 商業 course も 個別 購入 CTA LIVE (¥8,800-¥19,800)。

## 4. 自動 化 pipeline (常時 稼働)

| pipeline | 状態 | 備考 |
|---|---|---|
| xai-vps SMTP 4段 outreach | 22 target sent / 68 form_only queued | FDA grant to /bin/bash 未実行 (Reo 30秒) |
| SNS farm (X + note draft) | X @XioraO1 active、 note draft 生成 中 | 8 accounts config、 X post generator daily |
| Xiora Lingua API VPS | Caddy + Docker、 43 lesson × 3 course serve 中 | Postgres wiring 済 (opt DATABASE_URL) |
| CF Pages deploy | Push → 1-3 min auto deploy | 本 session 14 commit 全 反映 |
| GitHub Actions billing | ✅ 復旧 済 (task #91) | 定額 内 |

## 5. Reo 残 action (合計 40-50 分)

| # | action | 所要 | blocker | 効果 |
|---|---|---|---|---|
| 1 | FDA grant to /bin/bash (System Settings > Privacy > Full Disk Access) | 30秒 | 手動 | Playwright form_fill 68 target 一括 activate |
| 2 | Kigen App Store 「KigenX → Kigen」 rename (新 version 提出) | 30 分 | Apple ID + 2FA | brand 統一 · Xiora HP CTA との 整合 |
| 3 | Kigen Lifetime IAP MISSING_METADATA 補完 (App Store Connect) | 5 分 | Apple ID | 買い切り option 提供 |
| 4 | Xiora Lingua ¥690/¥1,180 Stripe metadata 追加 | 5 分 | Stripe login | 有料 tier LIVE 化 |
| 5 | launchctl load lingua-conversion daemon | 3 分 | Mac terminal | conversion tracking |

## 6. 本 session commit 履歴 (14 commit)

```
24c26aa comparisons/index.html: 撤退 事業 の 2 card に amber badge
8304392 comparisons + news: 撤退 事業 の 4 記事 に amber banner
4fc1375 insights/: 撤退 pillar 15 記事 に amber banner
46e6077 sitemap.html: Products section を 4 core に 更新
6e23598 xiora HP: 撤退 18 pillar を footer + sitemap.xml から 自動 除外
7c31738 sitemap.xml: 撤退 16 pillar entry 削除
3564b41 products/: 撤退 16 pillar page を short redirect 化
cb9cee9 xiora-apps.html rewrite: iOS 事業 Kigen 集中
72ed658 xiora HP: legal/comparisons/insights の 残 甘さ 修正
5523b39 xiora index.html: family cards 12→4
04d9cc7 xiora pricing.html 全 rewrite: 集中 4 core
a4cb49a xiora products/index 全 rewrite: 集中 4 core
bbb74c4 xiora HP: 甘さ 大 一括 修正 (誇大 + ¥980 mismatch 全 除去)
501cb45 xiora HP: consulting-thanks + lingua-beta-thanks 甘さ 除去
```

**削除 行数**: 約 4,000 行 (誇大 表現 · 未 実装 主張 · 撤退 pillar 露出 全 除去)
**追加 行数**: 約 500 行 (short redirect + amber banner + 4 core focus)

## 7. 判断 · 意思決定 の 根拠

- Reo directive: 「Xiora Systems じゃなく、 xiora で いい」 → 全 file 「xiora」 lowercase 統一
- Reo directive: 「Kigen 以外 は よく わかんない ので なくして いい」 → 6 iOS app + 25+ SaaS pillar 「事業 見直し 中」 status に 収束
- Reo directive: 「甘 過ぎ ます、 全て において 見直し」 → 誇大 表現 · 未 実装 主張 (FSRS / Azure Speech / 音素 発音 評価 / On-Device / No Tracking) 全 除去、 fact-only tone に refactor
- Reo directive: 「業務 報告 みたい な 感じ → 告知 · 疑問 解消 に」 → X post は 削除 + rewrite 中
- Reo directive: 「そっち で 考えて 進めて」 → CLI Claude 自律 execute (Brain 経由 の 3 AI 判断 は Chrome renderer 障害 中)

---

**次 の block**: Reo 残 action 5 件 の 完了 待ち。 完了 で 4 core 全 revenue-collectible + brand-clean な complete operational state 達成。
