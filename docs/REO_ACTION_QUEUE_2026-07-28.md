# Reo action queue — 直接 revenue impact 順 (2026-07-28)

## 直近 30 日 で 「稼ぐ」の に 必要 な action 全 リスト

### 🥇 tier 1: 実 課金 直結 (合計 20-30 分)

| # | action | 所要 | 効果 | doc |
|---|---|---|---|---|
| 1 | **Xiora Lingua Stripe A/B/C 決定** (Super/Family ¥690/¥1,180) | 5 分 | Web SaaS 実 課金 開始 · 月 ¥50k-¥500k 見込み | `reo_action_xiora_lingua_stripe_2026-07-28.md` |
| 2 | **Kigen App Store rename** (KigenX → Kigen · 新 version 提出) | 30 分 | brand 統一 · 月 ¥5k-¥50k up 見込み | operational_state doc §5 |
| 3 | **Kigen Lifetime IAP MISSING_METADATA 補完** | 5 分 | 買い切り option 追加 (¥3,000 想定) | operational_state doc §5 |

### 🥈 tier 2: L3 affiliate 開通 (合計 15-20 分)

| # | action | 所要 | 効果 | doc |
|---|---|---|---|---|
| 4 | **ROOM 1 account manual login** (Playwright storage_state 保存) | 3-5 分 | 47 AI 生成 posts の 半 自動 ROOM 投稿 開始 · 月 ¥500-¥3,000 見込み | `reo_action_room_login_2026-07-28.md` |
| 5 | **Amazon Associates 登録** (Bizboost.dx 個人 情報 コピペ) | 5-10 分 | 家電/tech 系 affiliate · 月 ¥2,000-¥15,000 見込み | `services/systems/XAIAffiliateHub/amazon_associates_2026-07-25/REO_REGISTRATION_GUIDE.md` |
| 6 | **A8.net 登録** (副 サイト 対応 · ゆうちょ 銀行 推奨) | 5 分 | 大手 SaaS 案件 提携 · 月 ¥3,000-¥30,000 見込み | `services/systems/XAIAffiliateHub/a8_2026-07-25/REO_REGISTRATION_GUIDE.md` |

### 🥉 tier 3: pipeline activate (合計 5 分)

| # | action | 所要 | 効果 |
|---|---|---|---|
| 7 | **FDA grant to /bin/bash** (System Settings > Privacy > Full Disk Access) | 30 秒 | Playwright form_fill 68 target 一括 activate |
| 8 | **AI batch approve (47 posts の 目視 判定)** | 10-15 分 | ROOM/X posting 開始 (Reo action #4 と セット) |

### 4️⃣ tier 4: Reo 権限 gate (時間 あれば)

| # | action | 所要 | 効果 |
|---|---|---|---|
| 9 | **Rakuten Web Service dashboard** の 「拒否」status 解除 + production domain 設定 | 5 分 | Rakuten API v2 で inventory 自動 update 開通 |
| 10 | **Mac IPv6 fix** (Cloudflare block 突破) | 10 分 | ROOM Playwright login 環境 準備 |

## tier 1-4 全 完了 の 見込み revenue (Phase 1 · 3 ヶ月 稼働 後)

- **Kigen** (現行 LIVE): + ¥5k-¥50k / 月 (rename + Lifetime IAP · SNS traffic 押し)
- **Xiora Lingua** (準備 中 → 稼働): + ¥50k-¥500k / 月 (Super/Family LIVE 化)
- **ROOM affiliate** (L3): + ¥500-¥3,000 / 月
- **Amazon Associates** (L3): + ¥2,000-¥15,000 / 月
- **A8.net** (L3): + ¥3,000-¥30,000 / 月
- **Nexa Academy** (現行 LIVE): + traffic 増 で + ¥10k-¥100k / 月
- **XCloud Connect** (現行 LIVE): + 越谷/草加 outreach で + ¥10k-¥100k / 月

**合計 Phase 1 楽観 見込み**: **月 ¥80k-¥800k** (実 tier 1 完了 + tier 2 3 platform 稼働 + traffic 拡大)

**Phase 2 (6 ヶ月 稼働)**: 記事 数 3x · SNS follower 3x · SaaS 顧客 累積 で **月 ¥300k-¥3M**

## Reo が この 30 日 で 触る 必要 が ある 物 (最小 セット)

- Stripe dashboard (1 回、 5 分)
- App Store Connect (2 回、 合計 35 分)
- ROOM app or Web (1 回、 3-5 分)
- Amazon.co.jp affiliate 画面 (1 回、 5-10 分)
- A8.net 画面 (1 回、 5 分)
- Mac 設定 (2 回、 合計 10-15 分)
- (Optional) Rakuten Web Service dashboard (1 回、 5 分)

**合計 = 68-105 分** (30 日 に 分散 すれば 1 日 2-3 分)。

私 は これら 以外 の 全 automation を 執行、 Reo は 最終 承認 と 「稼働 開始」の GO/NO-GO のみ。

## 私 (Body Claude) 側 で 自動 執行 中 · 執行 予定

- ✅ HP 4 core 集中 rebuild + 47 commit 済 (2026-07-27/28)
- ✅ L3 affiliate 47 posts AI 生成 済 (VPS Ollama qwen2.5:7b)
- ✅ 法務 · comparison · insights · news の 4 core rebrand 済
- ⏳ Reo action #1-#8 完了 待ち → 待ち 中 は HP 追加 polish + 次 batch 準備
- ⏳ Reo action 完了 通知 で 私 が pipeline 追加 automate

「Reo が 触る」= 最小、 「Reo が 決める」= 最大。 これ が Reo 単独 SaaS 会社 の 運営 モデル。
