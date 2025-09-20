from typing import List, Optional

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import EMBED_MODEL, INDEX_DIR
from utils import load_local_docs, load_web_docs, split_docs, _normalize_metadata

def ingest(urls: Optional[List[str]] = None):
    print("[Ingest] Loading documents ...")
    local = load_local_docs()
    web = load_web_docs(urls or [])
    raw_docs = local + web
    if not raw_docs:
        print("[Ingest] No documents found. Put files in ./docs or pass --urls.")
        return
    
    print(f"[Ingest] Loaded {len(raw_docs)} raw docs; splitting ...")
    chunks = split_docs(_normalize_metadata(raw_docs))
    print(f"[Ingest] {len(chunks)} chunks -> embedding & indexing ...")

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vs = FAISS.from_documents(chunks, embeddings)
    vs.save_local(INDEX_DIR)
    print(f"[Ingest] Saved FAISS index to {INDEX_DIR}")