# Prompt 01 — 診断的コードレビュー

**用途**: Claude Code / Cursor / ChatGPT に コードレビュー を 頼む際、「LGTM」を返されずに business logic + security + performance の 3 層で 実質的 な 指摘 を 引き出す。

## Prompt (コピペ用)

```
以下のコードをレビューしてください。ただし、私は「良さそう」「一般的にOK」といった表面的な回答を必要としていません。
以下の3層で診断的レビューをお願いします。

【Layer 1: Business logic】
- このコードが解こうとしている問題を、コードから逆算して1-2文で説明してください。
- そのうえで、コードの実装が問題定義とズレている箇所を特定してください。
- Edge case (空入力/最大値/並行実行/ネットワーク遅延) で想定外挙動が発生する箇所を列挙してください。

【Layer 2: Security】
- 入力を信頼している箇所 (validation なしの user input, external API response, DB read) を全て指摘してください。
- OWASP Top 10 のいずれかに該当する箇所 (SQLi, XSS, SSRF, IDOR, auth bypass, sensitive data logging, insecure deserialization 等) を全て挙げてください。該当なしなら「該当なし」と明示してください。
- Secret / credential / PII が log / error message / URL に漏出する経路を確認してください。

【Layer 3: Performance & Maintainability】
- N+1 クエリ / 不要なループ / メモリリーク候補 / blocking I/O in async context を指摘してください。
- 「この変更を6か月後の私が読んで意図が分かるか」の観点で、コメント/命名/構造の改善点を挙げてください (「WHY-only comment」の原則、What はコードで語る)。
- テストされていない branch を列挙してください (test coverage が数字で出せる場合はカバー率も)。

【Format】
- 各 Layer の指摘は必ず file_path:line_number 形式で参照してください。
- 指摘は 重要度 (P0/P1/P2) をつけてください。
- 「良さそう」「一般的にOK」等の主観語は禁止です。事実 + 根拠 だけを述べてください。
- 修正案は 「変更差分の概要」だけ、実際のコード書き換えは別途依頼するまで実施しないでください。

【対象コード】
<ここに対象コードを貼り付け>
```

## なぜ効くか (実運用 evidence)

- **Xiora WorkAgent** の Phase 2E.4H 納品文 QC で 実際に使用。 表面的 pass → 誤字 3 箇所 + 文字数超過 1 箇所 の 指摘 が Layer 1 で 引き出せた。
- 「私は良さそうを必要としていません」明示 が LLM の 標準的な「基本的にはOKですが...」pattern を 抑制する rhetorical device。
- Layer 分割 は 一度の response で 3 面 を 網羅させるための forcing function。 1 layer だけの review は「主観」に流れやすい。

## Tips

- **Cursor / GitHub Copilot Chat**: 対象 code は @-mention or /explain で 添付
- **Claude Code**: file path で 直接指定、複数 file は 順に review
- **ChatGPT / Gemini**: 対象 code は 3 backtick で 囲んで 貼付
- 指摘 が P0/P1/P2 で ranked されるので、そのまま git commit message の template にも使える

## Anti-pattern (これは やらない)

- 「日本語で詳しく」だけ 追加 → 冗長 化 して 実質 情報 量 減
- 「初心者向けに」→ 難易度 下がって Layer 2 が 抜ける
- 全 Layer 一度 に 「全部書いて」→ 8-16k token 消費、要点 埋没

## v2 予定

- Layer 4: Accessibility (a11y)
- Layer 5: i18n (国際化)
- Layer 6: Type safety (TS/Python type coverage)
