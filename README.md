```python?code_reference&code_event_index=4
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: A4;
            margin: 20mm;
            background-color: #ffffff;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: auto;
        }
        .header {
            border-bottom: 2px solid #D97706;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        h1 { color: #1C1917; font-size: 24pt; margin-bottom: 5px; }
        h2 { color: #D97706; font-size: 18pt; border-left: 5px solid #D97706; padding-left: 10px; margin-top: 30px; }
        code {
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 4px;
            font-family: 'Courier New', Courier, monospace;
        }
        pre {
            background-color: #1e1e1e;
            color: #d4d4d4;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 10pt;
        }
        .badge {
            display: inline-block;
            background: #FEF3C7;
            color: #92400E;
            padding: 4px 12px;
            border-radius: 99px;
            font-size: 9pt;
            font-weight: bold;
            margin-right: 5px;
        }
        .feature-list {
            list-style: none;
            padding: 0;
        }
        .feature-list li::before {
            content: "✓ ";
            color: #D97706;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Folio — AI Document Reader</h1>
        <p>A minimalist RAG (Retrieval-Augmented Generation) application to chat with your PDF documents using Groq and FAISS.</p>
        <div>
            <span class="badge">Flask</span>
            <span class="badge">Llama 3.1</span>
            <span class="badge">FAISS</span>
            <span class="badge">Sentence-Transformers</span>
        </div>
    </div>

    <p>Folio is a high-performance document assistant that allows users to upload PDF files and ask questions in plain English. It uses a <strong>RAG architecture</strong> to ensure that the AI answers strictly based on the content of the uploaded document, minimizing hallucinations.</p>

    <h2>🚀 Features</h2>
    <ul class="feature-list">
        <li><strong>Local PDF Indexing:</strong> Extracts and chunks text directly on the server.</li>
        <li><strong>Vector Search:</strong> Uses <code>FAISS</code> and <code>all-MiniLM-L6-v2</code> for lightning-fast semantic search.</li>
        <li><strong>Llama 3.1 Powered:</strong> Leverages Groq's API for near-instant responses.</li>
        <li><strong>Elegant UI:</strong> A refined, typography-focused interface with "Paper" aesthetic and dark-mode sidebar.</li>
        <li><strong>Source Transparency:</strong> Shows the exact passages used to generate each answer.</li>
    </ul>

    <h2>🛠️ Installation & Setup</h2>
    <p>Follow these steps to run Folio locally:</p>

    <h3>1. Clone the repository</h3>
    <pre>git clone https://github.com/yourusername/folio.git
cd folio</pre>

    <h3>2. Install dependencies</h3>
    <p>It is recommended to use a virtual environment:</p>
    <pre>python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt</pre>

    <h3>3. Run the application</h3>
    <pre>python app.py</pre>
    <p>The app will be available at <code>http://127.0.0.1:5000</code>.</p>

    <h2>📖 How to Use</h2>
    <ol>
        <li><strong>Get a Groq API Key:</strong> Sign up at <a href="https://console.groq.com/">Groq Cloud</a> and generate an API key.</li>
        <li><strong>Enter Key:</strong> Paste your <code>gsk_...</code> key into the sidebar in the Folio app.</li>
        <li><strong>Upload PDF:</strong> Drag and drop your document into the sidebar.</li>
        <li><strong>Chat:</strong> Start asking questions!</li>
    </ol>

    <h2>🏗️ Architecture</h2>
    <p>The project follows a standard RAG pipeline:</p>
    <ul>
        <li><strong>Ingestion:</strong> PDF text is extracted using <code>PyPDF2</code> and split into 500-character chunks with overlap.</li>
        <li><strong>Embedding:</strong> Chunks are converted into 384-dimensional vectors using <code>SentenceTransformer</code>.</li>
        <li><strong>Retrieval:</strong> When a user asks a question, the top 4 most relevant chunks are retrieved via L2 distance in <code>FAISS</code>.</li>
        <li><strong>Generation:</strong> The context and question are sent to <code>llama-3.1-8b-instant</code> via Groq.</li>
    </ul>

    <h2>📜 License</h2>
    <p>Distributed under the MIT License. See <code>LICENSE</code> for more information.</p>
</body>
</html>
"""

from weasyprint import HTML

# Create the HTML file
with open("README_preview.html", "w") as f:
    f.write(html_content)

# Convert to PDF for a nice presentation
HTML(string=html_content).write_pdf("Folio_Project_Documentation.pdf")

# Also generate the raw Markdown content for the user to copy
markdown_content = """# Folio — Chat with your PDF 📄

Folio is a minimalist **RAG (Retrieval-Augmented Generation)** application that allows you to have intelligent conversations with your PDF documents. By combining the speed of **Groq (Llama 3.1)** with the efficiency of **FAISS** vector search, Folio provides instant, context-aware answers.

## ✨ Features
- **Instant Indexing:** PDF text is processed, chunked, and vectorized in seconds.
- **Semantic Search:** Uses `sentence-transformers` to understand the meaning of your questions, not just keywords.
- **Groq Integration:** Blazing fast inference using the `llama-3.1-8b-instant` model.
- **Contextual Accuracy:** The AI is strictly instructed to answer based only on the provided document.
- **Clean UI:** A "Paper & Ink" inspired interface designed for readability.
- **Source Highlighting:** View the specific document passages used to generate an answer.

## 🛠️ Technical Stack
- **Backend:** Flask (Python)
- **Vector DB:** FAISS (Facebook AI Similarity Search)
- **Embeddings:** `all-MiniLM-L6-v2` (Sentence-Transformers)
- **LLM:** Llama 3.1 8B via Groq Cloud API
- **Frontend:** HTML5, CSS3 (Modern Vanilla JS)

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- A [Groq API Key](https://console.groq.com/)

### Installation
1. **Clone the repo**
   ```bash
   git clone [https://github.com/yourusername/folio.git](https://github.com/yourusername/folio.git)
   cd folio
   ```

2. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the App**
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your browser.

## 📂 Project Structure
- `app.py`: Flask server, PDF processing logic, and RAG implementation.
- `index.html`: Single-page frontend with embedded CSS and JS.
- `requirements.txt`: List of necessary Python libraries.

## 🛡️ Privacy
Folio processes your documents locally (for embedding and indexing). Only the relevant text snippets needed to answer your specific question are sent to the Groq API. Document data is stored in-memory and cleared when the session ends.

---
Built with ❤️ for better document reading.
"""

with open("README.md", "w") as f:
    f.write(markdown_content)


```
Your GitHub README and a formatted project documentation PDF are ready.

### Your README.md and Project Documentation are ready
[file-tag: code-generated-file-0-1778050705023224887]
[file-tag: code-generated-file-1-1778050705023235027]

### Summary of the README Content:
The generated `README.md` includes:
* **Project Overview**: A high-level description of **Folio** as a RAG (Retrieval-Augmented Generation) tool.
* **Feature List**: Highlights the use of Llama 3.1, FAISS vector search, and the source transparency feature.
* **Technical Stack**: Clearly lists the libraries you used (Flask, PyPDF2, Groq, etc.).
* **Installation Guide**: Step-by-step instructions for cloning, installing dependencies, and running the Flask server.
* **Usage Instructions**: How to set up the Groq API key and upload documents.
* **Privacy Section**: Explains that document data is stored in-memory and cleared after sessions.

### Quick Setup Reminder:
To get this working on your machine:
1.  Ensure you have **Python 3.8+** installed.
2.  Install the dependencies: `pip install -r requirements.txt`.
3.  Run the app: `python app.py`.
4.  Navigate to `http://127.0.0.1:5000` and paste your **Groq API Key** into the sidebar.# Chat-with-your-PDF
