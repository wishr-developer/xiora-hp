# Reo action — Xiora Lingua Super/Family Stripe 有効 化 (5 分)

## 現状 の 不整合

| 場所 | Super 価格 | Family 価格 | 状態 |
|---|---|---|---|
| HP `/lingua.html` (marketing) | ¥690/月 | ¥1,180/月 | 「準備 中」明示 |
| HP `/pricing.html` (marketing) | ¥690/月 | ¥1,180/月 | 「準備 中」明示 |
| API `plans/router.py` (backend) | ¥980/月 | ¥1,980/月 | LIVE payment_link あり |
| Stripe dashboard | ¥980/月 | ¥1,980/月 | 現行 product (`buy.stripe.com/dRmfZhfmY0jVaQkb5Q1ck0y` / `buy.stripe.com/14AfZhb6Ic2DaQk6PA1ck0z`) |

**問題**: HP marketing と 実 課金 (API + Stripe) で ¥290 / ¥800 の 差 が ある。 HP は 「準備 中」で 隔離 して いる ため 実 損害 は 出て いない が、 意思決定 が 曖昧。

## Reo が 決める こと (5 分 · 3 択)

### 選択 肢 A: HP の ¥690/¥1,180 を 採用 (下げる · 推奨)

- Stripe dashboard で 既存 2 product の price を ¥690/¥1,180 に 変更 (buy.stripe.com URL は 保持)
- または 新 price 作成 + payment link 再生成
- API 側 `plans/router.py` の `amount_jpy=980/1980` を `690/1180` に 更新 + main で PR
- HP の 「準備 中」表記 を 「¥690/月 · ¥1,180/月 · Now Available」に 更新
- 効果: Duolingo (¥1,200 相当) より 安く positioning、 conversion 向上

### 選択 肢 B: Stripe の ¥980/¥1,980 を 採用 (上げる)

- HP `/lingua.html` + `/pricing.html` の 「¥690/月 · ¥1,180/月 · 準備 中」表記 を 「¥980/月 · ¥1,980/月 · Now Available」に 変更
- API 側 は 現状 維持 (¥980/¥1,980)
- HP + comparisons LP + 「Web で 動く 語学 学習 サービス を 選ぶ 3 判断 軸」記事 も 数値 更新
- 効果: 現行 Stripe そのまま、 変更 工数 最小

### 選択 肢 C: 両方 廃止 · Free plan のみ 継続 (monetization 保留)

- HP から Super/Family plan 説明 を 削除、 Free ¥0 のみ 明示
- API 側 `plans/router.py` を Free only に 縮小
- 効果: Stripe 依存 ゼロ、 コンテンツ + 有料 subscription は 後日

## 推奨 = A (¥690/¥1,180)

**根拠**:
- Reo directive「甘 過ぎ · 全 見直し」+ 収益 早期 化 の 両立
- ¥690 は Duolingo Super Free (無料) と Duolingo Super (¥1,200 相当) の 中間、 competitive
- Family ¥1,180 は 家族 4 名 で 割ると 1 名 ¥295、 明らか に お得
- HP は 既に この 数値 を 前提 に refactor 済 (2026-07-27 batch)

## 実 行 手順 (10 分 想定)

### Step 1 — Stripe dashboard で price 変更 (3 分)

1. https://dashboard.stripe.com/products にアクセス (Bizboost.dx account · Xiora メイン acct_1RcC1HFoGzoX9pTQ)
2. 「Xiora Lingua Super」product を開く → Prices > 現行 ¥980/月 に「Add another price」で ¥690/月 (JPY, recurring, monthly) を追加
3. 新 price の 「Update default」で default 化 (旧 ¥980 は archive)
4. 同様 に 「Xiora Lingua Family」で ¥1,980 → ¥1,180 変更
5. 各 product の payment link を新 default price で 再 発行 (「Create payment link」ボタン)、 URL を メモ

### Step 2 — 私 (Body Claude) が API 側 更新 (Reo 依頼 で 実行)

Reo が Step 1 完了 後 に 「Stripe 更新 完了 · Super=<URL>, Family=<URL>」と 教えて くれれば、 以下 を 私 が execute:

- `apps/api/src/domains/plans/router.py` の amount_jpy + payment_link 更新
- `apps/api/tests/test_freemium_pivot.py` の 想定 値 更新
- HP `/lingua.html` + `/pricing.html` の 「準備 中」 → 「Now Available」変更
- lingua-app ビルド + VPS deploy

### Step 3 — 検証

1. `https://lingua-app.pages.dev/pricing` に アクセス、 Super/Family が ¥690/¥1,180 で 表示 される か
2. 「Get Super」click で Stripe checkout が ¥690 表示 で 開く か
3. Test card `4242 4242 4242 4242` で 1 件 実 決済 (Reo card 使用 NG · Stripe test mode 推奨)

## 参考: 現行 Stripe 設定 場所

- Stripe products dir (memory): `services/systems/SalesAIOS/deploy/stripe-live-products.json` (17 products)
- webhook `we_1TvsQWFoGzoX9pTQWZ6EkBow` (Bizboost.dx account、 Xiora メイン acct_1RcC1HFoGzoX9pTQ)
- Xiora account structure: `~/.claude/projects/-Users-kutsuzawareo-Desktop-XAI/memory/xiora_stripe_account_structure.md`

## 副産物

Step 2 完了 で 以下 の 導線 が 同時 稼働:
- Xiora Lingua の 有料 tier 実 販売 (月 ¥690 / ¥1,180)
- HP の 「準備 中」表記 が 全 消去、 conversion 阻害 要因 除去
- API + Stripe + HP の 数値 SoT 統一 (次回 audit で 不整合 0)

---

**questions to Reo**: A/B/C の どれ?  A なら Stripe 更新 開始、 私 が API + HP 追い 更新 で 実行。
