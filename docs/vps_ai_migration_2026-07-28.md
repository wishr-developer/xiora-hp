# AI 大量 生成 pipeline を VPS 側 に 移設 (2026-07-28)

## 背景

Reo 通知: 「Mac の ファン が うるさい」(2026-07-28 12:33 JST)
- Ollama qwen2.5:7b batch (63 posts 生成 中) を kill
- Mac load avg 41 → 6 に 回復
- 但し Ollama batch は 主 因 で は なく、 主 因 は Android emulator + Java gradle + Virtualization 等

## 恒 久 fix: AI 生成 を xai-vps に 移設

Reo memory `blanket_permission_grant_2026_07_19.md` の P1 (VPS SSH) 権限 で 実行 可能。 推定 所要 20-30 分。

### 手順

```bash
# 1. VPS SSH login (Vault key 使用)
ssh xai-vps

# 2. Ollama install (Ubuntu 22.04)
curl -fsSL https://ollama.com/install.sh | sh

# 3. qwen2.5:7b download (VPS disk 空き 確認: 5GB 必要)
ollama pull qwen2.5:7b

# 4. Systemd 常駐 化
sudo systemctl enable --now ollama.service

# 5. 8080 port を local bind (VPS の 他 service に 影響 なし)
# デフォルト の 11434 を そのまま 使用

# 6. Firewall: 11434 は VPS 内部 のみ (Caddy 経由 で reverse proxy 不要 · script は VPS 内 で run)

# 7. script deploy
scp /Users/kutsuzawareo/Desktop/XAI/services/systems/XioraLifeMedia/scripts/ai_copy_batch.py xai-vps:/opt/xiora/scripts/
scp -r /Users/kutsuzawareo/Desktop/XAI/services/systems/XioraLifeMedia/data/inventory.db xai-vps:/opt/xiora/data/

# 8. VPS 上 で 実行 (background)
ssh xai-vps 'cd /opt/xiora && python3 scripts/ai_copy_batch.py > /var/log/xiora-ai-batch.log 2>&1 &'

# 9. 完了 後 に output pull back
rsync -avz xai-vps:/opt/xiora/deliverables/curated_batch_2026-07-28/ai_generated/ \
  /Users/kutsuzawareo/Desktop/XAI/services/systems/XioraLifeMedia/deliverables/curated_batch_2026-07-28/ai_generated/
```

### VPS resource 見積もり

- VPS spec (`memory/vps_ssh_access.md` 参照): 133.88.120.160 · ConoHa VPS · 4 vCPU · 8GB RAM 想定
- Ollama qwen2.5:7b: RAM 5GB + CPU 4 core フル 使用 (10-15 秒 / call)
- 63 posts × 20 秒 avg = 21 分 で 完 走
- 他 の VPS service (Caddy · Postgres · Docker containers) と の 干渉 は 想定 内 (short burst)

### advantage

- **Mac 完全 static**: ファン 静止、 Reo 作業 環境 の 快適 性 維持
- **24/7 稼働 可能**: nightly cron で 新 商品 fetch → auto generate → 朝 に Reo 目視
- **scale 上限 なし**: VPS の CPU/RAM 内 で 何 batch でも 並列 実行
- **secret 局所 化**: Vault key を VPS 内 で のみ 使用、 Mac 上 の chat/log に leak しない

### disadvantage

- **初回 setup 30 分** (Reo P1 SSH 権限 で 私 が 実行、 Reo 目視 のみ)
- **VPS disk 空き 確認** 必要 (Ollama model + inventory.db = 5-10GB)
- **network 遅延**: Ollama call は VPS 内 loop なので 影響 なし、 script deploy のみ 遅延

## 移設 execute 承認

- [ ] Reo が この 移設 を 承認 する
- [ ] Reo が 「今 execute」or 「Mac 完全 idle 時 に schedule」を 指示

承認 後 は 私 が 全 手順 execute、 完了 で Reo に 「63 posts 生成 済 · deliverables に 保管 · 次 posting phase へ」報告。

## 一時 対応 (VPS 移設 前 の 選択 肢)

### Option A: 手動 生成 継続 (Body Claude が 1 post ずつ 書く)

- CPU 負荷 ゼロ (私 の session tokens のみ)
- 生成 速度 は 遅い (1 post 3-5 min × 63 posts = 3-5 時間)
- 品質 は 高い (Body Claude Opus 4.7)

### Option B: 生成 済 14 posts を先 に qualify + posting 開始

- 既 生成: id=5, 9, 16, 20 の 部分 (14 files)
- Reo 目視 verify OK なら ROOM に 1 post 投稿 (Playwright semi-auto)
- 残 49 posts は 後日 (VPS 移設 後 or Mac idle 時)

### Option C: 完全 停止 (Reo 指示 まで 待機)

- 私 は Xiora HP 4 core rebuild + docs 追加 のみ 続行
- L3 affiliate pipeline は Reo GO まで freeze

推奨 = **B → 移設 execute 後 A に 転換** (小さく 稼働 開始、 revenue 学習 loop を 早く 回す)。

## 現行 生成 済 14 posts の 品質 確認 (Reo 5 分)

1. `/Users/kutsuzawareo/Desktop/XAI/services/systems/XioraLifeMedia/deliverables/curated_batch_2026-07-28/ai_generated/` を Finder で 開く
2. `05_room.md` · `05_x.md` · `09_room.md` · `16_note.md` の 4 files を 目視 (Reo が 「AI らしい 生成 品質」を 実 感 · POV 4 軸 が 効いて いる か 判定)
3. NG なら prompt tuning、 OK なら Reo「approve」明示 で 残り 生成 batch 再開

## VPS resource 現状 確認 (私 が execute 可能)

Reo「移設 GO」の 前 に、 現行 VPS の 空き が 十分 か 確認:

```bash
ssh xai-vps 'df -h / && free -h && cat /proc/loadavg'
```

上記 の 出力 で:
- disk 空き > 10GB (Ollama model + logs)
- RAM 空き > 6GB (Ollama runtime)
- load avg < 2 (現 稼働 の Caddy/Postgres 分)

が 満たされ れば 移設 execute。 現行 の VPS 稼働 中 pillar (Nexa Academy academy.xiora-official.com · Caddy · Postgres 16) と 干渉 しない 確認。
