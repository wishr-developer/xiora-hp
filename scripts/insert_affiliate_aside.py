#!/usr/bin/env python3
"""
insert_affiliate_aside.py — Xiora HP insights 記事末尾に affiliate aside を追加

Reo directive 2026-07-19「アフィリエイトも追加でやって」対応。
placeholder Amazon Associate tag = xiora-22 (Reo 承認後に real ID へ一括置換)。

方針:
- 各記事に topic-tailored な Amazon 検索 link を 2-3 件
- disclosure 「本記事はアフィリエイトリンクを含みます」+ アソシエイト表記
- 憲法 5 条 (「絶対」「必ず」「保証」禁止) 遵守
- 挿入マーカー: <!-- affiliate-integration-2026-07-19 START/END --> で reversibility
- 既存の <!-- product-cta-audit-2026-07-19 END --> の直後に挿入 (kigen は </aside></div> の直前)
- 冪等: 既に START マーカーがあれば skip
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

INSIGHTS_DIR = Path(__file__).resolve().parent.parent / "insights"
ASSOCIATE_TAG = "xiora-22"  # placeholder — Reo が Amazon アソシエイト承認後に real ID へ置換

# --- topic mapping ---
# 各記事に「関連書籍検索キーワード」を 2-3 件割り当てる。
# Amazon 検索 link は https://www.amazon.co.jp/s?k=<query>&tag=<tag> 形式。
# 商品固定 link (dp/xxx) は在庫切れ/絶版リスクがあるため検索型を採用。

ARTICLE_MAP: dict[str, dict] = {
    "ai-agent-5-rules": {
        "intro": "本記事で取り上げた AI エージェント運用ルール (執行境界 / BAN リスク / OAuth guardrail / 可逆性 diff / blanket 承認) を深掘りする参考書籍です。",
        "amazon_searches": [
            ("AI エージェント 実装", "AI エージェント実装の入門書"),
            ("Claude Code 実践", "Claude Code / Anthropic API 実践本"),
            ("SaaS スタートアップ 設計", "SaaS スタートアップ 運用本"),
        ],
    },
    "ai-agent-task-selection-4-axes": {
        "intro": "AI エージェントに何をやらせるかの判断 (時間・可逆性・失敗コスト・データ整備度) を深めるための参考書籍です。",
        "amazon_searches": [
            ("AI 業務自動化", "AI 業務自動化・タスク設計"),
            ("プロダクトマネジメント 意思決定", "PdM 意思決定フレーム"),
            ("生成AI 実装", "生成 AI 実装の実務書"),
        ],
    },
    "ai-implementation-architecture": {
        "intro": "AI 実装アーキテクチャの学習に使える書籍と、記事内で触れた基盤 SaaS の紹介です。",
        "amazon_searches": [
            ("AI アーキテクチャ 設計", "AI システムアーキテクチャ本"),
            ("LLM アプリケーション 実装", "LLM アプリ実装本"),
            ("Kubernetes 実践", "Kubernetes 実装本 (基盤参考)"),
        ],
    },
    "ai-saas-solo-founder": {
        "intro": "単独創業で SaaS を作る過程で役立つ書籍と実装リソースです。",
        "amazon_searches": [
            ("SaaS 起業 実践", "SaaS 起業本"),
            ("一人 SaaS", "個人開発 SaaS 本"),
            ("スタートアップ 実務", "スタートアップ運営実務書"),
        ],
    },
    "api-integration-design": {
        "intro": "API 連携設計 (指数バックオフ・冪等性・エラーハンドリング) を深める参考書籍です。",
        "amazon_searches": [
            ("Web API 設計", "Web API 設計本"),
            ("マイクロサービス 実装", "マイクロサービス実装本"),
            ("システム連携 設計", "システム連携 (EAI) 設計本"),
        ],
    },
    "from-poc-to-production": {
        "intro": "PoC を本番運用に乗せる過程 (信頼性・監視・SLO・障害対応) を体系化する参考書籍です。",
        "amazon_searches": [
            ("SRE 実践", "SRE 実践本"),
            ("運用設計 本番", "本番運用設計本"),
            ("PoC 本番化", "PoC からプロダクトへ"),
        ],
    },
    "ga4-bigquery-analytics": {
        "intro": "GA4 × BigQuery で意思決定に効く計測基盤を作るための参考書籍です。",
        "amazon_searches": [
            ("GA4 実践", "GA4 実装本"),
            ("BigQuery SQL", "BigQuery SQL 実務本"),
            ("データ分析 基盤", "分析基盤設計本"),
        ],
    },
    "gourmie-beta-learnings": {
        "intro": "飲食業向け SaaS の β 運用で参考にした書籍と、飲食 DX の関連リソースです。",
        "amazon_searches": [
            ("飲食店 DX", "飲食店 DX 実務書"),
            ("顧客体験 デザイン", "CX デザイン本"),
            ("SaaS β 運用", "β 運用と PMF"),
        ],
    },
    "kigen-5-problems": {
        "intro": "免許更新・車検・保証・サブスク・薬など、期限管理に関連する実務書と関連商品です。免許更新・車検の教本や実物商品検索を含みます。",
        "amazon_searches": [
            ("運転免許 更新 教本", "運転免許更新の教本"),
            ("車検 費用 節約", "車検関連ガイド"),
            ("家計簿 サブスク 管理", "サブスク管理ガイド"),
        ],
    },
    "koshigaya-it-ai-4-axes": {
        "intro": "中小 IT/SaaS 企業の AI 導入判断 (規模 / 導入コスト / データ整備 / 現場受容) の学習に役立つ書籍です。",
        "amazon_searches": [
            ("中小企業 DX", "中小企業 DX 実務書"),
            ("AI 導入 中小", "中小の AI 導入本"),
            ("SaaS 受託開発", "SaaS 受託開発の実務"),
        ],
    },
    "nextjs-15-corporate-site-design": {
        "intro": "Next.js 15 でコーポレートサイトを設計する際の参考書籍と関連リソースです。",
        "amazon_searches": [
            ("Next.js 実践", "Next.js 実装本"),
            ("React 実装 パターン", "React 設計パターン本"),
            ("Web パフォーマンス", "Web パフォーマンス本"),
        ],
    },
    "rag-architecture-for-smb": {
        "intro": "RAG (Retrieval-Augmented Generation) アーキテクチャを中小企業で現実的に運用する際の参考書籍です。",
        "amazon_searches": [
            ("RAG 実装", "RAG 実装本"),
            ("ベクトル検索", "ベクトル DB / 検索本"),
            ("LLM 応用 実践", "LLM 応用実践"),
        ],
    },
    "reduce-churn-ai-3-patterns": {
        "intro": "SaaS 解約率 (churn) を下げる設計を深めるための参考書籍と実務書です。",
        "amazon_searches": [
            ("SaaS チャーン", "SaaS チャーン改善本"),
            ("カスタマーサクセス", "カスタマーサクセス本"),
            ("プロダクト分析", "プロダクト分析本"),
        ],
    },
    "restaurant-qr-order-2026": {
        "intro": "飲食店の QR モバイルオーダー導入判断に役立つ書籍と関連リソースです。",
        "amazon_searches": [
            ("飲食店 モバイルオーダー", "モバイルオーダー実務書"),
            ("飲食店 経営 効率化", "飲食店経営本"),
            ("POS システム 導入", "POS システム導入本"),
        ],
    },
    "restaurant-review-ai-5-caveats": {
        "intro": "飲食店の口コミ AI 返信で押さえるべき法令 (景表法 / 薬機法) と顧客体験の参考書籍です。",
        "amazon_searches": [
            ("景表法 実務", "景品表示法の実務書"),
            ("薬機法 広告", "薬機法広告実務"),
            ("口コミ マーケティング", "口コミマーケ本"),
        ],
    },
    "smb-subsidy-ai-2026": {
        "intro": "持続化補助金 2026 の申請書作成を深める書籍と、会計 SaaS の関連リソースです。",
        "amazon_searches": [
            ("持続化補助金", "持続化補助金 実務書"),
            ("小規模事業者 事業計画", "小規模事業者事業計画本"),
            ("創業融資 事業計画書", "創業融資 事業計画本"),
        ],
    },
    "stripe-webhook-6-pitfalls": {
        "intro": "Stripe webhook 本番運用 (冪等性 / 署名検証 / 再送 / 重複 / 失敗記録) を深める書籍です。",
        "amazon_searches": [
            ("Stripe 決済 実装", "Stripe 実装本"),
            ("Webhook 冪等性 設計", "冪等性設計本"),
            ("決済 システム 設計", "決済システム設計本"),
        ],
    },
    "subsidy-ai-draft-3-stages": {
        "intro": "補助金・助成金の申請書 AI 下書きプロセスを深める書籍と行政書士法適合の参考書です。",
        "amazon_searches": [
            ("補助金 申請書 書き方", "補助金申請書の書き方本"),
            ("行政書士 実務", "行政書士業務本"),
            ("事業計画書 書き方", "事業計画書の書き方"),
        ],
    },
    "xai-org-architecture": {
        "intro": "AI エージェント組織アーキテクチャ設計を深める書籍と実務書です。",
        "amazon_searches": [
            ("マルチエージェント システム", "マルチエージェント本"),
            ("組織 設計 スタートアップ", "組織設計本"),
            ("AI オーケストレーション", "AI オーケストレーション本"),
        ],
    },
    "zero-spend-saas-startup": {
        "intro": "¥0 で SaaS 会社を立ち上げる過程の書籍と、記事で触れた無料枠クラウドの参考リソースです。",
        "amazon_searches": [
            ("SaaS 資本ゼロ", "資本ゼロ起業本"),
            ("VPS 運用", "VPS 運用本"),
            ("個人開発 SaaS", "個人開発 SaaS 本"),
        ],
    },
}


def amazon_search_link(query: str) -> str:
    q = quote(query, safe="")
    return f"https://www.amazon.co.jp/s?k={q}&tag={ASSOCIATE_TAG}"


def build_aside(slug: str, spec: dict) -> str:
    intro = spec["intro"]
    items_html = []
    for query, label in spec["amazon_searches"]:
        link = amazon_search_link(query)
        items_html.append(
            f'      <li><a href="{link}" rel="sponsored nofollow noopener" target="_blank">{label} を Amazon で見る</a></li>'
        )
    items_block = "\n".join(items_html)

    # 憲法 5 条準拠 (「絶対」「必ず」「保証」なし)、disclosure 明記、アソシエイト表記
    aside = f'''<!-- affiliate-integration-2026-07-19 START -->
<hr/>
<aside aria-label="関連書籍・アフィリエイト" class="affiliate-recommendations" style="margin:32px 0 8px;padding:24px clamp(16px,3.5vw,32px);border:1px solid #e5e7eb;border-radius:14px;background:#fafafa;">
  <p style="font-size:11.5px;letter-spacing:0.14em;text-transform:uppercase;color:#6b7280;margin:0 0 10px;font-family:'Inter',sans-serif;">・ Recommended Reading</p>
  <p style="margin:0 0 12px;color:#4b5563;line-height:1.75;font-size:14.5px;">{intro}</p>
  <ul style="margin:0 0 14px;padding-left:1.2em;color:#374151;font-size:14px;line-height:1.9;">
{items_block}
  </ul>
  <p style="margin:0;font-size:11.5px;color:#9ca3af;line-height:1.7;">本記事はアフィリエイトリンクを含みます。 Amazon.co.jp のアソシエイトとして、当メディアは適格販売により収入を得ています。 掲載内容は執筆時点の情報であり、購入判断はご自身の責任でお願いします。</p>
</aside>
<!-- affiliate-integration-2026-07-19 END -->
'''
    return aside


# --- 挿入 pattern ---
# 大半の記事: <!-- product-cta-audit-2026-07-19 END --> の直後 (article-back の直前) に挿入
# kigen: product-cta マーカー無し。 </aside></div> の直後 article-back の直前 に挿入

INSERT_MARKER_STANDARD = "<!-- product-cta-audit-2026-07-19 END -->"
INSERT_MARKER_KIGEN_PATTERN = re.compile(r'(</aside>\n</div>\n)(<a class="article-back")', re.MULTILINE)
IDEMPOTENT_MARKER = "<!-- affiliate-integration-2026-07-19 START -->"


def insert_into(html: str, slug: str) -> tuple[str, bool]:
    """Returns (new_html, was_modified)."""
    if IDEMPOTENT_MARKER in html:
        return html, False

    if slug not in ARTICLE_MAP:
        return html, False

    aside_block = build_aside(slug, ARTICLE_MAP[slug])

    if INSERT_MARKER_STANDARD in html:
        # after the END marker + its newline
        marker_line = INSERT_MARKER_STANDARD + "\n"
        idx = html.find(marker_line)
        if idx < 0:
            # fallback: without trailing newline
            idx = html.find(INSERT_MARKER_STANDARD) + len(INSERT_MARKER_STANDARD)
            new_html = html[:idx] + "\n" + aside_block + html[idx:]
        else:
            insert_pos = idx + len(marker_line)
            new_html = html[:insert_pos] + aside_block + html[insert_pos:]
        return new_html, True

    # kigen path
    m = INSERT_MARKER_KIGEN_PATTERN.search(html)
    if m:
        new_html = html[: m.start()] + m.group(1) + aside_block + m.group(2) + html[m.end():]
        return new_html, True

    return html, False


def main() -> int:
    modified = []
    skipped = []
    for html_path in sorted(INSIGHTS_DIR.glob("*.html")):
        slug = html_path.stem
        if slug == "index":
            continue
        original = html_path.read_text(encoding="utf-8")
        new_html, was_modified = insert_into(original, slug)
        if was_modified:
            html_path.write_text(new_html, encoding="utf-8")
            modified.append(slug)
        else:
            skipped.append(slug)
    print(f"Modified {len(modified)} articles:")
    for s in modified:
        print(f"  + {s}")
    print(f"Skipped {len(skipped)} articles:")
    for s in skipped:
        print(f"  - {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
