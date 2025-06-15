import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from db_utils import fetch_recipes_for_indexing

# === File Paths ===
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INDEX_PATH = os.path.join(BASE_DIR, 'faissIndex', 'recipe_index.faiss')
ID_PATH = os.path.join(BASE_DIR, 'faissIndex', 'id_map.txt')
META_PATH = os.path.join(BASE_DIR, 'faissIndex', 'recipe_metadata.json')
GLOSSARY_PATH = os.path.join(BASE_DIR, 'glossary.json')

# === Globals for Reuse ===
MATCHABLE_FIELDS = {
    "diet_type": "recipe_diet_type",
    "flavor": "recipe_flavor_profile",
    "course": "recipe_course_type",
    "difficulty": "recipe_difficulty",
    "tags": "recipe_tags"
}
_model = None
_faiss_index = None
_id_map = None
_metadata = None
_glossary = None

# === Singleton Loaders ===
def get_glossary():
    global _glossary
    if _glossary is None:
        try:
            with open(GLOSSARY_PATH, "r") as f:
                _glossary = json.load(f)
        except FileNotFoundError:
            _glossary = {}
    return _glossary

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def get_index():
    global _faiss_index
    if _faiss_index is None:
        _faiss_index = faiss.read_index(INDEX_PATH)
    return _faiss_index

def get_id_map():
    global _id_map
    if _id_map is None:
        with open(ID_PATH, 'r') as f:
            _id_map = json.load(f)
    return _id_map

def get_metadata():
    global _metadata
    if _metadata is None:
        with open(META_PATH, 'r') as f:
            _metadata = json.load(f)
    return _metadata

# === Preprocessing Functions ===
def expand_query_with_glossary(query: str) -> str:
    try:
        glossary = get_glossary()
        words = query.lower().split()
        expanded = []

        for word in words:
            expanded.append(word)
            if word in glossary:
                expanded.extend(glossary[word])

        return " ".join(expanded)
    except Exception:
        print("[ERROR 🔴] Error occurred while expanding query with glossary.")

def embed_text_from_recipe(recipe: dict) -> str:
    try:
        tags = recipe.get('recipe_tags', '')
        if isinstance(tags, list):
            tags = " ".join(tags)
            
        parts = [
            recipe.get('recipe_name', ''),
            recipe.get('recipe_description', ''),
            recipe.get('recipe_ingredients', ''),
            recipe.get('recipe_steps', ''),
            recipe.get('recipe_cooktime', ''),
            recipe.get('recipe_course_type', ''),
            recipe.get('recipe_difficulty', ''),
            recipe.get('recipe_flavor_profile', ''),
            tags,
            recipe.get('recipe_diet_type', '')
        ]
        return " | ".join([str(p) for p in parts if p])  # remove empty/null values
    except Exception as E:
        print("[ERROR 🔴] Error occurred while embeding text from recipe.")
    
def dynamic_filter(results, query):
    try:
        query_words = query.lower().split()
        filtered = []

        for recipe in results:
            matched = False

            # Match query words against known fields
            for field in MATCHABLE_FIELDS.values():
                field_value = str(recipe.get(field, "")).lower()
                if any(qword in field_value for qword in query_words):
                    matched = True
                    break

            # Check against tags list if present
            tags = recipe.get("recipe_tags", "")
            if isinstance(tags, list):
                tags_text = " ".join(tags).lower()
            else:
                tags_text = str(tags).lower()

            if any(qword in tags_text for qword in query_words):
                matched = True

            if matched:
                filtered.append(recipe)

        return filtered if filtered else results
    except Exception as E:
        print("[ERROR 🔴] Error occurred while applying dynamic filter.")        

# === FAISS Index Builder ===
def build_index():
    try:
        recipes = fetch_recipes_for_indexing()
        model = get_model()

        # Prepare texts and IDs in bulk
        texts = [embed_text_from_recipe(r) for r in recipes]
        IDs = [r['recipe_id'] for r in recipes]
        metadata = recipes  # full object already in list

        # Batch encode all at once
        vectors = model.encode(texts, batch_size=64, show_progress_bar=True)
        vectors = np.array(vectors).astype("float32")

        # Normalize and build FAISS index
        faiss.normalize_L2(vectors)
        index = faiss.IndexFlatIP(vectors.shape[1])
        index.add(vectors)

        # Ensure output directory
        os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)

        # Save index and metadata
        faiss.write_index(index, INDEX_PATH)
        with open(ID_PATH, "w") as f:
            json.dump(IDs, f)
        with open(META_PATH, "w") as f:
            json.dump(metadata, f)

        print("[✅] FAISS index built and saved.")
    except Exception as E:
        print(f"[ERROR 🔴] Error occurred while building index: {E}")

# === Similarity Search ===
def similar_search(query, k=5):
    try:
        model = get_model()
        index = get_index()
        ids = get_id_map()
        metadata = get_metadata()

        expanded_query = expand_query_with_glossary(query)
        query_vec = model.encode([expanded_query]).astype("float32")
        faiss.normalize_L2(query_vec)

        scores, result_indices = index.search(query_vec, k * 3)
        result_ids = [ids[i] for i in result_indices[0]]

        id_to_meta = {r['recipe_id']: r for r in metadata}
        results = [id_to_meta.get(rid, {}) for rid in result_ids]

        results = dynamic_filter(results, query)
        return results[:k]
    except Exception as E:
        print("[ERROR 🔴] Error occurred while performing similarity search.")    

# === Manual Test Block ===
# if __name__ == "__main__":
#     # build_index()

#     print("\n🔎 Testing Search:")
    
#     query = "Easy non-vegetarian recipes"
#     results = similar_search(query, 5)
#     print(results)
    # for i, recipe in enumerate(results, 1):
    #     print(f"\n#{i}: {recipe['recipe_name']}")
    #     print(f"    cooktime: {recipe['recipe_cooktime']}")
    #     print(f"    course: {recipe['recipe_course_type']}")
    #     print(f"    difficulty: {recipe['recipe_difficulty']}")
    #     print(f"    flavours: {recipe['recipe_flavor_profile']}")
    #     print(f"    Diet: {recipe['recipe_diet_type']}")

