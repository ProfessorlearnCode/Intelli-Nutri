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
            preferences.get('diet'),
            preferences.get('disease'),
            preferences.get('likes'),
            preferences.get('dislikes'),
            preferences.get('avoid')
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
    
def fetch_user_id():
    status, connect_obj = build_connection()
    if status == 1:
        query = 'SELECT MAX(Id) AS id FROM user_preferences'
        row = connect_obj.execute(query).fetchone()
        connect_obj.close()

        return dict(row)  # Now returns {'id': 18}
    else:
        print("[ERROR 🔴] Error occurred while connecting to the DB for fetching user preferences.")
        return {}


def fetch_recipes_by_id(ids):
    status, connect_obj = build_connection()
    if status == 1:
        placeholders = ','.join('?' * len(ids))
        query = f"SELECT * FROM recipes WHERE recipe_id IN ({placeholders})"
        rows = connect_obj.execute(query, ids).fetchall()
        connect_obj.close()
        return [dict(row) for row in rows]
    else:
        print("[ERROR 🔴] Error occurred while connecting to the DB for fetching recipes by ID.")
        return []

def fetch_recipes_for_indexing():
    status, connect_obj = build_connection()
    if status:
        query = f'''SELECT recipe_id,
                            recipe_name,
                            recipe_link,
                            recipe_description,
                            recipe_cooktime,
                            recipe_ingredients,
                            recipe_steps,
                            recipe_course_type,
                            recipe_difficulty,
                            recipe_flavor_profile,
                            recipe_tags,
                            recipe_diet_type
                    FROM recipes'''
        rows = connect_obj.execute(query).fetchall()
        connect_obj.close()
        return [dict(row) for row in rows]
    else:
        print("[ERROR 🔴] Error occurred while connecting to the DB for fetching recipes for indexing.")
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

if __name__ == "__main__":
    pref_context = fetch_user_prefs(17)[0]
    print(pref_context)