# NeuroAgent — AI-Powered Educational Content Generator

## Project Description

NeuroAgent is a local AI educational assistant designed to help teachers and instructional designers generate high-quality academic documents automatically. Given a subject, a pedagogical approach, and a learning objective, the system produces structured **lesson plans**, **syllabi**, and **curriculum maps** in Markdown, and exports them as **PDF** or **DOCX** files.

The agent is grounded by a structured knowledge base (`relationaldata.json`) that contains calculus topics, mathematical formulas, worked examples, and pedagogical methodologies (UDL, CRA, 3Rs). When a query is related to those topics, the backend injects this context directly into the LLM prompt, acting as a lightweight RAG (Retrieval-Augmented Generation) system without a vector database.

A second, more advanced pipeline (`embeddingforjson.py`) implements full semantic retrieval using sentence embeddings and a vector store, enabling natural-language querying over the same knowledge base via a local LLM.

The C++ file (`generate_umath_validation_data.cpp`) defines and validates a structured subject registry — Math, Calculus, Trigonometry, Physics — with rigor scores, prerequisites, and floating-point ULP tolerances. It serves as a typed data model and validation layer for the academic domain.

---

## Technologies Used

### Backend

| Technology | Purpose |
|---|---|
| **Python 3.10+** | Main backend language |
| **Flask** | REST API server; serves the frontend and exposes `/api/` endpoints for plan generation and export |
| **Flask-CORS** | Allows the browser frontend to call the Flask API from any origin |
| **Ollama** (`gemma:2b`) | Runs the LLM locally; Flask sends prompts via HTTP to `localhost:11434` |
| **python-docx** | Exports generated Markdown content to formatted `.docx` Word documents |
| **ReportLab** | Exports generated content to styled `.pdf` files |
| **requests** | HTTP client used to communicate with Ollama's local API |

### Frontend

| Technology | Purpose |
|---|---|
| **HTML5 / CSS3 / Vanilla JS** | Single-page UI (`index.html`) with a dark purple theme, sidebar navigation, and real-time result rendering |
| **Google Fonts** (Outfit + Noto Sans Mono) | Typography — loaded from CDN, no build step needed |
| **Marked.js** | Renders the Markdown returned by the API into formatted HTML inside the browser |

### Knowledge & Embedding Pipeline

| Technology | Purpose |
|---|---|
| **JSON** (`relationaldata.json`) | Domain knowledge base — stores calculus topics, formulas, examples, and pedagogical strategies in a structured relational format |
| **LangChain** | Orchestration framework for the embedding pipeline; chains retriever → prompt → LLM → output parser |
| **ChromaDB** | Vector database used by `embeddingforjson.py`; persists embeddings to disk at `./calculus_vector_db/` so they are not recomputed on every run |
| **HuggingFace `sentence-transformers`** (`all-MiniLM-L6-v2`) | Converts text chunks from the JSON into dense vector embeddings for semantic similarity search |
| **Ollama** (`llama3.2`) | Local LLM backend used in the embedding pipeline for answering queries in natural language |

### Validation Layer

| Technology | Purpose |
|---|---|
| **C++17** (`generate_umath_validation_data.cpp`) | Defines a typed `Subject` struct with rigor scores, prerequisites, themes, and ULP tolerances; validates and sorts the subject registry at compile time and runtime |

---

## Why These Databases?

### `relationaldata.json` — Structured Domain Knowledge Store
A plain JSON file is used here instead of a SQL or NoSQL database because the knowledge is **static, hierarchical, and read-only at runtime**. JSON maps naturally to the nested structure of academic content (subject → topics → formulas → examples) and can be loaded once into memory at server startup. This eliminates any external database dependency, making the project portable and easy to run locally.

### ChromaDB (`./calculus_vector_db/`) — Persistent Vector Store
ChromaDB is chosen for the semantic search pipeline because it is **embedded** (no separate server process needed), **persists embeddings to disk** automatically, and integrates natively with LangChain. Once the JSON documents are embedded and stored, subsequent runs skip re-embedding entirely. It pairs naturally with HuggingFace sentence-transformers in Python environments without requiring cloud services.

---

## How to Run the Project Locally

### Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.com) installed and running
- A pulled model: `ollama pull gemma:2b` (for the Flask backend) and optionally `ollama pull llama3.2` (for the embedding pipeline)
- C++ compiler (g++ or clang++) — only if you want to run the validation tool

---

### 1. Install Python Dependencies

```bash
pip install flask flask-cors requests python-docx reportlab
```

For the embedding pipeline only:

```bash
pip install langchain langchain-community langchain-ollama chromadb sentence-transformers
```

---

### 2. Start Ollama

```bash
ollama serve
```

Make sure the model is available:

```bash
ollama list
# Should show gemma:2b (and llama3.2 if using the embedding pipeline)
```

---

### 3. Prepare the Project Files

Place all files in the same directory:

```
project/
├── app.py                          # Flask backend (rename from app__1_.py)
├── index.html                      # Frontend (rename from index_.html)
├── relationaldata.json             # Knowledge base
├── embeddingforjson.py             # Optional: embedding/RAG pipeline
└── generate_umath_validation_data.cpp  # Optional: C++ validator
```

---

### 4. Run the Flask Backend

```bash
python app.py
```

The server starts at **http://localhost:5000**. Open that URL in your browser — Flask serves `index.html` automatically from the same directory.

---

### 5. (Optional) Run the Embedding Pipeline

```bash
python embeddingforjson.py
```

On the first run, this embeds the JSON topics into ChromaDB (stored in `./calculus_vector_db/`). Subsequent runs load from disk. The script prints an example query and answer in the terminal.

---

### 6. (Optional) Compile and Run the C++ Validator

```bash
g++ -std=c++17 -o validator generate_umath_validation_data.cpp
./validator
```

This prints the subject registry sorted by rigor score and searches for a specific theme (e.g., "Limits") across all subjects.

---

## API Endpoints (Flask)

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Serves the frontend (`index.html`) |
| `GET` | `/api/saludo?nombre=...` | Returns a personalized greeting from the agent |
| `POST` | `/api/plan-clase` | Generates a lesson plan |
| `POST` | `/api/silabo` | Generates an academic syllabus |
| `POST` | `/api/malla` | Generates a curriculum map |
| `POST` | `/api/exportar` | Exports content as PDF or DOCX |
| `GET` | `/api/estado` | Checks if Ollama is reachable and lists available models |

---

## Project Structure Summary

```
project/
├── app.py                  # Flask API + knowledge base loader + export logic
├── index.html              # Single-page frontend (HTML/CSS/JS)
├── relationaldata.json     # Static knowledge base (calculus + pedagogy)
├── embeddingforjson.py     # LangChain + ChromaDB + HuggingFace RAG pipeline
└── generate_umath_validation_data.cpp  # C++ subject registry and validator
```
