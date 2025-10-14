from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import TodoDatabase
import os

app = Flask(__name__)
app.secret_key = (
    "your-secret-key-here"  # セキュリティのため実際の運用では変更してください
)

# データベースインスタンスを作成
db = TodoDatabase()


@app.route("/")
def index():
    """メインページ - すべてのtodoを表示"""
    todos = db.get_all_todos()
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add_todo():
    """新しいtodoを追加"""
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not title:
        flash("タイトルは必須です", "error")
        return redirect(url_for("index"))

    try:
        todo_id = db.create_todo(title, description)
        flash("Todoが正常に追加されました", "success")
    except Exception as e:
        flash(f"エラーが発生しました: {str(e)}", "error")

    return redirect(url_for("index"))


@app.route("/toggle/<int:todo_id>")
def toggle_todo(todo_id):
    """todoの完了状態を切り替え"""
    try:
        success = db.toggle_todo(todo_id)
        if success:
            flash("Todoの状態が更新されました", "success")
        else:
            flash("Todoが見つかりません", "error")
    except Exception as e:
        flash(f"エラーが発生しました: {str(e)}", "error")

    return redirect(url_for("index"))


@app.route("/edit/<int:todo_id>")
def edit_todo(todo_id):
    """todo編集ページを表示"""
    todo = db.get_todo_by_id(todo_id)
    if not todo:
        flash("Todoが見つかりません", "error")
        return redirect(url_for("index"))

    return render_template("edit.html", todo=todo)


@app.route("/update/<int:todo_id>", methods=["POST"])
def update_todo(todo_id):
    """todoを更新"""
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not title:
        flash("タイトルは必須です", "error")
        return redirect(url_for("edit_todo", todo_id=todo_id))

    try:
        success = db.update_todo(todo_id, title=title, description=description)
        if success:
            flash("Todoが正常に更新されました", "success")
            return redirect(url_for("index"))
        else:
            flash("Todoが見つかりません", "error")
    except Exception as e:
        flash(f"エラーが発生しました: {str(e)}", "error")

    return redirect(url_for("edit_todo", todo_id=todo_id))


@app.route("/delete/<int:todo_id>")
def delete_todo(todo_id):
    """todoを削除"""
    try:
        success = db.delete_todo(todo_id)
        if success:
            flash("Todoが正常に削除されました", "success")
        else:
            flash("Todoが見つかりません", "error")
    except Exception as e:
        flash(f"エラーが発生しました: {str(e)}", "error")

    return redirect(url_for("index"))


@app.route("/api/todos")
def api_todos():
    """API: すべてのtodoをJSONで返す"""
    todos = db.get_all_todos()
    todo_list = []

    for todo in todos:
        todo_dict = {
            "id": todo[0],
            "title": todo[1],
            "description": todo[2],
            "completed": bool(todo[3]),
            "created_at": todo[4],
            "updated_at": todo[5],
        }
        todo_list.append(todo_dict)

    return jsonify(todo_list)


if __name__ == "__main__":
    # templatesフォルダが存在しない場合は作成
    if not os.path.exists("templates"):
        os.makedirs("templates")

    # staticフォルダが存在しない場合は作成
    if not os.path.exists("static"):
        os.makedirs("static")

    app.run(debug=True, host="0.0.0.0", port=5000)
