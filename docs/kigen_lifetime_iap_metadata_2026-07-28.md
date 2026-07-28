# Kigen Lifetime IAP 補完 metadata (Reo 10 分 · Apple ID Login)

**Reo action**: App Store Connect の Kigen (id=6776154131) の Lifetime IAP に 下記 metadata を copy-paste する だけ。 10 分。

**why**: 現状 「MISSING_METADATA」 で 販売 不可、 補完 完了 で **¥4,980 一括 の 買い切り 収益 が 開通** (Kigen Plus ¥600/月 に 追加 revenue stream)。

## Step 1 — App Store Connect login

URL: https://appstoreconnect.apple.com/apps/6776154131/appstore/subscriptions

Kigen アプリ を 開き、 「App 内 課金 · サブスクリプション」→ 「非 消耗 型 (Non-Consumable)」→ Lifetime IAP を 選択。

## Step 2 — 下記 metadata を copy-paste

### 参考 名 (Reference Name)
```
Kigen Lifetime
```

### 製品 ID (Product ID · 既存 なら 変更 不要)
```
com.kigen.app.lifetime
```

### 価格 tier
```
Tier 30 (¥4,980)
```
(¥4,900 or ¥5,000 に 最も 近い tier を 選択、 通常 Tier 30 = ¥4,980)

### 表示 名 (日本語 · 30 字 以内)
```
Kigen Lifetime · 買い切り
```

### 説明 (日本語 · 45 字 以内)
```
月額なし · 一度 の 購入 で 全 Plus 機能 · 家族 共有 対応
```

### 表示 名 (英語 · 30 chars 以内)
```
Kigen Lifetime · One-time
```

### Description (英語 · 45 chars 以内)
```
One purchase, all Plus features forever
```

### Review Notes (審査 用 · 内部)
```
Non-consumable IAP for permanent Plus tier upgrade.
Buyer gets all Plus features (family share, advanced notifications, unlimited categories)
without recurring subscription. 
Price: JPY 4,980 (Tier 30).
No content that requires special review.
```

### Screenshot (2 枚 必要 · 4.7" iPhone + 6.5" iPhone)

既 存 の Plus tier screenshot が あれば 流用 可、 なけれ ば:
- iPhone 15 Pro / 12 Pro simulator で Kigen を 起動
- 設定 画面 で 「Plus プラン」を tap
- 「¥4,980 で 買い切り」と 「¥600/月 で サブスク」の 2 択 が 見える 画面 を capture
- Kigen アプリ 内 で 「screenshot」command で 2 枚 (4.7" 上 で · 6.5" 上 で)

## Step 3 — 「Submit for Review」→ 「Save」

Apple 側 の 審査 は 24-72h。 通常 通り approved になる 想定 (Plus 機能 は 既 に approved 済 の 拡張 なので)。

## 完了 後 (私 が 執行)

- Xiora HP の Kigen page に 「¥4,980 買い切り」 tier を 明示 追加
- comparisons/kigen 比較 LP に Lifetime 表記 追加
- 新 insights 記事「サブスク 疲れ の 人 の Kigen Lifetime 買い切り」draft

## 質問 が 出た 時

Apple の 審査 で reject された 場合、 通常 の 理由:
- Screenshot と 実 アプリ の 挙動 が 不一致 → 実 動作 で 撮り 直し
- 説明 に 「Best」「Guaranteed」等 の 単語 → 削除

いずれ も 私 が 修正 draft を 提供 する ので、 reject メール を 転送 で 対応。

**期待 収益**: Kigen 現行 downloads の 5-15% が Lifetime に conversion 想定。 100 downloads/月 × 10% × ¥4,980 = **¥49,800/月 追加**。
