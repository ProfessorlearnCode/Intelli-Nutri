"""
seed_data.py - Load Recipes into the Database

- Load recipes from Kaggle dataset / Spoonacular API / custom CSV
- Populate the recipes table in SQLite
- Optionally, embed recipes and build FAISS index in vector_utils

Run this after `init_db.py` is complete.
"""


#Recipes.cs

import os
import csv
import sqlite3

# 📂 Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, 'Recipes.csv')
db_path = os.path.join(base_dir, 'schema', 'app.db')

# 📥 Read CSV using csv module
with open(csv_path, mode='r', encoding='latin1') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]

# 🔗 Insert into SQLite DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

for row in data:
    cursor.execute("""
        INSERT INTO recipes (recipename, ingredients, description, diet_type, recipe_steps, totaltime)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        row['recipename'],
        row['ingredients'],
        row['description'],
        row['diet_type'],
        row['recipe_steps'],
        int(row['totaltime']) if row['totaltime'].isdigit() else 0  # handles non-numeric values safely
    ))

conn.commit()
conn.close()

print("✅ Recipes inserted into app.db successfully.")
