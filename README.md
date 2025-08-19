# FlaskBook

# Flaskbook Sample App

学習用の Flask アプリ。ログイン/CRUD/画像アップロード 等の基本を実装。

## セットアップ
```bash
py -m venv venv
venv\Scripts\Activate.ps1   # Windows（Mac/Linux: source venv/bin/activate）
pip install -r requirements.txt
flask run -p 5001

## 環境変数の設定
プロジェクト直下に `.env` を配置してください。
サンプルは `.env.example` をコピーして編集してください。
