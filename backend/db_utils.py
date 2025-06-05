import sqlite3, json
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'schema', 'app.db'))

def build_connection():
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = sqlite3.Row
        return 1, con
    except:
        return 0, None

def save_user_prefs(preferences: dict):
    status, connect_obj = build_connection()
    if status == 1:
        placeholders = (
            preferences.get('name'),
            preferences.get('age'),
            preferences.get('dietary_preference'),
            preferences.get('health_conditions'),
            preferences.get('likes'),
            preferences.get('dislikes'),
            preferences.get('allergies')
        )

        query = '''INSERT INTO user_preferences 
                   (name, age, dietary_preference, health_conditions, likes, dislikes, allergies) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        connect_obj.execute(query, placeholders)
        connect_obj.commit()
        connect_obj.close()
    else:
        print("[ERROR 🔴] Error occurred while connecting to the DB for inserting user preferences.")

def fetch_user_prefs(user_id):
    status, connect_obj = build_connection()
    if status == 1:
        query = 'SELECT * FROM user_preferences WHERE id = ?'
        rows = connect_obj.execute(query, (user_id,)).fetchall()
        connect_obj.close()
        return [dict(row) for row in rows]
    else:
        print("[ERROR 🔴] Error occurred while connecting to the DB for fetching user preferences.")
        return []

def fetch_recipes_by_id(ids):
    status, connect_obj = build_connection()
    if status == 1:
        placeholders = ','.join('?' * len(ids))
        query = f"SELECT * FROM recipes WHERE recipeid IN ({placeholders})"
        rows = connect_obj.execute(query, ids).fetchall()
        connect_obj.close()
        return [dict(row) for row in rows]
    else:
        print("[ERROR 🔴] Error occurred while connecting to the DB for fetching recipes by ID.")
        return []

def fetch_tables():
    status, connect_obj = build_connection()
    if status == 1:
        placeholder = 'table'
        query = "SELECT name FROM sqlite_master WHERE type=?"
        cursor = connect_obj.execute(query, (placeholder,))
        tables = cursor.fetchall()
        connect_obj.close()
        return [table[0] for table in tables]
    else:
        print("[ERROR 🔴] Error occurred while connecting to the DB for fetching tables.")
        return []
