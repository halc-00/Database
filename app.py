from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from models import db
from routes import api  # 追加

app = Flask(__name__)

# DB設定
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?client_encoding=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# DB初期化
db.init_app(app)
migrate = Migrate(app, db)

# APIルートを登録
app.register_blueprint(api, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)

from flask import render_template

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
