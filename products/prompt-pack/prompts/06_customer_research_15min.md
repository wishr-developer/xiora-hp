# Prompt 06 — 会社 URL → 15 分で ICP + pain + fit + 提案切口

**用途**: B2B cold email / 営業前準備 で、会社 URL 1 本 から 15 分 以内 に 「なぜ弊社サービスがフィットするか」の 提案切口 を 引き出す。

## Prompt (コピペ用)

```
以下の会社について、15 分以内で「弊社サービスがフィットするか + どの角度で提案するか」を判定する事前調査を行ってください。

【対象会社】
- URL: <会社 URL>
- 弊社サービス概要: <自社サービス 3 行で。 例: Xiora AI Prompt Pack + Nexa Academy コース販売 + WorkAgent AI 自動化受託>
- 想定 ticket 単価: <¥XX,XXX>

【調査項目】
1. 会社基本情報 (公式サイトから取得可能なもののみ、推測禁止)
   - 業種 / 従業員規模 / 所在地 / 設立年
   - 提供 product / service
   - 主要顧客セグメント (BtoB / BtoC / SMB / Enterprise)
   - 直近ニュース or プレスリリース (公式サイト掲載分のみ)

2. 想定 ICP (Ideal Customer Profile) fit 判定
   - 弊社サービスの target size と 一致する社員規模か
   - 弊社サービスの target 業種 (SMB / 士業 / EC 等) と 合致するか
   - ¥XX,XXX の ticket が 意思決定 決裁範囲か (規模 × 予算感)

3. 推定 pain point (公開情報からの推定、断定禁止)
   - 事業内容から推定される 3 大 pain (人手不足 / データ活用 / 顧客対応 / 業務効率 / SEO / 契約管理 等)
   - 業種特有の 制約 (規制 / 季節性 / 人材確保 難易度 等)
   - 直近ニュースから読み取れる「今 動いている topic」

4. 弊社サービス fit 分析
   - どの pain に対して 弊社の どの機能 が 効くか (機能名で具体的に)
   - 導入 の 障壁 (既存システム / 業界慣習 / 内製比較) 3 つ
   - 「弊社でなければならない理由」or 「代替 (競合 or 内製) との差分」

5. 提案 切口 (top 3、outreach の 冒頭 hook 用)
   - 切口 A: <1 文 hook>
   - 切口 B: <1 文 hook>
   - 切口 C: <1 文 hook>
   - 各切口の「使いどころ」(cold email 冒頭 / 電話 / 事業提携 の どこで 効くか)

6. 判定 (最後に 1 行)
   - GO / MAYBE / NO-GO
   - 理由 (fit / 予算 / タイミング / 障壁 の いずれか)

【禁止事項】
- 推測を事実として書かない (「〜と思われる」「〜と推測する」を明示)
- 会社 URL に載っていない情報を fabricate しない
- ICP fit しなくても 「一応 GO」に流さない
- 15 分以上使わない (深掘りは receive 反応後)

【対象コード = ここに 会社 URL 貼付】
```

## なぜ効くか (実運用 evidence)

- **XAIOutreach 越谷/草加 飲食 5 + スクール美容 5** の 2026-07-18 target 調査 で 実際 使用。 従来 30-60 分 かけていた 事前調査 が 15 分 に 短縮。
- 「推測禁止」と 「fabrication check」の 明示 で LLM が 空想 pain point を 書かなくなる → cold email の 精度 向上 = spam 化 防止
- 「GO / MAYBE / NO-GO」の 明示的 判定 forcing で 「一応 送る」を 排除

## Tips

- **Playwright MCP** で 対象会社 URL を snapshot → 情報を Prompt に貼付 (公式 HP のみ、推測なし)
- **Xiora 実サービス** の 「target size / target 業種 / ticket」は 事前に memory 化 して Prompt に組込済 template を用意
- 判定 GO なら → Prompt 07 (cold email 起草) に そのまま繋げる

## Anti-pattern

- 会社 SNS (X / Instagram) を推測ソースにする → 事実精度 下がる
- 「LinkedIn の 経歴」を fabricate → プライバシー観点で NG
- 「業界平均」を出典なしで書く → 見抜かれると即座に信頼喪失

## 実 output 例 (Xiora WorkAgent が 08-18 に この Prompt で 出した ROI サマリ)

- 調査 5 社 (越谷 飲食): 平均 15 分/社
- GO 判定 3 社、MAYBE 1、NO-GO 1
- cold email 送信 5/5、reply 0 (D+7 時点、blocker = FDA grant 未解決)
- 「事前調査精度」の 手応え = 実際に GO 判定 会社 の web に載っていない pain を fabricate しなかった → 「知ったかぶり email」を避けられた
