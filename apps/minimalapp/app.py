# Flaskクラスをインポートする
from flask import Flask, render_template, request, url_for, redirect, flash
from email_validator import validate_email, EmailNotValidError
import logging
import os
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

# Flaskクラスをインスタンス化する
# __name__ には、今動いているPythonファイルの名前 が入ります。
# Flask はそれを使って「このアプリがどこにあるか」を把握
app = Flask(__name__)

# Mailクラスのコンフィグを追加
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# flask-mail 拡張を登録
mail = Mail(app)

# SECRET_KEYを設定
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"
app.logger.setLevel(logging.DEBUG)
app.logger.critical("重大なエラー")
app.logger.error("エラー")
app.logger.warning("警告")
app.logger.info("情報")
app.logger.debug("デバック情報")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
toolbar = DebugToolbarExtension(app)


# #デコレーターを使用してルーティングする(URI [http://127.0.0.1:5001/])と関数の関連づけ
@app.route("/")  # ("/")…エンドポイント
def index():  # ルーティング　関数と関連付け
    # print(__name__) 実行するアプリ名が入る
    return "Hello,Flaskbook"


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        is_valid = True
        if not username:
            flash("ユーザー名は必須です")
            is_valid = False

        if not email:
            flash("メールアドレスは必須です")
            is_valid = False
        else:
            try:
                validate_email(email)
            except EmailNotValidError:
                flash("メールアドレスの形式で入力してください")
                is_valid = False

        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        flash(
            "問い合わせ内容はメールにて送信しました。問い合わせありがとうございます。"
        )

        def send_email(to, subject, template, **kwargs):
            msg = Message(subject, recipients=[to])
            msg.body = render_template(template + ".txt", **kwargs)
            msg.html = render_template(template + ".html", **kwargs)
            mail.send(msg)

        send_email(
            email,
            "問い合わせありがとうございます。",
            "contact_mail",
            username=username,
            description=description,
        )
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")
