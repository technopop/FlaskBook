from pathlib import Path
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config
from flask_login import LoginManager
import os
import secrets  # ← 追加（開発用のフォールバックに使う）
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=BASE_DIR / ".env")

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.signup"
login_manager.login_message = ""


def create_app(config_key="development"):
    app = Flask(__name__)

    app.config.from_object(config[config_key])
    secret_key = os.environ.get("SECRET_KEY") or secrets.token_urlsafe(32)
    csrf_key = os.environ.get("WTF_CSRF_SECRET_KEY") or secrets.token_urlsafe(32)

    db_uri = (
        os.environ.get("DATABASE_URL")  # .envにあればそれを使う
        or f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}"  # なければ従来のsqlite
    )

    app.config.update(
        SECRET_KEY=secret_key,
        WTF_CSRF_SECRET_KEY=csrf_key,
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
    )

    db.init_app(app)
    Migrate(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    # vews.pyのblueprintの機能を読み込み(アプリ分割機能)
    from apps.crud import views as crud_views
    from apps.auth import views as auth_views
    from apps.detector import views as dt_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    app.register_blueprint(dt_views.dt)
    app.register_error_handler(404, page_not_fonund)
    app.register_error_handler(500, internal_server_error)
    return app


def page_not_fonund(e):
    return render_template("404.html"), 404


def internal_server_error(e):
    return render_template("500.html"), 500
