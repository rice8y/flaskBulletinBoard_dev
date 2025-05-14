from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL接続設定（環境変数から取得）
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM posts ORDER BY id DESC')
    posts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['POST'])
def add_post():
    content = request.form['content']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO posts (content) VALUES (%s)', (content,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')
