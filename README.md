
### **📌 README.md**
```markdown
# 📚 学習管理アプリ

## 📖 概要
このアプリは、学習計画の作成・記録・可視化を行う 学習管理アプリ です。  
ユーザーは以下の機能を利用できます。

- 学習計画の登録：曜日ごとに学習予定を設定
- 学習記録の入力：日付ごとに学習時間を記録
- メモ機能：学習内容を記録し、後から参照可能
- カレンダー表示：学習計画・記録・メモをカレンダーに可視化
- 統計機能：
  - 週間学習時間の棒グラフ
  - 教科ごとの達成率（円グラフ）
  - 学習割合の円グラフ

---

## ⚙️ セットアップ手順

### 1️⃣ 環境の準備
本アプリは Python（Flask） と PostgreSQL を使用します。  
以下のツールをインストールしてください。

- Python 3.x
- PostgreSQL
- `venv`（仮想環境）

### 2️⃣ 仮想環境の作成と依存パッケージのインストール
```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

# 必要なパッケージをインストール
pip install -r requirements.txt
```

### **3️⃣ データベースのセットアップ**
```bash
# PostgreSQL に接続してデータベースを作成
psql -U <your_username>
CREATE DATABASE study_management;

# .env にデータベースURLを設定（例）
DATABASE_URL=postgresql://<your_username>:<your_password>@localhost/study_management

# マイグレーションの実行
flask db upgrade
```

### **4️⃣ アプリの起動**
```bash
flask run
```
ブラウザで **`http://127.0.0.1:5000/dashboard`** にアクセス。

---

## 🛠️ 機能一覧

### **📅 1. 学習計画**
- 学習予定を **曜日ごと** に登録
- **カレンダー（赤色）** に表示
- 予定を削除可能

### **📝 2. 学習記録**
- 日ごとの学習時間を記録
- **カレンダー（青色）** に表示
- 週間学習時間の棒グラフを表示
- 記録を削除可能

### **🗒️ 3. メモ機能**
- **日付ごとにメモを作成**
- クリックでメモの内容を確認
- 削除可能

### **📊 4. 統計機能**
- **週間学習時間（棒グラフ）**
- **教科ごとの達成率（円グラフ）**
- **学習割合（円グラフ）**
- カレンダーと連携

---

## 📡 API エンドポイント一覧

| HTTPメソッド | エンドポイント | 説明 |
|-------------|--------------|------|
| **POST** | `/api/study_plans` | 学習計画を登録 |
| **GET** | `/api/study_plans/<user_id>` | 学習計画を取得 |
| **PUT** | `/api/study_plans/<plan_id>` | 学習計画を更新 |
| **DELETE** | `/api/study_plans/<plan_id>` | 学習計画を削除 |
| **POST** | `/api/study_records` | 学習記録を登録 |
| **GET** | `/api/study_records/<user_id>` | 学習記録を取得 |
| **DELETE** | `/api/study_records/<record_id>` | 学習記録を削除 |
| **POST** | `/api/study_notes` | メモを登録 |
| **GET** | `/api/study_notes/<user_id>` | メモを取得 |
| **DELETE** | `/api/study_notes/<note_id>` | メモを削除 |
| **POST** | `/api/review_list` | 復習リストに追加 |
| **GET** | `/api/review_list/<user_id>` | 復習リストを取得 |
| **DELETE** | `/api/review_list/<review_id>` | 復習リストを削除 |
| **GET** | `/api/stats/weekly/<user_id>` | 週間学習時間を取得 |
| **GET** | `/api/stats/progress/<user_id>` | 教科ごとの達成率を取得 |
| **GET** | `/api/stats/subject_distribution/<user_id>` | 教科ごとの学習割合を取得 |
| **GET** | `/api/stats/calendar/<user_id>` | カレンダー表示用データを取得 |

---

## 🏗️ 開発について
### **🛠️ 使用技術**
- **バックエンド**: Flask, SQLAlchemy, PostgreSQL
- **フロントエンド**: HTML, CSS, JavaScript
- **ライブラリ**
  - `FullCalendar.js`（カレンダー表示）
  - `Chart.js`（グラフ表示）

### **🔧 改善・追加したい機能**
- 🔹 **ログイン機能**：ユーザーごとのデータ管理を強化
- 🔹 **リマインダー通知**：計画の通知機能を追加
- 🔹 **学習時間の分析**：より詳細な統計情報を提供

