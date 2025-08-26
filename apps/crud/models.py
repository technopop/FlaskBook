from datetime import datetime
from apps.app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column("passward_hush", db.String)
    create_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    user_images = db.relationship(
        "UserImage",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def password(self):
        raise AttributeError("読み取り不可")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))  # 文字列→整数に揃える
    except (TypeError, ValueError):
        return None
