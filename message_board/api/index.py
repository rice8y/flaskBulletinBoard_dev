from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

# Initialize Flask app
app = Flask(__name__, template_folder='templates')

# データベース接続設定 - 環境変数から読み込む
db_url = os.environ.get("DATABASE_URL", "postgresql://neondb_owner:npg_qWge0kfXZV7U@ep-morning-bonus-a1izqnc2-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# 掲示板の投稿モデルを定義
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Post {self.id}>'
    
    def formatted_date(self):
        # UTC時間から日本時間(UTC+9)に変換
        jst_time = self.created_at + timedelta(hours=9)
        return jst_time.strftime('%Y-%m-%d %H:%M:%S')

# データベーステーブルの作成
def create_tables():
    with app.app_context():
        db.create_all()

# アプリケーション開始時にテーブル作成を確認
@app.before_first_request
def setup():
    try:
        create_tables()
    except Exception as e:
        print(f"テーブル作成エラー: {str(e)}")

@app.route('/', methods=['GET'])
def index():
    # データベースから全ての投稿を取得（最新順）
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['POST'])
def add_post():
    # フォームから内容を取得
    content = request.form.get('content')
    if content:
        # 新しい投稿をデータベースに追加
        new_post = Post(content=content)
        db.session.add(new_post)
        db.session.commit()
    return redirect(url_for('index'))

# Vercelのデプロイ対応
if __name__ == '__main__':
    app.run(debug=True)