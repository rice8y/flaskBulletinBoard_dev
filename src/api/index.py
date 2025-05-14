from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__, template_folder='templates')

db_url = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Post {self.id}>'
    
    def formatted_date(self):
        jst_time = self.created_at + timedelta(hours=9)
        return jst_time.strftime('%Y-%m-%d %H:%M:%S')

def create_tables():
    with app.app_context():
        db.create_all()

@app.before_request
def setup():
    try:
        create_tables()
    except Exception as e:
        print(f"テーブル作成エラー: {str(e)}")

@app.route('/', methods=['GET'])
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['POST'])
def add_post():
    content = request.form.get('content')
    if content:
        new_post = Post(content=content)
        db.session.add(new_post)
        db.session.commit()
    return redirect(url_for('index'))