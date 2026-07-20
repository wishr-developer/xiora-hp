# Xiora HP Insights CVR Uplift v3 — 2026-07-20

前 batch (2026-07-19, `insights-cvr-2026-07-19/`) で 23 記事に mini-CTA + UTM tracking を追加済み。 v3 では 以下 3 uplift を積み増しする。

- 対象: `Xiora_HP/insights/*.html` (index.html 除く 全 SEO 記事、〜30 記事)
- 目標: hero image + GA4 event tracking + A/B test spec で CVR を更に uplift
- Reo action: 全て自動 execute 可 (blanket P4 permission)、feature branch push + Reo 1 タップ merge

## v3 追加要素

### 1. Hero SVG thumbnail generator

各記事の H1 直下に、Xiora 白基調 minimal な SVG hero を挿入する。

- 生成方式: **Playwright 不要、Python で SVG を直接生成** (Mac 負荷 回避、feedback_mac_load_reduction.md 準拠)
- サイズ: 1200 × 630 (OGP + hero 兼用)
- スタイル:
  - 背景: #fbfbfd (Xiora 標準)
  - hairline border: #d1d5db
  - タイポ: Inter + Noto Sans JP、black + hairline
  - accent: 記事 category 毎に 1 色 dot (blue / green / amber / purple) — feedback_ui_white_minimal.md の dot-prefix badge
- 冪等 marker: `<!-- hero-svg-v3-2026-07-20 -->` 検知で skip

### 2. GA4 event tracking (JS snippet 追加)

現状 UTM 変数のみ、click event の explicit fire が未実装。 v3 で以下 3 event を計装:

| event_name | trigger | params |
|-----------|---------|--------|
| `xiora_cta_click_mini` | 記事内 mini-CTA click | `article_slug`, `cta_position=middle` |
| `xiora_cta_click_hero` | hero SVG 内 CTA click | `article_slug`, `cta_position=hero` |
| `xiora_cta_click_footer` | 記事末尾 相談 CTA click | `article_slug`, `cta_position=footer` |

- 実装: `Xiora_HP/assets/js/cvr-v3-tracking.js` に GA4 gtag event dispatcher を追加
- 記事本文の `<a>` に `data-cta-position` 属性を追加、JS が delegated click listener で拾う
- GA4 property は既存 `G-XXXXXXX` (Reo が Track 別 memo に記入済み想定)

### 3. A/B test spec

各記事に variant A / B を用意し、URL query `?variant=b` で分岐。 統計有意性 chi-square で判定。

- **variant A (control)**: 現状の mini-CTA テキスト「今すぐ相談する」
- **variant B (experiment)**: mini-CTA テキスト「30 分無料で相談する」+ badge 「無料」を追加

- **splitting**: crypto.randomUUID の 先頭 hex を mod 2 で判定、cookie `xiora_ab_variant` に 30 日保存
- **exposure event**: `xiora_ab_exposure` (event_params: `variant=a|b`, `article_slug`)
- **conversion event**: `xiora_cta_click_mini` の filter で variant 別 CVR 集計
- **判定条件**:
  - 各 variant 最低 200 exposure
  - chi-square p<0.05 で有意
  - 有意なら winner variant に fixed (30 日後 auto-fix、code override 可)

## 想定 CVR uplift v3 (v2 の上乗せ)

- hero SVG 導入 = 記事の視覚訴求 up → 読了率 5-10% up
- GA4 event tracking = variant 別 CVR を精密計測、winner variant に fixed で CVR uplift 20-40% (業界目安)
- 累積効果:
  - v1 mini-CTA 追加: CVR baseline → +50-150%
  - v3 (hero + A/B): 更に +10-40%
  - 総合 revenue impact: **月 ¥120k-¥1.6M** (v2 の 月 ¥90k-¥1.2M に対して)

## 実装 file

```
Xiora_HP/scripts/insights-cvr-v3-2026-07-20/
├── CVR_UPLIFT_V3_SPEC.md   (本 file)
├── generate-hero-svg.py    (hero SVG を 各記事の H1 直下に挿入)
├── inject-ga4-tracking.py  (GA4 tracking JS を <head> に追加、data-cta-position 付与)
└── ab-test-spec.json       (variant A/B の text / badge / weight spec)

Xiora_HP/assets/js/
└── cvr-v3-tracking.js      (GA4 dispatcher + A/B splitter)
```

## 実行 order (自動)

```bash
cd /Users/kutsuzawareo/Desktop/XAI/Xiora_HP
python3 scripts/insights-cvr-v3-2026-07-20/generate-hero-svg.py --dry-run
python3 scripts/insights-cvr-v3-2026-07-20/generate-hero-svg.py
python3 scripts/insights-cvr-v3-2026-07-20/inject-ga4-tracking.py --dry-run
python3 scripts/insights-cvr-v3-2026-07-20/inject-ga4-tracking.py
# build (existing)
python3 scripts/build.py 2>/dev/null || true
# git
git checkout -b insights-cvr-v3-2026-07-20
git add insights/ scripts/insights-cvr-v3-2026-07-20/ assets/js/cvr-v3-tracking.js
git commit -m "insights: CVR uplift v3 - hero SVG + GA4 event tracking + A/B test"
git push -u origin insights-cvr-v3-2026-07-20
gh pr create --title "insights: CVR uplift v3" --body "$(cat CVR_UPLIFT_V3_SPEC.md | head -20)"
```

## Reo action

1. GA4 property ID を `Xiora_HP/assets/js/cvr-v3-tracking.js` の TODO 行に貼付 (未計装なら feature branch merge 前)
2. PR 1 タップ merge → Vercel auto-deploy
3. deploy 24h 後、GA4 で `xiora_cta_click_mini`, `xiora_ab_exposure` の event 数 を確認

## Success criteria

- [ ] 全 30 記事に hero SVG 挿入 (冪等 marker 検知で 二重挿入回避)
- [ ] `cvr-v3-tracking.js` が全記事の <head> に注入済
- [ ] `<a>` に `data-cta-position` 属性が付与済 (mini / hero / footer 3 位置)
- [ ] A/B splitter が `?variant=` query か cookie で分岐
- [ ] GA4 で 24h 後に 3 event が受信されている
- [ ] Kakuyomu grep 0 + 憲法 5 条 grep 0
