#!/usr/bin/env python3
"""Xiora HP - Affiliate footer injector (placeholder tags, Reo approve 待ち).

Injects a footer with placeholder affiliate URLs into existing insight
articles.  Real referral IDs are pending Reo Absolute-gate action
(docs/AFFILIATE_REO_ACTION_2026-07-19.md).  Placeholders are marked
`XIORA_AFFIL_PENDING::<provider>` and will be replaced by a single sed
script after Reo hands-on account creation.

Idempotent: skips articles that already contain the marker.
"""
from __future__ import annotations

import sys
from pathlib import Path

INSIGHTS_DIR = Path(__file__).resolve().parents[1] / "insights"
MARKER_START = "<!-- affiliate-footer-placeholder-2026-07-19 START -->"
MARKER_END = "<!-- affiliate-footer-placeholder-2026-07-19 END -->"

# Providers where Xiora is targeting a partner/referral program.
# Rakuten / Amazon 楽天 excluded here (per no-楽天 dinner directive; separate PR pending sid).
PROVIDERS = [
    ("Notion",  "XIORA_AFFIL_PENDING::notion",  "SMB のドキュメント / ナレッジ管理 SaaS"),
    ("Vercel",  "XIORA_AFFIL_PENDING::vercel",  "Next.js を最速で公開する PaaS"),
    ("Railway", "XIORA_AFFIL_PENDING::railway", "コンテナ / DB を 1 分で立てる PaaS"),
    ("Cloudflare", "XIORA_AFFIL_PENDING::cloudflare", "エッジ CDN + Zero Trust"),
]


def _footer_html(article_slug: str) -> str:
    lis = "\n".join(
        f'    <li><a href="{url}?ref={article_slug}" rel="sponsored noopener" target="_blank"><strong>{name}</strong></a> — {desc}</li>'
        for name, url, desc in PROVIDERS
    )
    return f"""{MARKER_START}
<hr/>
<h2 id="関連ツール-affiliate">関連ツール (提携リンク)</h2>
<p style="font-size:13px;color:#6b7280;">本記事の内容を実装するにあたり、Xiora が業務で採用しているツール群です。 リンクは提携リンク (advertisement) を含み、経由でお申込みの場合は Xiora に紹介料が入る場合があります。 記事内容の中立性は維持しています。</p>
<ul class="article-list">
{lis}
</ul>
<p style="font-size:12px;color:#9ca3af;">※ Reo Absolute Gate (KYC) 承認待ちの placeholder URL。 承認後、代理人が sed で real referral ID に一括置換します。</p>
{MARKER_END}
"""


def _inject(path: Path) -> str:
    src = path.read_text(encoding="utf-8")
    if MARKER_START in src:
        return "skip"
    # Inject just before the closing article-back link
    anchor = '<a class="article-back" href="/insights/">'
    if anchor not in src:
        return "no-anchor"
    slug = path.stem
    footer = _footer_html(slug)
    new = src.replace(anchor, footer + anchor, 1)
    path.write_text(new, encoding="utf-8")
    return "injected"


def main() -> int:
    files = sorted(INSIGHTS_DIR.glob("*.html"))
    counts = {"injected": 0, "skip": 0, "no-anchor": 0}
    # Only inject into the first 20 existing articles (per Reo directive)
    # Skip the 8 dinner-batch articles (they already have their own product CTAs)
    dinner_slugs = {
        "xiora-ocean-llm-p0-p5-roadmap",
        "xiora-rei-24-7-secretary-dogfood",
        "xiora-tradingview-21-strategy-backtest",
        "smb-ai-tools-30-curated-2026",
        "kigen-app-3-record-2026",
        "aiverse-30-min-quickstart-5-steps",
        "nexa-career-6-sku-comparison",
        "gourmie-ai-review-response-3-month-record",
    }
    processed = 0
    for f in files:
        if f.name == "index.html":
            continue
        if f.stem in dinner_slugs:
            continue
        if processed >= 20:
            break
        result = _inject(f)
        counts[result] = counts.get(result, 0) + 1
        processed += 1
        print(f"[affil] {f.name}: {result}")
    print(
        f"[affil] summary: injected={counts.get('injected', 0)} "
        f"skip={counts.get('skip', 0)} no-anchor={counts.get('no-anchor', 0)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
