# Multi-Document Research Assistant

A command-line and interactive research assistant built with [LangChain](https://www.langchain.com/).  
It ingests local and web documents, builds embeddings with FAISS, and provides structured answers by synthesizing across multiple sources.

---

## ✨ Features

- **Document ingestion**
  - Local PDFs, text (`.txt`, `.md`) files
  - Web pages via URL
- **Text splitting**
  - Recursive chunking with configurable size/overlap
- **Vector search**
  - FAISS with HuggingFace embeddings (`all-MiniLM-L6-v2`)
- **Hybrid retrieval**
  - Dense semantic search + BM25 keyword retriever (Ensemble)
  - Optional multi-query expansion via LLM
  - Contextual compression with LLM chain extractor
- **Answer synthesis**
  - ChatGPT (OpenAI) generates structured responses
  - Sources cited with `[source | p.N]`
- **Interactive shell**
  - Adjustable parameters (`k`, multi-query toggle, re-ingest, URLs)
  - Ask multiple research questions in one session

---

## 📦 Requirements

- Python 3.9+
- [LangChain](https://www.langchain.com/)
- [LangChain Community integrations](https://python.langchain.com/docs/integrations/)
- [LangChain OpenAI](https://python.langchain.com/docs/integrations/llms/openai)
- [FAISS](https://github.com/facebookresearch/faiss)
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
- HuggingFace embeddings
- OpenAI API key (`OPENAI_API_KEY` must be set in your environment)

Install dependencies:

```bash
pip install langchain langchain-community langchain-openai faiss-cpu pymupdf sentence-transformers
```
---

## 🚀 Usage
1. Ingest documents: Place your local documents under ./docs or pass web URLs.
```bash
python app.py ingest --urls "https://example.com,https://another.com"
```
2. Ask a question (single-shot)
```bash
python app.py ask "What are the key findings about X?" --k 8
```
3. Interactive shell
```bash
python app.py shell --k 5 --urls "https://example.com"
```
