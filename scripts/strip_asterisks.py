#!/usr/bin/env python3
"""Strip stray asterisks from published insight HTML files.

Reason (memory: feedback_articles_one_per_day_no_asterisk_2026_08_29):
Raw `*` / `**` in rendered article body signals unrendered markdown ("AI slop").
Convert to proper HTML tags in-place. URL unchanged → SEO safe.

Usage:
    python3 Xiora_HP/scripts/strip_asterisks.py [--dry-run]

Rules:
- **text** → <strong>text</strong>  (only within body text, not inside <script>/<style>/<code>)
- *text*   → <em>text</em>           (heuristic: not inside URLs or code blocks)
- Any remaining lone `*` → removed
- Skips <script>, <style>, <code>, <pre> regions
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


BOLD_RE = re.compile(r"\*\*([^*\n]+?)\*\*")
ITALIC_RE = re.compile(r"(?<![*\w/])\*([^*\n]+?)\*(?![*\w/])")

# Preserve regions we should NOT touch
PRESERVE_RE = re.compile(
    r"(<script\b[^>]*>[\s\S]*?</script>|<style\b[^>]*>[\s\S]*?</style>|<code\b[^>]*>[\s\S]*?</code>|<pre\b[^>]*>[\s\S]*?</pre>)",
    re.IGNORECASE,
)


def strip_body(html: str) -> tuple[str, int]:
    """Return (new_html, count_of_asterisk_ops)."""
    n = 0
    parts: list[str] = []
    last = 0
    for m in PRESERVE_RE.finditer(html):
        body = html[last:m.start()]
        new_body, ops = _process(body)
        parts.append(new_body)
        parts.append(m.group(0))
        n += ops
        last = m.end()
    tail = html[last:]
    new_tail, ops = _process(tail)
    parts.append(new_tail)
    n += ops
    return "".join(parts), n


def _process(s: str) -> tuple[str, int]:
    n = 0
    new, ops = BOLD_RE.subn(lambda m: f"<strong>{m.group(1)}</strong>", s)
    n += ops
    new, ops = ITALIC_RE.subn(lambda m: f"<em>{m.group(1)}</em>", new)
    n += ops
    # Any remaining lone asterisks
    remaining = new.count("*")
    if remaining:
        new = new.replace("*", "")
        n += remaining
    return new, n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="report only, do not write")
    ap.add_argument("--dir", default="Xiora_HP/insights", help="target directory (relative to repo root)")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[2]
    target = repo / args.dir
    if not target.exists():
        print(f"missing dir: {target}", file=sys.stderr)
        return 1

    total_files = 0
    changed = 0
    total_ops = 0
    for f in sorted(target.glob("*.html")):
        total_files += 1
        html = f.read_text(encoding="utf-8")
        new, ops = strip_body(html)
        if ops > 0:
            changed += 1
            total_ops += ops
            if args.dry_run:
                print(f"[dry] {f.name}: {ops} ops")
            else:
                f.write_text(new, encoding="utf-8")
                print(f"[fix] {f.name}: {ops} ops")

    print(f"\nscanned: {total_files}, changed: {changed}, total ops: {total_ops}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
