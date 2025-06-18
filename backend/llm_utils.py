# llm_utils.py

import os
from typing import List, Dict
from dotenv import load_dotenv
from google import genai
from google.genai import types
import timeit

load_dotenv()
client = genai.Client(api_key=os.getenv("API_KEY"))

# ----------------------------------------
# Static: Full system prompt to inject ONCE per session
# ----------------------------------------
GENERAL_PROMPT = """
You are a seasoned Pakistani chef with decades of experience in cooking and nutrition, known for your deep understanding of Pakistani cuisine and culture. Your tone is steady, firm, friendly, trustworthy, and helpful. You will assist users by providing tailored recipe recommendations, meal plans, nutritional advice, and ingredient substitutions based on their preferences.

Context Instructions:
1. The user preferences will be provided to you, including dietary restrictions, favorite ingredients, or specific cuisines they enjoy.
2. You will receive a list of up to 3 similarly searched recipes with additional information to help you provide contextually relevant advice.
3. Always prioritize discussing recipes, meal planning, nutrition, and cooking techniques. Do not engage in topics unrelated to food or cooking.

Response Guidelines:
- Begin by acknowledging the user's preferences and the provided recipe context.
- Recommend recipes or meal plans that align with the user's preferences, explaining why each choice is suitable.
- Offer ingredient substitutions when necessary, using your expertise to suggest alternatives that maintain the dish's integrity.
- Provide cooking tips and nutritional information relevant to the recipes discussed.
- Maintain clarity and simplicity in your explanations, utilizing Roman Urdu where it enhances understanding (e.g., "yeh recipe bohot asan hai" or "aap isme ye cheezein daal sakte hain").

Stay focused on the culinary realm, ensuring your responses are informative and directly related to the user's food and cooking inquiries.

Keep responses short and conversational — ideally one or two sentences. Focus on directly answering the user's query with practical suggestions.
"""

# ----------------------------------------
# Builds structured Gemini prompt messages
# ----------------------------------------
def build_user_prompt(
    user_query: str,
    user_preferences: Dict[str, str],
    similar_recipes: List[Dict],
    chat_history: List[Dict[str, str]],
    include_general_prompt: bool
) -> List[types.Content]:

    messages: List[types.Content] = []

    # One-time system prompt injection per session
    if include_general_prompt:
        messages.append(types.Content(
            role="user",
            parts=[types.Part(text=GENERAL_PROMPT)]
        ))

    # Step 1: User Preferences
    pref_text = "\n".join([f"- {k}: {v}" for k, v in user_preferences.items()])
    preference_block = f"User Preferences:\n{pref_text}"

    # Step 2: Similar Recipes (contextual relevance)
    recipe_block = ""
    if similar_recipes:
        recipe_lines = []
        for i, recipe in enumerate(similar_recipes[:3], 1):
            title = recipe.get('title', 'Unknown')
            desc = recipe.get('description', 'No description')
            ingredients = ", ".join(recipe.get('ingredients', []))
            recipe_lines.append(f"{i}. {title} – {desc} (Ingredients: {ingredients})")
        recipe_block = "Similar Recipes:\n" + "\n".join(recipe_lines)

    # Step 3: Current Query with Injected Context
    context_blocks = [preference_block]
    if similar_recipes:
        context_blocks.append(recipe_block)

    context = "\n\n".join(context_blocks) + f"\n\nUser Query:\n{user_query.strip()}"

    # Step 4: Add chat history (last 5)
    for turn in chat_history[-5:]:
        messages.append(types.Content(
            role=turn['role'],
            parts=[types.Part(text=turn['content'])]
        ))

    # Step 5: Add the current contextualized query
    messages.append(types.Content(
        role="user",
        parts=[types.Part(text=context.strip())]
    ))

    return messages

# ----------------------------------------
# Wraps Gemini API Call
# ----------------------------------------
def get_gemini_response(
    prompt_messages: List[types.Content],
    model_id: str,
) -> str:
    try:
        # Method 1: Try without config first
        response = client.models.generate_content(
            model=model_id,
            contents=prompt_messages
        )
        return response.text.strip()
    except Exception as e:
        print(f"Method 1 failed: {e}")
        
        try:
            # Method 2: Try with minimal config
            config = types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=500  # Increased from 100
            )
            
            response = client.models.generate_content(
                model=model_id,
                contents=prompt_messages,
                config=config
            )
            return response.text.strip()
        except Exception as e2:
            print(f"Method 2 failed: {e2}")
            
            try:
                # Method 3: Try with different parameter structure
                response = client.models.generate_content(
                    model=model_id,
                    contents=prompt_messages,
                    generation_config={
                        "temperature": 0.7,
                        "max_output_tokens": 500
                    }
                )
                return response.text.strip()
            except Exception as e3:
                raise Exception(f"All methods failed. Last error: {e3}")


# if __name__ == "__main__":
#     # Mocked User Preferences
#     user_preferences = {
#         "Diet": "Vegetarian",
#         "Avoids": "Onions",
#         "Likes": "Chickpeas, Potatoes"
#     }

#     # Mocked Similar Recipes
#     similar_recipes = [
#         {
#             "title": "Aloo Chana Chaat",
#             "description": "A tangy and spicy chickpea-potato salad",
#             "ingredients": ["Chickpeas", "Potatoes", "Spices"]
#         },
#         {
#             "title": "Tandoori Aloo",
#             "description": "Smoky grilled potatoes marinated in yogurt and spices",
#             "ingredients": ["Potatoes", "Yogurt", "Red Chili Powder"]
#         }
#     ]

#     # Initial User Query
#     user_query = "I want a quick lunch idea"

#     # Empty chat history for first interaction
#     chat_history = []

#     # Flag to include system prompt (only once per session)
#     include_general_prompt = True

#     # Build messages
#     prompt_messages = build_user_prompt(
#         user_query=user_query,
#         user_preferences=user_preferences,
#         similar_recipes=similar_recipes,
#         chat_history=chat_history,
#         include_general_prompt=include_general_prompt
#     )

#     # Try different model names (use the correct one for your setup)
#     possible_models = [
#         "gemini-2.0-flash-exp",
#         "gemini-1.5-flash",
#         "gemini-1.5-pro",
#         "Gemini-2.5-Flash"  # Your original
#     ]
    
#     response = None
#     for model_id in possible_models:
#         try:
#             print(f"🔍 Trying model: {model_id}")
#             timeit.default_timer()
#             response = get_gemini_response(prompt_messages, model_id)
#             print(f"✅ Success with model: {model_id}")
#             break
#         except Exception as e:
#             print(f"❌ Failed with {model_id}: {str(e)[:100]}...")
#             continue
    
#     if response:
#         print("\n🧠 Chatbot Response:\n")
#         print(response)

#         # Simulate a follow-up question with memory
#         follow_up_query = "What should I eat for dinner then?"
#         updated_chat = chat_history + [
#             {"role": "user", "content": user_query},
#             {"role": "model", "content": response}
#         ]

#         follow_up_messages = build_user_prompt(
#             user_query=follow_up_query,
#             user_preferences=user_preferences,
#             similar_recipes=[],  # You can fetch new ones if needed
#             chat_history=updated_chat,
#             include_general_prompt=False  # Already added earlier
#         )

#         try:
#             follow_up_response = get_gemini_response(follow_up_messages, model_id)
#             print("\n💬 Follow-up Response:\n")
#             print(follow_up_response)
#         except Exception as e:
#             print(f"Follow-up failed: {e}")
#     else:
#         print("❌ All models failed. Please check your API key and model availability.")