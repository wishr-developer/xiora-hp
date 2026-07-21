# Xiora Vault Setup Guide 2026

- 発行元: Xiora（沓澤 怜士 個人事業）
- 版数: v1.0 (2026-07-21)
- 対象: SaaS 開発者 / freelance エンジニア / secret management を code 側 に統合したい方
- 用途: macOS Keychain / iOS Passkey / systemd-creds ベースの secret 一元管理 の 30 分 setup
- 想定環境: macOS 14+ / Linux (systemd) / iOS 17+

このガイドは、Xiora が 2026 年に 全 credential を macOS Keychain / iOS Passkey / Postfix relay / systemd-creds で 統合的 に 管理している 実 architecture を、 誰でも 30 分 で 再現できる 手順 に 落としたものです。

**重要**: 本ドキュメントには 実 credential 値 は 一切 含みません。 全 例示 は placeholder / pattern のみです。 実運用 の 値 は 皆様 の 環境 に あわせて 入力してください。

## 目次

1. なぜ .env に 頼らないのか — 問題設定
2. Vault Architecture の 全体像 (macOS / Linux / iOS)
3. macOS Keychain へ の credential 保存 手順
4. macOS Keychain の Access Control ACL 設定
5. Vault key naming 規約
6. Python から Vault を 参照する pattern
7. Node.js から Vault を 参照する pattern
8. Bash から Vault を 参照する pattern
9. iOS Passkey / Keychain との 統合
10. Linux systemd-creds への 保存 手順
11. Postfix relay の credential 統合
12. credential 分類 と 命名 例 (Xiora 実運用の 分類 表)
13. rotation / 削除 の 手順
14. troubleshooting — 5 頻出パターン
15. 憲法 grep — Vault leak を 静的検出する方法

---

## 1. なぜ .env に 頼らないのか — 問題設定

`.env` file ベースの secret 管理には 以下 5 つの 恒常的 リスク が あります:

1. **git commit 事故**: `.gitignore` から漏れる、historical commit に混入
2. **backup 経由 漏洩**: Time Machine / iCloud / Dropbox が 平文 `.env` を バックアップ
3. **プロセス env 経由 漏洩**: `ps auxe` / `/proc/PID/environ` で 見える
4. **shell history 経由 漏洩**: `export XXX=yyy` を コピペ すると `.zsh_history` に残る
5. **CI 経由 漏洩**: CI ログ / artifact / build cache に 混入

Vault (macOS Keychain / iOS Keychain Services / systemd-creds) は:

- OS カーネル レベル で 保護 (Full Disk Encryption と 統合)
- process 単位 の access control (ACL) で 明示 許可 が 必要
- backup / clone 経由 の 漏洩 は 不可 (Secure Enclave)
- shell history には 「参照コマンド」しか残らない (`security find-generic-password -s xxx -w`)

**Xiora の 実 運用 方針**: Anthropic API / Stripe SK / Rakuten rafcid / GitHub token / SMTP password / DB password の 6 大分類 は 全て Vault、 `.env` は 「Vault key の 名前 だけ」 を 記載 する構造 に 統一しています。

---

## 2. Vault Architecture の 全体像 (macOS / Linux / iOS)

```
┌────────────────────────────────────────────────────────┐
│                    Vault Sources                        │
├────────────────────────────────────────────────────────┤
│  macOS: Keychain (login.keychain-db)                   │
│  Linux: systemd-creds (LoadCredentialEncrypted=)       │
│  iOS:   Keychain Services (kSecClassGenericPassword)   │
│  Postfix: /etc/postfix/sasl_passwd (root readable)     │
└────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────┐
│               Runtime Language Bindings                 │
├────────────────────────────────────────────────────────┤
│  Python: subprocess (security), keyring (macOS)        │
│  Node.js: keytar (native module) / child_process       │
│  Bash: security find-generic-password -s KEY -w        │
└────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────┐
│                Application code                         │
├────────────────────────────────────────────────────────┤
│  const sk = get_vault("xai:XXX:STRIPE_SECRET_KEY")     │
│  # 一度 process 内 に 展開されたら env にも file にも   │
│  # 書き出さない                                         │
└────────────────────────────────────────────────────────┘
```

**原則**:

- Vault から取得した値は process memory のみ に 保持
- log / print / trace への 出力 は 静的検出 (mask formatter)
- rotation は Vault 側 の 更新 で 即時 反映 (application は次回参照時に新値取得)

---

## 3. macOS Keychain へ の credential 保存 手順

macOS Keychain は `security` CLI で操作します。

### 3-1. 新規追加

```bash
# Generic Password として追加
security add-generic-password \
  -a "SERVICE_ACCOUNT_NAME" \
  -s "vault:project:CREDENTIAL_NAME" \
  -w "SECRET_VALUE" \
  -U  # 既存の同名 key を update
```

- `-a`: account (自由文字列、Xiora では runner user 名を使用)
- `-s`: service (Vault key、後述の naming 規約に従う)
- `-w`: password (SECRET_VALUE、shell history に残る点に注意 → 下記 3-2 の対話入力 推奨)
- `-U`: 既存 update

**推奨**: shell history に SECRET_VALUE を 残さない ために、対話入力 を 使用:

```bash
# -w 引数を省略すると 対話プロンプトで入力できる (履歴に残らない)
security add-generic-password -a "runner" -s "vault:xiora:STRIPE_SK" -U
# → password: を promptで入力
```

### 3-2. 取得

```bash
security find-generic-password -s "vault:xiora:STRIPE_SK" -w
# → SECRET_VALUE が stdout に出る
```

### 3-3. 削除

```bash
security delete-generic-password -s "vault:xiora:STRIPE_SK"
```

### 3-4. 全 list (Vault key 一覧確認、値は 表示 されない)

```bash
security dump-keychain | grep -E "^\s+\"svce\"<blob>" | sort -u
```

---

## 4. macOS Keychain の Access Control ACL 設定

Keychain の 各 entry には Access Control List (ACL) が 設定できます。 デフォルトでは 生成した process (通常 zsh / bash) からのみ 読める設定 に なっています。

### 4-1. 特定 binary からの 読み取り のみ許可

Keychain Access.app で 対象 key を 右クリック → 「情報」 → 「アクセス制御」タブ で、 許可 binary を 追加/削除できます。

CLI からは `security set-generic-password-partition-list` を使用します。

```bash
# 例: python3 と node からの 読み取り を 追加
security set-generic-password-partition-list \
  -S "apple-tool:,apple:,codesign:" \
  -s "vault:xiora:STRIPE_SK"
```

- `-S`: partition list (許可 binary の hash や codesign teamid)
- 対話 promptで keychain unlock password を 求められる

### 4-2. 「常に許可」 リスト の 設計方針

Xiora では以下 2 分類 で 運用:

- **開発中 の 一時 secret**: 「常に許可」 に せず、 参照 の 都度 unlock (安全側)
- **daemon / launchd 起動 の secret**: 「常に許可」 に する必要あり (unlock 不能)

daemon 用 の secret は 別 keychain (`~/Library/Keychains/xiora-daemon.keychain-db`) を 作成し、 daemon プロセスの codesign teamid を ACL に 明示 追加 する パターンを 推奨。

---

## 5. Vault key naming 規約

一貫した命名 は 「grep で 静的検出」 と 「rotation の 対象 特定」 を 両立させます。

**Xiora 規約** (推奨テンプレ):

```
<vault>:<Project>:<CREDENTIAL_NAME>
```

例:

- `xai:XCloudAxive:STRIPE_SECRET_KEY`
- `xai:XioraFounderPackBundle2026:PRODUCT_ID`
- `xai:Rakuten:RAFCID`
- `xai:GitHub:PAT_XCLOUD_DEPLOY`
- `xai:Gmail:INFO_APP_PASSWORD`

**規約**:

1. namespace prefix (`xai:` or `vault:`) を 全 key に つける (dump時 に 検索容易)
2. Project 名 は PascalCase (プロジェクト名 が Vault で 集約表示 される)
3. CREDENTIAL_NAME は SCREAMING_SNAKE_CASE (env var と 名前が 一致 する)
4. 環境 (prod / staging) を 区別する場合、 CREDENTIAL_NAME の suffix に `_PROD` / `_STAGING` を 付与

---

## 6. Python から Vault を 参照する pattern

Python では標準ライブラリ `subprocess` で `security` CLI を 呼ぶ pattern を 推奨します。

### 6-1. 参照 helper (推奨実装)

```python
# vault.py
import subprocess
import functools


class VaultError(RuntimeError):
    pass


@functools.lru_cache(maxsize=64)
def get_vault(key: str) -> str:
    """
    macOS Keychain から credential を取得する。 プロセス内キャッシュ有。
    key は 「xai:Project:CREDENTIAL_NAME」形式。
    """
    if not key or ":" not in key:
        raise VaultError(f"invalid vault key: {key!r}")

    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-s", key, "-w"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
    except subprocess.CalledProcessError as e:
        raise VaultError(f"vault key not found: {key}") from e
    except subprocess.TimeoutExpired as e:
        raise VaultError(f"vault access timeout: {key}") from e

    value = result.stdout.strip()
    if not value:
        raise VaultError(f"vault key empty: {key}")
    return value


def mask(value: str, prefix: int = 4) -> str:
    """log 出力用 の mask helper"""
    if not value or len(value) <= prefix:
        return "***"
    return f"{value[:prefix]}...***"
```

### 6-2. 使用例

```python
from vault import get_vault, mask
import logging

log = logging.getLogger(__name__)

sk = get_vault("xai:XCloudAxive:STRIPE_SECRET_KEY")
log.info("stripe sk loaded: %s", mask(sk))
# → INFO stripe sk loaded: sk_l...***
```

### 6-3. 禁則事項

- `os.environ[...] = sk` で env に 書き戻さない (child process に leak)
- `print(sk)` / f-string log を 避ける (formatter で mask 必須)
- pytest fixture で `sk` を 平文 で 引き渡す → conftest.py で mask 済み fixture を 提供する

---

## 7. Node.js から Vault を 参照する pattern

### 7-1. child_process 版 (追加依存なし)

```javascript
// vault.js
const { execFileSync } = require("child_process");

const cache = new Map();

function getVault(key) {
  if (!key || !key.includes(":")) {
    throw new Error(`invalid vault key: ${key}`);
  }
  if (cache.has(key)) return cache.get(key);

  let value;
  try {
    value = execFileSync("security", ["find-generic-password", "-s", key, "-w"], {
      encoding: "utf8",
      timeout: 5000,
    }).trim();
  } catch (e) {
    throw new Error(`vault key not found: ${key}`);
  }

  if (!value) throw new Error(`vault key empty: ${key}`);
  cache.set(key, value);
  return value;
}

function mask(value, prefix = 4) {
  if (!value || value.length <= prefix) return "***";
  return `${value.slice(0, prefix)}...***`;
}

module.exports = { getVault, mask };
```

### 7-2. keytar 版 (native module、追加依存あり)

```javascript
// keytar は Chromium / Electron でも 使われている 高信頼 native module
const keytar = require("keytar");

async function getVaultAsync(service, account = "runner") {
  const value = await keytar.getPassword(service, account);
  if (!value) throw new Error(`vault key not found: ${service}`);
  return value;
}

// 使用例
const sk = await getVaultAsync("xai:XCloudAxive:STRIPE_SECRET_KEY");
```

### 7-3. 禁則事項

- `process.env.STRIPE_SK = sk` で env に 書き戻さない
- `console.log(sk)` を 避ける (winston / pino の formatter で redact 必須)
- Next.js の `serverRuntimeConfig` / `env` に 展開 する場合 は build 時 embed の 挙動 に 注意 (production build の chunk に 埋まる 恐れ)

---

## 8. Bash から Vault を 参照する pattern

### 8-1. 参照 helper

```bash
# vault.sh
vault_get() {
  local key="$1"
  if [[ -z "$key" || "$key" != *:* ]]; then
    echo "invalid vault key: $key" >&2
    return 2
  fi

  local value
  value=$(security find-generic-password -s "$key" -w 2>/dev/null)
  if [[ -z "$value" ]]; then
    echo "vault key not found: $key" >&2
    return 3
  fi
  printf '%s' "$value"
}
```

### 8-2. 使用例 (curl での API 呼び出し)

```bash
source vault.sh

SK=$(vault_get "xai:XCloudAxive:STRIPE_SECRET_KEY")
# → curl に 引き渡す。 shell の env には 展開 しない
curl -s -u "${SK}:" "https://api.stripe.com/v1/products" | jq .
```

### 8-3. 禁則事項

- `export SK=$(vault_get ...)` は 避ける (child process 全て に 漏洩)
- shell script の 冒頭 に `set -x` (trace) が 有効 に なっていないか 確認 (SK が stdout に出る)
- history に 残さない: script 内 で 使用、対話 shell で 直接 `security ... -w` を 実行 しない

---

## 9. iOS Passkey / Keychain との 統合

iOS では Keychain Services API を Swift / Objective-C から 利用します。 (Xiora の iOS アプリ KigenX / Xiora Lingua で 実 使用中)

### 9-1. Swift 例 (kSecClassGenericPassword)

```swift
import Foundation
import Security

enum VaultError: Error {
    case notFound(String)
    case osStatus(OSStatus)
}

func saveToVault(key: String, value: String) throws {
    guard let data = value.data(using: .utf8) else {
        throw VaultError.osStatus(errSecParam)
    }

    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrService as String: key,
        kSecValueData as String: data,
        kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlock
    ]

    SecItemDelete(query as CFDictionary)  // 既存 削除 (idempotent)
    let status = SecItemAdd(query as CFDictionary, nil)
    guard status == errSecSuccess else { throw VaultError.osStatus(status) }
}

func getFromVault(key: String) throws -> String {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrService as String: key,
        kSecReturnData as String: kCFBooleanTrue as Any,
        kSecMatchLimit as String: kSecMatchLimitOne
    ]

    var item: CFTypeRef?
    let status = SecItemCopyMatching(query as CFDictionary, &item)
    guard status == errSecSuccess else { throw VaultError.notFound(key) }

    guard let data = item as? Data,
          let value = String(data: data, encoding: .utf8) else {
        throw VaultError.notFound(key)
    }
    return value
}
```

### 9-2. Access Level 選択

- `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` — 最も 厳格 (パスコード 設定必須 + backup 対象外)
- `kSecAttrAccessibleAfterFirstUnlock` — daemon 用 (再起動後 の 初回 unlock 以降 利用可)
- `kSecAttrAccessibleWhenUnlocked` — foreground 前提

### 9-3. Passkey (WebAuthn) 統合

Passkey は Keychain と 統合されており、 iCloud Keychain 経由 で デバイス間 同期 されます。 サーバー側 に は 公開鍵 のみ 保存、 秘密鍵 は Secure Enclave 内 で 保持されます。

---

## 10. Linux systemd-creds への 保存 手順

Linux (systemd 250+) では `systemd-creds` が macOS Keychain 相当 の 役割 を 担います。

### 10-1. 保存

```bash
# root 権限で暗号化保存
sudo systemd-creds encrypt \
  --name=xiora_stripe_sk \
  - /etc/credstore.encrypted/xiora_stripe_sk.cred
# → stdin で SECRET_VALUE を入力し Ctrl+D
```

### 10-2. systemd unit から 参照

```ini
# /etc/systemd/system/xiora-daemon.service
[Service]
LoadCredentialEncrypted=xiora_stripe_sk:/etc/credstore.encrypted/xiora_stripe_sk.cred
Environment=STRIPE_SK_FILE=%d/xiora_stripe_sk
ExecStart=/usr/local/bin/xiora-daemon
```

- `%d` は systemd の credential directory placeholder
- application は `open($STRIPE_SK_FILE)` で 平文 credential を 取得

### 10-3. 禁則事項

- `LoadCredential=` (暗号化なし) は 使用禁止、必ず `LoadCredentialEncrypted=`
- credential file を `/tmp` などに コピー しない (systemd が session tmpfs で 隔離)

---

## 11. Postfix relay の credential 統合

Postfix で SMTP relay (Gmail / SES / SendGrid) を使う場合、 `sasl_passwd` に 平文 password を 書く 必要が あります。 セキュリティ確保 の ため:

### 11-1. `sasl_passwd` の ACL

```bash
sudo tee /etc/postfix/sasl_passwd > /dev/null <<'EOF'
[smtp.gmail.com]:587 info@xiora-official.com:APP_PASSWORD_PLACEHOLDER
EOF

sudo chmod 600 /etc/postfix/sasl_passwd
sudo chown root:root /etc/postfix/sasl_passwd
sudo postmap /etc/postfix/sasl_passwd
sudo chmod 600 /etc/postfix/sasl_passwd.db
```

- ACL: root のみ 読取可
- `postmap` で `.db` (Berkeley DB) 生成 後、 元 file の 削除 も 検討可 (rotation 時 再生成 想定)

### 11-2. main.cf 設定

```
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_tls_security_level = encrypt
smtp_sasl_tls_security_options = noanonymous
```

### 11-3. rotation

Gmail の app password が rotation された 場合:

```bash
sudo sed -i 's/APP_PASSWORD_OLD/APP_PASSWORD_NEW/' /etc/postfix/sasl_passwd
sudo postmap /etc/postfix/sasl_passwd
sudo systemctl reload postfix
```

`sed` の直前に `history -d $((HISTCMD-1))` で shell history を 削除 する運用も推奨。

---

## 12. credential 分類 と 命名 例 (Xiora 実運用の 分類 表)

Xiora が 実運用 で 使用している 分類 pattern (実 値 は 含みません、名前 pattern のみ):

| 分類 | Vault key pattern | 用途 |
|------|------------------|------|
| **Stripe** | `xai:<ProjectPascal>:STRIPE_SECRET_KEY` | 決済 API |
| **Stripe** | `xai:<ProjectPascal>:STRIPE_WEBHOOK_SECRET` | webhook 検証 |
| **Stripe** | `xai:<ProjectPascal>:PRODUCT_ID` | Payment Link 参照 |
| **Stripe** | `xai:<ProjectPascal>:PRICE_ID` | Payment Link 参照 |
| **Stripe** | `xai:<ProjectPascal>:PAYMENT_LINK_URL` | 販売 URL |
| **Stripe** | `xai:<ProjectPascal>:LOOKUP_KEY` | Price lookup |
| **Anthropic** | `xai:Anthropic:API_KEY_<usage>` | Claude API |
| **OpenAI** | `xai:OpenAI:API_KEY_<usage>` | OpenAI API |
| **Rakuten** | `xai:Rakuten:RAFCID` | 楽天アフィリエイト |
| **GitHub** | `xai:GitHub:PAT_<repo>` | private repo push |
| **Gmail** | `xai:Gmail:<address>_APP_PASSWORD` | SMTP / IMAP |
| **DB** | `xai:Postgres:<service>_PASSWORD` | DB 接続 |
| **VPS** | `xai:VPS:SSH_PRIVATE_KEY_<name>` | SSH 秘密鍵 |
| **DNS** | `xai:ConoHa:API_TOKEN` | ConoHa DNS 操作 |

**運用ポイント**:

- 1 サービス = 1 分類 = 1 Vault key namespace
- rotation は 分類 単位 で 実施
- 監査 log は `security find-generic-password ...` の 実行 history を launchd で 収集

---

## 13. rotation / 削除 の 手順

### 13-1. rotation (交換)

```bash
# 1. 新 credential を Vault に 追加 (別 key)
security add-generic-password -s "xai:Project:STRIPE_SK_v2" -a "runner"
# → 対話 promptで 新 value 入力

# 2. application 側 の 参照 key を v2 に 切替 (deploy)

# 3. 動作確認 後、 旧 key を 削除
security delete-generic-password -s "xai:Project:STRIPE_SK"

# 4. v2 の suffix を 外す rename (可読性)
V2=$(security find-generic-password -s "xai:Project:STRIPE_SK_v2" -w)
security add-generic-password -s "xai:Project:STRIPE_SK" -a "runner" -w "$V2" -U
security delete-generic-password -s "xai:Project:STRIPE_SK_v2"
unset V2
```

**注意**: step 4 で shell env に 一時展開 する 際 は 直後 に `unset` する。 shell history に `V2=...` の 行 が 残る 場合 `history -d` で 削除。

### 13-2. 完全 削除 (Vault key を 破棄)

```bash
security delete-generic-password -s "xai:Project:STRIPE_SK"

# 確認
security find-generic-password -s "xai:Project:STRIPE_SK" -w
# → security: SecKeychainSearchCopyNext: The specified item could not be found in the keychain.
```

削除後の revocation は Vault 側 だけ では 実現されない — 対応する API 側 (Stripe SK の revoke など) も 必ず実行。

---

## 14. troubleshooting — 5 頻出パターン

### 14-1. `security` command が Permission denied

- 原因: launchd 起動 プロセスで Keychain が unlock されていない
- 対処: daemon 用の `xiora-daemon.keychain-db` を 別途 作成し、 ACL を Codesign teamid で 明示

### 14-2. Node の keytar が Electron sandbox で 失敗

- 原因: keytar は native module で sandbox 環境 では 動作しない
- 対処: `child_process` fallback (本 guide 7-1) に 切替

### 14-3. `security add-generic-password: -U` を 忘れて 「already exists」

- 原因: 同名 key が 既存
- 対処: `-U` (update flag) を 常に つける習慣に

### 14-4. Keychain が unlock 要求で 対話 prompt を返す (自動化不能)

- 原因: 「常に許可」 ACL が 未設定
- 対処: Keychain Access.app で 対象 key の 「アクセス制御」 → 「すべてのアプリケーションによるこの項目へのアクセスを許可」 を 選択 (or CLI で `set-generic-password-partition-list`)

### 14-5. Vault key に 改行 / スペース が 混入

- 原因: `-w "$(cat file)"` で trailing newline が 混入
- 対処: `-w "$(cat file | tr -d '\n')"` or 対話 input を 使用

---

## 15. 憲法 grep — Vault leak を 静的検出する方法

「Vault key を bypass して 平文 secret を code に 埋め込んだ」ケースを 静的検出する grep pattern。

### 15-1. .gitignore に .env* を 追加 (必須)

```
.env
.env.*
!.env.example
```

### 15-2. pre-commit hook (`.git/hooks/pre-commit`)

```bash
#!/usr/bin/env bash
# pre-commit hook: 平文 secret の commit を block

# Stripe SK pattern
if git diff --cached | grep -qE 'sk_(live|test)_[A-Za-z0-9]{24,}'; then
  echo "ERROR: Stripe SK detected in staged changes" >&2
  echo "  → Use Vault key like get_vault('xai:Project:STRIPE_SK') instead" >&2
  exit 1
fi

# Anthropic API key pattern
if git diff --cached | grep -qE 'sk-ant-api[0-9]+-[A-Za-z0-9_-]{40,}'; then
  echo "ERROR: Anthropic API key detected in staged changes" >&2
  exit 1
fi

# OpenAI API key pattern
if git diff --cached | grep -qE 'sk-[A-Za-z0-9]{40,}'; then
  echo "WARN: possible OpenAI API key in staged changes" >&2
fi

# Gmail app password pattern (16 chars, group by 4)
if git diff --cached | grep -qE '\b[a-z]{4} [a-z]{4} [a-z]{4} [a-z]{4}\b'; then
  echo "WARN: possible Gmail app password in staged changes" >&2
fi

# generic .env line commit
if git diff --cached --name-only | grep -qE '(^|/)\.env(\.|$)'; then
  echo "ERROR: .env file being committed" >&2
  exit 1
fi

exit 0
```

### 15-3. CI (GitHub Actions) での 追加検出

```yaml
- name: constitution-grep
  run: |
    if grep -rE 'sk_(live|test)_[A-Za-z0-9]{24,}' --include='*.js' --include='*.py' --include='*.ts' .; then
      echo "::error::plain Stripe SK detected in source"
      exit 1
    fi
    if grep -rE 'sk-ant-api' --include='*.js' --include='*.py' --include='*.ts' .; then
      echo "::error::plain Anthropic key detected in source"
      exit 1
    fi
```

### 15-4. gitleaks / trufflehog の 併用

上記 pattern に加え、`gitleaks detect` を CI に 組み込むと 汎用 パターン (AWS / GCP / Slack / Twilio 等) も 検出可能。

---

## 更新履歴

- 2026-07-21 v1.0 初版 (macOS Keychain / iOS Passkey / Linux systemd-creds / Postfix / 15 セクション)

---

**発行元**: Xiora（沓澤 怜士 個人事業）
**販売ページ**: https://xiora-official.com/products/xiora-vault-setup-guide-2026.html
**特商法**: https://xiora-official.com/legal/tokusho.html
**問い合わせ**: info@xiora-official.com
