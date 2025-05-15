from flask_app import db
from datetime import datetime, timedelta

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def formatted_date(self):
        jst_time = self.created_at + timedelta(hours=9)
        return jst_time.strftime('%Y-%m-%d %H:%M:%S')