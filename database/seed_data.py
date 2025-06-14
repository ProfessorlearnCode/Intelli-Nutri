import os
import csv
import sqlite3

# 📂 Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, 'recipes.csv')
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
                    INSERT INTO recipes (recipe_name,
                                        recipe_link,
                                        recipe_description,
                                        recipe_cooktime,
                                        recipe_ingredients,
                                        recipe_steps,
                                        recipe_course_type,
                                        recipe_difficulty,
                                        recipe_flavor_profile,
                                        recipe_tags,
                                        recipe_diet_type) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        
    """, (
        row['name'],
        row['link'],
        row['description'],
        int(row['cooktime']) if row['cooktime'].isdigit() else 0,
        row['ingredients'],
        row['recipe_steps'],
        row['course_type'],
        row['difficulty'],
        row['flavor_profile'],
        row['tags'],
        row['diet_type']
    ))

conn.commit()
conn.close()

print("✅ Recipes inserted into app.db successfully.")
