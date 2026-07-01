# Xiora Content — Single Source of Truth

このディレクトリはサイトの動的コンテンツ（News / Insights / Labs / Products）のシングルソースです。
ここを編集して push すると、GitHub Actions が `scripts/build.py` を実行し、以下 7 箇所を自動再生成してから本番へ FTP デプロイします。

## 自動更新される箇所

| ソース | 出力先 |
| --- | --- |
| `updates.json` | `index.html` の **Build in Public** セクション（最新 6 件） |
| `updates.json` | `news/index.html` のニュース一覧（type=news） |
| `updates.json` | `insights/index.html` の記事グリッド（type=insight） |
| `updates.json` | `sitemap.xml` のニュース URL エントリ |
| `products.json` | `products/index.html` のカード + product-meta |
| `products.json` | **全 HTML のフッター Products ブロック** |
| `products.json` | `sitemap.xml` のプロダクト URL エントリ |

## 新しい News 記事を追加する

1. `news/2026-08-XX-slug.html` を作成（既存の news 記事を複製すれば OK）
2. `updates.json` の `items` 配列の**先頭**に新規エントリを追加:

```jsonc
{
  "id": "2026-08-01-new-thing",
  "date": "2026-08-01",
  "type": "news",
  "kind": "release",            // color-key: release / product / venture / research / engineering / labs / case / update
  "title": "新機能をリリースしました。",
  "description": "…（1〜2 文）",
  "url": "/news/2026-08-01-new-thing.html",
  "build_cat": "Release Updates", // Build in Public に載せたい場合のみ設定
  "news_cat": "Release"           // /news/ で見えるカテゴリタグ
}
```

3. `git commit && git push` — Actions が自動で index / news / sitemap を再生成。

## 新しい Insights 記事を追加する

1. `insights/slug.html` を作成
2. `updates.json` に追加:

```jsonc
{
  "id": "insight-slug",
  "date": "2026-08-01",
  "type": "insight",
  "kind": "engineering",          // color-key for Build in Public
  "insight_cat": "AI",            // /insights/ でのタグ
  "title": "記事タイトル",
  "description": "リード文",
  "url": "/insights/slug.html",
  "build_cat": "Engineering Notes", // 任意
  "author": "Xiora Engineering"
}
```

3. commit && push

## 新しい Product を追加する

1. `products/new-product.html` を作成
2. `products.json` の `products` 配列に追加:

```jsonc
{
  "id": "new-product",
  "name": "New Product",
  "brand_html": "New<br/><span>Product</span>",
  "status": "Released",
  "category_ja": "対象業界",
  "sub_desc_ja": "一言説明",
  "who": "誰向けか",
  "problem": "解決すること",
  "ai_use": "AI の使い所",
  "url": "/products/new-product.html",
  "svg_motif": "<svg viewbox=\"0 0 120 60\" xmlns=\"http://www.w3.org/2000/svg\">…</svg>",
  "card_class": "prod-card--new"
}
```

3. commit && push — /products/、Footer、sitemap が全ページ自動更新されます。

> **注意**: `index.html` の Flagship 大ブロック（Kigen 特集）とサブカード 3 枚は手作りセクションのため、ここは Products 追加時に手動更新が必要です（`<!-- ===== 3. Products ===== -->` セクション）。

## ローカルでビルドしてプレビューしたい

```bash
python3 scripts/build.py
python3 -m http.server 8000
# → http://localhost:8000
```

`build.py` は冪等（何度実行しても同じ出力）。git diff で差分を確認して push すれば OK。

## Marker Convention

自動再生成される箇所は、以下のコメントで囲まれています:

```html
<!-- BUILD:start <region> -->
（この間の内容は build.py が管理）
<!-- BUILD:end <region> -->
```

**この区間の中は手で編集しないでください** — 次回ビルドで上書きされます。書き換えたいときは `content/*.json` を編集してください。

## Region 一覧

| Region | 場所 |
| --- | --- |
| `build-in-public` | index.html |
| `news-list` | news/index.html |
| `insights-grid` | insights/index.html |
| `products-cards` | products/index.html |
| `products-meta` | products/index.html |
| `footer-products` | 全 HTML |
| `sitemap-news` | sitemap.xml |
| `sitemap-products` | sitemap.xml |
