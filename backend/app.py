"""
main.py - Flask App Entry Point

Define all main routes here:
- /save_preferences (POST): Accepts user dietary data
- /recipes_load (POSTGET): Returns recipes based on user prefs or search query
- /chat (POST): Receives chat input and returns response from AI

Other files like llm_utils.py or db_utils.py will be imported and used here.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import db_utils as d
import vector_utils as v

app = Flask(__name__)
CORS(app, origins="https://laughing-space-waddle-4j7wgxr5rvpwcg55-5500.app.github.dev")

@app.route("/")
def server_health():
    return "Backend is on 💯"

@app.route("/save_preferences", methods=["POST"])
def save_preferences():
    try:
        fetch = request.get_json()
        print("Received JSON:", fetch)

        preferences = fetch.get("preferences")
        if not preferences:
            return jsonify({"status" : 0,
                            "message": "[🔴 ERROR] No preferences received"}), 400
            
        d.save_user_prefs(preferences=preferences)
        print("[🟢 SUCCESS] preferences saved to the database")
        
        return jsonify({"status" : 1}), 200
    except Exception as e:
        print("Server error:", str(e)) 
        return jsonify({"status" : 0,
                "message": "[🔴 ERROR] Exception during preferences saving"}), 500

@app.route("/recipes_load")
def recipes_load():
    try:
        recipes = d.fetch_recipes_for_indexing()
        print("[🟢 SUCCESS] Recipes fetched from the database")
        
        # Return the plain list
        return jsonify(recipes), 200
    except Exception as e:
        print("Server error:", str(e)) 
        return jsonify({
            "status": 0,
            "message": "[🔴 ERROR] Exception during recipe loading"
        }), 500

@app.route("/smart_search", methods=["POST"])
def similarity_search():
    try:
        data = request.get_json()
        query = data.get("query", "")
        print("Received query:", query)

        results = v.similar_search(query, 4)
        return jsonify({"status": 1, "recipes": results}), 200
        
    except Exception as e:
        print("Server error:", str(e)) 
        return jsonify({"status" : 0,
                "message": f"[🔴 ERROR] Exception during preferences saving {e}"}), 500

@app.route("/chat", methods=["POST", "GET"])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    user = data.get('user', 'User')

    if not user_message:
        return jsonify({'reply': '⚠️ Please send a valid message.'}), 400

    # For now, just echo back the message
    reply = f"👨‍🍳 Hi {user}, you said: '{user_message}'"
    
    return jsonify({'reply': reply})


if __name__ == "__main__":
    app.run(debug=True, port=5000)