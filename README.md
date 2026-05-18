# Xiora Official Site

AI・Web制作・DX支援会社 **Xiora** のコーポレートサイト（静的HTML/CSS/JS）。
GitHub Actions により `main` ブランチへの push で ConoHa WING へ自動デプロイされます。

---

## 📁 ディレクトリ構成

```
.
├── index.html
├── assets/
│   ├── css/style.css
│   └── js/main.js
├── .github/
│   └── workflows/deploy.yml      # GitHub Actions 設定
├── .gitignore
└── README.md
```

---

## 🚀 デプロイ仕様

| 項目 | 内容 |
| --- | --- |
| デプロイ方式 | GitHub Actions（FTPS） |
| トリガー | `main` ブランチへの push、または手動実行 |
| デプロイ先 | サイトルート直下（`/home/cXXXXXXX/public_html/xiora-official.com/`） |
| FTPユーザー接続許可ディレクトリ | `/home/cXXXXXXX/public_html/xiora-official.com/`（サイトルート） |
| 既存ファイル削除 | **しない**（`dangerous-clean-slate: false`）— WordPress関連ファイルは保持 |
| プロトコル | FTPS（暗号化FTP・ポート21） |

> **NOTE**: サイトルート直下にデプロイされます。`dangerous-clean-slate: false` により WordPress 等の既存ファイルは削除されません（追加・上書きのみ）。

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

```bash
# 変更を加える
git add .
git commit -m "update: ヒーローコピーを修正"
git push origin main
```

→ push と同時に GitHub Actions が走り、約 1〜3 分で ConoHa WING に反映されます。

### 手動デプロイ

GitHub → **Actions** → **Deploy to ConoHa WING** → **Run workflow** から手動実行も可能。

---

## 🚫 デプロイ対象外ファイル

以下は FTP アップロード時に **除外** されます（`.github/workflows/deploy.yml` の `exclude` で制御）。

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
