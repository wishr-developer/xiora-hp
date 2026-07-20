# Xiora Taxonomy — アプリ / サービス / システム / 内部 stack

Version: 2026-07-19
Owner: Xiora 代表 沓澤 怜士 (Reo)
Status: SoT (Single Source of Truth) for Xiora HP + all product / offering copy

---

## 0. なぜ 分類 が 必要か

Xiora が 提供 する ものを、 客観的 に 見た とき「アプリ」「サービス」「システム」が 混ざって いて、 一般 の 訪問者 には「何を 買えば 良いか」「何が 継続 課金 で、 何が 単発 提供 か」「顧客 が 使う ものか、 Xiora が 使う ものか」が 分かり ません でした。

このドキュメント は、 Xiora 全 offering を 4 tier に 分類 し、 HP / 契約書 / 営業資料 / メール で 用語 を 統一 するための SoT です。

---

## 1. 分類 定義

### 1.1 「アプリ」 (App)

- 定義 : consumer-facing の 独立 install / use。 ダウンロード or 単独 web 起動 で、 その日から 使える もの。
- 対象 : 個人 (B2C) が 中心。 家族 共有 / チーム 共有 は 副 機能。
- 課金 : Free + Plus (¥数百 / 月) が 標準。 買い切り も 選択肢。
- 承認 sales cycle : ゼロ (App Store / Web で 完結)。
- 特徴 : install → 5 分で 使える。 Xiora 側 の 実装稼働 は 不要 (Xiora は 制作 と 運用 のみ)。

該当 offering (2026-07-19 時点) :
1. Kigen (iOS app 、 期限管理) — Released
2. Ocean Chat (public web app 、 ChatGPT 相当 対話) — Preparing (DNS pending)
3. Aiverse Studio (web app 、 AITuber 配信) — M1a Waitlist
4. (将来) Rei public interface — 現状 内部 専用、 一般 公開 は 未定

### 1.2 「サービス」 (Service)

- 定義 : 顧客 に 提供 する 事業 offering。 Xiora の 代理人 or 人間 が 実行 する 労働 or 制作 or 相談。
- 対象 : SMB / 個人事業主 / 個人 (B2B + B2C)。
- 課金 : spot (単発 ¥X 万) or 継続 リテナー (¥X 万 / 月)。
- 承認 sales cycle : 初回 商談 30 分 → 見積 → 発注。
- 特徴 : 納品物 が ある (資料、 コード、 動画、 記事、 面接候補者 等)。 継続 契約 でも「稼働 時間」 or「制作 数」で 契約。

該当 offering (2026-07-19 時点) :
1. AI 導入 支援 コンサル (spot ¥15-30 万 / 案件)
2. Web / LP / HP 制作 (受託 ¥30-300 万 / 案件)
3. SEO コンサル (継続 ¥8-20 万 / 月)
4. 動画代行 (video-creator agent 経由、 ¥3-15 万 / 本)
5. 求人代行 (XioraHire 受託 ¥10-40 万 / 案件)
6. 就活支援 コンサル (Xiora Career spot ¥3-10 万 / 学生 案件)
7. 法人研修 (Nexa 経由 講師 派遣 ¥15-40 万 / 講座)

### 1.3 「システム」 (System)

- 定義 : B2B SaaS or infrastructure。 顧客 が 契約 して 使う。 継続 課金 が 標準。
- 対象 : SMB / 中堅 企業 / 個人事業主 (契約 主体 は 法人 が 中心)。
- 課金 : ¥数千 - ¥数万 / 月 の subscription が 標準。 initial fee + 従量 も 選択肢。
- 承認 sales cycle : 商談 → 無料 trial → 有料 化 (2-4 週 目安)。
- 特徴 : Xiora が 開発 + 保守 + 運用 を 継続 で 提供。 顧客 は login して 使う。

該当 offering (2026-07-19 時点) :
1. Nexa Academy (教育 SaaS 、 subscription) — Live (staging → prod 準備 中)
2. Gourmie (飲食コンシェルジュ SaaS) — β Running
3. XCloud Connect (飲食 QR モバイルオーダー SaaS) — Released
4. XCloud Flow (スクール 運営 SaaS) — Released
5. Restaurant OS (飲食店 経営 OS) — Building
6. Shigyo Agents (士業 AI SaaS) — Coming
7. Agent Factory (500 業種 AI 基盤 SaaS) — Coming
8. Content Engine (自動 コンテンツ SaaS) — Beta
9. TradeOS (個人 投資家 情報 tool) — Phase 1
10. XioraEC (EC 統合 SaaS) — Coming
11. XioraTrader (TradingView インジ 会員 SaaS) — Beta
12. XioraPredict (指標 データ 予測 SaaS) — Coming
13. XioraSalon (オンライン サロン SaaS) — Coming

### 1.4 「内部 stack」 (Internal)

- 定義 : 顧客 対象外。 Xiora が 自社 運用 する ため の infrastructure / handler / assistant。
- 対象 : Xiora 内部 (Reo + 代理人 群) のみ。
- 課金 : なし (社内 経費)。
- 承認 sales cycle : なし。
- 特徴 : 一般 訪問者 は 触れられない。 HP 露出 は 原則 禁止 (insights の tech 記事 で 事例 として 紹介 する場合 は OK 、 ただし「顧客 が 買える」と 誤認 される 表現 は NG)。

該当 offering (2026-07-19 時点) :
1. X Systems (brain + handlers 、 Xiora 内部 AI infrastructure)
2. Rei (Chief of Staff 、 Xiora 内部 専用 秘書 AI)
3. Ocean LLM (base model project 、 R&D)
4. XiroraRegistrar (Xiora 内部 registration bot)
5. XAILegalChain (Xiora 内部 legal gate)
6. XAIOutreach (Xiora 内部 cold email)
7. XAISeoAutomation (Xiora 内部 SEO 自動化)
8. XAIPR (Xiora 内部 PR pipeline)
9. XAIPortal (Xiora 内部 admin portal)

---

## 2. 数え 方 (tier 別 count)

| tier | 数 | 主な 公開 URL 導線 |
|:---|---:|:---|
| アプリ | 3 (+1 未定) | /products/kigen.html · /products/ocean-chat.html · /products/aiverse.html |
| サービス | 7 | /ai-consulting.html · /web-engineering.html · /growth-marketing.html · /dx-engineering.html · /system-app-development.html · /pricing.html |
| システム | 13 | /products/{nexa-academy · gourmie · xcloud-connect · xcloud-flow · restaurant-os · shigyo-agents · agent-factory · content-engine · tradeos · xiora-trader · xiora-predict · xiora-salon}.html + xioraec (未 page) |
| 内部 stack | 9 | (HP 非公開) |

合計 offering (顧客 向け) : 3 + 7 + 13 = **23** 。 加えて 内部 stack 9 = 32 asset。

---

## 3. HP での 表示 rule

### 3.1 category badge

各 product page の 冒頭 に、 status pill と 並列 で category badge を 追加。 例 :

```html
<p class="page-hero__eyebrow reveal">
  <span class="dash"></span>Products / Kigen
  <span class="pill pill--muted" style="margin-left:12px;">[アプリ]</span>
  <span class="pill pill--muted" style="margin-left:8px;">iOS App · Released</span>
</p>
```

badge は 全 product page 必須。 顧客 が「これは アプリ？ サービス？ システム？」を 3 秒で 判別 できる 状態 に する。

### 3.2 products/index.html の 一覧

3 section に 分離 :

1. **アプリ** (3 card + 将来 枠) — 「install して すぐ 使える」導線
2. **システム** (13 card) — 「契約 して 継続 で 使う」導線
3. **サービス** は products/ ではなく、 /ai-consulting.html 等 の 個別 サービス LP に 誘導 (products/ = 買える もの、 サービス = 相談 する もの、 と 導線 分離)

### 3.3 top page の hero

3 pillar を 明示 :

- **アプリ**: 「Kigen (iOS) 、 Ocean Chat (Web) 、 Aiverse Studio — 個人 の 生活 · 仕事 を 支える アプリ」
- **サービス**: 「AI 導入 コンサル · Web 制作 · 動画 代行 — Xiora が 直接 提供 する 事業」
- **システム**: 「Nexa · Gourmie · XCloud · Restaurant OS · Shigyo Agents 等 — 継続 契約 の SaaS 群」

### 3.4 内部 stack の 露出

**原則 禁止** : X Systems / Rei / XiroraRegistrar / XAILegalChain / XAIOutreach / XAISeoAutomation / XAIPR / XAIPortal は Xiora HP から 完全 隔離。

**例外** : insights の tech 記事 で「Xiora が 内部 で こう 使っている」文脈 で 引用 する のは OK。 ただし :
- 「これは 顧客 が 買える もの ではない」と 明示
- CTA / 導入 リンク は 禁止 (相談 CTA へ 誘導 は OK)
- 内部 codename を そのまま 露出 する 場合 は「Xiora 内製」の prefix / 説明 を 付ける

---

## 4. 用語 統一 (禁止 / 推奨)

| 禁止 | 推奨 | 理由 |
|:---|:---|:---|
| 「app / アプリ」を SaaS 意味 で 使用 | SaaS = 「システム」 | 混在 が 客観 的 に 分かり にくい |
| 「service / サービス」を SaaS 意味 で 使用 | SaaS = 「システム」 | 単発 労働 と 継続 契約 が 区別 されない |
| 「system」を hardware 意味 で 使用 | B2B SaaS = 「システム」 | HP 上 は 一貫 |
| 「プロダクト」を サービス 意味 で 使用 | アプリ or システム のみ「プロダクト」呼称 | 「Products」page は アプリ + システム 限定 |

---

## 5. 適用 対象 (2026-07-19 以降)

- Xiora HP 全 page (index / products / insights / legal / contact / company / pricing / etc)
- Stripe products の name / description
- 契約書 template
- 営業 email (XAIOutreach template)
- SNS / 記事 冒頭 の 定型 phrase

## 6. 例外 承認

新規 offering が 4 tier に 収まらない 場合、 Reo が 明示 承認 後 に この doc を revise。 代理人 判断 で 5 tier 目 を 増やす のは 禁止。

---

## 7. Change log

- 2026-07-19 v1.0 : 初版。 3 tier + 内部 stack 定義、 23 offering の 分類 確定。
- 以降 の 変更 は Change log に 追記 、 diff は commit history 参照。
