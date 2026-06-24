from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"


class Job(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    company = db.Column(db.String(100))
    role = db.Column(db.String(100))
    status = db.Column(db.String(50))

    job_link = db.Column(db.String(500))

    priority = db.Column(
        db.String(20),
        default="Medium"
    )

    date_applied = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    deadline = db.Column(db.Date)

    interview_date = db.Column(db.Date)

    notes = db.Column(db.Text)