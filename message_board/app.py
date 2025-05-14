from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app with explicit template folder
app = Flask(__name__, 
           template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates')))

# Set connection string from Vercel's dashboard
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://neondb_owner:npg_qWge0kfXZV7U@ep-morning-bonus-a1izqnc2-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
# Initialize SQLAlchemy
db = SQLAlchemy(app)

# 掲示板の投稿モデルを定義
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Post {self.id}>'

# Create database tables in the PostgreSQL database
with app.app_context():
    db.create_all()

@app.route('/')
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

if __name__ == '__main__':
    app.run(debug=False)