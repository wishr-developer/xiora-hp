# Reo action — ROOM 1 account manual login (3-5 分)

## 目的

VPS 側 で AI 生成 中 の 42 posts (ROOM + X) を、 実 posting する 前 提。 楽天 ROOM は 個人 login が KYC 相当 なので Reo 手動 login → storage_state 保存 で 以降 半 自動 post が 動く。

## 前提

- VPS 側 の AI 生成 (Mac fan 静止 維持) は 別 途 稼働 中
- ROOM の 生存 account: `xai:ROOM:ROOM_EMAIL_ACCOUNT1` (Vault 済、 memory `xiora_life_media_2026_07_21.md`)
- Mac IPv6 fix (Cloudflare block 回避) が 未 完了 なら 先 に 対応 必要

## Reo 手順 (Mac 上、 3-5 分)

### Step 0: Mac IPv6 の 状態 確認

```bash
# ターミナル で:
networksetup -listallnetworkservices | grep -v denoted
# Wi-Fi の 場合:
networksetup -getinfo Wi-Fi | grep IPv6
```

出力 で `IPv6: Automatic` なら OK。 `IPv6: Off` の 場合 は 一時 有効 化:

```bash
sudo networksetup -setv6automatic Wi-Fi
```

### Step 1: Playwright headed mode で ROOM login

```bash
cd /Users/kutsuzawareo/Desktop/XAI/services/systems/XioraLifeMedia
python3 -c "
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto('https://room.rakuten.co.jp/login')
        print('Reo: login して下さい (email + password + 2FA)、 login 完了 したら Enter')
        input()
        await context.storage_state(path='data/storage_state/room_account1.storage.json')
        print('storage_state saved')
        await browser.close()

asyncio.run(main())
"
```

Chromium window が 開く → Reo が email + password 入力 · 2FA (SMS or Authenticator) 通過 · login 完了 → ターミナル で Enter 押す → storage_state 保存 完了。

### Step 2: 保存 確認

```bash
ls -la /Users/kutsuzawareo/Desktop/XAI/services/systems/XioraLifeMedia/data/storage_state/
# → room_account1.storage.json (30-100KB) が 存在 する はず
```

## 後 続 flow (私 が execute)

Reo login 完了 通知 後、 私 が:

1. **VPS 側 の AI batch 完了** を 待つ (推定 60-90 min · Mac 影響 なし)
2. **AI 生成 42 posts + 手動 note 15 posts** を Reo review 用 に 提出
3. **Reo 明示 approve** の post から Playwright semi-auto で ROOM に 順次 投稿
   - 1 時間 3 件 以下、 45 分 同 shop 空け の guardrail 遵守
   - 各 post は 「PR」明示 (消費 者 庁 stealth marketing 規制 対応)
4. **1 週間 continuous** で ROOM traffic + click + conversion を 集計、 EV2 score 実 験証
5. **月 ¥500-¥3,000** の Phase 1 revenue 見込み (memory `xiora_life_media_2026_07_21.md` の 実 実績 参照)

## 並行 準備 中 の 他 channel

- **Amazon Associates 登録** (`services/systems/XAIAffiliateHub/amazon_associates_2026-07-25/REO_REGISTRATION_GUIDE.md`) — 5-10 分 で 登録 · 家電 / tech 系 revenue 開通
- **A8.net 登録** (`services/systems/XAIAffiliateHub/a8_2026-07-25/REO_REGISTRATION_GUIDE.md`) — 5 分 で 登録 · 大手 案件 (SaaS/金融) 提携 準備

3 platform 同時 稼働 で **月 ¥5,500-¥48,000 (Phase 1)** の 見込み (詳細 `docs/affiliate_revenue_channel_2026-07-28.md`)。

## 現在 の 進行 状態 (2026-07-28)

- ✅ 戦略 doc + AI 化 doc + VPS 移設 doc 完成
- ✅ Ollama VPS install + qwen2.5:7b pull 完了
- ✅ AI batch 稼働 中 (2/42 生成 済、 Mac 静止)
- ✅ 15 posts の Reo review 版 提出 済 (`docs/REO_REVIEW_affiliate_batch1_2026-07-28.md`)
- ⏳ Reo 待ち: 本 doc の ROOM login (3-5 分)
- ⏳ Reo 待ち: Amazon Associates + A8.net 登録 (合計 10-15 分)

Reo が 3 action (ROOM login + Amazon + A8) の いずれ か 1 つ でも execute すれば、 私 が 続き の 全 automation を 稼働 化 する。
