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
_model = None
_faiss_index = None
_id_map = None
_metadata = None

# === Singleton Loaders ===
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
        with open(GLOSSARY_PATH, "r") as f:
            glossary = json.load(f)
    except FileNotFoundError:
        return query  # Skip if glossary doesn't exist

    words = query.lower().split()
    expanded = []

    for word in words:
        expanded.append(word)
        if word in glossary:
            expanded.extend(glossary[word])

    return " ".join(expanded)

def embed_text_from_recipe(recipe: dict) -> str:
    parts = [
        recipe.get('recipe_name', ''),
        recipe.get('recipe_description', ''),
        recipe.get('recipe_ingredients', ''),
        recipe.get('recipe_steps', ''),
        recipe.get('recipe_cooktime', ''),
        recipe.get('recipe_course_type', ''),
        recipe.get('recipe_difficulty', ''),
        recipe.get('recipe_flavor_profile', ''),
        recipe.get('recipe_tags', ''),
        recipe.get('recipe_diet_type', '')
    ]
    return " | ".join([str(p) for p in parts if p])  # remove empty/null values

# === FAISS Index Builder ===
def build_index():
    recipes = fetch_recipes_for_indexing()
    IDs, VECs, metadata = [], [], []

    model = get_model()

    for recipe in recipes:
        text = embed_text_from_recipe(recipe)
        vector = model.encode(text)
        VECs.append(vector)
        IDs.append(recipe['recipe_id'])
        metadata.append(recipe)  # store full object for lookup

    # Normalize and build FAISS index
    VECs = np.array(VECs).astype("float32")
    faiss.normalize_L2(VECs)
    index = faiss.IndexFlatIP(VECs.shape[1])
    index.add(VECs)

    # Ensure directory
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)

    # Save index and metadata
    faiss.write_index(index, INDEX_PATH)
    with open(ID_PATH, "w") as f:
        json.dump(IDs, f)
    with open(META_PATH, "w") as f:
        json.dump(metadata, f)

    print("[✅] FAISS index built and saved.")

# === Similarity Search ===
def similar_search(query, k=5):
    model = get_model()
    index = get_index()
    ids = get_id_map()
    metadata = get_metadata()

    expanded_query = expand_query_with_glossary(query)
    query_vec = model.encode([expanded_query]).astype("float32")
    faiss.normalize_L2(query_vec)

    scores, result_indices = index.search(query_vec, k)
    result_ids = [ids[i] for i in result_indices[0]]

    id_to_meta = {r['recipe_id']: r for r in metadata}
    return [id_to_meta.get(rid, {}) for rid in result_ids]

# === Manual Test Block ===
if __name__ == "__main__":
    # build_index()

    print("\n🔎 Testing Search:")
    
    query = "Something spicy for lunch"
    results = similar_search(query, 5)

    for i, recipe in enumerate(results, 1):
        print(f"\n#{i}: {recipe['recipe_name']}")

