from db_utils import fetch_recipes_for_indexing
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'faissIndex','recipe_index.faiss')
ID_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'faissIndex','id_map.txt')

def build_index():
    recipes = fetch_recipes_for_indexing()
    
    IDs = []
    VECs = []

    for recipe in recipes:
        text = f"{recipe['recipename']} {recipe.get('ingredients', '')} {recipe.get('diet_type', '')} {recipe.get('description', '')} {recipe.get('totaltime', '')}"
        vector = model.encode(text)
        
        IDs.append(recipe['recipeid'])
        VECs.append(vector)
    
    # Normalize vectors before adding
    VECs = np.array(VECs).astype("float32")
    faiss.normalize_L2(VECs)  # Normalize vectors to unit length

    index = faiss.IndexFlatIP(VECs.shape[1])  # Use Inner Product index for cosine similarity
    index.add(VECs)
    
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    
    faiss.write_index(index, INDEX_PATH)
    with open(ID_PATH, "w") as f:
        json.dump(IDs, f)

    print("[✅] FAISS index built and saved.")

def expand_query_with_glossary(query: str, glossary_path="glossary.json") -> str:
    try:
        with open(glossary_path, "r") as f:
            glossary = json.load(f)
    except FileNotFoundError:
        return query  # skip if glossary doesn't exist

    words = query.lower().split()
    expanded_words = []

    for word in words:
        expanded_words.append(word)
        if word in glossary:
            expanded_words.extend(glossary[word])

    return " ".join(expanded_words)

def similar_search(query, k):
    # Loading indexes and id-maps
    indexes = faiss.read_index(INDEX_PATH)
    with open(ID_PATH, 'r') as f:
        ids = json.load(f)
    
    expanded = expand_query_with_glossary(query)
    query_vector = model.encode([expanded]).astype("float32")
    faiss.normalize_L2(query_vector)  # Normalize query vector as well

      
    # Search
    _, result_indices = indexes.search(query_vector, k)

    # Return matching recipe IDs
    return [ids[i] for i in result_indices[0]]

if __name__ == "__main__":
    
    build_index()
    
    print("\n🔎 Testing Search:")
    query = "Something sweet 😋"
    result = similar_search(query, 5)
    recipes = fetch_recipes_for_indexing()

    # Create a dict for quick lookup by recipeid
    recipe_dict = {r['recipeid']: r for r in recipes}
    
    for recipe_id in result:
        recipe = recipe_dict.get(recipe_id)
        if recipe:
            print(recipe)
        else:
            print(f"Recipe ID {recipe_id} not found.")
        
    print(f"Top results for: '{query}' → {result}")
