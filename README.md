# FlaskBook – 物体検出デモアプリ

## 📌 プロジェクト概要
Flask を使った Web アプリケーションです。  
PyTorch の **Mask R-CNN (ResNet50 + FPN, COCO学習済みモデル)** を利用し、画像から物体検出を行います。

---

## 🚀 セットアップ手順

### 1. リポジトリをクローン
```bash
git clone https://github.com/<yourname>/flaskbook.git
cd flaskbook
```

### 2. 仮想環境を作成 & 有効化
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. ライブラリをインストール
```bash
pip install -r requirements.txt
```

### 4. 環境変数を設定
`.env.example` をコピーして `.env` を作成し、自分の環境に合わせて編集します：
```bash
cp .env.example .env
```

---

## ▶️ 実行方法
```bash
flask run -p 5001
```

ブラウザで開く：  
👉 http://127.0.0.1:5001

---

## 📂 ディレクトリ構成
```
flaskbook
├─ apps/          # アプリ本体
│  ├─ auth/       # 認証機能
│  ├─ crud/       # CRUD機能
│  ├─ detector/   # 物体検出機能
│  ├─ templates/  # HTMLテンプレート
│  ├─ static/     # CSS・画像
│  └─ config.py   # 設定ファイル
├─ migrations/    # DBマイグレーション
├─ .env.example   # 環境変数サンプル
├─ requirements.txt
├─ run.py
└─ README.md
```

---

## ⚠️ 注意
- `model.pt`（学習済みモデル）と `local.sqlite`（ローカルDB）は **GitHubにアップロードしません**  
- `.env` には秘密情報（メール設定やキー）を入れるので **絶対に公開しないこと**

---

## 📖 今後の拡張アイデア
- Docker 対応  
- CI/CD (GitHub Actions)  
- API 化（JSONで物体検出結果を返す）  
