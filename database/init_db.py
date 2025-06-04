"""
init_db.py - Initialize SQLite Database

- Connects to SQLite
- Runs schema.sql to create necessary tables
- Run this ONCE before using the app
"""

# 📁 FILE: database/init_db.py
# Purpose: Initialize the SQLite database with users and recipes tables

import sqlite3
import os

# Step 1: Get current directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Step 2: Build full path to the database inside a 'schema' folder
schema_folder = os.path.join(base_dir, 'schema')
db_file = os.path.join(schema_folder, 'app.db')

# Step 3: Create 'schema' folder if it doesn't exist
if not os.path.exists(schema_folder):
    os.makedirs(schema_folder)

# Step 4: Connect to the SQLite database (will auto-create app.db)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Step 5: Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    dietary_preference TEXT,
    health_conditions TEXT,
    likes TEXT,
    dislikes TEXT,
    allergies TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS recipes (
    recipeid INTEGER PRIMARY KEY,
    recipename TEXT,
    ingredients TEXT,
    description TEXT,
    diet_type TEXT,
    recipe_steps TEXT,
    totaltime INTEGER
)
''')

# Step 6: Save changes and close
conn.commit()
conn.close()

print("✅ Tables created successfully in schema/app.db")
