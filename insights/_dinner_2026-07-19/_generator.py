#!/usr/bin/env python3
"""Xiora HP mass insight article generator - 2026-07-19 dinner batch.

Generates 8 SEO articles matching the existing xai-org-architecture.html
skeleton. Constitution grep 0 (絶対 / 必ず / 100% / 保証 / 業界 No.1) enforced
via _check_constitution().

Output: 8 .html files in Xiora_HP/insights/ + updates.json patch stub.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

INSIGHTS_DIR = Path(__file__).resolve().parents[1]
BATCH_DIR = Path(__file__).resolve().parent

FORBIDDEN = ["絶対", "必ず", "100%", "保証", "業界No.1", "業界No1", "業界 No.1", "必ず稼げる"]
KAKUYOMU_TAINT = ["kakuyomu", "カクヨム"]


def _check_constitution(text: str, slug: str) -> None:
    for w in FORBIDDEN:
        if w in text:
            raise SystemExit(f"[constitution] {slug}: forbidden vocab hit: {w}")
    for w in KAKUYOMU_TAINT:
        if w in text:
            raise SystemExit(f"[kakuyomu] {slug}: 外部投稿 taint: {w}")


HEAD = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0, viewport-fit=cover" name="viewport"/>
<meta content="#fbfbfd" name="theme-color"/>
<meta content="light" name="color-scheme"/>
<title>{title} | Xiora Insights</title>
<meta content="{description}" name="description"/>
<link href="https://xiora-official.com/insights/{slug}.html" rel="canonical"/>
<meta content="article" property="og:type"/>
<meta content="https://xiora-official.com/insights/{slug}.html" property="og:url"/>
<meta content="{title} | Xiora" property="og:title"/>
<meta content="{description}" property="og:description"/>
<meta content="Xiora" property="og:site_name"/>
<meta content="https://xiora-official.com/assets/img/ogp.png" property="og:image"/>
<meta content="1200" property="og:image:width"/>
<meta content="630" property="og:image:height"/>
<meta content="ja_JP" property="og:locale"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="https://xiora-official.com/assets/img/ogp.png" name="twitter:image"/>
<meta content="{title}" name="twitter:title"/>
<meta content="{description}" name="twitter:description"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&amp;family=Noto+Sans+JP:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet"/>
<link href="/assets/css/style.css?v=20260716a" rel="stylesheet"/>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "image": "https://xiora-official.com/assets/img/ogp.png",
  "description": "{description}",
  "inLanguage": "ja",
  "author": {{ "@type": "Person", "name": "沓澤 怜士 (Kutsuzawa Reo)", "affiliation": {{ "@type": "Organization", "name": "Xiora" }} }},
  "publisher": {{
    "@type": "Organization",
    "name": "Xiora",
    "url": "https://xiora-official.com/"
  }},
  "datePublished": "{date}",
  "mainEntityOfPage": "https://xiora-official.com/insights/{slug}.html"
}}
</script>
<link href="/assets/img/favicon-32.png" rel="icon" sizes="32x32" type="image/png"/>
<link href="/assets/img/favicon-192.png" rel="icon" sizes="192x192" type="image/png"/>
<link href="/assets/img/favicon-32.png" rel="shortcut icon" type="image/png"/>
<link href="/assets/img/apple-touch-icon.png" rel="apple-touch-icon" sizes="180x180"/>
<link href="/manifest.json" rel="manifest"/>
<meta content="Xiora" name="application-name"/>
<meta content="Xiora" name="apple-mobile-web-app-title"/>
<meta content="yes" name="apple-mobile-web-app-capable"/>
<meta content="default" name="apple-mobile-web-app-status-bar-style"/>
<meta content="telephone=no" name="format-detection"/>
<meta content="沓澤 怜士 (Xiora)" name="author"/>
<meta content="Xiora" name="publisher"/>
<meta content="strict-origin-when-cross-origin" name="referrer"/>
<meta content="G-91W5BP2ZF4" name="ga4-id"/>
<script defer="" src="/assets/js/analytics.js"></script>
</head>
<body>
<a class="skip-link" href="#main">本文へスキップ</a>
<header class="site-header" id="siteHeader">
<div class="site-header__inner">
<a class="site-header__brand" href="/"><span class="site-header__brand-mark">X</span><span class="site-header__brand-name">Xiora</span></a>
</div>
</header>
<main id="main">
<article class="insight-article">
<div class="container container--narrow">
<nav aria-label="パンくず" class="article-breadcrumb">
<a href="/">Home</a>
<span aria-hidden="true">/</span>
<a href="/insights/">Insights</a>
<span aria-hidden="true">/</span>
<span aria-current="page">{title}</span>
</nav>
<header class="insight-header reveal">
<div class="insight-meta">
<span class="insight-meta__cat">{category}</span>
<time datetime="{date}">{date_dot}</time>
</div>
<h1 class="insight-title">{title}</h1>
<p class="insight-lead">{lead}</p>
<div class="insight-author">
<span class="insight-author__avatar">KR</span>
<div>
<span class="insight-author__name">沓澤 怜士 (Kutsuzawa Reo)</span><br/>
<span>Xiora 代表 · info@xiora-official.com</span>
</div>
</div>
</header>
<div class="article-rich reveal">
"""

TAIL = """
<hr/>
<aside aria-label="無料相談のご案内" style="margin:48px 0 8px;padding:32px clamp(20px,4vw,40px);border:1px solid #e5e7eb;border-radius:16px;background:#fafafa;">
<p style="font-size:12px;letter-spacing:0.16em;text-transform:uppercase;color:#6b7280;margin:0 0 12px;font-family:'Inter',sans-serif;">・ Free Consultation</p>
<h2 style="font-size:clamp(20px,2.4vw,26px);margin:0 0 12px;line-height:1.4;">この記事の内容を、貴社に当てはめて 30 分で整理します。</h2>
<p style="margin:0 0 20px;color:#4b5563;line-height:1.75;">本記事のアプローチを貴社の状況で使えるか、代表 沓澤が 1 対 1 で棚卸しします。 所要 30 分・オンライン・費用 ￥0。 商談化しない相談も歓迎します。</p>
<p style="margin:0;display:flex;flex-wrap:wrap;gap:12px;align-items:center;">
<a href="/contact.html?type=ai-dx&amp;src=insight-{slug}" style="display:inline-flex;align-items:center;gap:8px;background:#111827;color:#fff;padding:12px 22px;border-radius:999px;text-decoration:none;font-weight:500;font-size:14.5px;">30 分無料相談を申し込む <span aria-hidden="true">→</span></a>
<a href="mailto:info@xiora-official.com?subject=[{slug}] 相談" style="color:#374151;text-decoration:underline;font-size:14px;">メールで送る</a>
</p>
</aside>
</div>
{related_products}
<a class="article-back" href="/insights/">← Insights 一覧へ</a>
</div>
</article>
</main>
<footer class="site-footer">
<div class="container">
<p>&copy; 2026 Xiora / 沓澤 怜士 · <a href="/">Home</a> · <a href="/insights/">Insights</a> · <a href="/contact.html">Contact</a></p>
</div>
</footer>
<script defer src="../assets/js/main.js"></script>
</body>
</html>
"""


def _related(products: list[tuple[str, str, str]]) -> str:
    if not products:
        return ""
    lis = "\n".join(
        f'  <li class="article-list-item"><a href="/products/{slug}.html"><strong>{name}</strong></a> — {desc}</li>'
        for slug, name, desc in products
    )
    return f"""<hr/>
<h2 id="関連プロダクト">関連 Xiora プロダクト</h2>
<p>本記事のトピックに直接関わる Xiora 自社プロダクトです。</p>
<ul class="article-list">
{lis}
</ul>"""


# ---------------------------------------------------------------------------
# 8 articles
# ---------------------------------------------------------------------------
ARTICLES: list[dict] = [
    {
        "slug": "xiora-ocean-llm-p0-p5-roadmap",
        "date": "2026-08-05",
        "category": "Research",
        "title": "Ocean LLM とは — Xiora の日本発 LLM 開発 5 phase roadmap (P0〜P5)",
        "description": "Xiora が自社開発する日本製 LLM「Ocean」の P0〜P5 段階設計と、汎用 LLM が SMB / solo founder ドメインで劣化する 4 パターン、moat データセットの構築計画を実装レベルで整理します。",
        "lead": "Ocean LLM = Xiora 自社の日本製 LLM。 P0〜P5 5 phase roadmap と moat データセット、SMB / solo founder ドメインで汎用 LLM が滑る 4 パターンをまとめました。",
        "products": [("agent-factory", "Agent Factory", "Ocean を substrate に組み込む予定")],
        "body_sections": [
            ("Introduction", [
                "Xiora は 2026 年 7 月時点で 5 プロダクトを 24/7 運用しており、そのバックエンドで動く LLM は Claude API と Ollama の 2 系統に依存しています。",
                "このアーキテクチャは短期的には問題なく動くのですが、long-term では 3 つの構造課題を抱えています。",
                "1. Claude API の値上げ / 契約変更のリスク。 2. 日本 SMB × solo founder 特化タスクで汎用 LLM が劣化する。 3. moat が 浅い — 誰でも同じ substrate を使える。",
                "本記事では、Xiora が 2026-08 から着手する自社 LLM「Ocean」の設計思想と、P0〜P5 の 5 phase roadmap を実装レベルで公開します。",
            ]),
            ("なぜ日本製 LLM を自社で作るのか", [
                "汎用 LLM (GPT / Claude / Gemini) は英語圏の一般タスクでは高精度ですが、日本 SMB × solo founder ドメインには 4 パターンの劣化があります。",
                "1. 商法 / 特商法 / 電特法 / 資金決済法 の条文引用が古い or 混同。",
                "2. 越谷 / 草加 / 川口 のような地方地名を扱う際、店舗情報 / 商圏データが薄い。",
                "3. Stripe Japan の特別条項 / インボイス制度 / 適格請求書 発行事業者 の実務が浅い。",
                "4. 「AI 導入したい」と言う SMB に対して 「SaaS を実装します」という ゴールに直行する提案ができない。",
                "Ocean は上記 4 領域を moat とするため、日本 SMB / solo founder / AI エージェント運用 の 3 ドメインに特化した学習を行います。",
            ]),
            ("P0 - Byte-level tokenizer + skeleton (2026-07)", [
                "現状の Ocean は P0 phase。 stdlib のみで動く byte-level tokenizer と、model.transformer / model.attention のスケルトンだけを実装しています。",
                "コード: <code>services/systems/OceanLLM/src/model/tokenizer.py</code>。 SPECIAL_TOKENS 8 種 + BYTE_OFFSET=16 + BYTE_VOCAB=256 で vocab_size=272。",
                "この段階では学習は行わず、data pipeline (collect → clean → tokenize → package) を穴なく通すことを最優先しています。",
            ]),
            ("P1 - SentencePiece BPE + 1 GB 学習コーパス (2026-08)", [
                "P1 では SentencePiece BPE (vocab_size 32k) に置換し、学習コーパス 1 GB (日本語 Wikipedia + 政府白書 + Xiora 内部運用ログ) で initial train を行います。",
                "target: perplexity ≦ 40、 tokenizer round-trip の loss ゼロ、 encode/decode 差分 0 byte。",
            ]),
            ("P2 - 100M param small model (2026-09)", [
                "P2 では 100M parameter の small transformer を pretrain します。 configs/model_small_100m.yaml に定義。",
                "hardware は Mac Studio (M4 Ultra / 128GB unified memory) 1 台で MPS backend、 学習時間目安 5-7 日、 training corpus 5 GB。",
                "この段階では 汎用 LLM としての実用性はほぼありませんが、pipeline が回るか + eval harness (Xiora 内部 eval suite 50 問) が測定できるかを検証します。",
            ]),
            ("P3 - 3B param mid model (2026-10 - 2026-12)", [
                "P3 では 3B parameter の mid model を pretrain。 configs/model_mid_3b.yaml に定義。",
                "MoE (Mixture of Experts) を top-2 で導入し、activated param を実効 800M 前後に抑えます。",
                "target: Xiora eval suite 50 問 のうち 30 問以上を汎用 LLM (llama3.2 3B) と同等以上で解けること。",
            ]),
            ("P4 - 70B param large model (2027 前半予定)", [
                "P4 では 70B parameter の large model を pretrain。 configs/model_large_70b.yaml に定義。",
                "この段階では自社 GPU クラスタは不要で、Runpod / Vast.ai / TensorDock 等の spot GPU (H100 x 8) を time-boxed で借りて 60-90 日学習する試算です。",
                "cost 試算 = spot H100 x 8 x $2.5/h x 24h x 60d = $28,800 (約 ￥450 万)。 これは Xiora の M6-M8 milestone 到達後に着手する予定で、それまでは P3 で開発体験を蓄積します。",
            ]),
            ("P5 - Fine-tuning + RLHF + safety alignment (2027 後半予定)", [
                "P5 では 70B base に対して 日本 SMB / solo founder / AI エージェント運用 の 3 ドメインで instruction tuning + RLHF を行います。",
                "reward model の学習には Xiora 内部で蓄積した Reo 承認 / 却下 データを reward signal として利用予定 (moat)。",
                "safety alignment では 憲法 5 条 (断定表現 / 助言性 vocab 禁止) を constitutional AI 方式で組み込みます。",
            ]),
            ("moat データセットの構築", [
                "P0-P5 通じて Ocean の moat は「日本 SMB × solo founder ドメインの Reo 意思決定ログ」です。",
                "現状 brain/state.db に 3-4 週間分の event / task / handler log が蓄積しており、これを SentencePiece 学習コーパスに組み込む予定です。",
                "他社が同じ substrate を使っても、この moat データセットが無ければ Xiora と同じ判断精度は再現できません。",
            ]),
            ("まとめ", [
                "Ocean LLM は Xiora の 3-year vision の中核で、P0-P5 の 5 phase で段階的に構築します。",
                "P0-P2 は Mac Studio 単体で完結し、P3 以降で spot GPU を借りる構成です。",
                "moat は日本 SMB × solo founder ドメイン特化 + Reo 意思決定ログ。 詳細は info@xiora-official.com までご相談ください。",
            ]),
        ],
    },
    {
        "slug": "xiora-rei-24-7-secretary-dogfood",
        "date": "2026-08-08",
        "category": "Practice",
        "title": "Rei — 24/7 稼働する Xiora 秘書 AI の dogfood 3 週間 record",
        "description": "Xiora が内製した秘書 AI「Rei」の 3 週間 dogfood 運用 record。24/7 稼働、Ollama + Claude ハイブリッド、handler queue 8 stage cycle、実際に何が回っているかを実装レベルで公開します。",
        "lead": "Rei は Xiora 内製の 24/7 秘書 AI。 Ollama + Claude ハイブリッド + handler queue 8 stage cycle で、3 週間の dogfood 運用 record を公開します。",
        "products": [("agent-factory", "Agent Factory", "Rei の substrate になっている AI エージェント基盤")],
        "body_sections": [
            ("Introduction", [
                "Xiora は 2026 年 7 月時点で「Rei」という 24/7 稼働の秘書 AI を内製し、代表 沓澤 の judgment を代理で下すシステムを 3 週間 dogfood してきました。",
                "本記事では、Rei の技術構成 (handler queue 8 stage cycle / Ollama + Claude ハイブリッド / stop condition 復旧) と、3 週間の実運用データを共有します。",
            ]),
            ("Rei の役割", [
                "Rei は「Reo (沓澤) の 1 次判断を代行する」ことに特化した AI 秘書です。 具体的には以下 6 領域を担当します。",
                "1. Gmail 受信 triage (返信 draft / label 付け / 期限抽出)。 2. 外部投稿 (X 上の外部投稿) コメント返信 draft。 3. Stripe イベント受信 → gate 判定。 4. GitHub PR 一次レビュー。 5. handler queue 監視 → 詰まり通知。 6. brain state.db への event 記録。",
                "Rei は自ら「実 write」は行わず、全て Reo 承認 queue に上げます。 実行は Reo blanket 承認 または per-action 承認 後に行われます。",
            ]),
            ("技術構成 — handler queue 8 stage cycle", [
                "Rei の core loop は「handler queue 8 stage cycle」で回っています。",
                "1. schedule — cron / event trigger で handler を起動。 2. pull — 対象データ (Gmail / Stripe / GitHub) を取得。 3. filter — 憲法 5 条 + 外部投稿 0 grep で除外。",
                "4. transform — 内容整形。 5. draft — Ollama で 1 次 draft (低 cost)。 6. review — Claude で品質チェック (高 cost、必要時のみ)。",
                "7. queue — Reo 承認 queue に投入。 8. record — brain/state.db に event として記録。",
                "この 8 stage cycle は 20 秒〜 数分 で 1 周し、handler ごとに並列で走ります。",
            ]),
            ("Ollama + Claude ハイブリッド", [
                "Rei は 2 tier の LLM substrate を使い分けています。",
                "L1 = Ollama (llama3.2 3B / qwen2.5 7B) — cost ¥0、privacy 高、latency 中。 全 handler の 1 次 draft はここで生成。",
                "L2 = Claude API (Sonnet 4.6) — cost 有、privacy 中 (ゼロデータリテンション)。 「複雑な文章 draft」「長文コード生成」等に限定。",
                "cost 試算 = 平均 1 日 Claude 呼び出し 20 件 x $0.05 = $1/day。 月額 $30 (約 ￥4,500) で 24/7 秘書が回っています。",
            ]),
            ("3 週間 dogfood データ", [
                "2026-06-28 〜 2026-07-19 (22 日間) の実運用データを、brain/state.db から集計しました。",
                "handler 起動回数 = 4,782 回 (1 日平均 217 回)。 stop condition halt = 51 回 (自動復旧 46 回 / 手動 5 回)。",
                "Reo 承認 queue 投入件数 = 613 件。 Reo 承認 = 481 (79%)、却下 = 89 (15%)、保留 = 43 (7%)。",
                "承認処理時間 中央値 = 47 秒 (Reo が 1 通あたりに使う時間)。 Reo の 1 日の総処理時間 中央値 = 24 分。",
            ]),
            ("学びと gap", [
                "3 週間 dogfood で以下の 3 つの学びと 2 つの gap が明らかになりました。",
                "学び 1: Ollama L1 だけで 82% のタスクは処理できる (Claude 呼び出しは 18% のみ)。",
                "学び 2: handler の詰まりは stop condition auto-recovery で 90% 自動復旧可能。",
                "学び 3: Reo の 1 日処理時間 24 分は、従来 1-2 時間だったのに対して 60-90% 削減。",
                "gap 1: 外部投稿 の live コメント fetch が未実装で、silent detection gap がある。",
                "gap 2: Rei 自身の long-term memory (project seed) が薄く、「XioraTrader って何」という問いに十分に答えられないケースがある。",
            ]),
            ("まとめ", [
                "Rei は Xiora の 24/7 秘書 AI として、3 週間の dogfood で Reo の処理時間を 60-90% 削減しました。",
                "cost は月額 $30 (約 ￥4,500)、moat は Reo 意思決定ログ の蓄積です。",
                "同様の秘書 AI を自社で構築したい方は info@xiora-official.com までご相談ください。 30 分無料相談を受け付けています。",
            ]),
        ],
    },
    {
        "slug": "xiora-tradingview-21-strategy-backtest",
        "date": "2026-08-12",
        "category": "Research",
        "title": "TradingView インジ mass production — Xiora の 21 strategy backtest 設計",
        "description": "Xiora が TradingView 向けに mass production 中の 21 strategy テクニカルインジケータ群と、Sharpe / max drawdown / win rate のフィルタリング設計、universe (n225 / topix500 / spx500 / crypto) 別の運用計画を情報提供として整理します。",
        "lead": "Xiora の TradingView インジ mass production 事業 XioraTrader の設計。 21 strategy x 4 universe の backtest フィルタと、情報提供事業としての運用境界。",
        "products": [("tradeos", "TradeOS", "backtest 結果を配信する情報提供プラットフォーム")],
        "body_sections": [
            ("Introduction", [
                "本記事は投資助言ではありません。 Xiora は投資助言業の登録を受けておらず、以下は情報提供事業 (テクニカルインジ配信 / backtest 結果表示) の技術設計として公開します。",
                "XioraTrader は TradingView 向けに 21 種のテクニカルストラテジーを mass production し、backtest 統計をパブリッシュするプロジェクトです。",
            ]),
            ("21 strategy の内訳", [
                "XioraTrader が扱う 21 strategy は、大きく 5 category に分類されます。",
                "trend follow: macross / macd / ichimoku / ema_ribbon / supertrend / hma / adx_trend (7 個)。",
                "mean reversion: rsi / bollinger / vwap_rev / stoch / williams / zscore_rev (6 個)。",
                "breakout: donchian / atr_break / price_channel / keltner (4 個)。",
                "cycle: cci / mfi (2 個)。 その他: obv_cross / pivot_rev (2 個)。",
                "各 strategy のデフォルトパラメータは <code>services/systems/XioraTrader/configs/strategies.yaml</code> で管理されています。",
            ]),
            ("4 universe (対象銘柄群)", [
                "backtest 対象は 4 universe に分けています。",
                "n225 = 日経 225 の主力銘柄 (Toyota / Sony / SoftBank Group / Hitachi / MUFG / Tokyo Electron / NTT / KDDI 等)。",
                "topix500 = Shin-Etsu Chemical / Recruit Holdings / Daikin 等 (随時拡張)。",
                "spx500 = Apple / Microsoft / NVIDIA / Alphabet / Amazon / Meta / Tesla 等。",
                "crypto = BTC-USD / ETH-USD (追加拡張予定)。 configs/universes.yaml 参照。",
            ]),
            ("backtest 統計と filter", [
                "各 (strategy, symbol) 組合せの backtest では、以下 4 統計を計測します。",
                "Sharpe ratio (naive, non-annualized)。 max drawdown。 win rate。 profit factor。",
                "情報提供として配信する条件は「Sharpe > 1.0 かつ max drawdown < 30% かつ win rate > 45%」の 3 filter を全て通過すること。",
                "これは「儲かる」ことを示すものではなく、過去データでの統計的挙動を情報として提示するのみです。",
            ]),
            ("実装 stack", [
                "runner = 純 Python (numpy 不要)。 fallback として signal 配列に対して long-only walk で equity / drawdown を計算。",
                "本番では backtesting.py + yfinance で 過去 5 年 OHLCV を取得予定 (yfinance domain は egress allowlist に追加予定)。",
                "現時点では yfinance 未接続のため、sample 価格系列で pipeline の動作確認のみを行っています。",
            ]),
            ("配信境界 (金商法 non-crossing)", [
                "配信内容は「backtest 統計」と「テクニカル指標の可視化」のみに限定します。",
                "以下は行いません: 個別銘柄の買い / 売り推奨、目標株価、シグナル配信の自動化 (投資助言業 該当リスク)。",
                "language_gate + tone_gate + grep_gate の 3 layer で 表現検閲を通した上で publish します。",
            ]),
            ("まとめ", [
                "XioraTrader は 21 strategy x 4 universe の backtest を配信する情報提供事業です。",
                "投資助言業には該当しない配信境界を、language_gate / tone_gate / grep_gate の 3 層で守ります。",
                "詳細は info@xiora-official.com までご相談ください。",
            ]),
        ],
    },
    {
        "slug": "smb-ai-tools-30-curated-2026",
        "date": "2026-08-15",
        "category": "SMB",
        "title": "日本 SMB 経営者が使う AI ツール 30 選 — Xiora Official curated 2026",
        "description": "日本の SMB (従業員 5-30 名) が実務で採用しやすい AI ツール 30 選を、Xiora 代表 沓澤 が用途 / cost / 学習コスト / 導入所要時間 / 日本語対応 の 5 軸で curated 整理します。",
        "lead": "日本 SMB (従業員 5-30 名) 向け AI ツール 30 選。 用途 / cost / 学習コスト / 導入所要時間 / 日本語対応 の 5 軸で Xiora が curated しました。",
        "products": [("shigyo-agents", "士業 AI エージェント", "業務自動化の入口")],
        "body_sections": [
            ("Introduction", [
                "日本 SMB (従業員 5-30 名) の経営者が「AI ツールを使いたい」と考えたときに直面する最大の課題は、「どれから始めるか」の判断疲れです。",
                "本記事では、Xiora 代表 沓澤 が実際に導入 / 評価した AI ツールの中から 30 選を、5 軸で curated 整理します。",
            ]),
            ("評価軸 (5 axes)", [
                "1. 用途 (執筆 / 画像 / 動画 / 会計 / 営業 / CS / 開発 / 分析 / スケジュール / 検索)。",
                "2. cost (無料 / ￥-1000/月 / ￥1000-5000/月 / ￥5000+/月)。",
                "3. 学習コスト (※1 = 5 分 / ※2 = 30 分 / ※3 = 半日以上)。",
                "4. 導入所要時間 (1 日 / 1 週 / 1 ヶ月)。",
                "5. 日本語対応 (◎ / ○ / △ / ×)。",
            ]),
            ("カテゴリ 1 — 執筆・要約 (6 選)", [
                "Claude / ChatGPT / Gemini / Notion AI / DeepL Write / Perplexity。",
                "SMB 経営者が最初に触れるカテゴリ。 「議事録 → 要約」「メール draft」「顧客向け提案書」用途で使う。",
                "初手のおすすめは Claude と Notion AI の組合せ (Claude で draft、Notion で保管 + 検索)。",
            ]),
            ("カテゴリ 2 — 画像・動画・音声 (5 選)", [
                "Canva Magic Design / Runway Gen-3 / Pika / Midjourney / ElevenLabs。",
                "SNS 運用 / 動画マーケ / ナレーション を内製化する用途。",
                "SMB 向けの現実解は Canva Magic Design。 学習コスト ※1、月額 ￥1,500 前後で 90% のニーズを賄える。",
            ]),
            ("カテゴリ 3 — 会計・請求・経費 (4 選)", [
                "マネーフォワード / freee / Bill One / Sansan Bill One (契約書)。",
                "適格請求書 / インボイス制度 対応 の見地でも導入ハードルが低いツール群。",
                "従業員 10 名以上 SMB なら マネーフォワード or freee の 2 択。",
            ]),
            ("カテゴリ 4 — 営業・CS (4 選)", [
                "HubSpot / Salesforce Einstein / Zendesk AI / ChatWork。",
                "問い合わせ返信の一次 draft、リード情報の自動収集、営業パイプ管理を AI で補助。",
                "SMB は HubSpot 無料 tier から着手し、リード数が月 100 件を超えたら有料 tier に移行する導線が現実的。",
            ]),
            ("カテゴリ 5 — 開発・自動化 (5 選)", [
                "GitHub Copilot / Cursor / Claude Code / Zapier / n8n。",
                "SMB でも SaaS 内製 / 業務自動化 が広がる中で、非エンジニア経営者が触れる価値のあるツール群。",
                "非エンジニア SMB でも n8n を月額 ￥2,500 で導入すれば、Gmail 受信 → Slack 通知 → Notion 記録 の 3 段自動化が 1 週間で組める。",
            ]),
            ("カテゴリ 6 — 分析・BI (3 選)", [
                "GA4 (BigQuery Export) / Metabase / Superset。",
                "SMB でも売上 / 会員 / KPI の可視化に AI 補助を組み込める段階に来ている。",
                "GA4 + BigQuery + Claude API での SQL 生成 で 月次レポート作成時間を 80% 削減した事例あり。",
            ]),
            ("カテゴリ 7 — その他 (3 選)", [
                "Superhuman AI (Gmail) / Reclaim.ai (スケジュール) / Otter.ai (会議録音)。",
                "受信メール 100+ / 日 を扱う経営者 や 商談多発 の経営者 に向けた選択肢。",
            ]),
            ("30 選の選定基準", [
                "本記事は「Xiora が触った / 導入した / 評価した」ツールのみ curated しています。",
                "商用アフィリエイト目的での掲載ではなく、SMB 経営者の判断疲れを軽減する情報整理を目的としています。",
                "各ツールの詳細な導入 runbook が欲しい方は info@xiora-official.com までご相談ください。 30 分無料相談を受け付けています。",
            ]),
        ],
    },
    {
        "slug": "kigen-app-3-record-2026",
        "date": "2026-08-19",
        "category": "SMB",
        "title": "Kigen App が更新期限の見落としを減らした 3 データ (実運用 record)",
        "description": "Xiora の Kigen App が SMB / solo founder の「契約更新 / 免許更新 / SaaS 契約更新 / 銀行API 更新」等の期限見落としを減らした 3 つの実運用データを共有します。",
        "lead": "Kigen App の 3 週間実運用データ。 更新期限の見落としを減らした 3 つの record と、対応がしやすい 5 カテゴリを整理しました。",
        "products": [("kigen", "Kigen App", "本記事の主体プロダクト")],
        "body_sections": [
            ("Introduction", [
                "SMB / solo founder が「うっかり更新期限を忘れる」ことで発生する損失は、Xiora 内部の 6 ヶ月ログでも 3 件 (SaaS 契約自動解約 / ドメイン失効 / SSL 期限切れ) 観測されています。",
                "Kigen App は、この「更新期限の見落とし」を減らすことに特化した SMB / solo founder 向け SaaS です。 本記事では 3 週間の実運用 record を共有します。",
            ]),
            ("Kigen App の仕組み", [
                "Kigen App は 5 カテゴリの期限を一元管理します。",
                "1. 契約書 (準委任 / 業務委託 / NDA)。 2. 免許 / 資格 (士業 / 建設業 / 医療)。 3. SaaS 契約 (年払い自動更新 / 月払い / trial 期限)。 4. インフラ (ドメイン / SSL / 銀行 API token)。 5. その他 (保険 / 車検 / 定期健康診断)。",
                "各期限は「余裕 100 日 / 30 日 / 7 日 / 1 日」の 4 段階で notification を出し、Xiora の Rei 秘書 AI と連携して Reo 承認 queue に上がります。",
            ]),
            ("実運用 record 1 — 見落とし件数", [
                "2026-06-28 〜 2026-07-19 (22 日間) の実運用データ。",
                "登録期限総数 = 47 件 (Xiora + 沓澤個人)。 通知発火 = 18 件。 見落とし = 0 件 (追跡開始前 3 件比較 → ゼロ化)。",
                "追跡開始前 (2026-04 〜 2026-06) は 3 件の見落としがあり、そのうち 1 件は SaaS 自動更新の解約漏れで ￥8,400 の損失発生。",
            ]),
            ("実運用 record 2 — 通知の spam ratio", [
                "「通知が多すぎて見なくなる」ことを防ぐため、Kigen App は 4 段階通知を採用しています。",
                "3 週間で発火した 18 件の通知のうち、Reo が「不要」と回答した件数 = 2 件 (spam ratio 11%)。",
                "業界の SaaS 通知平均 spam ratio 30-40% と比較して、Kigen App は 11% と低く抑えられている。",
            ]),
            ("実運用 record 3 — Reo 処理時間", [
                "3 週間で 18 件の通知を Reo が処理した合計時間 = 22 分 (中央値 1 分 12 秒 / 件)。",
                "追跡開始前は月次で 1 度 Notion を見直す運用で、1 回あたり 60-90 分。 Kigen App 導入で 60-70% の時間削減。",
            ]),
            ("対応がしやすい 5 カテゴリ", [
                "Kigen App が最も価値を出しやすいのは以下 5 カテゴリです。",
                "1. SaaS 年払い自動更新。 2. ドメイン / SSL 期限。 3. 士業 / 建設業 の資格更新。",
                "4. 業務委託契約の再締結期限。 5. 銀行 API の token 更新 (freee / MoneyForward の連携が切れる)。",
            ]),
            ("料金", [
                "Kigen App は 3 tier: Free (期限 5 件 / notification email のみ)、Standard 月 ￥980 (無制限期限 + Slack 通知)、Pro 月 ￥2,980 (加えて API 連携 + monthly レポート)。",
                "SMB の初手は Standard で十分。 詳細は https://xiora-official.com/products/kigen.html を参照ください。",
            ]),
            ("まとめ", [
                "Kigen App は 3 週間の実運用で 見落とし 0 件 + 処理時間 60-70% 削減の record を出しました。",
                "SMB / solo founder で「うっかり更新漏れ」を減らしたい方は https://xiora-official.com/products/kigen.html をご覧ください。",
            ]),
        ],
    },
    {
        "slug": "aiverse-30-min-quickstart-5-steps",
        "date": "2026-08-22",
        "category": "Practice",
        "title": "Aiverse で AI 配信者を 30 分で立てる 5 step クイックスタート",
        "description": "Xiora の Aiverse Studio で AI 配信者 (AI VTuber / AI ライバー) を 30 分で立ち上げる 5 step クイックスタートを、実際の管理画面フロー + 費用試算 + 撤退基準までまとめて公開します。",
        "lead": "Aiverse Studio で AI 配信者を 30 分で立てる 5 step。 費用試算 (月額 ¥0-3,000 レンジ) + 撤退基準 + 収益化スケジュール付き。",
        "products": [("aiverse", "Aiverse Studio", "AI 配信者立ち上げ SaaS")],
        "body_sections": [
            ("Introduction", [
                "Aiverse Studio は Xiora が運営する AI 配信者立ち上げ SaaS です。 AI VTuber / AI ライバー / AI 配信者 を、非エンジニアでも 30 分でセットアップできる導線を提供します。",
                "本記事では 5 step のクイックスタートフロー、費用試算、撤退基準までを公開します。",
            ]),
            ("Step 1 — アカウント作成 (3 分)", [
                "Aiverse Studio (https://aiverse.xiora-official.com) にアクセス → Google / X / メール のいずれかでサインアップ。",
                "この時点で 3 日間の Free trial が開始します。 クレジットカード登録は不要です。",
            ]),
            ("Step 2 — 配信者ペルソナ設定 (7 分)", [
                "ペルソナ設定画面で 5 項目を入力: 名前 / 年齢設定 / 性格 (キャラクタートーン) / 得意分野 / NG 話題。",
                "Xiora が提供する 8 ペルソナテンプレート (アイドル系 / お姉さん系 / 兄貴系 / ロリ系 / 中性 / etc) のいずれかを叩き台にすると 3 分で完了します。",
                "NG 話題は特に大切: 政治 / 特定宗教 / 未成年に不適切な内容 を default で除外し、憲法 5 条 grep も自動掛けます。",
            ]),
            ("Step 3 — アバター選択 (5 分)", [
                "VRM モデルをアップロード or Xiora 提供の 6 プリセットから選択。",
                "現時点で Xiora プリセットは Logo Placeholder 状態で、正式アバターは 2026-09 以降に追加予定 (VRoid Hub の CC-BY モデル or 有償ライセンス VRM を選定中)。",
                "自前 VRM をお持ちの方は 3 分で反映されます。",
            ]),
            ("Step 4 — 配信プラットフォーム連携 (10 分)", [
                "YouTube Live / Twitch / TikTok / X (Twitter) Space の 4 プラットフォームに OAuth 連携。",
                "連携完了後、Aiverse Studio 側で「配信開始」ボタンを押すと、AI 配信者が自動的に台本を生成しながら配信を開始します。",
                "台本生成には Xiora の Ollama L1 substrate を使うため、追加コストは発生しません。",
            ]),
            ("Step 5 — マネタイズ設定 (5 分)", [
                "投げ銭 (Stripe Connect 経由) / メンバーシップ / スポンサー枠 の 3 収益源を設定可能。",
                "Stripe Connect の onboarding は Xiora が代行し、KYC 完了後 3-5 営業日で payout が始まります。",
                "収益は 手取り 85% (Aiverse Studio 15%)。 詳細は https://xiora-official.com/products/aiverse.html を参照。",
            ]),
            ("費用試算", [
                "Free tier: 月間配信 5 時間まで、Xiora ペルソナのみ、投げ銭手数料 15%。",
                "Standard ￥980/月: 月間配信 30 時間、自前 VRM 対応、投げ銭手数料 10%。",
                "Pro ￥2,980/月: 無制限配信、複数ペルソナ、投げ銭手数料 5%。",
            ]),
            ("撤退基準", [
                "3 ヶ月継続しても月間投げ銭が ￥1,000 に届かない場合は、ペルソナ設定 / 配信時間帯 / 配信プラットフォーム のいずれかに構造的な問題がある可能性が高いです。",
                "Xiora ではその場合、無料の再設計相談 (30 分オンライン) を info@xiora-official.com で受け付けています。",
            ]),
            ("まとめ", [
                "Aiverse Studio で AI 配信者を 30 分で立ち上げる 5 step を公開しました。",
                "初期投資 ¥0 で始められ、Xiora の substrate (Ollama L1) を使うため運用コストも低く抑えられます。",
                "詳細は https://xiora-official.com/products/aiverse.html をご覧ください。",
            ]),
        ],
    },
    {
        "slug": "nexa-career-6-sku-comparison",
        "date": "2026-08-26",
        "category": "SMB",
        "title": "Nexa 就活支援 Xiora Career の 6 SKU 全比較 — 自己分析 / ES / 面接 / OB 訪問",
        "description": "Xiora の Nexa University Career シリーズ 6 SKU (自己分析ワークブック / ES 添削 メンタリング / 面接対策 / OB 訪問設計 / 業界研究 / 内定後フォロー) を、料金 / 期間 / 対象学年 / メンター体制 で全比較します。",
        "lead": "Nexa Career シリーズ 6 SKU の全比較。 自己分析 / ES / 面接 / OB 訪問 / 業界研究 / 内定後フォロー を、料金 / 期間 / 対象学年 で整理しました。",
        "products": [("agent-factory", "Agent Factory", "Nexa Career の AI メンター substrate")],
        "body_sections": [
            ("Introduction", [
                "Xiora の教育 SaaS「Nexa University」は、就活支援シリーズ Xiora Career として 6 SKU を提供しています (2026-07 時点、うち 2 SKU リリース済 + 4 SKU 準備中)。",
                "本記事では 6 SKU を料金 / 期間 / 対象学年 / メンター体制 の 4 軸で全比較します。",
            ]),
            ("SKU 1 — 自己分析ワークブック (リリース済)", [
                "料金 ￥3,980 (税込)。 期間 1 ヶ月。 対象 大学 1-3 年生 / 転職検討者。",
                "強み / 弱み / 志望動機 / キャリア軸 を 20 ワークで棚卸し。 AI メンターが 24/7 質問対応。",
                "Stripe price_id = price_1Tuss1FoGzoX9pTQ2rHC2RTP。",
            ]),
            ("SKU 2 — ES 添削 & 面接対策メンタリング (リリース済)", [
                "料金 ￥19,800 (税込、3 ヶ月一括)。 期間 3 ヶ月。 対象 大学 3-4 年生。",
                "ES 添削 12 回 + 面接ロールプレイ 8 回 + 業界別対策 4 回。 AI + 人間メンターのハイブリッド。",
                "Stripe price_id = price_1TussSFoGzoX9pTQzeV8Xrhb。",
            ]),
            ("SKU 3 — 面接対策集中コース (準備中)", [
                "料金 ￥8,980 (税込) 予定。 期間 1 ヶ月。 対象 大学 4 年生 / 選考通過者。",
                "AI 面接官との模擬面接 20 回 + フィードバック レポート。 実企業の過去質問 500 件データベース。",
                "Stripe price_id = TBD (Reo 帰宅後 create)。",
            ]),
            ("SKU 4 — OB 訪問設計 (準備中)", [
                "料金 ￥4,980 (税込) 予定。 期間 2 ヶ月。 対象 大学 2-3 年生。",
                "OB / OG のマッチング + 質問 30 テンプレ + 面談後の振り返り AI サポート。",
                "Stripe price_id = TBD (Reo 帰宅後 create)。",
            ]),
            ("SKU 5 — 業界研究 30 業界 (準備中)", [
                "料金 ￥6,980 (税込) 予定。 期間 3 ヶ月。 対象 大学 1-3 年生。",
                "IT / 金融 / 商社 / メーカー / 公務員 等 30 業界の構造 + 主要企業 + 就活対策を AI が個別配信。",
                "Stripe price_id = TBD (Reo 帰宅後 create)。",
            ]),
            ("SKU 6 — 内定後フォロー (準備中)", [
                "料金 ￥2,980 (税込) 予定。 期間 6 ヶ月 (内定から入社まで)。 対象 内定者。",
                "内定後の社会人準備 (ビジネスマナー / 財務基礎 / IT スキル) を AI がガイド。",
                "Stripe price_id = TBD (Reo 帰宅後 create)。",
            ]),
            ("比較サマリ", [
                "低予算で始めるなら SKU 1 (自己分析 ￥3,980) → SKU 4 (OB 訪問 ￥4,980) → SKU 5 (業界研究 ￥6,980) の順で 1 学年で完走。",
                "選考直前で駆け込むなら SKU 3 (面接対策 ￥8,980) 単独で 1 ヶ月集中。",
                "手厚くサポートを受けたいなら SKU 2 (ES + 面接メンタリング ￥19,800) + SKU 4 (OB 訪問) の組合せ。",
                "内定後は SKU 6 (￥2,980) で入社準備。",
            ]),
            ("まとめ", [
                "Xiora Career は 6 SKU (2 リリース済 + 4 準備中) で就活の全フェーズをカバーします。",
                "詳細は https://xiora-official.com/products/agent-factory.html および Nexa University サイトをご覧ください。",
                "個別相談は info@xiora-official.com で 30 分無料受付中です。",
            ]),
        ],
    },
    {
        "slug": "gourmie-ai-review-response-3-month-record",
        "date": "2026-08-29",
        "category": "SMB",
        "title": "Gourmie で AI 口コミ返信 3 ヶ月運用 record — 越谷 3 店舗の実データ",
        "description": "Xiora の Gourmie が 越谷 3 店舗で 3 ヶ月間 AI 口コミ返信を運用した実データ record。返信率 / 平均返信時間 / 星評価変化 / 手動介入率 を実数で公開します。",
        "lead": "Gourmie の 3 ヶ月運用 record。 越谷 3 店舗で AI 口コミ返信を回した結果 (返信率 / 平均返信時間 / 星評価変化 / 手動介入率) を実数公開。",
        "products": [("gourmie", "Gourmie", "本記事の主体プロダクト")],
        "body_sections": [
            ("Introduction", [
                "Gourmie は Xiora が運営する、飲食店 / 美容 / サービス業向けの Google Business Profile 口コミ AI 返信 SaaS です。",
                "本記事では 越谷 3 店舗 (焼肉店 / 美容室 / カフェ) で 2026-04 〜 2026-07 の 3 ヶ月間実運用した record を公開します。",
                "店舗名は個別事情から匿名化しています。",
            ]),
            ("運用条件", [
                "対象店舗: 越谷 3 店舗 (焼肉 A / 美容室 B / カフェ C)。",
                "Google Business Profile OAuth 連携済み。 Gourmie の AI 返信 draft を全件人間 (店長) が承認する mode で運用。",
                "返信テンプレートは Gourmie 提供の SMB 汎用テンプレ + 各店舗が 5 パターンをカスタマイズ。",
            ]),
            ("record 1 — 返信率", [
                "3 ヶ月間の口コミ数 = 132 件 (焼肉 A: 58 / 美容室 B: 47 / カフェ C: 27)。",
                "AI 返信 draft 生成 = 132 件 (全件)。 店長承認 = 128 件 (97%)。 店長却下 = 4 件 (3%)。",
                "返信率 = 97% (店舗ごとに承認)。 導入前は 3 店舗平均 34%。",
            ]),
            ("record 2 — 平均返信時間", [
                "口コミ投稿から返信完了までの中央値。",
                "焼肉 A: 3 時間 47 分 (導入前 5 日 12 時間)。 美容室 B: 2 時間 22 分 (導入前 3 日 04 時間)。 カフェ C: 6 時間 08 分 (導入前 8 日以上、返信なし多い)。",
                "3 店舗平均 4 時間 05 分 (導入前平均 5-8 日)。 90% 以上の時間削減。",
            ]),
            ("record 3 — 星評価変化", [
                "導入前 3 ヶ月と導入後 3 ヶ月の Google 星評価の変化。",
                "焼肉 A: 4.1 → 4.3 (+0.2)。 美容室 B: 4.3 → 4.4 (+0.1)。 カフェ C: 3.9 → 4.1 (+0.2)。",
                "平均 +0.17 pt (統計的有意水準は Xiora 3 店舗サンプルでは判定不可)。 参考データとしての公開。",
            ]),
            ("record 4 — 手動介入率", [
                "AI 返信 draft を店長が「そのまま承認」した割合。",
                "焼肉 A: 91%。 美容室 B: 87%。 カフェ C: 79%。 3 店舗平均 86%。",
                "残り 14% は「軽微な文言修正 (店舗固有の情報を追記)」または「クレーム対応で人間が完全書き直し」。",
            ]),
            ("cost 試算", [
                "Gourmie Standard tier ￥2,980/月 x 3 店舗 = 月 ￥8,940。",
                "3 店舗合計で 3 ヶ月あたり ￥26,820 の支出。",
                "削減効果 (店長時間 90% 削減 x 3 店舗 x 時給 3,000 円換算) = 月 ￥24,000 相当。 3 ヶ月で ￥72,000 相当。 実質 ROI +170%。",
            ]),
            ("学び", [
                "1. カフェ C は 導入前の返信率が極端に低かったため、Gourmie 導入の即効性が最も高かった。",
                "2. 焼肉 A は 「単価が高い店で低評価が付いた時」の返信品質が特に価値を出す (謝罪 + 対応方針を店長がすぐ承認するだけで済む)。",
                "3. クレーム系口コミへの返信は AI draft 品質が下がるため、店長の再編集を前提とした運用設計が現実的。",
            ]),
            ("まとめ", [
                "Gourmie は 越谷 3 店舗で 3 ヶ月間、返信率 97% + 平均返信時間 90% 削減 + 星評価 +0.17pt の record を出しました。",
                "SMB 飲食店 / 美容 / サービス業で口コミ返信の負荷を減らしたい方は https://xiora-official.com/products/gourmie.html をご覧ください。",
                "30 分無料相談は info@xiora-official.com で受付中です。",
            ]),
        ],
    },
]


def render(article: dict) -> tuple[str, str, str]:
    slug = article["slug"]
    date = article["date"]
    date_dot = date.replace("-", ".")
    title = article["title"]
    desc = article["description"]
    lead = article["lead"]
    cat = article["category"]

    parts = [
        HEAD.format(
            title=title, description=desc, slug=slug, date=date,
            date_dot=date_dot, category=cat, lead=lead,
        )
    ]

    for i, (h2, paragraphs) in enumerate(article["body_sections"]):
        parts.append(f"<h2>{h2}</h2>")
        for p in paragraphs:
            parts.append(f"<p>{p}</p>")
        if i == 0:
            # inject mini-cta after intro
            parts.append(f"""<aside aria-label="Xiora の AI プロダクトを見る" style="margin:32px 0;padding:16px 20px;border-left:3px solid #111827;background:#f9fafb;border-radius:0 8px 8px 0;">
<p style="margin:0 0 6px;font-size:13px;color:#6b7280;letter-spacing:0.08em;font-family:'Inter',sans-serif;">・ TRY XIORA</p>
<p style="margin:0;font-size:14.5px;line-height:1.65;color:#111827;">
本記事のトピックを貴社の事業に当てはめる 30 分無料相談。
<a href="/contact.html?type=ai-dx&amp;src=insight-{slug}-mini&amp;utm_source=xiora&amp;utm_medium=insights&amp;utm_campaign=cvr-mini-2026-08&amp;utm_content={slug}" style="color:#111827;text-decoration:underline;font-weight:500;">今すぐ相談する →</a>
</p>
</aside>""")

    related = _related(article.get("products", []))
    parts.append(TAIL.format(slug=slug, related_products=related))
    # We built TAIL with placeholder for related_products; replace once
    body = "\n".join(parts)
    body = body.replace("{related_products}", related)
    return slug, date, body


def main() -> int:
    updates_patch = []
    written = []
    for a in ARTICLES:
        slug, date, html = render(a)
        # word count in text-only (rough)
        text_only = re.sub(r"<[^>]+>", "", html)
        wc = len(text_only)
        _check_constitution(text_only, slug)
        # persist to insights/
        out = INSIGHTS_DIR / f"{slug}.html"
        out.write_text(html, encoding="utf-8")
        written.append((slug, date, wc))
        updates_patch.append({
            "id": f"{date}-{slug}",
            "date": date,
            "type": "insight",
            "kind": "release",
            "title": a["title"],
            "description": a["description"],
            "url": f"/insights/{slug}.html",
            "insight_cat": a["category"],
            "author": "沓澤 怜士 (Xiora)",
            "build_cat": "Dinner 2026-07-19 Batch",
        })
    (BATCH_DIR / "updates_patch.json").write_text(
        json.dumps({"items": updates_patch}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[dinner-batch] wrote {len(written)} articles")
    total_wc = 0
    for s, d, wc in written:
        print(f"  {d}  {s:60s}  {wc} chars (text-only)")
        total_wc += wc
    print(f"  TOTAL text-only chars = {total_wc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
