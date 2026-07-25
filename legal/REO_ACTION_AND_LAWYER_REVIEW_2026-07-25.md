# Xiora Legal Pages · Reo 決定 事項 + 弁護士 review 依頼 統合 資料

**発行**: 2026-07-25 (audit 経過 sub-agent + main 実装 完了 版)
**対象**: 沓澤 怜士 (Xiora 代表 · 弁護士 依頼 前 の 事前 準備)
**目的**: 現行 legal pages の 「Reo 決定 必須 事項」 と 「弁護士 review 必須 事項」 を 一枚 で 整理、弁護士 spot 面談 30-60 分 で 収束 させる。

---

## 1. Reo が 弁護士 に 会う 前 に 決定 が 必要 な 5 事項

### 1.1 事業者 所在地 (最重要)

現状 全 legal pages で 「〒XXX-XXXX 埼玉県 越谷市 XXXX」の placeholder。 2026-07-25 audit で 「埼玉県 越谷市 (詳細 住所 は 請求時 遅滞なく 開示)」に **暫定** 昇格 (特商法施行規則 第 23 条 通信販売 例外 の 立て付け)。

**選択肢** (Reo 判断):

| 選択 | 月額 | プライバシー | 弁護士 難易度 |
|---|---|---|---|
| A. 越谷 自宅 住所 | ¥0 | 低 (公開 リスク) | 低 (シンプル) |
| B. 私書箱 (郵便 局 の 私書箱) | ¥0-500 | 中 | 中 (受取 flow 整備 要) |
| C. バーチャル オフィス · 越谷 プライバシーゾーン | ¥550 | 高 | 中 |
| D. バーチャル オフィス · GMO オフィスサポート 銀座 | ¥1,650 | 最 高 | 中 |
| E. 現状 の 「請求時 開示」立て付け 継続 | ¥0 | 高 | 高 (通信販売 例外 立て付け の 弁護士 review 必須) |

**推奨**: E → C or D の 順 (E は 弁護士 が OK 出せば 最 安 + 最 privacy 高、ダメ なら C = 越谷 継続 で ¥550/月)

### 1.2 事業者 形態

現状 全 legal pages で 「Xiora（沓澤 怜士 個人事業）」統一。 法人化 予定 が 3 ヶ月 以内 なら 一括 差替 準備 必要。

**Reo 決定**:
- [ ] 個人事業 継続 (現状 維持)
- [ ] 法人化 予定 (時期: ______、屋号: ______) → 一括 差替 準備

### 1.3 電話 番号 開示 方針

現状 「請求時 遅滞なく 開示」立て付け (特商法施行規則 第 23 条)。

**選択肢**:
- A. 継続 「請求時 開示」 (¥0、越谷 消費生活センター 監査 で 通るか 弁護士 確認)
- B. 050 IP 電話 (SMARTalk: ¥0/月 · 通話 従量、Twilio 050: 月 額 ¥100 前後) を 取得 して 常時 掲載
- C. 090/080 個人 携帯 掲載 (プライバシー 最低)

**推奨**: B (050 IP、¥0-100/月 で プライバシー 保護 + 常時 開示 で 消費者 安心 度 UP)

### 1.4 Data Protection Officer (DPO / 個人情報保護管理者)

現状 privacy.html に 「沓澤 怜士 (代表者 兼務)」明記 済。 個人事業 の 場合 は これで OK。 GDPR EU 顧客 が 25 名 超 で DPO 選任 義務 発生 (現時点 EU 顧客 ゼロ で 該当 なし)。

**Reo 決定**:
- [x] 「沓澤 怜士 (代表者 兼務)」で 継続 (default)
- [ ] EU 顧客 獲得 前 に 外部 DPO 委託 検討 (¥30,000-100,000/月 relatively expensive)

### 1.5 Xiora Algo の 位置付け 再定義

現状 実装 0 で LP は waitlist mode に 修正 済。 investment-disclaimer.html は 販売 停止 中 の 立て付け 反映 済。

**Reo 決定** (弁護士 面談 で):
- [ ] Xiora Algo は β 開始 時 に 「投資 助言 業 登録 なし の 情報 提供」で 継続
- [ ] Xiora Algo は 廃止 → LP + 4 legal 該当箇所 全 削除
- [ ] Xiora Algo は 投資 助言 業 登録 を 検討 (¥15 万+ 登録 費 + 弁護士 依頼 費)

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
