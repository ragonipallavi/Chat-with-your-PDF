from flask import Flask, request, jsonify, render_template, session
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from groq import Groq
import faiss
import numpy as np
import os
import io
import pickle
import base64

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ── In-memory store (per process) ─────────────────────────────────────────────
store = {}   # session_id → { chunks, index, embed_model }

# ── Load embedding model once ─────────────────────────────────────────────────
print("Loading embedding model…")
EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
print("Model ready.")

# ── Helpers ───────────────────────────────────────────────────────────────────
def read_pdf(file_bytes: bytes) -> tuple[str, int]:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text, len(reader.pages)

def split_text(text: str) -> list[str]:
    chunk_size = 500
    overlap    = 100
    chunks     = []
    start      = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def build_index(chunks: list[str]) -> faiss.IndexFlatL2:
    embeddings = EMBED_MODEL.encode(chunks, show_progress_bar=False)
    embeddings = np.array(embeddings, dtype="float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index

def search(query: str, index, chunks: list[str], k: int = 4) -> list[str]:
    vec = EMBED_MODEL.encode([query])
    vec = np.array(vec, dtype="float32")
    _, indices = index.search(vec, k=k)
    return [chunks[i] for i in indices[0] if i < len(chunks)]

def ask_llm(context: str, question: str, history: list, api_key: str) -> str:
    client = Groq(api_key=api_key)
    system_prompt = (
        "You are a helpful assistant that answers questions strictly based on the "
        "provided document context. If the answer is not in the context, say: "
        "'I couldn't find that information in the document.'\n\n"
        f"Document context:\n{context}"
    )
    messages = [{"role": "system", "content": system_prompt}]
    for h in history[-6:]:
        messages.append(h)
    messages.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.2,
    )
    return response.choices[0].message.content

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "pdf" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["pdf"]
    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    file_bytes = file.read()
    try:
        text, page_count = read_pdf(file_bytes)
    except Exception as e:
        return jsonify({"error": f"Failed to read PDF: {str(e)}"}), 500

    if not text.strip():
        return jsonify({"error": "No text found. The PDF may be image-based/scanned."}), 400

    chunks = split_text(text)
    index  = build_index(chunks)

    # Store in memory keyed by session
    sid = session.get("sid") or base64.b64encode(os.urandom(12)).decode()
    session["sid"] = sid
    store[sid] = {
        "chunks":   chunks,
        "index":    index,
        "filename": file.filename,
        "pages":    page_count,
        "history":  [],
    }

    return jsonify({
        "success":  True,
        "filename": file.filename,
        "pages":    page_count,
        "chunks":   len(chunks),
    })

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()
    api_key  = data.get("api_key", "").strip()

    if not question:
        return jsonify({"error": "Question is empty"}), 400
    if not api_key:
        return jsonify({"error": "Groq API key is required"}), 400

    sid = session.get("sid")
    if not sid or sid not in store:
        return jsonify({"error": "No PDF uploaded yet"}), 400

    s = store[sid]
    relevant = search(question, s["index"], s["chunks"])
    context  = "\n\n".join(relevant)

    try:
        answer = ask_llm(context, question, s["history"], api_key)
    except Exception as e:
        err = str(e)
        if "auth" in err.lower() or "api_key" in err.lower() or "401" in err:
            return jsonify({"error": "Invalid Groq API key. Please check and try again."}), 401
        return jsonify({"error": f"LLM error: {err}"}), 500

    s["history"].append({"role": "user",      "content": question})
    s["history"].append({"role": "assistant",  "content": answer})

    return jsonify({
        "answer":  answer,
        "sources": relevant,
    })

@app.route("/clear", methods=["POST"])
def clear():
    sid = session.get("sid")
    if sid and sid in store:
        del store[sid]
    session.clear()
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)