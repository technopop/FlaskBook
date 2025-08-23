import os
import shutil

import pytest

from apps.app import create_app, db
from apps.crud.models import User
from apps.detector.models import UserImage, UserImageTag


@pytest.fixture
def app(tmp_path):
    # テスト用アプリ作成
    app = create_app("testing")

    # テストごとに固有のアップロード先を割り当て
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = str(upload_dir)

    # DBのセットアップ
    with app.app_context():
        db.create_all()
        yield app
        # テスト後始末：セッション掃除→DBを落とす
        db.session.remove()
        db.drop_all()


@pytest.fixture
def fixture_app():
    app = create_app("testing")

    app.app_context().push()

    with app.app_context():
        db.create_all()

    os.makedirs(app.config["UPLOAD_FOLDER"])

    yield app

    User.query.delete()

    UserImage.query.delete()

    UserImageTag.query.delete()

    shutil.rmtree(app.config["UPLOAD_FOLDER"])

    db.session.commit()


@pytest.fixture
def client(app):
    return app.test_client()
