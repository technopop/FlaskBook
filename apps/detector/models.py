from datetime import datetime
from apps.app import db


class UserImage(db.Model):
    __tablename__ = "user_images"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.String, db.ForeignKey("users.id"), nullable=False, index=True
    )
    image_path = db.Column("image_pah", db.String)
    is_detected = db.Column(db.Boolean, default=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    user = db.relationship("User", back_populates="user_images")


class UserImageTag(db.Model):
    __tablename__ = "user_image_tags"
    id = db.Column(db.Integer, primary_key=True)
    user_image_id = db.Column(db.String, db.ForeignKey("user_images.id"))
    tag_name = db.Column(db.String)
    create_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
