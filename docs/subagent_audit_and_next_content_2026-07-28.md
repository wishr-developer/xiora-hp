# Subagent Audit + Next Content Plan (2026-07-28)

Auditor: Claude Opus 4.7 (CLI, subagent)
Scope: (1) Kigen LP conversion audit, (2) 5 next SEO article candidates.
Source files:
- `/Users/kutsuzawareo/Desktop/XAI/Xiora_HP/products/kigen.html`
- `/Users/kutsuzawareo/Desktop/XAI/Xiora_HP/insights/kigen-3-use-cases-2026-07-28.html`

---

## Task 1 — Kigen App Store Conversion Audit

### 1.1 CTA clarity

Present CTAs (4 total, all deep-link to App Store with UTM):
1. Top strip: `App Store で 入手 →` (white pill on dark strip)
2. Hero: `App Store で 入手` (btn--primary) + `機能 を 見る` (btn--ghost)
3. Pricing Free card: `App Store で 入手 ↗`
4. Get Started aside: `App Store で 入手 →` (rounded pill)

Assessment:
- CTA density is healthy (4 CTAs on a short LP is fine, not spammy).
- All 4 CTAs use the same phrase — good for recognition, but no CTA communicates the free-download benefit. "App Store で 入手" is neutral; competing utility apps typically use "無料で ダウンロード" or "無料 で 始める" which reduces perceived commitment.
- No install-friction language addressed (Apple ID / 決済不要 for free tier). Users on the fence assume they need to enter card info.
- No visible download count / rating / review social proof. Utility category App Store CVR is heavily driven by trust signals.

### 1.2 Value proposition specificity

Hero H1: 「免許 の 更新 · 保証 の 期限、うっかり 切らして いま せん か?」
Lead: 「Kigen (キゲン) は iOS 期限 管理 アプリ。 App Store LIVE、 Free で 基本 機能。 免許 · 保証 · サブスク · 薬 · パスポート · 車検 の 期限 を 逆算 で 通知」

Strengths:
- Specific subjects listed (免許 / 保証 / サブスク / 薬 / パスポート / 車検) — better than generic "予定管理".
- Concrete pain "うっかり 切らす" is well-chosen — this is exactly the search intent.

Gaps:
- No quantified consequence of forgetting (e.g. "免許 失効 → 再取得 数万 円 + 数日").
- Lead sentence starts with a product introduction ("Kigen (キゲン) は…") rather than the user benefit — this is generic B2B tone, not consumer utility tone.
- 「便利」 avoided — good.
- 「逆算 で 通知」 is jargon-lite; consumers understand 「事前 に 通知」 better.

### 1.3 Friction points

- Rename disclosure line ("App Store 内 表示 名 は 現在 「KigenX」です (「Kigen」への rename 予定)") is placed under the hero, immediately post-CTA. This is honest but plants doubt at the exact click moment. Recommend either moving it to a footnote or reframing as reassurance ("App Store では KigenX と 表示 されます 同じ アプリ です")。
- Family sharing (Plus) is under `features`, but the value story for Plus is weak: "家族 分 の 期限 を まとめて 管理" is presented without quantifying why (Free vs Plus differentiation blurry).
- Get Started section says "5 分 以内 に 開始 可能" — good micro-commit anchor. Underused; should be earlier in the funnel.
- No hero image or app screenshot. Consumer apps without any visual on the LP have measurably lower conversion than those with a phone mockup. Not fixable in a single-file edit, noted for future.
- Related articles at the bottom drive traffic away rather than to App Store. Consider only 1-2 related articles + prominent App Store CTA below them.

### 1.4 Best hero-copy hook (based on common consumer pain)

Ranked by search-intent match and click-through psychology:

1. **Consequence-first**: 「免許 が 切れた 日、初めて 気付く。 それ を 二度と 起こさない ため の iOS アプリ」— strong emotional recall.
2. **Time-anchored**: 「更新 通知 の 郵便、いつ 届く か 知って います か？」— curiosity gap, but weak call to action.
3. **Free-download first**: 「免許 · 保証 · サブスク の 期限 を 逆算 通知。 無料 で 始める iOS アプリ」— safe and CVR-lifting.
4. **Current copy**: baseline.

Recommend (1) for hero H1 and use (3) tone for the CTA button label.

### 1.5 Three concrete edits (single-file, `products/kigen.html`)

Each is a single-line edit that likely lifts App Store click-through.

---

**Edit 1 — CTA label: reduce commitment friction on hero button**

File: `/Users/kutsuzawareo/Desktop/XAI/Xiora_HP/products/kigen.html`
Line: 115

Before:
```html
<a class="btn btn--primary" href="https://apps.apple.com/jp/app/kigenx/id6776154131?utm_source=xiora_hp&utm_medium=kigen_hero&utm_campaign=kigen_traffic">App Store で 入手</a>
```

After:
```html
<a class="btn btn--primary" href="https://apps.apple.com/jp/app/kigenx/id6776154131?utm_source=xiora_hp&utm_medium=kigen_hero&utm_campaign=kigen_traffic">無料 で App Store から ダウンロード</a>
```

Rationale: Adds "無料" (removes fear of hidden charge) and "ダウンロード" (says what will happen). Utility-app consumers scan CTAs for these two signals before clicking. Zero legal risk (Free tier is real).

---

**Edit 2 — Hero H1: consequence-first hook + move rename disclosure to reassurance**

File: `/Users/kutsuzawareo/Desktop/XAI/Xiora_HP/products/kigen.html`
Lines: 107–109 and 118

Before (lines 107–109):
```html
<h1 class="page-hero__title reveal">
免許 の 更新 · 保証 の 期限、<br class="sp-only"/> うっかり 切らして いま せん か?
</h1>
```

After:
```html
<h1 class="page-hero__title reveal">
免許 が 切れて から 気付く 前 に。<br class="sp-only"/> 家庭 の 期限 を 一 つ の iOS アプリ で 逆算 通知。
</h1>
```

Before (line 118):
```html
<p style="margin-top:12px;font-size:13px;color:#6b7280;">App Store 内 表示 名 は 現在 「KigenX」です (「Kigen」への rename 予定)。 上記 「App Store で 入手」から 直接 遷移 可能。</p>
```

After:
```html
<p style="margin-top:12px;font-size:13px;color:#6b7280;">App Store では 現在 「KigenX」の 名前 で 掲載 されて います (Kigen と 同一 アプリ、 rename 手続 中)。 上記 ボタン から 直接 遷移 可能。</p>
```

Rationale: The H1 pivots from question form (weaker in Japanese consumer copy) to consequence + solution. The rename note is reframed from "現在 KigenX です" (doubt) to "同一 アプリ、rename 手続 中" (reassurance) — same fact, different framing.

---

**Edit 3 — Add trust micro-copy under hero CTA (5 分・Apple ID のみ・広告 なし)**

File: `/Users/kutsuzawareo/Desktop/XAI/Xiora_HP/products/kigen.html`
Line: 117 (immediately after `</div>` that closes `.page-hero__actions`)

Before:
```html
<div class="page-hero__actions reveal">
<a class="btn btn--primary" href="https://apps.apple.com/jp/app/kigenx/id6776154131?utm_source=xiora_hp&utm_medium=kigen_hero&utm_campaign=kigen_traffic">App Store で 入手</a>
<a class="btn btn--ghost" href="#features">機能 を 見る</a>
</div>
<p style="margin-top:12px;font-size:13px;color:#6b7280;">App Store 内 表示 名 は 現在 「KigenX」です (「Kigen」への rename 予定)。 上記 「App Store で 入手」から 直接 遷移 可能。</p>
```

After (insert one new `<p>` between `</div>` and the rename note; keep the rename note as separate line, apply Edit 2 rewording to it):
```html
<div class="page-hero__actions reveal">
<a class="btn btn--primary" href="https://apps.apple.com/jp/app/kigenx/id6776154131?utm_source=xiora_hp&utm_medium=kigen_hero&utm_campaign=kigen_traffic">無料 で App Store から ダウンロード</a>
<a class="btn btn--ghost" href="#features">機能 を 見る</a>
</div>
<p style="margin-top:10px;font-size:13px;color:#4b5563;">Apple ID の み で 開始 · 初期 登録 5 分 · 広告 なし · On-Device 完結</p>
<p style="margin-top:12px;font-size:13px;color:#6b7280;">App Store では 現在 「KigenX」の 名前 で 掲載 されて います (Kigen と 同一 アプリ、 rename 手続 中)。 上記 ボタン から 直接 遷移 可能。</p>
```

Rationale: Four proof anchors placed at the exact conversion moment. All four are factually true (per existing LP content and insight article). Each addresses a common last-second consumer hesitation: (1) 決済 info 不要 / (2) セットアップ 労力 / (3) 広告 疲れ / (4) データ 送信 不安。 This is the highest-leverage single insertion possible without new file / new asset.

---

## Task 2 — Next SEO Article Topics (5 titles)

Guardrails applied:
- Cover 4 core products (Kigen / Xiora Lingua / Nexa / XCloud Connect), at least 1 each.
- Avoid retired pillar names (Sales AI OS / EC-Autopilot / TradeOS).
- Include specific number where sensible.
- Fact-first tone; no exaggeration; comply with 景表法 / 特商法.
- Spread: 1 article per day starting 2026-07-29 (5 titles = 5 days = W1 of the next content cycle).

### 2.1 Publish schedule proposal

| Date | Title # | Pillar |
|------|---------|--------|
| 2026-07-29 (Tue) | Article 1 (Kigen) | consumer utility |
| 2026-07-30 (Wed) | Article 2 (Xiora Lingua) | edtech consumer |
| 2026-07-31 (Thu) | Article 3 (Nexa) | edtech B2B |
| 2026-08-01 (Fri) | Article 4 (XCloud Connect) | dev/infra B2B |
| 2026-08-02 (Sat) | Article 5 (Kigen cross-topic) | consumer utility |

Kigen gets 2 slots because it is the only LIVE-with-paid-tier consumer product and CTR uplift there directly lifts App Store revenue.

### 2.2 The 5 titles

---

**Article 1 — 2026-07-29 (Tue) · Kigen**

- **(a) Title**: 車 の 車検 · 保険 · 免許 3 つ の 期限 を 1 画面 で 管理 する 手順 (iOS Kigen 実運用)
- **(b) Target SEO keyword**: 車検 免許 保険 期限 管理 アプリ
- **(c) 1-line abstract**: 車 保有者 が うっかり しがち な 3 期限 (車検 · 自賠責 · 免許 更新) を Kigen で 1 画面 統合 する 実手順 と、通知 タイミング の 現実 的 な 設定 例。
- **(d) Target pillar**: Kigen (consumer utility / mobility owner segment)

Search-intent rationale: 「車検 期限 管理 アプリ」の 単月 検索 は 中量 帯 (competitor は Cocoro 等)、 「免許 · 保険 · 車検 セット で」の 統合 intent は 未 充足。 車 所有 世帯 は 平均 3 期限 保有 = Plus ¥600 の 費用対効果 説明 が しやすい。

---

**Article 2 — 2026-07-30 (Wed) · Xiora Lingua**

- **(a) Title**: 英語 学習 アプリ を 3 日 で 挫折 しない ため の 4 設計 原則 (Xiora Lingua 開発 log)
- **(b) Target SEO keyword**: 英語 学習 アプリ 挫折 続かない
- **(c) 1-line abstract**: 英語 学習 アプリ が 続か ない 原因 を UX 4 側面 (session 長 / 復習 密度 / 通知 頻度 / progress 可視化) で 分解 し、Xiora Lingua が どう 設計 判断 して いるか の 記録。
- **(d) Target pillar**: Xiora Lingua (edtech consumer)

Search-intent rationale: 「英語 学習 挫折」 系 の 検索 は 高 volume · 高 意 図 (Duolingo 難民 の 受け皿 として) 未 充足 領域。 Xiora Lingua は α status なので product 直販 tone を 避け、「設計 log」tone で ブランド 認知 型 に。 Reo memory の 「Xiora Lingua β 有料 化 M6 target」 と 整合。

---

**Article 3 — 2026-07-31 (Thu) · Nexa**

- **(a) Title**: 社内 研修 の 完了 率 を 上げる ため の 5 データ 項目 (Nexa Education OS で 追跡 する 実 例)
- **(b) Target SEO keyword**: 社内 研修 完了 率 データ 分析
- **(c) 1-line abstract**: 中 小 企業 の 社内 研修 が 途中 で 止まる 原因 を、5 データ 項目 (完了 率 / 中断 章 / 平均 セッション 時間 / 復習 頻度 / 質問 回数) で 見える 化 し、Nexa の 実 dashboard 例 で 説明。
- **(d) Target pillar**: Nexa Education OS (edtech B2B)

Search-intent rationale: 「社内 研修 完了 率」 は HR/L&D 決裁 者 の 検索 keyword、 Teachable / Thinkific / TalentLMS 系 の 記事 は 英語 中心 で 日本語 圏 未 充足。 Nexa v2 の 11 商業 course が LIVE で、B2B 決裁 者 flow の 上流 集客 記事 が 不足 して いる (feedback_no_competitor_names hybrid rule 遵守: 記事 内 で 「A 社 LMS」形式 使用)。

---

**Article 4 — 2026-08-01 (Fri) · XCloud Connect**

- **(a) Title**: 個人 開発 で 使う 認証 サービス を 選ぶ 3 判断 軸 (Auth0 / Firebase Auth / XCloud Connect の 実装 差)
- **(b) Target SEO keyword**: 個人 開発 認証 サービス 選び方
- **(c) 1-line abstract**: 個人 · 小 規模 チーム の 認証 サービス 選定 を 3 判断 軸 (無料 枠 / 実装 時間 / ロック イン リスク) で 整理 し、XCloud Connect Basic Auth と 主要 3 サービス の 実装 コード 差 を 比較。
- **(d) Target pillar**: XCloud Connect (developer / infra B2B)

Search-intent rationale: 「Auth0 vs Firebase Auth」 の 検索 は 高 volume、 「個人 開発 認証 選び方」の 判断 軸 記事 は 日本語 圏 で 不足。 hybrid rule 遵守 (title で SEO 用 実名、本文 は 匿名 化 or 中立 tone)。 XCloud Connect の 開発 者 流入 経路 は 現状 SEO のみ、 上流 集客 の 一手 と なる。

---

**Article 5 — 2026-08-02 (Sat) · Kigen (cross-topic)**

- **(a) Title**: パスポート · ビザ · 海外 保険 の 3 期限 を 出発 前 30 日 で 確認 する チェック リスト (Kigen 運用)
- **(b) Target SEO keyword**: パスポート ビザ 期限 チェック リスト
- **(c) 1-line abstract**: 海外 出発 前 30 日 · 14 日 · 3 日 の 3 タイミング で 確認 すべき 期限 系 書類 の チェック リスト。 Kigen で 出発 逆算 リマインド を 組む 手順 と 過去 事例 での 抜け パターン。
- **(d) Target pillar**: Kigen (consumer utility / traveler segment)

Search-intent rationale: 「パスポート 期限 チェック」 は 旅行 前 検索 意 図 の 常 時 需要 keyword、 Kigen の App Store カテゴリ (Utility) と 完全 一致。 Article 1 と セット で 「車 owner segment + traveler segment」の Kigen 二 大 pain point 網羅。 事実 chart (パスポート 残存 6 ヶ月 rule 等) 中心 で 誇大 表現 リスク ゼロ。

---

### 2.3 Retired pillars audit

Confirmed: none of the 5 titles reference Sales AI OS / EC-Autopilot / TradeOS / Algo / XSocialOS internal names. All titles surface Xiora の 4 現行 主力 product のみ。

### 2.4 Fact-first compliance check

Each abstract is scoped to (a) 実装 手順、(b) 開発 log、(c) 判断 軸、(d) チェック リスト — 全て 事実 提示 tone。 効果 保証 表現 (「必ず」「劇的」等) を 排除。 legal_pages_official + LP audit rule と 整合。

---

*Auditor: Claude Opus 4.7 (CLI subagent). Date: 2026-07-28.*
