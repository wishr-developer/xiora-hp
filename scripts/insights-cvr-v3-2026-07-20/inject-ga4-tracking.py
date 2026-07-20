#!/usr/bin/env python3
"""inject-ga4-tracking.py — Xiora HP insights 記事に cvr-v3-tracking.js を注入。

- 全 insights/*.html の </head> 直前に <script defer src="/assets/js/cvr-v3-tracking.js?v=2026-07-20"> を追加
- mini-CTA / hero CTA / footer CTA の <a> 要素に data-cta-position 属性を付与
- 冪等 marker: <!-- cvr-v3-tracking-2026-07-20 --> 検知で skip

Usage:
    python3 inject-ga4-tracking.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

INSIGHTS = Path("/Users/kutsuzawareo/Desktop/XAI/Xiora_HP/insights")
MARKER = "<!-- cvr-v3-tracking-2026-07-20 -->"
SCRIPT_LINE = (
    f'{MARKER}\n'
    '<script defer src="/assets/js/cvr-v3-tracking.js?v=2026-07-20"></script>\n'
)


def _inject_script(html: str) -> tuple[str, bool]:
    if MARKER in html:
        return html, False
    m = re.search(r"</head>", html, re.IGNORECASE)
    if not m:
        return html, False
    new = html[:m.start()] + SCRIPT_LINE + html[m.start():]
    return new, True


def _annotate_cta(html: str) -> tuple[str, int]:
    """Add data-cta-position to known CTA anchors.

    Heuristics:
    - <a> href contains '/contact.html' and 'src=insight-*-mini'     -> middle
    - <a> href contains '/contact.html' and 'src=insight-*-hero'     -> hero
    - <a> href contains '/contact.html' and no position hint          -> footer
    - Skip if data-cta-position already present
    """
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        tag = m.group(0)
        if 'data-cta-position' in tag:
            return tag
        href_m = re.search(r'href="([^"]+)"', tag)
        if not href_m:
            return tag
        href = href_m.group(1)
        if '/contact.html' not in href:
            return tag
        pos = None
        if 'src=insight-' in href and '-mini' in href:
            pos = 'middle'
        elif 'src=insight-' in href and '-hero' in href:
            pos = 'hero'
        elif 'src=insight-' in href:
            pos = 'footer'
        else:
            return tag
        new_tag = tag[:-1] + f' data-cta-position="{pos}">'
        # replace only the opening '>'
        count += 1
        return new_tag

    # match <a ... > (opening tag only, non-greedy)
    new_html = re.sub(r"<a\b[^>]*?>", repl, html)
    return new_html, count


def _apply(path: Path, dry: bool) -> str:
    text = path.read_text(encoding="utf-8")
    new1, script_added = _inject_script(text)
    new2, cta_annotated = _annotate_cta(new1)
    if not script_added and cta_annotated == 0:
        return "skipped_all"
    if dry:
        return f"would_apply(script={script_added},cta={cta_annotated})"
    path.write_text(new2, encoding="utf-8")
    return f"applied(script={script_added},cta={cta_annotated})"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not INSIGHTS.exists():
        print(f"[err] insights dir not found: {INSIGHTS}", file=sys.stderr)
        return 3

    total_files = 0
    total_scripts = 0
    total_cta = 0
    for p in sorted(INSIGHTS.glob("*.html")):
        if p.name == "index.html":
            continue
        total_files += 1
        r = _apply(p, dry=args.dry_run)
        if "script=True" in r:
            total_scripts += 1
        m = re.search(r"cta=(\d+)", r)
        if m:
            total_cta += int(m.group(1))
        print(f"[{r}] {p.name}")

    print(f"\nsummary: files={total_files} scripts_added={total_scripts} cta_annotated={total_cta}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
