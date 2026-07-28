# xiora note magazine launch plan (Stream D · 2026-07-28)

**Target**: 月商 ¥14,500-¥65,000 (Phase 1) · time-to-first-yen 21-45 日
**Reo action**: note Pro upgrade (5 分) · xiora00000 既存 account 流用

## Magazine 位置 づけ

**Name**: 「xiora insider — 単独 で AI SaaS を 動かす 実 記録」
**Price**: ¥500/月 (定期 購読 magazine)
**単発 記事**: ¥980-¥1,980/号

## Content 供給 源

xiora の 内部 ops 記録 (Reo directive 「fact-only tone」) が そのまま content asset に:

- 4 core (Kigen · Xiora Lingua · Nexa · XCloud Connect) の 実 数値 · 実 conversion
- Rakuten ROOM / Amazon Associates / A8 の 実 revenue 経過 (匿名 化 集計)
- L3 AI batch (47 posts VPS 生成) の 実 実験 過程
- AI 3 段 モデル (Ollama qwen2.5:7b + subagent 委任) の cost / speed 実 log
- xiora HP 4 core rebuild (50+ commit / net -6,800 行) の 判断 経過

**note magazine の 差別 化**: 「経験 談」で は なく **「実 数値 · 実 コード · 実 意思決定 log」**。 SaaS 起業 検討 者 が 直接 使える 素材 提供。

## Magazine 3 号 分 (Reo Pro 有効 後 私 が draft):

### Vol.1 (2026 年 8 月 号)「35 分 で 5 収入 源 に した 話」

- 米国 「7 streams」 学習 → xiora 適用 の 実 手順
- Gumroad / KDP / iOS IAP / RapidAPI / note の 5 signup 実 log
- 各 stream の Phase 1 実 収益 (集計 期間 30 日)
- 想定 分量: 4,500 字

### Vol.2 (2026 年 9 月 号)「AI subagent に SaaS pricing 判断 を 委任 した 結果」

- Xiora Lingua Stripe A/B/C 選択 を Claude subagent に 完全 委任 した 実 log
- 3 択 提示 → 判断 根拠 → 執行 → 結果 の 全 プロセス
- 「Reo が review しない」運用 モデル の 実 効果 検証
- 想定 分量: 4,000 字

### Vol.3 (2026 年 10 月 号)「Ollama qwen2.5:7b を VPS で 動かして Mac 静音 化 した 話」

- Mac fan うるさい 事件 → VPS 移設 の 全 実 手順
- ¥XX の VPS で ¥YY の Anthropic API cost を replace した 収支
- CPU-only Ollama の 実 latency (30-140 秒/call の 数値 開示)
- 想定 分量: 4,500 字

## Sponsor / PR 掲載 rate card

**xiora HP insights** (月 X 万 PV 想定):
- 記事 内 sponsor 枠 (末尾): ¥30,000/回
- 記事 冒頭 sponsor 明記: ¥50,000/回
- 全 記事 fixed sponsor (バナー): ¥100,000/月

**X (@XioraO1)**:
- Product placement post (¥PR 明記): ¥15,000/回
- Thread 内 mention: ¥8,000/回

**note magazine**:
- 号 内 sponsor 記事: ¥25,000/回

**全 掲載 は 消費者 庁 stealth marketing 規制 対応 (「PR」明記)**。 fact-only tone 遵守。

## Body Claude 自動 execute (Reo Pro upgrade 後)

- Vol.1 draft 4,500 字 生成 (subagent 経由)
- Canva MCP で magazine cover (3 号 分 × 3 A/B variants)
- xiora HP insights の cross-link 追加
- SNS distribution (X @XioraO1 + Instagram xiora account)

## 除外

- 個人情報 · 顧客 identity は 掲載 しない
- Kakuyomu / 小説 家 名義 は 混入 しない (memory `feedback_no_kakuyomu_on_xiora_hp.md`)
- 資格 系 (税理士/弁護士/投資助言) の 助言 · 代行 tone は 避ける
