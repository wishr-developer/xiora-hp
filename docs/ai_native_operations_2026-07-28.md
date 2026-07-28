# xiora AI-native operations — Reo directive「AIをもっと活用して」(2026-07-28)

## 転換 の 意図

Reo directive: 「aiをもっと活用して」

これ まで の 一部 pipeline (contents 生成 · outreach 文面 · post drafts) は Body Claude が 手動 で 1 件 ずつ 生成 して いた。 以降 は **local LLM (Ollama qwen2.5:7b)** + Anthropic API + subagent 経由 で **AI 主体 の 大 量 生成 + 品質 gate + Reo 目視 verify** の 3 段 モデル に 統一 する。

## 3 段 モデル (AI 主体 の 標準 flow)

```
[data source (DB / API / web)]
    ↓
[LLM 大量 生成] (Ollama qwen2.5:7b local 無料 / 高 volume)
    ↓
[品質 gate] (forbidden words soft-replace + fact-check + 憲法 grep 自動)
    ↓
[Reo 目視 verify] (1-5 件 sample、 OK なら blanket approve)
    ↓
[SNS/HP/outreach へ 自動 posting]
```

各 段 で AI が 動く 責務 を 明確 化:

| 段 | AI の 役割 | 使用 tool |
|---|---|---|
| generate | LLM で 個別 変数 埋め + tone 制御 + POV 織り込み | Ollama qwen2.5:7b (無料 · local) / Claude Opus (品質 高 · API) |
| gate | 誇大 表現 検出 · soft-replace · 憲法 grep · 事実 差 checker | Python regex + 追加 で LLM judge (小 model) |
| verify | Reo が 1-5 件 目視、 OK/NG フィードバック を LLM の prompt 追加 学習 | 手動 (Reo) + Body Claude の prompt update |

## 適用 pipeline (実 稼働 中)

### 1. XioraLifeMedia (L3 affiliate revenue) — 本 turn で 実装

- 対象: `services/systems/XioraLifeMedia/data/inventory.db` の 21 商品
- 生成 対象: ROOM + X + note の 3 platform 分 = 21×3 = 63 posts
- script: `services/systems/XioraLifeMedia/scripts/ai_copy_batch.py`
- LLM: Ollama qwen2.5:7b (local · Mac 負荷 抑え目)
- 出力: `deliverables/curated_batch_2026-07-28/ai_generated/<id>_<platform>.md`
- 品質 gate: 「絶対 / 必ず / 100% / 神 / 爆売れ / 最高 / 最強 / 確実 / 保証」の 9 語 auto soft-replace
- 4 POV 差別 化 を prompt に 明示 (「AI data 選定」「founder 実 使用」「4 core 隣接 領域」「fact-first tone」)

### 2. XSocialOS (SNS 全 自動 6 layer) — 継続 稼働 中

- 対象: X @XioraO1 + note xiora00000 + Instagram + TikTok 等 の 8 accounts
- 既存: `services/systems/XSocialOS/deliverables/x_drafts/` に daily generator あり
- AI 拡張 候補:
  - hashtag suggestions を LLM に 依頼 (現行 は 固定 リスト)
  - engagement prediction (LLM に post 見せて 予測 スコア 算出、 上位 のみ 投稿)
  - reply/comment 自動 対応 (受信 comment → LLM が 返信 draft 生成 → Reo 承認 → 投稿)

### 3. Xiora HP insights 記事 生成 — 段階 移行

- 現行: 私 (Body Claude) が 1 記事 ずつ 手動 生成 (2026-07-28 batch = 2 記事)
- AI 拡張: 「keyword 一覧 → 記事 一括 生成 → 品質 gate → Reo verify → publish」の pipeline 化
- 対象 keyword source: Google Search Console (Reo action で 認証 完了 後) の CTR 低い 高 impression クエリ

### 4. XCloud Connect 越谷 / 草加 飲食 outreach — LLM 拡張

- 現行: 22 target sent / 68 form_only queued (`outreach_pipeline_full_stack_2026_07_25.md`)
- AI 拡張: 各 店舗 の website + Google Maps review を LLM に読ませ、 個別 提案 文面 に 差込み

### 5. Sales AI OS research queue (α稼働 中)

- 既に「crawler + ICP scorer」実装 (task #82)
- AI 拡張: ICP score + LLM の 「conversion probability 予測」を combine、 高 spot に 個別 提案

## Reo 「オリジナリティ 演出」の 実 手段 (差別 化 5 軸)

Reo 指摘「問題 は オリジナリティ 演出」に 対する 答え を 5 軸 で 立てた:

1. **data-driven curation** — EV2 score (期待 売上 model) で mechanical 選定、 感覚 選定 と 差別 化
2. **founder solo context** — 「1 人 で 4 core SaaS を 運用 する 会社」の 生活 context (渋谷 道玄坂 事務所) を 埋め込み
3. **4 core adjacent framing** — Kigen / Nexa / XCloud / Xiora Lingua の POV から 生活 品 を re-frame (「Kigen 使い が 期限 切れ しない 収納」等)
4. **fact-first tone** — xiora HP directive「甘 過ぎ 禁止」を 継承、 review 数値 · 実 使用 経過 で 裏付け
5. **AI-visible operation** — 「AI が curation して いる こと」を 隠さ ず、 むしろ 差別 化 factor と して 明示 (「AI 会社 が data で 選んだ 今 週 の 実 用 品」)

## 憲法 遵守 (CLAUDE.md 準拠)

- **Vault access**: LLM prompt に secret 埋め込み 禁止、 secret は `services/shared/vault_client` 経由 のみ
- **Supabase 禁止**: 全 pipeline は SQLite + Postgres direct のみ
- **Mac 負荷 抑制**: Ollama は 7b default、 14b は 品質 優先 時 のみ、 32b 禁止 (`memory/feedback_mac_no_heavy_load_2026_07_25.md`)
- **憲法 grep**: 全 pipeline output は kakuyomu / 小説 家 名義 / .env / supabase = 0 hit を 実行 前 に 自動 check
- **投稿 禁止 tone**: 誇大 · 医薬品 · 芸能人 · 他 EC URL 混入 = 全 auto reject + Reo 通知

## 次 の AI 化 対象 (Roadmap)

- 記事 SEO keyword clustering (Ollama で 意味 空間 分類)
- Xiora Lingua lesson の 音声 生成 (現行 = Web Speech API、 品質 上げる なら ElevenLabs / OpenAI TTS)
- Kigen アプリ 内 「AI 期限 提案」機能 (「保証 期限 30 日 前」で 通知 する 判断 を LLM が 個別 tuning)
- XCloud Connect 導入 店舗 の menu translation を LLM で 多 言語 化
- Nexa Academy AI 講師 の 個別 応答 品質 の LLM golden set (memory 済 spec)

## 稼働 中 の LLM 資源

- **Ollama local** (Mac): qwen2.5:14b (8.5GB), qwen2.5:7b (4.4GB), llama3 (4.4GB), embed models
- **Anthropic API** (Reo billing): Claude Opus 4.7 (本 Body Claude), Claude Sonnet 4.6 (subagent)
- **OpenAI API** (Reo billing 有): ChatGPT Plus (量産 · Body 経由 で orchestrate)
- **Gemini Pro** (Reo billing 有): 画像 / 動画 / search grounded (browser Claude 経由)

各 model の 使い 分け rule は `memory/multi_ai_routing_2026_07_27.md` に 記録 済。
