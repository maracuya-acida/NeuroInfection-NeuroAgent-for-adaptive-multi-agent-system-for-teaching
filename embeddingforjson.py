import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama          # ← Esta es la importación correcta
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ====================== CARGAR DATOS ======================
with open('relationaldata.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

documents = []

for topic_id, topic in data['calculus']['topics'].items():
    content = f"""
=== {topic.get('display_name', topic_id)} ===
Topic ID: {topic_id}

Definición:
{topic.get('definition', '')}

Fórmulas:
{json.dumps(topic.get('formulas', {}), indent=2, ensure_ascii=False)}

Ejemplos:
{json.dumps(topic.get('examples', {}), indent=2, ensure_ascii=False)}
""".strip()

    documents.append({
        "page_content": content,
        "metadata": {
            "subject": "Calculus",
            "topic_id": topic_id,
            "display_name": topic.get('display_name')
        }
    })

print(f"✅ {len(documents)} documentos creados.")

# ====================== EMBEDDINGS + VECTOR DB ======================
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(
    documents=[{"page_content": d["page_content"], "metadata": d["metadata"]} for d in documents],
    embedding=embeddings,
    persist_directory="./calculus_vector_db"
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# ====================== OLLAMA ======================
llm = ChatOllama(
    model="llama3.2",        # cambia a llama3.1, mistral, etc. según lo que tengas
    temperature=0.3,
    num_ctx=8192
)

# ====================== CADENA RAG ======================
prompt = ChatPromptTemplate.from_template("""
Eres un excelente tutor de Cálculo universitario. Sé claro, preciso y educativo.

Contexto:
{context}

Pregunta: {question}

Respuesta detallada:
""")

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# ====================== PROBAR ======================
def preguntar(pregunta):
    print(f"\n👤 Pregunta: {pregunta}")
    respuesta = chain.invoke(pregunta)
    print(f"\n🤖 Respuesta:\n{respuesta}")

if __name__ == "__main__":
    preguntar("Explícame la integración por partes con un ejemplo claro")