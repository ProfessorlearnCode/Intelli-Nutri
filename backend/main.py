"""
main.py - Flask App Entry Point

Define all main routes here:
- /save_preferences (POST): Accepts user dietary data
- /get_recipes (POSTGET): Returns recipes based on user prefs or search query
- /chat (POST): Receives chat input and returns response from AI

Other files like llm_utils.py or db_utils.py will be imported and used here.
"""

from flask import Flask


app = Flask(__name__)

@app.route("/")
def server_health():
    return "Backend is on 💯"



if __name__ == "__main__":
    app.run(debug=True, port=5000)