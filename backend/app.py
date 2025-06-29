
from flask import Flask, request, jsonify
from flask_cors import CORS
import db_utils as d
import vector_utils as v
import llm_utils as l

app = Flask(__name__)
CORS(app)

client = l.client
SELECTED_MODEL_ID = "gemini-2.0-flash-exp"
USER_ID = ""

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
    if not client:
        return jsonify({'reply': 'AI service is not initialized on the server.'}), 503

    data = request.get_json()
    user_message = data.get('message', '').strip()
    print(user_message)
    user_id = d.fetch_user_id()
    user_id_value = user_id.get('id')  # returns 18
    
    chat_history = data.get('chat_history', []) # Frontend sends current session history

    if not user_message:
        return jsonify({'reply': '⚠️ Please send a valid message.'}), 400
    if not user_id_value:
        return jsonify({'reply': '⚠️ User ID is required.'}), 400

    try:
        # 1. Fetch user preferences
        # Assuming fetch_user_prefs returns a list of dicts, take the first one
        user_preferences_list = d.fetch_user_prefs(user_id_value)
        user_preferences = user_preferences_list[0] if user_preferences_list else {}
        # 2. Get similar recipes
        similar_recipes = v.similar_search(user_message)

        # 3. Build the prompt messages for the LLM
        prompt_messages = l.build_user_prompt(
            user_query=user_message,
            user_preferences=user_preferences,
            similar_recipes=similar_recipes,
            chat_history=chat_history,
            include_general_prompt=True # Or manage based on session if it's the first message
        )

        # 4. Get response from Gemini
        ai_reply = l.get_gemini_response(
            prompt_messages=prompt_messages,
            model_id=SELECTED_MODEL_ID
        )

        return jsonify({'reply': ai_reply}), 200

    except Exception as e:
        # Log the error for debugging
        print(f"An unexpected error occurred in /chat: {e}")
        return jsonify({'reply': f'An internal server error occurred: {e}'}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
