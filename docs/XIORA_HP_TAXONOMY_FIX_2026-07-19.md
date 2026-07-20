# Xiora HP — 分類 混在 + 使い回し 文言 修正 spec

Version: 2026-07-19
Related : `docs/XIORA_TAXONOMY_2026-07-19.md`
Branch : `xiora-hp-taxonomy-revise-2026-07-20`

---

## 0. 前提

Reo directive 2026-07-19 :
> https://xiora-official.com/ の 全 page 確認、同じような文言が使い回しになっているのが多々見受けられます。 さらに、アプリとサービスとシステム混ぜないでください。 客観的にみたら よくわからなくなります。

本 spec は :
1. 使い回し 文言 の 検出 (Task 2 audit)
2. 分類 混在 の 検出 (Task 2 audit)
3. 内部 stack 露出 の 検出 (Task 2 audit)
4. 各 差分 の revise 前後 diff (Task 3 spec)

を まとめる SoT。

---

## 1. Audit 結果 — 使い回し 文言

### 1.1 出現 count top 10 (5+ occurrences 、 3+ files)

| 順位 | 出現 数 | file 数 | phrase (先頭 100 字) |
|---:|---:|---:|:---|
| 1 | 41 | 40 | `Xiora — AI-native software, engineered for business` |
| 2 | 36 | 36 | `本記事のトピックに直接関わる Xiora 自社プロダクトです` |
| 3 | 35 | 35 | `Xiora 代表 · info@xiora-official` (footer) |
| 4 | 30 | 30 | `この記事の内容を、貴社に当てはめて 30 分で整理します` |
| 5 | 30 | 30 | `本記事のアプローチを貴社の状況で使えるか、代表 沓澤が 1 対 1 で棚卸しします` |
| 6 | 30 | 30 | `© 2026 Xiora / 沓澤 怜士 · Home · Insights · Contact` |
| 7 | 26 | 21 | `System & App Development` (page label) |
| 8 | 23 | 23 | `Xiora の AI エージェント運用ノウハウを、貴社の SaaS / 業務自動化に当てはめる 30 分無料相談` |
| 9 | 17 | 17 | `本記事の内容を実装するにあたり、Xiora が業務で採用しているツール群です` |
| 10 | 14 | 14 | `本記事のトピックを貴社の事業に当てはめる 30 分無料相談` |

### 1.2 分類 (使い回し は 意図 vs 事故)

- **意図 された 使い回し** (残す) : 順位 1 (brand tagline) 、 3 (footer 連絡先) 、 6 (copyright)
- **CTA / affiliate block の 定型** (残す 、 統一 された 訴求 が 逆 に 良い) : 4 、 5 、 8 、 9 、 10
- **事故 / 曖昧 phrase** (variation 差替 対象) : 2 (「本記事のトピックに直接関わる Xiora 自社プロダクトです」は 30 件 に わたって 同じ、 記事 の 主題 と 関係 が 曖昧)、 7 (page 分類 が 不明瞭 「System & App Development」→ 「アプリ」「システム」明示)

### 1.3 hero copy 使い回し

top page の hero に :
- `AI · Software · Systems — engineered as one` (eyebrow)
- `AI-native software, / engineered for business.` (title)

これ 自体 は brand core message で 残す。 ただし hero lead は :
- 現状 : `業務システム・SaaS・AI アプリ・モバイルアプリを、設計から実装・運用まで一気通貫で。`
- revise : 3 pillar (アプリ / サービス / システム) を 明示 する 副 文 を 追加。

---

## 2. Audit 結果 — 分類 混在

### 2.1 products/ の 10 offering (main branch) 分類

| id | 現 category_ja (products.json) | 判定 | badge |
|:---|:---|:---|:---|
| kigen | iOS アプリ / 期限管理 | アプリ | [アプリ] |
| xcloud-connect | 飲食店向け SaaS | システム | [システム] |
| xcloud-flow | スクール運営 SaaS | システム | [システム] |
| aiverse | AI 配信 SaaS | アプリ (web app) | [アプリ] |
| gourmie | 飲食コンシェルジュ | システム (SaaS) | [システム] |
| shigyo-agents | 士業 AI アシスタント SaaS | システム | [システム] |
| agent-factory | 500 業種 AI エージェント基盤 | システム | [システム] |
| restaurant-os | 飲食店向け経営 OS | システム | [システム] |
| content-engine | 自動コンテンツ収益化基盤 | システム | [システム] |
| tradeos | 個人投資家向け情報 tool | システム | [システム] |

判定 補足 :
- Aiverse Studio は Twitch / YouTube / TikTok 配信 用 の web app。 個人 が login して そのまま 配信 開始 する UI 中心 の tool なので「アプリ」判定 (SaaS 契約 は している が、 ユーザ 体験 上 は アプリ)。 Reo は memory `xiora_taxonomy` で「Aiverse Studio (web app、 AITuber 配信)」と アプリ 分類 を 明示。
- Gourmie は wed 版 は 存在 する が、 店舗 側 は 継続 契約 SaaS 主。 幹事 側 UI は アプリ 的 だが、 収益 モデル + 契約 主体 は SaaS なので「システム」判定。

**混在 検出 数** : 10 pages 中 、 現状 分類 badge が **0 pages** (未 実装)。 全 page 追加 対象。

### 2.2 top page (index.html) の 混在

`業務システム・SaaS・AI アプリ・モバイルアプリ` — 4 種 が 羅列 されて 「何が どう 違う のか」が 不明。 3 pillar (アプリ / サービス / システム) に 集約。

### 2.3 products/index.html の 混在

- `<h2>10 のプロダクト。</h2>` — アプリ 1 + システム 9 が 平列。 3 section 分離 が 望ましい (アプリ section + システム section) 。 サービス は products/ ではなく 個別 サービス LP へ 誘導。

---

## 3. Audit 結果 — 内部 stack 露出

### 3.1 検出 一覧 (2026-07-19 grep)

`grep -RIln "X Systems|Rei|XiroraRegistrar|XAILegalChain|XAIOutreach|XAISeoAutomation|XAIPR|XAIPortal" Xiora_HP/*.html Xiora_HP/products/*.html Xiora_HP/insights/*.html`

**products/ 、 top level page** : 0 件 (露出 なし ✓)

**insights/** : 10 件 (既存 の tech 記事)
- `ai-agent-5-rules.html` — 事例 として `XAILegalChain publish gate` 引用 (顧客 対象外 は 明示 済)
- `ai-agent-task-selection-4-axes.html` — `XAILegalChain (Track Z)` の 4 軸 事例
- `api-integration-design.html` — `XAISeoAutomation / XAIOutreach` の 実装 例 (Xiora が 内部 で 採用 と 明記 済)
- `ga4-bigquery-analytics.html` — `XAISeoAutomation (port 3020)` 引用
- `kigen-app-3-record-2026.html` — `Rei 秘書 AI` の 連携 描写
- `xiora-rei-24-7-secretary-dogfood.html` — Rei の dogfood 記事 (Rei title 記事、 内部 tool の 経験談 公開)
- `xiora-ocean-llm-2027-vision.html` — `Rei-Reo 会話` を 4 unique data source として 引用
- `xiora-ocean-public-launch.html` — Rei は 社内 専用 と 明示 、 Ocean は 独立 と 説明
- `xiora-15-monetization-categories.html` — 12 product の 一覧 に XAIOutreach / Rei 含む
- `insights/index.html` — 上記 記事 title の 一覧

### 3.2 対応 方針

- **既存 insights の 内部 stack 記事 は そのまま 維持** (destructive 禁止 、 revise + add のみ) 。 これらは tech 記事 として 「Xiora が 内部 で こう 運用」文脈 で 顧客 対象外 を 明示 して いる。
- **新規 追加 記事** で 内部 stack を 露出 させない (本 PR の scope 外)。
- **products/ に は 一切 露出 させない** — 現状 0 件、 revise 後 も 0 件 維持。
- **top page (index.html) に は 一切 露出 させない** — 現状 0 件、 revise 後 も 0 件 維持。

---

## 4. Revise 前後 diff summary

### 4.1 index.html hero lead

- **前** :
  ```
  Xiora は、AI と ソフトウェアを事業に実装する Founder-led の技術パートナー。
  業務システム・SaaS・AI アプリ・モバイルアプリを、設計から実装・運用まで一気通貫で。
  ```
- **後** :
  ```
  Xiora は、AI と ソフトウェアを事業に実装する Founder-led の技術パートナー。
  提供 は 3 pillar : アプリ (Kigen / Aiverse Studio) 、 サービス (AI 導入 · Web 制作 · 動画 代行) 、 システム (Nexa · Gourmie · XCloud 等 の SaaS)。
  設計 から 実装 · 運用 まで 一気通貫 で 対応 します。
  ```

### 4.2 各 product page hero eyebrow

10 pages に category badge 追加 (status pill と 並列)。 例 :

- **kigen.html** 前 :
  ```html
  <p class="page-hero__eyebrow reveal"><span class="dash"></span>Xiora Apps / Kigen<span class="pill pill--muted" style="margin-left:12px;">iOS App · Released</span></p>
  ```
  後 :
  ```html
  <p class="page-hero__eyebrow reveal"><span class="dash"></span>Xiora Apps / Kigen<span class="pill pill--muted" style="margin-left:12px;">[アプリ]</span><span class="pill pill--muted" style="margin-left:8px;">iOS App · Released</span></p>
  ```

- **gourmie.html** 前 :
  ```
  Products / Gourmie [β running]
  ```
  後 :
  ```
  Products / Gourmie [システム] [β running]
  ```

- 同様 に xcloud-connect / xcloud-flow / aiverse (→ [アプリ]) / shigyo-agents / agent-factory / restaurant-os / content-engine / tradeos に adaption。

### 4.3 products/index.html hero + lead

- **前** : `<h2>10 のプロダクト。</h2>` + 単一 grid
- **後** : hero lead 差替 で「アプリ (1) + システム (9)」 明示 、 lineup section の 冒頭 に 「アプリ ／ システム」 の 分類 説明 を 追加 (BUILD:start products-cards region の 前 に 静的 な 補足 段落 を 挿入)。

### 4.4 使い回し phrase の variation

順位 2「本記事のトピックに直接関わる Xiora 自社プロダクトです」は 36 記事 で 同一。 本 PR scope 外 (別 subagent の insights 系 branch と 衝突 回避 の ため)。 別 PR で 差替 予定。

## 5. 適用 順 と 検証

1. `docs/XIORA_TAXONOMY_2026-07-19.md` 作成 (完了 ✓)
2. `docs/XIORA_HP_TAXONOMY_FIX_2026-07-19.md` 作成 (本 doc ✓)
3. 10 product page に category badge 追加
4. index.html hero lead revise
5. products/index.html hero + lineup 補足 追加
6. `python3 scripts/build.py` 実行、 exit 0 確認
7. novelist ブランド 混入 grep 、 内部 statute grep 実行、 0 件 確認 (Xiora tech HP は 独立)
8. `grep -RIln "X Systems|Rei|XiroraRegistrar|XAI(LegalChain|Outreach|SeoAutomation|PR|Portal)"` — 本 branch で 追加 した 差分 に 露出 が ない こと 確認
9. commit → push → PR

## 6. 制約 遵守

- Mac 負荷 : Playwright / Ollama 未使用 、 pure text + git のみ ✓
- destructive 禁止 : 既存 page rename / delete なし、 add + revise のみ ✓
- 内部 stack 露出 : products/ + top page は 0 件 維持 ✓
- novelist ブランド / internal statute grep 0 ✓
- Xiora 名義 ✓
- VPS SSH 不使用 ✓
- Rei restart なし ✓
- 前 subagent branch (`products-suite-plus-8-new-2026-07-20`) と 別 branch 、 conflict 回避 ✓

## 7. Change log

- 2026-07-19 v1.0 : 初版
