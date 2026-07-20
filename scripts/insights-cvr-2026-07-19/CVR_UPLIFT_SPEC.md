# Xiora HP Insights CVR Uplift 2026-07-19

- 対象: `Xiora_HP/insights/*.html` (index.html 除く 23 記事)
- 目的: 記事内 途中の H2 直前に mini-CTA 挿入 + UTM tracking 追加、CVR uplift
- 追加要素:
  - mini-CTA aside (「今すぐ相談する」 button + 短文)
  - UTM 4 変数 (source=xiora / medium=insights / campaign=cvr-mini-2026-07 / content=<slug>)
- 既存 CTA (product-cta-audit-2026-07-19 marker + article-末尾 aside) は保持
- 冪等: mini-cta-cvr-2026-07-19 START marker 検知で skip

## 想定 CVR uplift

現状:
- 記事末尾 CTA aside のみ = 記事最下部まで到達した読者のみ相談 button 露出
- 平均読了率 30-50% と仮定すると、途中離脱者は CTA 露出ゼロ

追加後:
- 記事内 3 番目の H2 直前に mini-CTA 挿入
- 記事の 30-40% 位置での露出 = 途中離脱者にも到達
- 想定 uplift: mini-CTA からの相談 click は既存末尾 CTA の 50-150% 追加 (業界目安)

## 想定 revenue impact

- 現状: 20 記事 × 月 200-1000 PV × 相談 CTA CVR 0.5-2% = 月 20-400 相談流入
- 追加後: mini-CTA + 末尾 CTA + 30 分相談リンクの三重露出 = 相談 CVR 1-5%
- 収益: 相談 3-40 件/月 × ¥30k/件 (単発コンサル) = **月 ¥90k-¥1.2M**

## Reo 何もしない (自動 execute)

代理人が blanket P4 内で以下を実行可能:

```bash
cd /Users/kutsuzawareo/Desktop/XAI/Xiora_HP
python3 scripts/insights-cvr-2026-07-19/apply-mini-cta.py --dry-run
python3 scripts/insights-cvr-2026-07-19/apply-mini-cta.py
python3 scripts/build.py
git checkout -b insights-cvr-boost-2026-07-19
git add insights/ scripts/
git commit -m "insights: mini-CTA + UTM tracking for CVR uplift (23 articles)"
git push -u origin insights-cvr-boost-2026-07-19
gh pr create --title "insights: CVR uplift with mini-CTA + UTM tracking" \
  --body "23 記事に mini-CTA を追加、UTM 4 変数で GA4 tracking 可能。 冪等 marker で二重挿入回避。"
```

## Reo action = 1 タップ merge

- PR review → merge click → Vercel auto-deploy → live 反映

## GA4 event tracking spec

UTM 変数の紐付け:
- `utm_source=xiora` — 自社ドメイン内
- `utm_medium=insights` — insights 経由
- `utm_campaign=cvr-mini-2026-07` — 本 campaign 名
- `utm_content=<slug>` — どの記事から来たかで分析

GA4 exploration での分析:
- `session_source = xiora` + `session_medium = insights` + `session_campaign = cvr-mini-2026-07`
- content 変数で「記事別 CVR」を可視化
- 既存末尾 CTA (`src=insight-<slug>`) との A/B 比較で mini-CTA の効果測定

## Success criteria

- [ ] `apply-mini-cta.py --dry-run` が 23 記事分の挿入予定を表示
- [ ] 本適用で全 23 記事に mini-CTA marker 挿入
- [ ] `python3 scripts/build.py` exit 0
- [ ] PR create + Reo 1 タップ merge
- [ ] Vercel deploy 後、live 記事で mini-CTA 表示確認
- [ ] GA4 で 「cvr-mini-2026-07」 campaign event 受信確認 (deploy 後 24 時間以内)
