# from flask_wtf import FlaskForm
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import PasswordField, StringField, SubmitField

# from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, length
from flask_wtf.file import FileAllowed, FileField, FileRequired


class UserForm(FlaskForm):
    username = StringField(
        "ユーザー名",
        validators=[
            DataRequired(message="ユーザー名は必須です"),
            length(max=30, message="30文字以内で入力してください"),
        ],
    )

    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired(message="メールアドレスは必須です"),
            Email(message="メールアドレスの形式で入力してください"),
        ],
    )

    password = PasswordField(
        "パスワード", validators=[DataRequired(message="パスワードは必須です")]
    )

    submit = SubmitField("新規登録")


class UploadImageForm(FlaskForm):
    image = FileField(
        validators=[
            FileRequired("画像ファイルを指定してください"),
            FileAllowed(["png", "jpg", "jpeg"], "サポートされていない形式です"),
        ]
    )
    # user_id,image_pathがないので、views.pyでエラー
    submit = SubmitField("アップロード")


class DetectorForm(FlaskForm):
    submit = SubmitField("検知")


class DeleteForm(FlaskForm):
    submit = SubmitField("削除")
