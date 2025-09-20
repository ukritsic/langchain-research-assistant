from pathlib import Path

DOCS_DIR = Path("docs")
INDEX_DIR = "faiss_index"
CHAT_MODEL = "gpt-5-mini"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2" # small, fast, free
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150