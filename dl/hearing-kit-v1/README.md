# Xiora AI ヒアリング & 業務改善 Prompt Kit v1

**販売者**: Xiora (沓澤 怜士 / 屋号)
**販売日**: 2026-09-18
**版**: v1.0

---

## 同梱物

- `01_business_hearing.txt` — 業務ヒアリング (8 問診断)
- `02_bottleneck_analysis.txt` — ボトルネック 6 軸分析
- `03_automation_roadmap.txt` — 90 日 自動化ロードマップ生成
- `04_roi_estimator.txt` — ROI 推定 (投資回収月数計算)
- `05_risk_and_ethics_check.txt` — リスク & 倫理 7 項目チェック
- `06_proposal_writer.txt` — 経営者向け 1 ページ提案書生成
- `07_kickoff_meeting_agenda.txt` — キックオフ MTG (60 分) アジェンダ
- `08_post_delivery_health_check.txt` — 導入後 30 日ヘルスチェック

## 想定利用者

- 中堅企業 / 個人事業主 の 経営者・情報システム担当
- 自社内 で AI 導入 or 業務自動化を検討している方
- 業務コンサル・IT コンサル で 顧客先の 診断 → 提案 → 実施 まで 一貫して支援したい方

## 使い方

1. **Claude (推奨) / ChatGPT / Gemini** の チャット画面を開く
2. `01_business_hearing.txt` の内容を貼り付け → 送信
3. AI が 質問 開始、顧客 (or 自分) が 8 問に回答
4. 全 回答終了後、AI が JSON 出力
5. その JSON を `02_bottleneck_analysis.txt` の Prompt と一緒に AI に渡す
6. 順次 03 → 04 → 05 → 06 の 5 プロンプトを実行 (Prompt チェーン)
7. 06 の 1 ページ提案書 を 経営者に提示
8. 実装後 30 日 で `08_post_delivery_health_check.txt` を実行

所要時間目安: 顧客との セッション 60-90 分 + AI 実行 30 分 = 合計 1.5-2 時間 で 1 案件の診断 → 提案 が完了します。

## 本 Kit の特徴

- **fabrication 禁止 clause 内蔵**: 各 Prompt 末尾に「相手のデータ以外の推測をしない」制約を明示
- **kill switch / risk 意識**: リスクチェック 7 項目 (05) で 導入前に 停止手段まで検証
- **Xiora 実装単価想定 (¥10,000/h)**: ROI 計算の 業界目安 前提を明記
- **Reality Check 必須**: Roadmap 末尾に「仮説であり、現場との Reality Check が必要」の一文が入る

## FAQ

**Q. Claude 以外の LLM でも 使えますか?**
A. ChatGPT / Gemini でも 動作します。ただし fabrication 禁止 clause が最も強く効くのは Claude です。

**Q. 顧客に この Kit の存在を知らせても 良いですか?**
A. Prompt テンプレの再配布は 禁止 ですが、Kit を使って生成した「提案書」「Roadmap」の 顧客への 提示は 自由 です。

**Q. v2 は いつ出ますか?**
A. 未定 です。v2 リリース時、v1 購入者は 差額のみで アップグレード (¥0 の場合もあり) 予定です。

## 免責

本 Kit を使用した診断・提案の結果に対して、Xiora は 商業的成功や ROI 実現を 保証 いたしません。実装は 使用者の判断・責任 で 行ってください。

## 連絡先

質問・改善提案: xiora00000@gmail.com

© 2026 Xiora — https://xiora-official.com
