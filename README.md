# Xiora Official Site

AI・Web制作・DX支援会社 **Xiora** のコーポレートサイト（静的HTML/CSS/JS）。
GitHub Actions により、ブランチ単位で ConoHa WING へ自動デプロイされます。

- `main` ブランチ → **本番**：https://xiora-official.com/
- `staging` ブランチ → **テスト**：https://xiora-official.com/v2/

---

## 📁 ディレクトリ構成

```
.
├── index.html
├── assets/
│   ├── css/style.css
│   └── js/main.js
├── .github/
│   └── workflows/
│       ├── deploy.yml            # 本番デプロイ（main → サイトルート）
│       └── deploy-staging.yml    # テストデプロイ（staging → /v2/）
├── .gitignore
└── README.md
```

---

## 🚀 デプロイ仕様

### 2環境構成

| 環境 | ブランチ | デプロイ先 | URL |
| --- | --- | --- | --- |
| **本番（Production）** | `main` | サイトルート直下 | https://xiora-official.com/ |
| **テスト（Staging）** | `staging` | サイトルート配下 `/v2/` | https://xiora-official.com/v2/ |

### 共通仕様

| 項目 | 内容 |
| --- | --- |
| デプロイ方式 | GitHub Actions（FTPS） |
| トリガー | 各ブランチへの push、または **Actions** タブからの手動実行 |
| FTPユーザー接続許可ディレクトリ | `/home/cXXXXXXX/public_html/xiora-official.com/`（サイトルート） |
| 既存ファイル削除 | **しない**（`dangerous-clean-slate: false`）— WordPress関連ファイルは保持 |
| プロトコル | FTPS（暗号化FTP・ポート21） |
| 同時実行制御 | 環境ごとに `concurrency` で1本ずつ実行 |

> **NOTE**: `dangerous-clean-slate: false` により、サーバー上の既存ファイル（WordPress等）は削除されません。アップロード対象ファイルの追加・上書きのみが行われます。

---

## 🔐 GitHub Secrets の設定（初回のみ）

GitHub リポジトリにアクセスし、以下の手順で Secrets を登録します。

1. リポジトリ → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
2. 下記 3 つの Secret を追加：

| Secret 名 | 値の例 | 取得元 |
| --- | --- | --- |
| `FTP_SERVER` | `ftp.xxxxxx.conoha.ne.jp` | ConoHa WING コントロールパネル → サイト管理 → FTP情報 |
| `FTP_USERNAME` | `xxxxx@xiora-official.com` | 同上（FTPユーザー名） |
| `FTP_PASSWORD` | `********` | 同上（FTPパスワード） |

> **ConoHa WING の FTP 情報確認手順**
> 1. ConoHa WING コントロールパネルにログイン
> 2. 左メニュー **「サイト管理」** → 対象ドメインを選択
> 3. **「FTP」** タブで FTP サーバー名／ユーザー名／パスワードを確認
> 4. パスワードを忘れた場合は再発行可能

---

## 🛠 セットアップ手順（初回）

### 1. GitHub リポジトリを作成

GitHub 上で新規リポジトリを作成（例：`xiora-hp`）。

### 2. ローカルを Git 管理 & push

```bash
cd /path/to/Xiora_HP

git init
git add .
git commit -m "Initial commit: Xiora HP"
git branch -M main
git remote add origin https://github.com/<your-account>/<repo-name>.git
git push -u origin main
```

### 3. GitHub Secrets を登録

[上記「GitHub Secrets の設定」](#-github-secrets-の設定初回のみ) を参照。

### 4. 自動デプロイの確認

push 後、GitHub リポジトリ → **Actions** タブ で `Deploy to ConoHa WING` の実行ログが確認できます。

成功すると以下URLでアクセス可能：

```
https://xiora-official.com/
```

---

## 🔄 通常運用（更新時）

### 🧪 まずテスト環境で確認 → 本番反映（推奨フロー）

```bash
# 1. staging ブランチに切り替えて作業
git checkout staging   # 初回のみ: git checkout -b staging
git pull origin staging

# 2. 変更を加えてコミット
git add .
git commit -m "update: ヒーローコピーを修正"

# 3. staging に push → /v2/ に自動デプロイ
git push origin staging
```

→ https://xiora-official.com/v2/ で確認 → 問題なければ本番へ：

```bash
# 4. main にマージして push → 本番反映
git checkout main
git pull origin main
git merge staging
git push origin main
```

### ⚡ 緊急時：直接本番

軽微な修正など、ステージングを飛ばしたい場合は `main` に直接コミットしてpush：

```bash
git checkout main
git add .
git commit -m "fix: typo"
git push origin main
```

### 🖱 手動デプロイ

GitHub → **Actions** タブ → 該当ワークフロー（Production / Staging）→ **Run workflow** から実行可能。

---

## 🚫 デプロイ対象外ファイル

以下は FTP アップロード時に **除外** されます（各ワークフローの `exclude` で制御。本番・ステージング共通）。

- `.git*`、`.github/`、`.vscode/`、`.idea/`
- `node_modules/`
- `.DS_Store`、`Thumbs.db`
- ZIP / TAR / RAR / 7z などのアーカイブ
- `*.log`、`*.bak`
- `README.md`、`LICENSE`
- `.env*`、`.gitignore`、`.editorconfig`
- `package.json` などの Node 関連ファイル

→ 本番サーバーに公開すべきは `index.html` と `assets/` のみ。

---

## 🧪 ローカルでの確認

ビルド不要。ブラウザで `index.html` を直接開くか、簡易サーバーを起動：

```bash
# Python が入っていれば
python3 -m http.server 8000
# → http://localhost:8000

# または npx を使う場合
npx serve .
```

---

## 🎨 デザインメモ

- カラー: `#0a0a0a` / `#1d1d1f` / `#6e6e73` / `#f5f5f7` / `#ffffff`
- フォント: Inter + Noto Sans JP
- スタイル: Apple 風 / 余白多め / 黒・白・グレー基調
- アニメーション: 軽量（IntersectionObserver によるフェードイン、`prefers-reduced-motion` 対応）

---

## 🆘 トラブルシューティング

| 症状 | 対処 |
| --- | --- |
| Actions が失敗：`530 Login authentication failed` | `FTP_USERNAME` / `FTP_PASSWORD` を再確認。コピペ時の余分なスペースに注意 |
| Actions が失敗：`ENOTFOUND` / `connection timeout` | `FTP_SERVER` のホスト名を ConoHa パネルで再確認 |
| `v2/` にアクセスしても 403 / 404 | ConoHa 側で対象ディレクトリの公開設定・パーミッション（755）を確認 |
| FTPS で接続できない | `deploy.yml` の `protocol` を `ftp` に一時変更して切り分け。原則はFTPS推奨 |
| 一部ファイルが反映されない | Actions ログの `excluded` に該当していないか確認。キャッシュは ConoHa パネルからクリア |

---

## 📩 Contact

- Mail: info@xiora-official.com
