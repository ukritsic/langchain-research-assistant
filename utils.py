# FILE: utils.py
from typing import List

from langchain_community.document_loaders import PyMuPDFLoader, TextLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import DOCS_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def _normalize_metadata(docs):
    for d in docs:
        src = d.metadata.get("source") or d.metadata.get("file_path") or d.metadata.get("url")
        d.metadata["source"] = str(src) if src else "unknown"
        if "page" in d.metadata and isinstance(d.metadata["page"], int):
            d.metadata["page_number"] = d.metadata["page"] + 1
    return docs

def load_local_docs() -> List:
    docs = []
    if not DOCS_DIR.exists():
        return docs
    for p in DOCS_DIR.rglob("*"):
        if p.is_dir():
            continue
        suf = p.suffix.lower()
        try:
            if suf == ".pdf":
                docs.extend(PyMuPDFLoader(str(p)).load())
            elif suf in {".txt", ".md"}:
                docs.extend(TextLoader(str(p), encoding="utf-8").load())
        except Exception as e:
            print(f"[WARN] Skipping {p}: {e}")
    return docs

def load_web_docs(urls: List[str]) -> List:
    docs = []
    if not urls:
        return docs
    
    for url in urls:
        try:
            docs.extend(WebBaseLoader(url).load())
        except Exception as e:
            print(f"[WARN] Skipping {url}: {e}")
    return docs

def split_docs(docs: List):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, add_start_index=True
    )
    return splitter.split_documents(docs)