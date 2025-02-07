from flask import Blueprint, request, jsonify
from models import db, StudyPlan

# Blueprintを作成（URLのプレフィックス: /api）
api = Blueprint("api", __name__)

# 1. 学習計画の新規作成（CREATE）
@api.route("/study_plans", methods=["POST"])
def create_study_plan():
    try:
        data = request.json
        user_id = data["user_id"]
        subject = data["subject"]
        goal_time = data["goal_time"]
        selected_day = data["selected_day"]  # 例: "Monday"
        
        # 週間スケジュールを作成（すべて0にして選択した曜日のみ時間をセット）
        weekly_schedule = {day: 0 for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
        weekly_schedule[selected_day] = goal_time  # 選択した曜日のみに時間をセット

        new_plan = StudyPlan(
            user_id=user_id,
            subject=subject,
            goal_time=goal_time,
            weekly_schedule=weekly_schedule
        )

        db.session.add(new_plan)
        db.session.commit()

        return jsonify({"message": "学習計画を作成しました", "id": new_plan.id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
#  2. 学習計画の取得（READ）
@api.route("/study_plans/<int:user_id>", methods=["GET"])
def get_study_plans(user_id):
    try:
        plans = db.session.query(
            StudyPlan.subject,
            func.sum(StudyPlan.goal_time).label("total_goal_time")
        ).filter(StudyPlan.user_id == user_id).group_by(StudyPlan.subject).all()

        return jsonify([
            {"subject": plan.subject, "goal_time": plan.total_goal_time} for plan in plans
        ])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#  3. 学習計画の更新（UPDATE）
@api.route("/study_plans/<int:plan_id>", methods=["PUT"])
def update_study_plan(plan_id):
    plan = StudyPlan.query.get(plan_id)
    if not plan:
        return jsonify({"error": "学習計画が見つかりません"}), 404

    data = request.json
    plan.subject = data.get("subject", plan.subject)
    plan.goal_time = data.get("goal_time", plan.goal_time)
    plan.weekly_schedule = data.get("weekly_schedule", plan.weekly_schedule)

    db.session.commit()
    return jsonify({"message": "学習計画を更新しました"})

#  4. 学習計画の削除（DELETE）
@api.route("/study_plans/<int:plan_id>", methods=["DELETE"])
def delete_study_plan(plan_id):
    plan = StudyPlan.query.get(plan_id)
    if not plan:
        return jsonify({"error": "学習計画が見つかりません"}), 404

    db.session.delete(plan)
    db.session.commit()
    return jsonify({"message": "学習計画を削除しました"})

from models import db, StudyRecord
from flask import Blueprint, request, jsonify

# 📌 1. 学習記録の新規作成（CREATE）
@api.route("/study_records", methods=["POST"])
def create_study_record():
    data = request.json
    
    # 必要なデータの取得
    user_id = data.get("user_id")
    plan_id = data.get("plan_id")  # 計画なしの記録もOK
    subject = data.get("subject")  # 追加: 科目
    study_time = data.get("study_time")
    record_date = data.get("record_date")

    # バリデーション（必須データの確認）
    if not user_id or not subject or study_time is None or not record_date:
        return jsonify({"error": "必要な情報が不足しています"}), 400

    # 学習記録を作成
    new_record = StudyRecord(
        user_id=user_id,
        plan_id=plan_id,
        subject=subject,  # 追加: 科目の保存
        study_time=study_time,
        record_date=record_date,
    )

    db.session.add(new_record)
    db.session.commit()

    return jsonify({"message": "学習記録を作成しました", "id": new_record.id}), 201
# 📌 2. 学習記録の取得（READ）
@api.route("/study_records/<int:user_id>", methods=["GET"])
def get_study_records(user_id):
    records = StudyRecord.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": record.id,
            "subject": record.subject,
            "study_time": record.study_time,
            "record_date": record.record_date.strftime("%Y-%m-%d")
    } for record in records])

# 📌 3. 学習記録の更新（UPDATE）
@api.route("/study_records/<int:record_id>", methods=["PUT"])
def update_study_record(record_id):
    record = StudyRecord.query.get(record_id)
    if not record:
        return jsonify({"error": "学習記録が見つかりません"}), 404

    data = request.json
    record.study_time = data.get("study_time", record.study_time)
    record.record_date = data.get("record_date", record.record_date)

    db.session.commit()
    return jsonify({"message": "学習記録を更新しました"})


from datetime import datetime, timedelta

@api.route("/stats/weekly_plan/<int:user_id>", methods=["GET"])
def get_weekly_plan(user_id):
    # 今日の曜日を取得
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())  # 月曜日
    end_of_week = start_of_week + timedelta(days=6)  # 日曜日

    # 学習計画を取得
    plans = StudyPlan.query.filter_by(user_id=user_id).all()

    # 今週の学習予定を取得
    week_schedule = []
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for plan in plans:
        schedule = plan.weekly_schedule  # JSONデータ
        if schedule:
            for day, study_time in schedule.items():
                if study_time > 0 and day in weekdays:  # 予定時間がある & 曜日が正しい
                    date = start_of_week + timedelta(days=weekdays.index(day))
                    if start_of_week <= date <= end_of_week:
                        week_schedule.append({
                            "title": f"{plan.subject} (予定 {study_time} 分)",
                            "start": date.strftime("%Y-%m-%d"),
                            "color": "red",  # 予定は赤色
                            "plan_id": plan.id
                        })

    return jsonify(week_schedule)


# 📌 4. 学習記録の削除（DELETE）
@api.route("/study_records/<int:record_id>", methods=["DELETE"])
def delete_study_record(record_id):
    record = StudyRecord.query.get(record_id)
    if not record:
        return jsonify({"error": "学習記録が見つかりません"}), 404

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "学習記録を削除しました"})


from models import db, StudyNote

# 📌 1. メモの新規作成（CREATE）
@api.route("/study_notes", methods=["POST"])
def create_study_note():
    data = request.json
    new_note = StudyNote(
        user_id=data["user_id"],
        content=data["content"],
        study_date=datetime.strptime(data["study_date"], "%Y-%m-%d")  # 文字列を日付に変換
    )
    db.session.add(new_note)
    db.session.commit()
    return jsonify({"message": "メモを作成しました", "id": new_note.id}), 201

# 📌 2. メモの取得（READ）
@api.route("/study_notes/<int:user_id>", methods=["GET"])
def get_study_notes(user_id):
    notes = StudyNote.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": note.id,
            "content": note.content,
            "study_date": note.study_date.strftime("%Y-%m-%d"),
        }
        for note in notes
    ])

@api.route("/stats/calendar_notes/<int:user_id>", methods=["GET"])
def get_calendar_notes(user_id):
    notes = StudyNote.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": note.id,
            "title": note.content,  # カレンダーに表示する内容
            "start": note.study_date.strftime("%Y-%m-%d"),
            "color": "gray",  # メモは灰色
            "note_id": note.id
        }
        for note in notes
    ])

# 📌 3. メモの更新（UPDATE）
@api.route("/study_notes/<int:note_id>", methods=["PUT"])
def update_study_note(note_id):
    note = StudyNote.query.get(note_id)
    if not note:
        return jsonify({"error": "メモが見つかりません"}), 404

    data = request.json
    note.content = data.get("content", note.content)
    note.study_date = data.get("study_date", note.study_date)

    db.session.commit()
    return jsonify({"message": "メモを更新しました"})

# 📌 4. メモの削除（DELETE）
@api.route("/study_notes/<int:note_id>", methods=["DELETE"])
def delete_study_note(note_id):
    note = StudyNote.query.get(note_id)
    if not note:
        return jsonify({"error": "メモが見つかりません"}), 404

    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "メモを削除しました"})


from models import db, ReviewList

# 📌 1. 復習リストの新規作成（CREATE）
@api.route("/review_list", methods=["POST"])
def create_review_list():
    data = request.json
    new_review = ReviewList(
        user_id=data["user_id"],
        study_note_id=data["study_note_id"],
        is_reviewed=False  # 初期状態では未復習
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"message": "復習リストに追加しました", "id": new_review.id}), 201

# 📌 2. 復習リストの取得（READ）
@api.route("/review_list/<int:user_id>", methods=["GET"])
def get_review_list(user_id):
    reviews = ReviewList.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": review.id,
        "study_note_id": review.study_note_id,
        "is_reviewed": review.is_reviewed,
        "created_at": review.created_at
    } for review in reviews])

# 📌 3. 復習の完了フラグを更新（UPDATE）
@api.route("/review_list/<int:review_id>", methods=["PUT"])
def update_review_status(review_id):
    review = ReviewList.query.get(review_id)
    if not review:
        return jsonify({"error": "復習リストが見つかりません"}), 404

    data = request.json
    review.is_reviewed = data.get("is_reviewed", review.is_reviewed)

    db.session.commit()
    return jsonify({"message": "復習リストのステータスを更新しました"})

# 📌 4. 復習リストの削除（DELETE）
@api.route("/review_list/<int:review_id>", methods=["DELETE"])
def delete_review_list(review_id):
    review = ReviewList.query.get(review_id)
    if not review:
        return jsonify({"error": "復習リストが見つかりません"}), 404

    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "復習リストから削除しました"})


from sqlalchemy.sql import func

# 📌 1. 週間の学習時間（棒グラフ用）
@api.route("/stats/weekly/<int:user_id>", methods=["GET"])
def get_weekly_stats(user_id):
    today = datetime.today()
    start_date = today - timedelta(days=6)  # 直近7日間
    end_date = today  # 今日まで

    # デフォルトで7日間のデータを作成（0分で初期化）
    weekly_data = { (start_date + timedelta(days=i)).strftime("%Y-%m-%d"): 0 for i in range(7) }

    # 実際のデータを取得
    records = (
        db.session.query(
            StudyRecord.record_date,
            func.sum(StudyRecord.study_time).label("total_time")
        )
        .filter(StudyRecord.user_id == user_id, StudyRecord.record_date.between(start_date, end_date))
        .group_by(StudyRecord.record_date)
        .all()
    )

    # 実際のデータを反映
    for record in records:
        weekly_data[record.record_date.strftime("%Y-%m-%d")] = record.total_time

    return jsonify([
        {"date": date, "total_time": total_time} for date, total_time in weekly_data.items()
    ])

# 📌 2. 目標達成率（％表示）
@api.route("/stats/progress/<int:user_id>", methods=["GET"])
def get_weekly_progress(user_id):
    try:
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())  # 月曜日
        end_of_week = start_of_week + timedelta(days=6)  # 土曜日

        subjects = ["japanese", "math", "science", "physics", "social", "english"]

        # 学習計画（分母）: その週の学習計画を取得
        plans = db.session.query(
            StudyPlan.subject,
            func.sum(StudyPlan.goal_time).label("goal_time")
        ).filter(
            StudyPlan.user_id == user_id
        ).group_by(StudyPlan.subject).all()

        print("学習計画のデータ:", plans)  # デバッグログ

        plan_dict = {subject: 1 for subject in subjects}  # デフォルト値
        for plan in plans:
            plan_dict[plan.subject] = plan.goal_time or 1  # None回避

        # 学習記録（分子）: その週の学習時間を取得
        records = db.session.query(
            StudyRecord.subject,
            func.sum(StudyRecord.study_time).label("study_time")
        ).filter(
            StudyRecord.user_id == user_id,
            StudyRecord.record_date.between(start_of_week, end_of_week)
        ).group_by(StudyRecord.subject).all()

        print("学習記録のデータ:", records)  # デバッグログ

        record_dict = {subject: 0 for subject in subjects}
        for record in records:
            record_dict[record.subject] = record.study_time or 0  # None回避

        # 達成率を計算
        progress = [
            {
                "subject": subject,
                "goal_time": plan_dict[subject],
                "total_time": record_dict[subject],
                "progress": round((record_dict[subject] / plan_dict[subject]) * 100, 2)
            }
            for subject in subjects
        ]

        print("計算結果:", progress)  # デバッグログ

        return jsonify(progress)

    except Exception as e:
        print("エラー発生:", str(e))  # エラーログ
        return jsonify({"error": str(e)}), 500



# 📌 3. 教科ごとの学習時間割合（円グラフ）
@api.route("/stats/subject_distribution/<int:user_id>", methods=["GET"])
def get_subject_distribution(user_id):
    try:
        # 科目リスト
        subjects = ["japanese", "math", "science", "physics", "social", "english"]

        # 学習記録から各教科ごとの累計学習時間を取得
        subject_data = (
            db.session.query(
                StudyRecord.subject,
                func.sum(StudyRecord.study_time).label("total_time")
            )
            .filter(StudyRecord.user_id == user_id)
            .group_by(StudyRecord.subject)
            .all()
        )

        # デフォルトで全ての科目を 0 に初期化
        subject_dict = {subject: 0 for subject in subjects}

        # 実際のデータを反映
        for record in subject_data:
            subject_dict[record.subject] = record.total_time or 0  # None 対応

        # JSON形式で返す
        return jsonify([
            {
                "subject": subject,
                "total_time": subject_dict[subject]
            }
            for subject in subjects
        ])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 📌 4. 学習履歴をカレンダー表示用に取得
@api.route("/stats/calendar/<int:user_id>", methods=["GET"])
def get_calendar_stats(user_id):
    try:
        # すべての学習記録を取得
        records = db.session.query(
            StudyRecord.id.label("record_id"),
            StudyRecord.subject,
            StudyRecord.record_date,
            StudyRecord.study_time
        ).filter(StudyRecord.user_id == user_id).all()

        # 学習記録（青色、科目ごとに分類）
        record_events = [
            {
                "title": f"{record.subject} {record.study_time} 分",
                "start": record.record_date.strftime("%Y-%m-%d"),
                "color": "blue",
                "record_id": record.record_id
            }
            for record in records
        ]

        # すべての学習計画を取得
        plans = db.session.query(
            StudyPlan.id.label("plan_id"),
            StudyPlan.subject,
            StudyPlan.weekly_schedule
        ).filter(StudyPlan.user_id == user_id).all()

        # 学習計画（赤色）
        plan_events = []
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())  # 月曜日

        for plan in plans:
            for day, minutes in plan.weekly_schedule.items():
                if minutes > 0:
                    event_date = start_of_week + timedelta(days=weekdays.index(day))
                    plan_events.append({
                        "title": f"{plan.subject} (予定 {minutes} 分)",
                        "start": event_date.strftime("%Y-%m-%d"),
                        "color": "red",
                        "plan_id": plan.plan_id
                    })

        return jsonify(record_events + plan_events)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


from flask import render_template
