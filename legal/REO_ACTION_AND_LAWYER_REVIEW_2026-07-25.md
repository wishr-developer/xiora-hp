# Xiora Legal Pages · Reo 決定 事項 + 弁護士 review 依頼 統合 資料

**発行**: 2026-07-25 (v2 · Reo 決定 反映 版)
**対象**: 沓澤 怜士 (Xiora 代表 · 弁護士 依頼 前 の 事前 準備)
**目的**: 現行 legal pages の 「Reo 決定 事項」(2026-07-25 確定) と 「弁護士 review 必須 事項」を 一枚 で 整理、弁護士 spot 面談 30-60 分 で 収束 させる。

## 2026-07-25 Reo 決定 済 (確定)

| 項目 | 決定 内容 |
|---|---|
| 所在地 | 〒150-0043 東京都渋谷区道玄坂 1-10-8 渋谷道玄坂東急ビル 2F-C |
| 電話 番号 | 070-9165-0203 (平日 10-18 時 目安、原則 メール info@xiora-official.com 優先) |
| 事業者 形態 | Xiora（沓澤 怜士 個人事業）継続 |
| DPO / 個人情報 保護管理者 | 沓澤 怜士 (代表者 兼務) |
| **資格 必要 事業 の 方針** | **業許可 · 士業 資格 が 必要 な 事業 は 一切 行わない** (投資 助言 業 / 医療 機器 業 / 弁護士 業 / 税理士 業 / 宅建 業 / 貸金 業 等)。 該当 する 機能 は 販売 停止 or 「情報 提供 のみ の 範囲」に 限定 する。 |

全 legal pages に 上記 を 反映 済 (下記 § 4)。

---

## 1. 決定 済 事項 の 各 legal file 反映 状況 (2026-07-25 確定)

上記 5 事項 は 全 legal file に 反映 済 (下記 § 4 状態 一覧)。 弁護士 面談 で 追加 決定 が 必要 な 事項 は § 1.5 のみ。

### 1.5 資格 必要 事業 NG 方針 に 基づく product 見直し

Reo 明示 「業許可 · 士業 資格 が 必要 な 事業 は 行わない」に 従い、以下 の product は 該当 リスク が ある。 弁護士 spot review で 個別 判定 が 必要。

| product | リスク 資格 | 現状 の 立て付け | 弁護士 判断 必要 |
|---|---|---|---|
| **Xiora Algo** (投資 シグナル) | 金商法 「投資 助言 · 代理 業」登録 (¥15 万+ · 弁護士 費 別) | waitlist mode (販売 停止 中)、β 開始 時 は 「価格 予測 · 個別 銘柄 推奨 を 提供 しない 情報 配信 のみ」で 登録 不要 の 範囲 を 目指す | Xiora Algo β 開始 の 具体 signal 内容 が 「投資 助言」に 該当 しない line を 弁護士 に 確認 → 該当 する 場合 は 廃止 判断 |
| **KigenX** の 薬 期限 リマインダー | 薬機法 医療 機器 業 許可 (Class I 該当時) | health-disclaimer.html で 「疾病 予防 目的 で ない、生活 支援 ソフトウェア」立て付け | Class I 該当 判定 なら 該当 機能 削除 or App Store 別 カテゴリ 変更 |
| **Shigyo Agents** (士業 AI Chain) | 弁護士 業 / 税理士 業 / 社労士 業 (代行 業務 該当時) | 士業 事務所 が 自社 業務 に 使う SaaS で、当社 が 士業 業務 を 代行 する もの で は ない 立て付け | 「士業 資格 の ない Xiora が 士業 業務 に あたる 助言 を 生成 する」機能 (契約 書 draft 等) の 弁護士 業法 72 条 (非弁護士 の 法律 事務 取扱 禁止) 該当 性 |
| **AI Legal Chain** (Track Z 内部) | 弁護士 業 (対外 販売 時) | 内部 draft 作成 tool、対外 販売 なし | 販売 なら 上記 と 同じ 判断 |

**Reo 方針** (2026-07-25 確定):
- 「資格 必要 = NG」= 弁護士 判定 で 「資格 必要」となった 機能 は 販売 停止
- 「資格 不要 の 範囲」に 収まる 場合 は 継続 (要 弁護士 line 引き)

---

## 2. 弁護士 に 見て もらう べき 項目 (優先度 順)

### 2.1 優先度 A (販売 開始 前 必須 · 面談 30-60 分)

| # | 項目 | 対象 file | 弁護士 に 聞く 内容 |
|---|---|---|---|
| A1 | 投資 助言 業 該当性 | `investment-disclaimer.html` | Xiora Algo の signal 配信 が 金商法 第 29 条 「投資 助言 業」に 該当 する か。 「価格 予測 · 個別 銘柄 推奨 を 提供 しない」で 通せる か の 具体 line 引き。 |
| A2 | 医療 機器 該当性 | `health-disclaimer.html` | KigenX の 「薬 の 使用期限 リマインダー」機能 が 薬機法 の Class I 医療 機器 に 該当 する リスク。 「疾病 予防 目的 で は ない、生活 支援」の 立て付け で 通るか。 |
| A3 | 特商法 施行規則 第 23 条 の 通信販売 例外 | `tokusho.html` | 「所在地 · 電話 番号 は 請求時 遅滞なく 開示」 の 立て付け が 越谷 消費生活センター 監査 で 通る か。 拒否 された 場合 の 対応 案。 |
| A4 | 免責 上限 条項 の 消費者契約法 適合 | `terms.html` §5 | 「当該 事象 が 生じた 月 の 料金 額 上限」 が 消契法 8 条 (全部 免責 無効) に 抵触 しない か。 買切 商品 の 場合 の 上限 明文化 案。 |
| A5 | β/α 版 販売 と 景品表示法 | 各 LP (Sales AI OS/EC-Autopilot/Xiora Lingua) | 「α 版 · 4/13 稼働」表記 で 有料 販売 する 場合 の 景表法 優良誤認 リスク の 判断。 現行 disclosure の 十分 度。 |

**予想 弁護士 費用**: spot 相談 30-60 分 = ¥15,000-30,000 (5 項目 まとめて)

### 2.2 優先度 B (販売 開始 3 ヶ月 以内 · 別 面談)

| # | 項目 | 対象 file | 内容 |
|---|---|---|---|
| B1 | GDPR SCC 対応 | `privacy.html` | EU/UK 顧客 獲得 前 に Standard Contractual Clauses (SCC) 締結 + privacy 記載 追加 |
| B2 | EU AI Act 対応 | `ai-disclaimer.html` | 2026-08 全面 適用、General-Purpose AI (GPAI) Provider の 責任 範囲 |
| B3 | 商標 出願 | `disclaimer.html` § 商標 | Xiora / Nexa / Ocean 3 brand の 商標 出願 (弁理士 経由、¥12,000 × 3 = ¥36,000) |
| B4 | 電子契約 法 対応 | `tokusho.html` § 支払 時期 | 「申込 意思 表示 の 確認 画面」記載 の 追加 |

### 2.3 優先度 C (自社 完結 可 · Reo 判断 のみ)

- `cookies.html` — 標準 テンプレ 範囲、Reo 修正 で OK
- `brand-separation.html` — 内部 運用 rule、Reo 意思 決定 のみ
- `disclaimer.html` 一般 部分 — product 列挙 更新 (既に 実施 済)
- `index.html` — hub page、product 追加時 更新

---

## 3. 弁護士 依頼 の 具体 手順

### 3.1 弁護士 を どう 見つけるか

Reo 明示 「弁護士 spot は 原則 不要、AI Legal Chain で 置換」の 方針 (`memory/feedback_lawyer_is_optional.md`)。 ただし 上記 優先度 A の 5 項目 は 弁護士 spot が 必要。

**候補**:
1. 弁護士 ドットコム · 有料 相談 (¥5,500-11,000/30 分) — spot に 最適
2. ココナラ IT 系 弁護士 (¥3,000-10,000/相談) — SaaS 実務 に 慣れて いる 人 選択 可
3. 越谷 · 地元 弁護士 会 の 中小 企業 法律 相談 (初回 30 分 ¥5,500)

**推奨**: 1 の 弁護士 ドットコム で 「IT 系 · SaaS 実務 経験 5 年 以上」の 弁護士 を 選び、上記 5 項目 を 事前 送付 + 60 分 対面 or Zoom で 一括 確認。

### 3.2 弁護士 面談 の 資料 (この 文書 が 全 準備)

弁護士 に 送る 資料:
1. 本 文書 (`REO_ACTION_AND_LAWYER_REVIEW_2026-07-25.md`)
2. 対象 5 file の 最新 版 URL:
   - https://xiora-official.com/legal/investment-disclaimer.html
   - https://xiora-official.com/legal/health-disclaimer.html
   - https://xiora-official.com/legal/tokusho.html
   - https://xiora-official.com/legal/terms.html
   - https://sales-ai-os.pages.dev/ (α 版 表記 例)
3. Xiora product 一覧 (`tokusho.html` の 販売 価格 table)

### 3.3 弁護士 面談 後 の 更新 flow

1. 弁護士 の 修正 指示 を 全 file に 反映 → git commit + CF Pages deploy
2. 見直し 周期 6 ヶ月 (次回 2027-01-25)
3. 弁護士 の 名前 · 事務所 名 は legal-lawyer-note に 明記 (「本 書類 は 弁護士 XXX の spot review を 経て 公開 して います」に 昇格)

---

## 4. 現状 の legal pages 状態 (2026-07-25 修正 反映 済)

| file | 修正 内容 | 状態 |
|---|---|---|
| `tokusho.html` | 販売 価格 表 を LIVE 反映 (13 product), 販売 終了 別 セクション, 所在地 昇格 | ✅ 修正 済 |
| `privacy.html` | product 列挙 更新, PPO 明記, 越境 データ 移転 詳細, 所在地 昇格 | ✅ 修正 済 |
| `terms.html` | product 列挙 更新, 販売 終了 明記 | ✅ 修正 済 |
| `disclaimer.html` | 商標 列挙 更新, 投資 関連 = Xiora Algo waitlist mode 反映 | ✅ 修正 済 |
| `brand-separation.html` | Xiora Tech ブランド 事業 一覧 全 再構成 | ✅ 修正 済 |
| `cookies.html` | 変更 なし (標準 テンプレ 範囲 OK) | ⚪ 現状 維持 |
| `health-disclaimer.html` | 変更 なし | ⚠️ 弁護士 review A2 対象 |
| `investment-disclaimer.html` | 変更 なし | ⚠️ 弁護士 review A1 対象 (Xiora Algo 統合 判断 保留) |
| `ai-disclaimer.html` | 変更 なし | ⚪ B2 対象 |
| `index.html` | 変更 なし | ⚪ 現状 維持 |

---

## 5. Reo 次 の action

**即 (5 分)**:
- [ ] 上記 § 1 の 5 事項 に つき 決定 内容 を チェック
- [ ] 弁護士 dot com or 地元 弁護士 会 に 「IT 系 SaaS 弁護士 60 分 spot 相談」を 予約 (¥15,000 前後)
- [ ] 予約 時 に 本 文書 URL (deploy 後) + 対象 5 file URL を 送付

**弁護士 面談 後 (1 日)**:
- [ ] 弁護士 の 修正 指示 を Reo が info@ に 転送 → 代理人 が 全 file に 反映 → commit + deploy

**継続**:
- [ ] 6 ヶ月 毎 に 見直し (次回 = 2027-01-25)
- [ ] 販売 開始 3 ヶ月 以内 に 商標 出願 (B3、¥36,000)
- [ ] EU/UK 顧客 獲得 前 に GDPR SCC 対応 (B1)

---

**発行元**: Xiora AI Legal Chain (Track Z, AI-assisted draft)
**責任**: 沓澤 怜士 (Xiora 代表)
**連絡**: info@xiora-official.com
