import sqlite3
import os
from datetime import datetime


class TodoDatabase:
    def __init__(self, db_path="todos.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """データベースとテーブルを初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # todosテーブルを作成
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    def get_connection(self):
        """データベース接続を取得"""
        return sqlite3.connect(self.db_path)

    def create_todo(self, title, description=""):
        """新しいtodoを作成"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO todos (title, description, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        """,
            (title, description, datetime.now(), datetime.now()),
        )

        todo_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return todo_id

    def get_all_todos(self):
        """すべてのtodoを取得"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, title, description, completed, created_at, updated_at
            FROM todos
            ORDER BY created_at DESC
        """
        )

        todos = cursor.fetchall()
        conn.close()

        return todos

    def get_todo_by_id(self, todo_id):
        """IDでtodoを取得"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, title, description, completed, created_at, updated_at
            FROM todos
            WHERE id = ?
        """,
            (todo_id,),
        )

        todo = cursor.fetchone()
        conn.close()

        return todo

    def update_todo(self, todo_id, title=None, description=None, completed=None):
        """todoを更新"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 更新するフィールドを動的に構築
        updates = []
        params = []

        if title is not None:
            updates.append("title = ?")
            params.append(title)

        if description is not None:
            updates.append("description = ?")
            params.append(description)

        if completed is not None:
            updates.append("completed = ?")
            params.append(completed)

        if updates:
            updates.append("updated_at = ?")
            params.append(datetime.now())
            params.append(todo_id)

            query = f"UPDATE todos SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)

        conn.commit()
        conn.close()

        return cursor.rowcount > 0

    def delete_todo(self, todo_id):
        """todoを削除"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))

        conn.commit()
        conn.close()

        return cursor.rowcount > 0

    def toggle_todo(self, todo_id):
        """todoの完了状態を切り替え"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE todos 
            SET completed = NOT completed, updated_at = ?
            WHERE id = ?
        """,
            (datetime.now(), todo_id),
        )

        conn.commit()
        conn.close()

        return cursor.rowcount > 0
