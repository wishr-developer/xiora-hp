#!/usr/bin/env python3
"""Xiora static content builder.

Reads content/updates.json and content/products.json, then regenerates
marker-delimited regions in:

    index.html                  → Build in Public section
    news/index.html             → News list
    insights/index.html         → Insights grid
    products/index.html         → Product cards + product-meta
    All HTML files              → Footer Products block
    sitemap.xml                 → News + Products URL entries

Marker convention:
    <!-- BUILD:start <region-name> -->
    ... generated content ...
    <!-- BUILD:end <region-name> -->

Idempotent: re-running yields the same output.

Usage:
    python3 scripts/build.py
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_json(name: str) -> dict:
    return json.loads((ROOT / "content" / name).read_text(encoding="utf-8"))


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def marker_replace(text: str, region: str, new_content: str) -> str:
    """Replace the block between <!-- BUILD:start region --> and
    <!-- BUILD:end region --> markers. Preserves the markers themselves."""
    pattern = re.compile(
        rf"(<!-- BUILD:start {re.escape(region)} -->)(.*?)(<!-- BUILD:end {re.escape(region)} -->)",
        re.DOTALL,
    )
    if not pattern.search(text):
        return text  # markers not present — no-op

    def replacer(m: re.Match) -> str:
        return f"{m.group(1)}\n{new_content}\n{m.group(3)}"

    return pattern.sub(replacer, text)


def sort_by_date_desc(items: list[dict]) -> list[dict]:
    """Sort by ISO 'date' descending. Dateless items go to the bottom
    (they're evergreen/experimental)."""

    def key(item: dict):
        d = item.get("date")
        if d:
            return (1, datetime.fromisoformat(d))
        return (0, datetime.min)

    return sorted(items, key=key, reverse=True)


def data_i18n_attr(item: dict, field: str) -> str:
    """Return ` data-i18n="..."` if the item has an i18n key for the field,
    else empty string."""
    key = item.get(f"i18n_{field}")
    return f' data-i18n="{key}"' if key else ""


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------
def render_build_log(updates: dict, limit: int = 6) -> str:
    items = [i for i in updates["items"] if i.get("build_cat")]
    items = sort_by_date_desc(items)[:limit]

    parts: list[str] = []
    for it in items:
        d = it.get("date")
        date_label = it.get("date_label") or (d.replace("-", ".") if d else "")
        datetime_attr = f' datetime="{d}"' if d else ""
        kind = it["kind"]
        parts.append('<li class="build-log__item">')
        parts.append(f'<a class="build-log__link" href="{it["url"]}">')
        parts.append('<div class="build-log__meta">')
        parts.append(f'<time class="build-log__date"{datetime_attr}>{date_label}</time>')
        parts.append(
            f'<span class="build-log__cat build-log__cat--{kind}">{html_escape(it["build_cat"])}</span>'
        )
        parts.append("</div>")
        parts.append(f'<h3 class="build-log__title">{html_escape(it["title"])}</h3>')
        parts.append(f'<p class="build-log__desc">{html_escape(it["description"])}</p>')
        parts.append('<span class="build-log__arrow" aria-hidden="true">→</span>')
        parts.append("</a>")
        parts.append("</li>")
    return "\n".join(parts)


def render_news_list(updates: dict) -> str:
    items = [i for i in updates["items"] if i["type"] == "news"]
    items = sort_by_date_desc(items)

    parts: list[str] = []
    for it in items:
        # news/index.html uses relative hrefs like "2026-07-01-xxx.html"
        rel_url = it["url"].split("/")[-1]
        d = it["date"] or ""
        date_display = d.replace("-", ".") if d else ""
        cat = it.get("news_cat", "News")
        parts.append('<li class="news-item reveal">')
        parts.append(f'<a class="news-item__link" href="{rel_url}">')
        parts.append(f'<time class="news-item__date" datetime="{d}">{date_display}</time>')
        parts.append(f'<span class="news-item__cat">{html_escape(cat)}</span>')
        title_i18n = data_i18n_attr(it, "title")
        parts.append(f'<p class="news-item__title"{title_i18n}>{html_escape(it["title"])}</p>')
        parts.append('<span aria-hidden="true" class="news-item__arrow">→</span>')
        parts.append("</a>")
        parts.append("</li>")
    return "\n".join(parts)


def render_insights_grid(updates: dict) -> str:
    items = [i for i in updates["items"] if i["type"] == "insight"]
    items = sort_by_date_desc(items)

    parts: list[str] = []
    for it in items:
        d = it.get("date") or ""
        date_display = d.replace("-", ".") if d else ""
        cat = it.get("insight_cat", "AI")
        author = it.get("author", "Xiora Engineering")
        title_i18n = data_i18n_attr(it, "title")
        desc_i18n = data_i18n_attr(it, "description")
        parts.append(
            f'<a class="insight-card reveal" href="{it["url"]}" style="text-decoration:none;color:inherit;">'
        )
        parts.append('<div class="insight-card__top">')
        parts.append(f'<span class="insight-card__cat">{html_escape(cat)}</span>')
        parts.append(f'<span class="insight-card__date">{date_display}</span>')
        parts.append("</div>")
        parts.append(f'<h2 class="insight-card__title"{title_i18n}>')
        parts.append(f"          {html_escape(it['title'])}")
        parts.append("        </h2>")
        parts.append(f'<p class="insight-card__desc"{desc_i18n}>')
        parts.append(f"          {html_escape(it['description'])}")
        parts.append("        </p>")
        parts.append('<div class="insight-card__foot">')
        parts.append(f'<span class="insight-card__author">{html_escape(author)}</span>')
        parts.append('<span aria-hidden="true" class="insight-card__arrow">→</span>')
        parts.append("</div>")
        parts.append("</a>")
    return "\n".join(parts)


def render_products_cards(products_data: dict) -> str:
    parts: list[str] = []
    for p in products_data["products"]:
        card_class = p.get("card_class", "")
        cta_text = (
            "優先案内を受け取る" if p["id"] == "coming-soon" else "詳細を見る"
        )
        parts.append(f'<a class="prod-card {card_class}" href="{p["url"]}">')
        parts.append('<div class="prod-card__top">')
        parts.append(f'<span class="prod-card__cat">{html_escape(p.get("category_ja", ""))}</span>')
        parts.append(f'<span class="prod-card__status">{html_escape(p.get("status", ""))}</span>')
        parts.append("</div>")
        parts.append(f'<p class="prod-card__brand">{p.get("brand_html", p["name"])}</p>')
        motif = p.get("svg_motif")
        if motif:
            parts.append('<div aria-hidden="true" class="prod-card__motif">')
            parts.append(motif)
            parts.append("</div>")
        parts.append(f'<h3 class="prod-card__title">{html_escape(p["name"])}</h3>')
        parts.append(f'<p class="prod-card__sub">{html_escape(p.get("sub_desc_ja", ""))}</p>')
        parts.append(f'<span class="prod-card__cta">{cta_text} <span aria-hidden="true">→</span></span>')
        parts.append("</a>")
    return "\n".join(parts)


def render_products_meta(products_data: dict) -> str:
    parts: list[str] = []
    for p in products_data["products"]:
        parts.append("<li>")
        parts.append(f'<p class="product-meta__name">{html_escape(p["name"])}</p>')
        parts.append(f'<p class="product-meta__for"><strong>誰向け：</strong>{html_escape(p.get("who", ""))}</p>')
        parts.append(f'<p class="product-meta__problem"><strong>解決すること：</strong>{html_escape(p.get("problem", ""))}</p>')
        parts.append(f'<p class="product-meta__ai"><strong>AI の使い所：</strong>{html_escape(p.get("ai_use", ""))}</p>')
        parts.append("</li>")
    return "\n".join(parts)


def render_footer_products(products_data: dict) -> str:
    parts: list[str] = []
    for p in products_data["products"]:
        if p.get("include_in_footer") is False:
            continue
        parts.append(f'<li><a href="{p["url"]}">{html_escape(p["name"])}</a></li>')
    parts.append('<li><a href="/products/">All Products</a></li>')
    return "\n".join(parts)


def render_sitemap_news(updates: dict) -> str:
    items = [i for i in updates["items"] if i["type"] == "news"]
    items = sort_by_date_desc(items)
    parts: list[str] = []
    for it in items:
        url = "https://xiora-official.com" + it["url"]
        parts.append("  <url>")
        parts.append(f"    <loc>{url}</loc>")
        parts.append("    <changefreq>yearly</changefreq>")
        parts.append("    <priority>0.4</priority>")
        parts.append("  </url>")
    return "\n".join(parts)


def render_sitemap_insights(updates: dict) -> str:
    items = [i for i in updates["items"] if i["type"] == "insight"]
    items = sort_by_date_desc(items)
    parts: list[str] = []
    for it in items:
        url = "https://xiora-official.com" + it["url"]
        parts.append("  <url>")
        parts.append(f"    <loc>{url}</loc>")
        parts.append("    <changefreq>monthly</changefreq>")
        parts.append("    <priority>0.4</priority>")
        parts.append("  </url>")
    return "\n".join(parts)


def render_sitemap_products(products_data: dict) -> str:
    parts: list[str] = []
    for p in products_data["products"]:
        if p.get("include_in_sitemap") is False:
            continue
        url = "https://xiora-official.com" + p["url"]
        parts.append("  <url>")
        parts.append(f"    <loc>{url}</loc>")
        parts.append("    <changefreq>monthly</changefreq>")
        parts.append("    <priority>0.9</priority>")
        parts.append("  </url>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def build_file(path: Path, region: str, new_content: str) -> bool:
    """Update marker region in a single file. Returns True if content changed."""
    text = path.read_text(encoding="utf-8")
    new_text = marker_replace(text, region, new_content)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> int:
    updates = load_json("updates.json")
    products = load_json("products.json")

    n_updates = len(updates["items"])
    n_build = sum(1 for i in updates["items"] if i.get("build_cat"))
    n_news = sum(1 for i in updates["items"] if i["type"] == "news")
    n_insights = sum(1 for i in updates["items"] if i["type"] == "insight")

    print(f"[xiora-build] loaded {n_updates} updates ({n_news} news, {n_insights} insights) / {len(products['products'])} products\n")

    # 1) index.html Build in Public
    changed = build_file(ROOT / "index.html", "build-in-public", render_build_log(updates))
    print(f"  {'✓' if changed else '·'} index.html                  build-in-public ({n_build} eligible → showing top 6)")

    # 2) news/index.html list
    changed = build_file(ROOT / "news" / "index.html", "news-list", render_news_list(updates))
    print(f"  {'✓' if changed else '·'} news/index.html             news-list ({n_news} entries)")

    # 3) insights/index.html grid
    changed = build_file(ROOT / "insights" / "index.html", "insights-grid", render_insights_grid(updates))
    print(f"  {'✓' if changed else '·'} insights/index.html         insights-grid ({n_insights} entries)")

    # 4) products/index.html cards + meta
    p_index = ROOT / "products" / "index.html"
    c1 = build_file(p_index, "products-cards", render_products_cards(products))
    c2 = build_file(p_index, "products-meta", render_products_meta(products))
    print(f"  {'✓' if (c1 or c2) else '·'} products/index.html         cards + meta ({len(products['products'])} products)")

    # 5) Footer Products block on ALL HTML files
    footer_html = render_footer_products(products)
    footer_touched = 0
    footer_seen = 0
    for path in sorted(ROOT.glob("**/*.html")):
        parts = path.parts
        if any(seg in ("node_modules", ".git", ".github", ".vscode", ".idea") for seg in parts):
            continue
        text = path.read_text(encoding="utf-8")
        if "BUILD:start footer-products" in text:
            footer_seen += 1
            new_text = marker_replace(text, "footer-products", footer_html)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8")
                footer_touched += 1
    print(f"  {'✓' if footer_touched else '·'} Footer Products             {footer_touched} of {footer_seen} files updated")

    # 6) sitemap.xml
    sm = ROOT / "sitemap.xml"
    c1 = build_file(sm, "sitemap-news", render_sitemap_news(updates))
    c2 = build_file(sm, "sitemap-products", render_sitemap_products(products))
    c3 = build_file(sm, "sitemap-insights", render_sitemap_insights(updates))
    print(f"  {'✓' if (c1 or c2 or c3) else '·'} sitemap.xml                 news + insights + products URL entries")

    print("\n[xiora-build] done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
