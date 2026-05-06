# Folio — AI Document Reader 📄

> A minimalist, high-performance RAG application to chat with your PDF documents using Groq and FAISS.

![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Llama](https://img.shields.io/badge/Llama_3.1-Meta-blue?style=flat)

Folio is a document assistant that lets you upload any PDF and ask questions in plain English. Powered by a **RAG (Retrieval-Augmented Generation)** pipeline, it answers strictly from your document's content — minimizing hallucinations and keeping responses grounded in your source material.

---

## ✨ Features

- **Local PDF Indexing** — Text is extracted and chunked directly on your server; your full document never leaves your machine.
- **Semantic Vector Search** — Uses `FAISS` + `all-MiniLM-L6-v2` for fast, meaning-aware retrieval (not just keyword matching).
- **Blazing Fast Inference** — Powered by `llama-3.1-8b-instant` via the Groq Cloud API for near-instant responses.
- **Source Transparency** — Every answer includes the exact document passages used to generate it.
- **Privacy First** — Only the relevant text snippets needed to answer your question are sent to the Groq API. Everything else stays local.
- **Elegant UI** — A "Paper & Ink" aesthetic with a clean reading experience and dark-mode sidebar.

---

## 🏗️ Architecture

Folio follows a standard RAG pipeline:

```
PDF Upload → Text Extraction → Chunking → Embedding → FAISS Index
                                                             ↓
User Question → Embed Question → Vector Search → Top-4 Chunks
                                                             ↓
                                          Groq (Llama 3.1) → Answer
```

| Stage | Detail |
|---|---|
| **Ingestion** | `PyPDF2` extracts text; split into 500-character chunks with overlap |
| **Embedding** | `SentenceTransformer` (`all-MiniLM-L6-v2`) converts chunks to 384-dimensional vectors |
| **Retrieval** | Top 4 most relevant chunks fetched via L2 distance in `FAISS` |
| **Generation** | Context + question sent to `llama-3.1-8b-instant` via Groq API |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask (Python) |
| Vector DB | FAISS (Facebook AI Similarity Search) |
| Embeddings | `all-MiniLM-L6-v2` (Sentence-Transformers) |
| LLM | Llama 3.1 8B via Groq Cloud API |
| Frontend | HTML5, CSS3, Vanilla JS |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A [Groq API Key](https://console.groq.com/) (free tier available)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/folio.git
cd folio
```

**2. Create a virtual environment and install dependencies**

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Run the application**

```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 📖 How to Use

1. **Get a Groq API Key** — Sign up at [Groq Cloud](https://console.groq.com/) and generate a `gsk_...` key.
2. **Enter your key** — Paste it into the sidebar in the Folio app.
3. **Upload a PDF** — Drag and drop your document into the sidebar, or click to browse.
4. **Chat** — Ask questions in plain English. Folio retrieves the most relevant passages and generates a grounded answer.
5. **Inspect sources** — Expand the "Sources" panel below any answer to see the exact document excerpts used.

---

## 📂 Project Structure

```
folio/
├── app.py               # Flask server, PDF processing logic, RAG pipeline
├── index.html           # Single-page frontend (CSS + JS embedded)
├── requirements.txt     # Python dependencies
└── LICENSE
```

---

## 🛡️ Privacy & Data Handling

Folio is designed with privacy in mind:

- PDF text is **extracted and indexed locally** on your server.
- Only the **top retrieved snippets** (not your full document) are sent to the Groq API per query.
- All document data is stored **in-memory** and cleared when the session ends — nothing is persisted to disk.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

*Built with ❤️ for better document reading.*
