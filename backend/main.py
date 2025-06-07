"""
main.py - Flask App Entry Point

Define all main routes here:
- /save_preferences (POST): Accepts user dietary data
- /get_recipes (POSTGET): Returns recipes based on user prefs or search query
- /chat (POST): Receives chat input and returns response from AI

Other files like llm_utils.py or db_utils.py will be imported and used here.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import db_utils as d

app = Flask(__name__)
CORS(app)

@app.route("/")
def server_health():
    return "Backend is on 💯"

@app.route("/save_preferences", methods=["POST"])
def save_preferences():
    try:
        fetch = request.get_json()
        preferences = fetch.get("preferences")
        if not preferences:
            return jsonify({"status" : 0,
                            "message": "[🔴 ERROR] Error Occured while fetching the preferences - Client side"}), 400
            
        d.save_user_prefs(preferences=preferences)
        return jsonify({"status" : 1}), 200
    except Exception as e:
        return jsonify({"status" : 0,
                "message": "[🔴 ERROR] Error Occured while fetching and saving the preferences - Server side"}), 500



if __name__ == "__main__":
    app.run(debug=True, port=5000)