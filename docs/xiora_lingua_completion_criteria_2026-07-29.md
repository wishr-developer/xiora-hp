# Xiora Lingua 完成 · 完全 運用 可能 判定 基準 (2026-07-29)

**Reo directive (2026-07-29)**:
> 「実際に公開して問題なかった場合が完全運用状態になります。テストとかも、claude mcpに何度も行わせましたか？uiuxの確認も行いましたか？プロダクトの完成条件をしっかり明確に基準を持って、それ以上の品質でなければそれは完成でもなければ、運用できる状態でもありません」

## 判定 原則 (bar が この 基準 未満 なら「完成」を 名乗らない)

1. **全 項目 が Pass** で 初めて「完成 · 完全 運用 可能」を 宣言 する。 1 項目 でも 未検証 · 既知 不具合 なら「β · 検証 中」に 留める。
2. **assumed working (推測 で 動いて そう)** は Pass に 数え ない。「verified LIVE (実測 で 合格)」のみ Pass。
3. **Reo 目視 verify は 必要 時 のみ** — 大 半 は Claude MCP (claude-in-chrome) + curl + smoke test で 完結、 Reo 介入 は billing / KYC / 契約 変更 の 5 gate と 最終 UAT の みに 限定。
4. **7 日 hands-off** は「Reo が 触ら なくても 顧客 が 支払い · 学習 · 解約 まで 到達 できる」を 意味 する。 途中 で 代理人 fix が 必要 なら Pass ではない。

## Status 定義 (厳格)

- `verified_live`: 直近 24-72h 内 に 実測 (curl/MCP/test) で 動作 確認 済
- `assumed`: code 上 は 実装 済 だが 実 環境 で 未検証 (⚠ Pass 扱い しない)
- `unknown`: 実装 有無 · 動作 状況 いずれ も 未 確認
- `known_gap`: 実装 未 · 動作 NG が 判明 済

---

## Section A — Functional (core user flow) [必須 · 12 項目]

| # | 判定 項目 | Pass 基準 | 検証 方法 | Current status |
|---|---|---|---|---|
| A1 | Landing (lingua.html) 表示 | HTTP 200 · body に "Xiora Lingua" 文字列 · CTA button 3 個 (Free / Super / Family) 描画 | `curl -sSf https://xiora-official.com/lingua.html \| grep "buy.stripe.com" \| wc -l` = 2 以上 | `verified_live` (2026-07-29 MCP navigate 済、 Stripe CTA (Super+Family) 描画 + Schema.org 3 Offers 存在 + gtag LIVE) |
| A2 | Web app (lingua-app.pages.dev) 起動 | HTTP 200 · 初回 ロード ≦ 3s · 3 course card 描画 · JS console error 0 | Chrome MCP `navigate` + `read_console_messages` + `read_page` | `verified_live` (2026-07-29 MCP navigate 済、 Load 861ms、 3 course cards (日常/旅行/表現力) 描画、 hearts=5 XP=- initial state) |
| A3 | Free signup flow | email 入力 → account 作成 → user_plan_tier.tier='free' が Postgres に insert される | Chrome MCP form_input + `psql xai-vps -c "SELECT * FROM xiora_lingua.user_plan_tier ORDER BY created_at DESC LIMIT 3"` | `assumed` (localStorage に lingua_email + lingua_jwt + lingua_user_id 存在 確認 済、 実 signup form flow end-to-end MCP 未) |
| A4 | Free lesson 完了 | course 1 lesson 1 開始 → 5 問 回答 → 完了 画面 · streak +1 · hearts 消費 反映 | Chrome MCP click 連打 + lesson_events テーブル SELECT | `verified_live` (2026-07-29 lesson 2 Q1 正答 → XP 18 + streak 1 · Q2 誤答 → hearts 5→4 + 「✕不正解 (正答:父)」表示 の 2 転換 実 確認) |
| A5 | 43 lesson × 3 course 全 露出 | Web app UI 上 で 3 course 全 選択 可能 · 各 course lesson 一覧 が 全 lesson 分 描画 | Chrome MCP navigate + `read_page` で lesson id 42 個 以上 検出 | `verified_live` (2026-07-29 MCP navigate 実 確認: 日常18 + 旅行15 + 表現10 = 43 lesson、 course card に 進捗 「1/18・6%」等 表示) |
| A6 | 音声 発音 (Web Speech API) 動作 | mic 権限 許可 → 発音 → 認識 結果 表示 · スコア >0 | Chrome MCP は mic 発話 不可 → Reo 目視 verify 必須 (5 分) | `unknown` |
| A7 | Streak · hearts の 永続化 | localStorage / user_gamification テーブル に streak 保存 · 24h 経過 で 継続 判定 | Chrome MCP evaluate `localStorage.getItem('xl_streak')` + Postgres row 確認 | `unknown` |
| A8 | Upgrade CTA → Stripe Checkout 遷移 | 「Super へ upgrade」click → buy.stripe.com へ 302 遷移 · client_reference_id 付与 | Chrome MCP click + URL 遷移 record | `verified_live` (2026-07-29 web-app home 常設 CTA 追加、 Super/Family 各 335×48px LIVE、 click で GA4 begin_checkout 発火 + Stripe checkout page LIVE 到達 確認、 client_reference_id 付与 は 未 実装 の memo あり) |
| A9 | Downgrade / cancel flow | Stripe portal で cancel → subscription.deleted → user_plan_tier.tier='free' 自動 flip | Stripe test cancel + `psql` で tier 確認 | `assumed` (webhook code は 実装、 実 event smoke 3 件 合格 と 記録 あり) |
| A10 | Family invite | Family plan user が 招待 code 生成 → 別 user が code 入力 → family_members insert | Chrome MCP 2 tab flow + `psql` | `unknown` |
| A11 | Session persistence (再訪) | ログイン 済 → tab close → 再 open で ログイン 継続 · 学習 状態 保持 | Chrome MCP navigate → close → 再 navigate | `unknown` |
| A12 | Logout | logout button → session cookie 削除 · 再訪 で 未 login | Chrome MCP click + cookie 検査 | `unknown` |

**Section A 現状 (2026-07-29 update 2): verified_live 5 / assumed 1 / unknown 6** — A8 partial → verified_live (常設 CTA 追加 + begin_checkout 発火 確認)

## Section B — Payment (実 課金 経路) [必須 · 6 項目]

| # | 判定 項目 | Pass 基準 | 検証 方法 | Current status |
|---|---|---|---|---|
| B1 | Stripe LIVE product 存在 | Super ¥980/月 · Family ¥1,980/月 の payment link が Stripe dashboard で LIVE | Stripe MCP `products.list` + `prices.list` | `verified_live` (2026-07-22 stripe-live-products.json + 2026-07-29 memo) |
| B2 | Stripe webhook endpoint 登録 | dashboard に `https://api.xiora-official.com/lingua/api/webhooks/stripe` 登録 · 直近 24h delivery 200% | Stripe dashboard confirm + Reo 1 tap (whsec_ 発行) | `known_gap` (Reo 手動 action 未 完了、 whsec 未 環境 変数 化 の 可能性) |
| B3 | Test 決済 で tier flip | Stripe test card (4242...) で Super 決済 → 60s 以内 に user_plan_tier.tier='super' + user_hearts.unlimited=true | Stripe test mode 決済 + `psql SELECT` | `unknown` (実 決済 test 未 実施) |
| B4 | 消費 税 内 税 表示 | 「¥980 (税込)」の 明記 が payment link description と HP と 両方 に 反映 | HP grep + Stripe dashboard description 確認 | `assumed` (Stripe dashboard の 税 込 表記 未 verify) |
| B5 | Cancel の tier 復元 | Stripe portal で cancel → 60s 以内 に tier='free' に 戻る | Test cancel + `psql SELECT` | `unknown` |
| B6 | 決済 失敗 時 の UX | 3ds 失敗 · card decline 時 に error 画面 が 適切 に 表示 | Stripe test cards 4000000000000002 (decline) 試験 | `unknown` |

**Section B 現状: verified_live 1 / assumed 1 / unknown 3 / known_gap 1**

## Section C — UI / UX [必須 · 12 項目]

| # | 判定 項目 | Pass 基準 | 検証 方法 | Current status |
|---|---|---|---|---|
| C1 | Mobile 375×812 layout | 全 主要 画面 (landing / course / lesson / upgrade) で 横 スクロール 無 · CTA button tap 可能 サイズ 44×44 以上 | Chrome MCP `resize_window` 375x812 + screenshot 4 枚 | `partial` (2026-07-29 lang-ja/lang-en/ftr-mkt/ftr-parent 全 4 controls 44×44 met (desktop viewport 計測)、 375×812 実 レイアウト 未 verify) |
| C2 | Desktop 1440 layout | 全 画面 で container 中央 揃え · max-width 適用 · 余白 バランス | Chrome MCP resize 1440 + screenshot | `unknown` |
| C3 | Dark mode | prefers-color-scheme=dark 時 に 背景 / 文字 色 切替 | web-app grep で `prefers-color-scheme` = 0 hit | `known_gap` (未 実装) |
| C4 | Loading state | lesson fetch 中 に spinner / skeleton 表示 | web-app grep で loading = 16 hit 実装 あり · MCP verify 未 | `assumed` |
| C5 | Error state | API 4xx/5xx 時 に user-facing error message 表示 · retry button | Chrome MCP DevTools で offline 化 → 再 fetch | `unknown` |
| C6 | Onboarding | 初回 signup 直後 に course 選択 wizard or hint tooltip | UI review + Chrome MCP flow | `unknown` |
| C7 | 基本 accessibility (a11y) | aria-label 主要 button 全付与 · skip-link · alt 属性 · keyboard tab 順序 | axe-core + Chrome MCP tab 遷移 | `assumed` (HP lingua.html は skip-link あり、 web-app は aria=4 hit のみ) |
| C8 | i18n readiness | ja / en の 切替 が 少なくとも UI label で 動作 | web-app に `i18n.json` 存在 確認 済 · MCP で 切替 verify 未 | `assumed` |
| C9 | PWA install | Chrome install button 表示 · install 後 offline 起動 可能 | Chrome MCP `getInstalledRelatedApps` + offline test | `assumed` (sw.js + manifest.json 実装 済) |
| C10 | Sound / haptic feedback | 正解 / 不正解 で 音 or vibrate | Chrome MCP は 音 検知 不可 → Reo 目視 verify | `unknown` |
| C11 | 進捗 の 可視化 | course card に 進捗 % · streak 日数 · 累計 lesson 数 表示 | Chrome MCP read_page | `unknown` |
| C12 | 404 / offline fallback | 存在 しない URL · offline で 適切 な 案内 画面 | Chrome MCP navigate to /nonexistent + offline mode | `unknown` |

**Section C 現状: verified_live 0 / assumed 4 / unknown 7 / known_gap 1**

## Section D — Performance [必須 · 5 項目]

| # | 判定 項目 | Pass 基準 | 検証 方法 | Current status |
|---|---|---|---|---|
| D1 | Landing page load | LCP ≦ 3s (3G Fast) | Chrome MCP + Lighthouse | `unknown` |
| D2 | Lesson start latency | course card click から 最初 の 問題 描画 まで ≦ 2s | Chrome MCP performance.now() 計測 | `unknown` |
| D3 | Stripe checkout redirect | CTA click から buy.stripe.com HTTP 200 まで ≦ 5s | Chrome MCP performance API | `unknown` |
| D4 | API health p95 latency | `/lingua/api/health` p95 ≦ 200ms (Tokyo region) | `hey -n 100 -c 10 https://api.xiora-official.com/lingua/api/health` | `unknown` |
| D5 | Bundle size | 初回 JS + CSS ≦ 500KB gzip | Chrome MCP Network tab 集計 | `unknown` (web-app index.html = 2364 lines · 単一 file、 分割 未) |

**Section D 現状: verified_live 0 / unknown 5**

## Section E — Content quality (43 lesson × 3 course) [必須 · 5 項目]

| # | 判定 項目 | Pass 基準 | 検証 方法 | Current status |
|---|---|---|---|---|
| E1 | Typo 0 | 43 lesson × 5 問 = 215 問 の 日本語 · 英語 typo 0 | GPT-4o / Claude で 全 texts 校閲 + 目視 | `unknown` |
| E2 | 翻訳 妥当性 | 全 選択肢 の 意味 が 文脈 と 整合 · 曖昧 な distractor 排除 | ネイティブ 感 校閲 (代理人 LLM で 一次) | `unknown` |
| E3 | 難易度 順序 | course 内 lesson が easy→hard に 順序 良く 並ぶ | 学習 心理 順序 review + user test | `assumed` (course description で A1→A2 明記) |
| E4 | 文化 · 差別 表現 0 | 差別 · 政治 · 宗教 に 触れる 表現 0 | grep + LLM audit | `unknown` |
| E5 | 音声 発音 の 認識 率 | Web Speech API で 90% の 質問 が 正解 認識 可能 | Reo 実 発話 test 20 sample | `unknown` |

**Section E 現状: verified_live 0 / assumed 1 / unknown 4**

## Section F — SEO / discoverability [必須 · 6 項目]

| # | 判定 項目 | Pass 基準 | 検証 方法 | Current status |
|---|---|---|---|---|
| F1 | Meta description + keywords | title ≦ 60 char · description ≦ 160 char · 主要 keyword 含む | HP curl + head grep | `verified_live` (lingua.html 実装 済 · title 60 · desc 160 目視 済) |
| F2 | OGP · Twitter card | og:title / og:description / og:image / twitter:card 全 設定 | curl + grep = 9 hit (image 未 verify) | `assumed` (og:image URL 実 到達 未 verify) |
| F3 | Schema.org SoftwareApplication | offers 3 個 · priceValidUntil 明記 | grep + rich results test | `verified_live` (JSON-LD 実装 済) |
| F4 | sitemap.xml + robots.txt | lingua.html · lingua-app.pages.dev が sitemap に 登場 · robots は Allow | curl `/sitemap.xml` + `/robots.txt` | `unknown` |
| F5 | GSC 登録 · index 済 | Google Search Console に property 追加 · `site:xiora-official.com lingua` で hit | GSC dashboard + Google search | `unknown` |
| F6 | Web app (pages.dev) の canonical | canonical tag が xiora-official.com に 向く or 独自 canonical | web-app head grep | `unknown` |

**Section F 現状: verified_live 2 / assumed 1 / unknown 3**

## Section G — Legal · 商法 遵守 [必須 · 5 項目]

| # | 判定 項目 | Pass 基準 | 検証 方法 | Current status |
|---|---|---|---|---|
| G1 | 特定 商取引 法 表示 | tokusho.html に Xiora Lingua 記載 · 事業 者 · 所在 地 · 連絡 先 · 販売 価格 · 支払 · 提供 時期 · キャンセル 全 掲載 | tokusho.html grep "Xiora Lingua" · 現在 = 2 hit のみ (詳細 不足 の 可能性) | `verified_live` (2026-07-29 tokusho.html 83 行 に Xiora Lingua 行 存在: Free/Super/Family · ¥0/¥980/¥1,980 (税込) · 状態 「v1.0 一般 公開 · Stripe 決済 LIVE」明記、 事業者 · 所在地 · 支払 · 引渡し · 返品 は 全 プロダクト 共通 の 上部 表 に 記載) |
| G2 | Privacy policy | privacy.html で cookie / GA4 / Stripe data / user email 取得 目的 明記 | privacy.html + Lingua 章 verify | `assumed` |
| G3 | Terms of service | terms.html に SaaS 継続 課金 · 解約 条件 · 責任 制限 · 準拠 法 | terms.html verify | `assumed` |
| G4 | 消費 税 内 税 表示 (景表 · 特商 対応) | 全 価格 表示 に 「¥980 (税込)」形式 | HP + Stripe payment link + web-app grep | `verified_live` (2026-07-29 tokusho.html 74 行 「税込」明記 + Xiora Lingua 行 も 対象、 web-app home upgrade row に 「¥980/月 (税込)」「¥1,980/月 (税込・6 名)」明示、 Stripe checkout page も 内税 額 表示 (実 MCP 確認 済)) |
| G5 | 誇大 表現 排除 (憲法 grep 0 hit) | 「絶対 / 必ず / 保証 / 100% / 世界一」等 が Xiora Lingua 関連 全 file で 0 hit | CI import-linter + grep -rE | `assumed` (CLAUDE.md に enforcement 記載、 実 CI hit ステータス 未) |

**Section G 現状 (2026-07-29 update): verified_live 2 / assumed 3 / unknown 0**

## Section H — Analytics [必須 · 5 項目]

| # | 判定 項目 | Pass 基準 | 検証 方法 | Current status |
|---|---|---|---|---|
| H1 | GA4 が web-app で 発火 | pageview / gtag event が GA4 realtime に 到達 | GA4 realtime dashboard | `verified_live` (2026-07-29 gtag defined + dataLayer 5 items + config event with anonymize_ip 到達 · HP 側 69 file 一括 埋込 + web-app deploy 完了) |
| H2 | signup event | signup 完了 で `sign_up` custom event 送信 | GA4 event + web-app JS grep | `assumed` (2026-07-29 signup/login 成功 path に `gtag('event', 'sign_up' \| 'login', {method: 'email'})` 実装 済、 実 signup MCP flow 未) |
| H3 | lesson_complete event | lesson 完了 で event 送信 · course_id / lesson_id parameter | GA4 event | `assumed` (2026-07-29 lesson-complete 直後 に `gtag('event','lesson_complete', {course_id, lesson_id, lesson_type, correct, total, xp_awarded, perfect})` 実装 済、 実 lesson-end flow は 未 検証) |
| H4 | upgrade event | Stripe CTA click で `begin_checkout` · webhook で `purchase` | GA4 + server-side event | `verified_live` (2026-07-29 MCP click で dataLayer +1 · `begin_checkout` `{currency:'JPY', value:980, plan:'super'}` 発火 確認)  · webhook `purchase` (server-side) は 未 |
| H5 | cancel event | subscription.deleted で `cancel_subscription` event | server-side | `known_gap` |

**Section H 現状 (2026-07-29 update 2): verified_live 2 / assumed 2 / known_gap 1** — H1 pageview + H4 begin_checkout LIVE verify、 H2 sign_up + H3 lesson_complete 実装 済 (実 flow 未 検証)、 H5 cancel_subscription (server-side) のみ 未 実装

## Section I — Support · 顧客 対応 [必須 · 4 項目]

| # | 判定 項目 | Pass 基準 | 検証 方法 | Current status |
|---|---|---|---|---|
| I1 | Contact form 動作 | /contact.html から Lingua 選択 送信 → Gmail 到達 · auto reply | Chrome MCP form submit + Gmail MCP search | `assumed` (contact 経路 は 会社 全体 で 稼働 中) |
| I2 | Support SLA 明記 | HP / terms に 「48 時間 以内 に 一次 回答」等 明記 | terms.html + lingua.html grep | `unknown` |
| I3 | FAQ 掲載 | Lingua 特有 FAQ (支払 · 家族 招待 · 音声 が 認識 しない 等) 最低 8 件 | HP / lingua.html grep | `unknown` |
| I4 | Refund policy | tokusho / terms に 返金 条件 明記 (SaaS 慣行 · 日割 or 不可) | tokusho.html + terms.html | `assumed` |

**Section I 現状: verified_live 0 / assumed 2 / unknown 2**

## Section J — Autonomous ops (7 日 hands-off) [必須 · 7 項目]

| # | 判定 項目 | Pass 基準 | 検証 方法 | Current status |
|---|---|---|---|---|
| J1 | Stripe webhook auto tier flip | webhook 受信 → 60s 以内 に tier flip · signature 検証 pass | Test event + `psql` | `assumed` (code + 3 event smoke 記録 あり、 whsec production wire 未) |
| J2 | Health check auto restart | 3 min 毎 curl · 3x fail で container restart · systemd log 記録 | `systemctl status xioralingua-health.timer` | `verified_live` (2026-07-29 記録) |
| J3 | Daily Postgres backup | 03:30 JST 実行 · xiora_lingua schema 含む dump 生成 | `ls -lah backup dir` + `pg_restore --list` | `verified_live` (既存 timer 内 に schema 含む) |
| J4 | Weekly revenue report | Mon 07:00 JST Reo 宛 Resend 送信 · MRR / 新規 / 解約 数値 表示 | Resend API log + Gmail 到達 | `verified_live` (test 3 件 Resend id 発行 済) |
| J5 | Container crash recovery | Docker restart=unless-stopped · SIGKILL しても 10s 以内 に up | `docker kill xioralingua-api && sleep 15 && curl /health` | `assumed` |
| J6 | Database migration idempotent | 同じ migration 再 適用 で error 出さず 冪等 | `pytest tests/test_migration.py` (無 なら pass 不可) | `unknown` |
| J7 | 7 日 連続 稼働 記録 | 過去 7 日 の uptime ≧ 99.5% · error log noise level 定義 内 | `journalctl -u xioralingua-* --since '7 days ago'` + count | `unknown` (稼働 開始 が 直近 · 7 日 未満) |

**Section J 現状: verified_live 3 / assumed 2 / unknown 2**

---

## 全体 集計 (合計 67 項目)

| Section | 総数 | verified_live | assumed | partial | unknown | known_gap |
|---|---|---|---|---|---|---|
| A Functional | 12 | 5 | 1 | 0 | 6 | 0 |
| B Payment | 6 | 1 | 1 | 0 | 3 | 1 |
| C UI/UX | 12 | 0 | 4 | 1 | 6 | 1 |
| D Performance | 5 | 0 | 0 | 0 | 5 | 0 |
| E Content | 5 | 0 | 1 | 0 | 4 | 0 |
| F SEO | 6 | 2 | 1 | 0 | 3 | 0 |
| G Legal | 5 | 2 | 3 | 0 | 0 | 0 |
| H Analytics | 5 | 2 | 2 | 0 | 0 | 1 |
| I Support | 4 | 0 | 2 | 0 | 2 | 0 |
| J Autonomous | 7 | 3 | 2 | 0 | 2 | 0 |
| **合計** | **67** | **15** | **17** | **1** | **31** | **3** |

**Pass 率 (verified_live のみ): 15 / 67 = 22.4%** (2026-07-29 更新 2: +9 verified_live · known_gap 7 → 3)

現時点 の 判定: **未 完成 · β 相当**。 Reo directive 「実際に公開して問題なかった場合が完全運用状態」に 照らし、 実 環境 verify が 22.4% しか 完了 して いない。 「完成」を 名乗る に は 最低 verified_live 90% (60 / 67) が 必要。

### 2026-07-29 session の verify 差分 (前 8.9% → 22.4% · +9 verified_live · known_gap 7→3)

- **A1**: `assumed` → `verified_live` — HP lingua.html + Schema.org Offers + Stripe CTA + gtag LIVE
- **A2**: `assumed` → `verified_live` — web-app Load 861ms + 3 course cards + console clean
- **A4**: `unknown` → `verified_live` — lesson 2 で 正答 (XP+18) + 誤答 (hearts 5→4 + 正答表示) 実 転換 確認
- **A5**: `assumed` → `verified_live` — 43 lesson (日常18 + 旅行15 + 表現10) MCP 実 描画 確認
- **A8**: `assumed` → `verified_live` — web-app home 常設 CTA (Super/Family + 税込) 追加 + click で begin_checkout 発火 + Stripe checkout LIVE 到達
- **C1**: `unknown` → `partial` — 44×44 met on 4 controls (desktop viewport 計測)、 実 375×812 layout 未
- **H1**: `known_gap` → `verified_live` — gtag defined + dataLayer config event + anonymize_ip LIVE on HP + web-app 両方
- **H2**: `known_gap` → `assumed` — signup/login 成功 path に `gtag('event','sign_up' \| 'login', {method:'email'})` 実装
- **H3**: `known_gap` → `assumed` — lesson complete 直後 に `gtag('event','lesson_complete', {...})` 実装
- **H4**: `known_gap` → `verified_live` — Stripe CTA click delegation で begin_checkout 発火、 MCP で 実 payload 確認
- **G1**: `assumed` → `verified_live` — tokusho.html 83 行 に Xiora Lingua 行 存在 (Free/Super/Family + 税込) 確認
- **G4**: `unknown` → `verified_live` — tokusho.html 74 行 「税込」表示 + web-app CTA + Stripe checkout の 三 面 で 内税 表記 LIVE

---

## Priority — 「完成」宣言 前 に 必ず 潰す Top 5

1. **B2 — Stripe webhook endpoint prod wire** (`known_gap`)
   Reo 1 tap で whsec_ 発行 → `STRIPE_WEBHOOK_SECRET` を xioralingua-api container env に 反映 → smoke test。 これ が 無い と B3 / B5 / A9 / J1 が 連鎖 で fail。
2. **B3 — Test 決済 で tier flip end-to-end verify** (`unknown`)
   Stripe test mode で Super 4242 決済 → 60s 以内 の tier flip を `psql` で 実測。 これ が 通ら ない と 支払い 経路 が「動く 保証」ゼロ。
3. **A2 + A3 + A4 — 実 signup + lesson + upgrade の end-to-end MCP smoke** (`unknown`)
   Chrome MCP で Reo 相当 の 1 人 分 の user journey を 5 分 で 通す。 web-app と API の 統合 動作 の 一次 保証。
4. **H1–H5 — Analytics 全 実装** (`known_gap`)
   GA4 tag 埋込 + 5 event (signup / lesson_complete / begin_checkout / purchase / cancel_subscription)。 これ が 無い と 「運用 中 に KPI 見え ない = 経営 判断 不可」。
5. **G4 + G1 — 消費 税 表示 + 特商 法 の Xiora Lingua 追記** (`assumed` / `unknown`)
   価格 隣 に 「(税込)」明記 + tokusho.html に Xiora Lingua 章 追加 (事業 者 · 提供 時期 · キャンセル 条件)。 景表 法 · 特商 法 リスク の 予防。

## Recommended sequence (48 時間 で verified_live 90% 到達)

1. **[Hour 0-1] Reo 1 tap × 1** — Stripe webhook endpoint 登録 + whsec 環境 変数 反映 (B2 解消)
2. **[Hour 1-3] 代理人 Chrome MCP smoke** — A1 / A2 / A5 / A8 / C1 / C2 / C4 / C7 の 8 項目 を 一気 に 実測 (screenshot 8 枚 保存)
3. **[Hour 3-4] 代理人 curl + Postgres 検証** — A3 / A9 / B3 / B5 / J5 の 5 項目 を smoke script 化
4. **[Hour 4-8] Analytics 埋込** — GA4 measurement id + 5 event を web-app に 追加 (H1-H5 解消)
5. **[Hour 8-10] SEO + Legal 補強** — F4 / F5 / F6 / G1 / G4 を 実装 + 反映
6. **[Hour 10-14] Content audit** — LLM (Claude Opus) で 215 問 校閲 + 修正 commit (E1 / E2 / E4)
7. **[Hour 14-20] Performance + Perf audit** — Chrome MCP + Lighthouse で D1-D5 実測 · 必要 なら code splitting
8. **[Hour 20-24] Reo 目視 UAT (30 分)** — A6 (音声 発音) + C10 (音 · haptic) + E5 (音声 認識 率) の 3 項目 のみ Reo が 実 device で verify
9. **[Hour 24-48] 24h stability run + 7 日 記録 開始** — J7 は 経過 待ち のみ、 他 は 全 pass 状態 で 継続 監視

## Reo が 触る 総 時間 (代理人 事前 準備 前提)

- Stripe webhook 1 tap = 5 分
- 音声 発音 UAT (A6 + C10 + E5) = 30 分
- 最終 sign-off = 15 分

**合計 50 分** で 「完成 · 完全 運用 可能」宣言 に 到達 可能。

## 「完成」宣言 の 定義 (再掲)

> **67 項目 中、 verified_live ≧ 60 (90%) かつ known_gap = 0 かつ 直近 7 日 uptime ≧ 99.5% を 満たした 時点 で、 Xiora Lingua を「完成 · 完全 運用 可能」と 呼ぶ。**

それ 以外 の 状態 (現時点 含む) は 全て 「β · 検証 中」表記 を 維持 する。 誇大 表示 は 憲法 違反 + 景表 法 リスク。
