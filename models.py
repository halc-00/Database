from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ユーザーテーブル
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

# 学習計画テーブル
class StudyPlan(db.Model):
    __tablename__ = "study_plans"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    goal_time = db.Column(db.Integer, nullable=False)  # 目標時間（分）
    weekly_schedule = db.Column(db.JSON)  # JSON型で曜日ごとの予定を保存
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="study_plans")

# 学習記録テーブル
class StudyRecord(db.Model):
    __tablename__ = "study_records"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey("study_plans.id", ondelete="SET NULL"))
    subject = db.Column(db.String(50), nullable=False)
    study_time = db.Column(db.Integer, nullable=False)  # 学習時間（分）
    record_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="study_records")
    plan = db.relationship("StudyPlan", backref="study_records")

    def __repr__(self):
        return f"<StudyRecord id={self.id} subject={self.subject} study_time={self.study_time}>"

# 学習メモテーブル
class StudyNote(db.Model):
    __tablename__ = "study_notes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    study_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="study_notes")

# 復習リストテーブル
class ReviewList(db.Model):
    __tablename__ = "review_list"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    study_note_id = db.Column(db.Integer, db.ForeignKey("study_notes.id", ondelete="CASCADE"), nullable=False)
    is_reviewed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="review_list")
    study_note = db.relationship("StudyNote", backref="review_list")
