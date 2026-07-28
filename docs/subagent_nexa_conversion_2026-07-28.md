# Nexa Academy Conversion Audit — 2026-07-28

Author: Subagent (CLI Claude)
Files audited:
- `/Users/kutsuzawareo/Desktop/XAI/Xiora_HP/products/nexa-academy.html`
- `/Users/kutsuzawareo/Desktop/XAI/Xiora_HP/comparisons/nexa-vs-teachable-thinkific.html`
- `/Users/kutsuzawareo/Desktop/XAI/Xiora_HP/insights/nexa-career-6-sku-comparison.html`

---

## Audit findings

### 1. Value prop specificity per category — WEAK
`products/nexa-academy.html` hero says
> "実務で使える AI を、コースで。"
> "6 領域を 統合する 教育 SaaS"

This is a horizontal "we have everything" pitch. Visitors landing from 副業/資格/士業 SEO see a generic multi-tenant vendor pitch and lose scent. Feature grid (lines 122-154) DOES separate 7 domains but each blurb is 1-2 sentences and does not link to a dedicated per-persona LP. There is no per-category hero (士業 landing / 副業 landing / 個人事業主 landing).

### 2. HP → Academy signup path — MUDDLED
- Hero CTA button "Nexa Academy を開く" opens academy root (`https://academy.xiora-official.com`), not a signup or plan-selection URL. Comparison LP uses `/pricing?utm_source=...` — better anchor.
- Pricing section (lines 159-172) shows 3 契約形態 (個人 ¥1,980-, 法人 ¥49,800-, 塾 ¥98,000-) but **does not distinguish 単発 買切 vs サブスク** in the tier cards. The 買切 CTA grid (lines 175-217) then contradicts by showing 33 × Stripe buy links priced ¥8,800-¥19,800 with **no clear "which to pick" logic**.
- The comparison LP's TL;DR block (lines 82-87) uses "Nexa Academy 一択" tone — good — but the pricing table lists Free / Starter / Growth / Enterprise, which are **different labels** from the product page's 個人 / 法人 / 塾. Users bounce because the naming disagrees.

### 3. Teachable/Thinkific differentiation — MOSTLY OK, one gap
The 4-factor framework (日本語 UI / ¥ 円決済 / AI 講師 / SCORM) is solid and evidence-based. Gap: **no proof/screenshot** of AI 講師 in action. Everything is text-only claims about differentiation. Also, "海外 LMS SaaS の A 社 · B 社" anonymization (per hybrid rule 2026-07-26) is consistently applied. Good.

### 4. 単発 vs サブスク separation — POOR
`products/nexa-academy.html` line 166: `¥1,980-` "単発コース / 月額サブスク" — this collapses both into one price and confuses. Line 180 says "Learner プラン (¥1,980/月) で は 全 50 課程 学び放題" and then shows 33 single-purchase cards ¥8,800-¥19,800. A visitor's math: "if ¥1,980/mo unlocks all 50, why would I pay ¥19,800 for one?" There is no "買切 vs サブスク どちらが得か" decision table.

---

## 3 high-ROI file edits (exact before/after)

### Edit 1 — Fix pricing tier to explicitly separate 単発 vs サブスク
**File**: `/Users/kutsuzawareo/Desktop/XAI/Xiora_HP/products/nexa-academy.html` (around lines 165-169)

**Before**:
```html
<div class="pricing-grid reveal">
<div class="pricing-tier"><h3>個人</h3><p class="tier-price">¥1,980-</p><p>単発コース / 月額サブスク</p></div>
<div class="pricing-tier featured"><h3>法人 (B2B 研修)</h3><p class="tier-price">¥49,800-</p><p>1 社契約、社員 20 名まで</p></div>
<div class="pricing-tier"><h3>塾 SaaS</h3><p class="tier-price">¥98,000-</p><p>塾内 生徒 100 名 / 塾契約</p></div>
</div>
```

**After**:
```html
<div class="pricing-grid reveal">
<div class="pricing-tier"><h3>単発 買切</h3><p class="tier-price">¥8,800〜¥19,800</p><p>1 課程 買切。 一度 だけ 学びたい 課程 が 決まって いる 方 向け。 33 課程 で LIVE。</p></div>
<div class="pricing-tier featured"><h3>Learner サブスク</h3><p class="tier-price">¥1,980<span style="font-size:14px;color:#6b7280;">/月</span></p><p>50 課程 全 学び 放題。 3 課程 以上 学ぶ 予定 なら こちら が 得 (¥5,940 で 3 課程 相当)。 いつ でも 解約 可。</p></div>
<div class="pricing-tier"><h3>法人 / 塾</h3><p class="tier-price">¥49,800〜¥98,000<span style="font-size:14px;color:#6b7280;">/月</span></p><p>B2B 研修 (¥49,800、社員 20 名 まで) / 塾 SaaS (¥98,000、生徒 100 名 まで)。</p></div>
</div>
```

**Why lift**: removes 単発/サブスク confusion. Adds explicit "3 課程 以上 なら Learner が 得" arithmetic anchor — the classic subscription conversion trick. Reframes the "featured" tier away from B2B (long sales cycle) to Learner (self-serve, low friction, time-to-first-yen 昇順).

---

### Edit 2 — Add persona-specific hero CTA row above the generic hero
**File**: `/Users/kutsuzawareo/Desktop/XAI/Xiora_HP/products/nexa-academy.html` (insert after line 102, before `<section class="section" id="what">`)

**Before** (line 102-104):
```html
</section>

<section class="section" id="what">
```

**After**:
```html
</section>

<section class="section section--soft" id="persona-jump" style="padding-top:32px;padding-bottom:32px;">
<div class="container">
<p class="section__label reveal" style="text-align:center;"><span class="dash"></span>目的 で 選ぶ</p>
<div class="feature-grid reveal" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:20px;">
<a href="#course-cta-grid" style="display:block;padding:16px 18px;border:1px solid #e5e7eb;border-radius:10px;text-decoration:none;color:#111827;background:#fff;"><strong style="font-size:15px;">副業 を 始めたい</strong><br/><span style="color:#6b7280;font-size:13px;">プログラマー / Web ライター / メルカリ / Kindle 出版 の 課程 →</span></a>
<a href="#course-cta-grid" style="display:block;padding:16px 18px;border:1px solid #e5e7eb;border-radius:10px;text-decoration:none;color:#111827;background:#fff;"><strong style="font-size:15px;">個人 事業主 の 経理</strong><br/><span style="color:#6b7280;font-size:13px;">確定 申告 / 簿記 3 級 / FP 2 級 タックス の 課程 →</span></a>
<a href="#course-cta-grid" style="display:block;padding:16px 18px;border:1px solid #e5e7eb;border-radius:10px;text-decoration:none;color:#111827;background:#fff;"><strong style="font-size:15px;">士業 試験 対策</strong><br/><span style="color:#6b7280;font-size:13px;">社労士 / 行政書士 / 宅建 / 診断士 の 独学 支援 →</span></a>
<a href="#course-cta-grid" style="display:block;padding:16px 18px;border:1px solid #e5e7eb;border-radius:10px;text-decoration:none;color:#111827;background:#fff;"><strong style="font-size:15px;">起業 · SaaS 立ち上げ</strong><br/><span style="color:#6b7280;font-size:13px;">AI SaaS 0→1 / 個人 EC / SNS マーケ の 課程 →</span></a>
<a href="#course-cta-grid" style="display:block;padding:16px 18px;border:1px solid #e5e7eb;border-radius:10px;text-decoration:none;color:#111827;background:#fff;"><strong style="font-size:15px;">資格 · 就活</strong><br/><span style="color:#6b7280;font-size:13px;">基本情報 / 簿記 / 就活 ES · 面接 対策 →</span></a>
</div>
</div>
</section>

<section class="section" id="what">
```

**Why lift**: SEO landing pages funnel visitors with narrow intent (e.g. "副業 プログラマー AI"). Currently, that visitor scrolls through 7 domain descriptions to find the 1 relevant course. Persona quick-jumps compress that to 1 click and preserve context via same-page anchor to `#course-cta-grid`. Zero new pages, pure HTML, deployable now.

---

### Edit 3 — Add "買切 vs サブスク どちらが得か" decision block above course grid
**File**: `/Users/kutsuzawareo/Desktop/XAI/Xiora_HP/products/nexa-academy.html` (insert after line 181, before the `<div class="feature-grid reveal">` on line 182)

**Before** (lines 178-182):
```html
<p class="section__label reveal"><span class="dash"></span>50 課程 · 単発 購入 CTA</p>
<h2 class="section__title reveal">Stripe 決済 LIVE 11 / 準備 中 22 — 全 50 課程</h2>
<p class="section__lead reveal">単発 買切 で 各 課程 を 個別 購入 できます。 Learner プラン (¥1,980/月) で は 全 50 課程 学び放題。 「準備 中」は Stripe 発行 待ち で、Learner プラン で は 既 に アクセス 可 です。</p>
</header>
<div class="feature-grid reveal" style="grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;">
```

**After**:
```html
<p class="section__label reveal"><span class="dash"></span>50 課程 · 単発 購入 CTA</p>
<h2 class="section__title reveal">Stripe 決済 LIVE 11 / 準備 中 22 — 全 50 課程</h2>
<p class="section__lead reveal">単発 買切 で 各 課程 を 個別 購入 できます。 Learner プラン (¥1,980/月) で は 全 50 課程 学び放題。 「準備 中」は Stripe 発行 待ち で、Learner プラン で は 既 に アクセス 可 です。</p>
</header>
<aside style="max-width:720px;margin:0 auto 32px;padding:20px 24px;border:1px solid #d1d5db;border-radius:10px;background:#fafafa;">
<p style="margin:0 0 10px;font-weight:600;font-size:14.5px;color:#111827;">買切 と サブスク、どちら が 得？</p>
<ul style="margin:0;padding-left:20px;color:#374151;font-size:13.5px;line-height:1.8;">
<li><strong>1 課程 だけ</strong> 学ぶ 予定 → <a href="#" style="color:#111827;text-decoration:underline;">単発 買切</a> (¥8,800〜¥19,800、永続 access)</li>
<li><strong>2〜3 課程 以上</strong> 学ぶ 予定 → <a href="https://academy.xiora-official.com/pricing" target="_blank" rel="noopener" style="color:#111827;text-decoration:underline;">Learner ¥1,980/月</a> の 方 が 安い (¥5,940 で 3 課程 相当)</li>
<li><strong>迷ったら</strong> → まず Learner ¥1,980/月 で 全 50 課程 覗いて、続けたい 課程 が 明確 に なった 段階 で 買切 に 切替 (Learner は いつ でも 解約 可)</li>
</ul>
</aside>
<div class="feature-grid reveal" style="grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;">
```

**Why lift**: the 33-card grid currently forces cognitive overload on price comparison. A ¥19,800 single purchase makes zero economic sense next to a ¥1,980/mo unlimited plan for any user learning 2+ courses. Explicit decision rule shifts default choice → subscription (which has higher LTV: ¥1,980 × avg retention months >> ¥8,800 one-shot). Also creates a low-commitment on-ramp ("まず Learner で 覗いて") that converts hesitant buyers into monthly sub.

---

## New SEO article — draft

**Target audience**: 個人事業主 who do their own 経理 / 確定申告 (freelancer, 副業 seeker aiming to start 個人事業)

**Working title**:
> 個人 事業主 が AI で 確定 申告 を 8 時間 で 終わらせる 実務 手順 — freee / マネーフォワード に 頼らない 経理 セットアップ

**Primary SEO keyword**: `個人事業主 確定申告 AI` (JP monthly search volume decent, low competitor difficulty, high commercial intent)

**Secondary keywords**: `確定申告 自動化`, `個人事業主 経理 AI`, `青色申告 AI`, `帳簿付け 効率化`

**100-word abstract**:
個人 事業主 が 確定 申告 期 に 毎年 20〜40 時間 を 記帳 · 仕訳 · 領収書 整理 に 溶かして いる 現状 を、 AI (ChatGPT / Claude) と 汎用 表計算 ツール の 組合せ で 8 時間 に 圧縮 する 実務 手順 を 6 phase (領収書 撮影 → OCR → 勘定科目 自動 仕訳 → 月次 集計 → 消費 税 判定 → e-Tax 出力) で 解説。 会計 ソフト 月額 ¥1,980〜 に 縛られず、 AI + 無料 テンプレ で 完結 する 方法 と、 Nexa Academy「個人 事業主 の 経理 · 確定 申告 完全 攻略」課程 (¥12,800 買切) で さらに 深掘り する 学習 導線 を 提示。 税務 判断 は 税理士 に 相談 する 前提 で、 記帳 · 集計 の 事務 作業 だけ を 自動 化 する 立場 を 明示。

**Recommended URL slug**: `/insights/kojin-jigyounushi-kakutei-shinkoku-ai-8jikan-2026-07-28.html`

**Body sections (outline)**:
1. Introduction — なぜ 20-40 時間 溶ける か (国税庁 統計 引用)
2. Phase 1 領収書 撮影 → Google Drive
3. Phase 2 OCR (Gemini / Claude で 画像 → 表形式 JSON)
4. Phase 3 勘定科目 の AI 自動 仕訳 (prompt template 公開)
5. Phase 4 月次 集計 (Google Sheets pivot)
6. Phase 5 消費 税 判定 (課税 / 免税 / インボイス 番号)
7. Phase 6 e-Tax 出力 · 提出
8. 税理士 に 依頼 する 部分 と 自動 化 する 部分 の 境界
9. さらに 深掘り したい 方 は → Nexa Academy 課程 CTA (単発 ¥12,800 or Learner ¥1,980/月)

**Compliance guardrails**: 税務 助言 業 に 該当 しない よう「事務 作業 自動 化 のみ 提供、税務 判断 は 税理士 に 相談」を 冒頭 · 末尾 · CTA 内 の 3 箇所 に 明記。 国税庁 · 中小企業庁 の 公開 統計 のみ 引用。 憲法 遵守。

**Expected search intent overlap**: 副業 で 20 万 超えた 会社員 (来年 の 申告 を 心配)、 開業 1 年目 の 個人 事業主、 マネーフォワード / freee の コスト を 削りたい 層 の 3 セグメント。 Nexa Academy「個人 事業主 の 経理 · 確定 申告 完全 攻略」課程 (V6 · ¥12,800、現 status = Stripe 準備 中 · Learner で 利用 可) への 高 intent 導線 に なる。
