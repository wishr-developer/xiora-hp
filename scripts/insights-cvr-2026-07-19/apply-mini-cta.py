#!/usr/bin/env python3
"""apply-mini-cta.py — Xiora HP insights 記事に mini-CTA + UTM tracking を追加。

Path C: 記事内 途中 (H2 の 3 番目) の直前に「Xiora AI エージェント を試す」mini-CTA を挿入。
既存 CTA aside (product-cta-audit-2026-07-19) は保持、既に mini-CTA marker がある
記事は skip (冪等)。

Usage:
    python3 apply-mini-cta.py [--dry-run]

Exit codes:
    0 = 適用完了 or dry-run 表示完了
    2 = usage error
    3 = target insights dir 未発見
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MARKER_START = "<!-- mini-cta-cvr-2026-07-19 START -->"
MARKER_END = "<!-- mini-cta-cvr-2026-07-19 END -->"

MINI_CTA_TEMPLATE = """
{start}
<aside aria-label="Xiora AI エージェントを試す" style="margin:32px 0;padding:16px 20px;border-left:3px solid #111827;background:#f9fafb;border-radius:0 8px 8px 0;">
<p style="margin:0 0 6px;font-size:13px;color:#6b7280;letter-spacing:0.08em;font-family:'Inter',sans-serif;">・ TRY XIORA</p>
<p style="margin:0;font-size:14.5px;line-height:1.65;color:#111827;">
Xiora の AI エージェント運用ノウハウを、貴社の SaaS / 業務自動化に当てはめる 30 分無料相談。
<a href="/contact.html?type=ai-dx&amp;src=insight-{slug}-mini&amp;utm_source=xiora&amp;utm_medium=insights&amp;utm_campaign=cvr-mini-2026-07&amp;utm_content={slug}" style="color:#111827;text-decoration:underline;font-weight:500;">今すぐ相談する →</a>
</p>
</aside>
{end}
""".strip()


def find_third_h2_index(html: str) -> int:
    """3 番目の <h2 の開始位置 (=直前 insertion point) を返す。 見つからない場合は -1。"""
    positions = [m.start() for m in re.finditer(r"<h2\b", html)]
    if len(positions) >= 3:
        return positions[2]
    if len(positions) >= 2:
        return positions[1]
    return -1


def apply_to_file(path: Path, dry_run: bool) -> tuple[str, int]:
    """Return (status, delta_len). status ∈ {inserted, skipped_marker, skipped_no_h2}."""
    html = path.read_text(encoding="utf-8")

    if MARKER_START in html:
        return ("skipped_marker", 0)

    idx = find_third_h2_index(html)
    if idx < 0:
        return ("skipped_no_h2", 0)

    slug = path.stem
    payload = MINI_CTA_TEMPLATE.format(start=MARKER_START, end=MARKER_END, slug=slug)
    new_html = html[:idx] + payload + "\n" + html[idx:]
    delta = len(new_html) - len(html)

    if not dry_run:
        path.write_text(new_html, encoding="utf-8")
    return ("inserted", delta)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent.parent
    insights_dir = repo_root / "insights"
    if not insights_dir.is_dir():
        print(f"ERROR: insights dir not found: {insights_dir}", file=sys.stderr)
        return 3

    print(f"==> insights dir: {insights_dir}")
    print(f"==> mode: {'dry-run' if args.dry_run else 'apply'}")
    print()

    files = sorted(p for p in insights_dir.glob("*.html") if p.name != "index.html")
    inserted = skipped_marker = skipped_no_h2 = 0
    for f in files:
        status, delta = apply_to_file(f, args.dry_run)
        if status == "inserted":
            inserted += 1
            print(f"  + {f.name}: +{delta} chars")
        elif status == "skipped_marker":
            skipped_marker += 1
            print(f"  = {f.name}: already has mini-cta marker")
        elif status == "skipped_no_h2":
            skipped_no_h2 += 1
            print(f"  ? {f.name}: no <h2> found, skipped")

    print()
    print(f"==> summary: {inserted} inserted, {skipped_marker} skipped (marker), {skipped_no_h2} skipped (no h2)")
    if args.dry_run:
        print("==> dry-run: no files modified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
