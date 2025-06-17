# 🧠 Intelligent Nutri – AI-Powered Recipe & Nutrition Assistant

**Eat smarter. Cook faster. Live healthier.**

Intelligent Nutri is a personalized AI-driven platform that helps users find recipes, analyze nutrition, generate shopping lists, and chat with a virtual food assistant — all based on their dietary needs and preferences.

---

## 📦 Project Structure

```bash
intelligent-nutri/
│
├── frontend/               # All UI code here
│   ├── index.html
│   ├── preferences.html
│   ├── chatbot.html
│   └── js/
│       ├── app.js          # JS for preferences form & search
│       └── chatbot.js      # JS for AI chat interface
│   └── css/
│       └── style.css      
│
├── backend/                # All Flask-related backend code
│   ├── main.py             # Entry point — define routes here
│   ├── llm_utils.py        # Functions to generate prompts & call Gemini/OpenAI
│   ├── db_utils.py         # Functions to interact with SQLite (CRUD)
│   └── vector_utils.py     # Handle FAISS search & embeddings
│
├── database/
│   ├── schema.sql          # Create tables
│   ├── init_db.py          # Script to create and initialize database
│   └── seed_data.py        # Preload recipes from dataset (Kaggle, etc.)
│
└── requirements.txt
```

---

## ⚙️ Tech Stack

| Layer     | Tech Used              |
|-----------|------------------------|
| Frontend  | HTML, CSS, JS, Bootstrap |
| Backend   | Python Flask, REST APIs |
| Database  | SQLite3, FAISS (Vector DB) |
| AI/NLP    | OpenAI / Gemini via API, Sentence Transformers |

---

## 🚀 Quick Start

### 1. Clone the Repo
```bash
git clone https://github.com/professorlearncode/intelli-nutri.git
cd intelligent-nutri
```

### 2. Backend Setup (Flask)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt

# Start the server
python run.py
```

### 3. Frontend Access
Open any of the following in your browser:
- `frontend/index.html` → Main dashboard
- `frontend/preferences.html` → User preferences form
- `frontend/chatbot.html` → Chat with the AI chef

---

## 🧠 Core Features

- **🧾 Preferences-Based Personalization:** Tailored recipes based on user's dietary needs and health goals.
- **🔍 Recipe Search:** Search by ingredients or dishes, powered by vector similarity search.
- **🧑‍🍳 AI Chatbot:** Talk to a virtual chef using LLM-based prompts.
- **🛒 Shopping List Generator:** (Optional) Exportable ingredient lists for selected recipes.
- **🧠 Agentic AI Flow (Optional):** Voice control & web search coming soon.

---

## 👥 Team & Collaboration Guidelines

### Branch Naming
- `main`: Production-ready
- `dev`: Ongoing development
- `feature/<feature-name>`: Individual tasks

### Suggested Roles
- Frontend UI
- Form & preference logic
- Chatbot & prompt design
- Recipe search integration
- Vector DB & embeddings
- Integration & DevOps

### Git Workflow
```bash
# Create a new branch
git checkout -b feature/<your-feature>

# Make changes and commit
git add .
git commit -m "Add: <describe your feature>"

# Push and create PR
git push origin feature/<your-feature>
```

---

## 📌 To-Do / Milestones

- [ ] User Authentication
- [ ] Preferences Form & Storage
- [ ] Recipe Search via API & Dataset
- [ ] Chatbot Integration with LLM
- [ ] Vector DB Setup
- [ ] Dashboard UI
- [ ] Deployment (Optional: Vercel + Render)

---

## 📄 License
MIT License

---

## 🧠 Inspired by
Foodie brains, AI chefs, and real-world meal struggles.

> “Good food is the foundation of genuine happiness.” – Auguste Escoffier
