#!/usr/bin/env python3
"""generate-hero-svg.py — Xiora HP insights 記事の H1 直下に hero SVG を挿入。

- 記事 category (ai / restaurant / trading / kigen / nexa / xcloud / other) を
  slug から推定して、accent dot 色を切り替える。
- 全て 1200x630 (OGP + hero 兼用)、Xiora 白基調 minimal (#fbfbfd bg, hairline border)。
- Playwright 不使用 (Mac 静音)。 Python で SVG を直接生成。
- 冪等 marker (<!-- hero-svg-v3-2026-07-20 -->) 検知で skip。

Usage:
    python3 generate-hero-svg.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

INSIGHTS = Path("/Users/kutsuzawareo/Desktop/XAI/Xiora_HP/insights")
MARKER = "<!-- hero-svg-v3-2026-07-20 -->"

# accent dot color by slug prefix / keyword
CATEGORY_ACCENT = [
    (["ai-", "llm", "claude", "aiverse"], "#3b82f6"),      # blue = AI
    (["restaurant", "gourmie"], "#10b981"),                # green = restaurant/food
    (["trad", "predict", "stripe"], "#f59e0b"),            # amber = commerce/finance
    (["kigen"], "#8b5cf6"),                                # purple = health/kigen
    (["nexa", "career", "internship"], "#ec4899"),         # pink = education
    (["xcloud"], "#06b6d4"),                               # cyan = infra
    (["ocean"], "#64748b"),                                # slate = platform
]

FORBIDDEN = ["絶対", "100%", "業界No.1", "業界初", "業界最高", "最安", "確実に"]


def _accent_for(slug: str) -> str:
    for keys, color in CATEGORY_ACCENT:
        for k in keys:
            if k in slug:
                return color
    return "#111827"  # default black


def _extract_title(html: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
    if not m:
        return ""
    raw = re.sub(r"<[^>]+>", "", m.group(1))
    return raw.strip()


def _wrap_title(title: str, max_per_line: int = 22) -> list[str]:
    """Wrap Japanese title into <=3 lines of ~max_per_line chars."""
    lines: list[str] = []
    cur = ""
    for ch in title:
        cur += ch
        if len(cur) >= max_per_line:
            lines.append(cur)
            cur = ""
        if len(lines) >= 3:
            break
    if cur and len(lines) < 3:
        lines.append(cur)
    return lines[:3]


def _svg_for(title: str, slug: str) -> str:
    """Generate 1200x630 SVG hero."""
    accent = _accent_for(slug)
    lines = _wrap_title(title, max_per_line=22)
    y0 = 260
    lh = 68
    title_tspans = "\n".join(
        f'<text x="80" y="{y0 + i * lh}" font-family="Noto Sans JP, Inter, sans-serif" font-size="52" font-weight="700" fill="#111827">{_escape(line)}</text>'
        for i, line in enumerate(lines)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img" aria-label="{_escape(title)} - Xiora Insight" style="width:100%;height:auto;display:block;max-width:100%;background:#fbfbfd;border:1px solid #d1d5db;border-radius:8px;margin:0 0 32px;">
<rect x="0" y="0" width="1200" height="630" fill="#fbfbfd"/>
<line x1="80" y1="120" x2="1120" y2="120" stroke="#e5e7eb" stroke-width="1"/>
<circle cx="80" cy="80" r="6" fill="{accent}"/>
<text x="100" y="86" font-family="Inter, sans-serif" font-size="15" font-weight="500" fill="#6b7280" letter-spacing="0.12em">XIORA INSIGHT</text>
<text x="1120" y="86" text-anchor="end" font-family="Inter, sans-serif" font-size="13" font-weight="400" fill="#9ca3af">xiora-official.com</text>
{title_tspans}
<line x1="80" y1="530" x2="220" y2="530" stroke="#111827" stroke-width="2"/>
<text x="80" y="580" font-family="Inter, sans-serif" font-size="15" font-weight="500" fill="#6b7280">Xiora — AI-native software, engineered for business.</text>
</svg>"""


def _escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def _check_constitution(text: str, slug: str) -> None:
    sanitized = re.sub(r"(width|max-width|height)\s*:\s*100%", "___CSS100___", text)
    for w in FORBIDDEN:
        if w in sanitized:
            raise SystemExit(f"[constitution] {slug}: forbidden vocab hit: {w}")


def _apply(path: Path, dry: bool) -> str:
    html = path.read_text(encoding="utf-8")
    if MARKER in html:
        return "skipped_marker"
    m = re.search(r"</h1>", html)
    if not m:
        return "skipped_no_h1"

    title = _extract_title(html)
    if not title:
        return "skipped_no_title"

    slug = path.stem
    svg = _svg_for(title, slug)
    block = f"\n{MARKER}\n{svg}\n"

    _check_constitution(block, slug)

    if dry:
        return "would_insert"

    new = html[:m.end()] + block + html[m.end():]
    path.write_text(new, encoding="utf-8")
    return "inserted"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not INSIGHTS.exists():
        print(f"[err] insights dir not found: {INSIGHTS}", file=sys.stderr)
        return 3

    stats: dict[str, int] = {"inserted": 0, "would_insert": 0, "skipped_marker": 0, "skipped_no_h1": 0, "skipped_no_title": 0}
    for p in sorted(INSIGHTS.glob("*.html")):
        if p.name == "index.html":
            continue
        r = _apply(p, dry=args.dry_run)
        stats[r] = stats.get(r, 0) + 1
        print(f"[{r}] {p.name}")

    print("\nsummary:", stats)
    return 0


if __name__ == "__main__":
    sys.exit(main())
