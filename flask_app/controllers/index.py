from flask import Blueprint, render_template, request, redirect, url_for
from flask_app.models import Post
from flask_app import db

bp = Blueprint('index', __name__)

@bp.route('/', methods=['GET'])
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@bp.route('/add', methods=['POST'])
def add_post():
    content = request.form.get('content')
    if content:
        new_post = Post(content=content)
        db.session.add(new_post)
        db.session.commit()
    return redirect(url_for('index.index'))