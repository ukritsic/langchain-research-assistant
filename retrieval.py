from typing import List

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers.ensemble import EnsembleRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_openai import ChatOpenAI

from config import EMBED_MODEL, INDEX_DIR, CHAT_MODEL

def build_retriever(k: int = 5, use_multi_query: bool = True):
    embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vs = FAISS.load_local(INDEX_DIR, embedding, allow_dangerous_deserialization=True)

    dense = vs.as_retriever(search_kwargs={"k": k})
    
    all_docs = list(vs.docstore._dict.values())
    bm25 = BM25Retriever.from_documents(all_docs)
    bm25.k = k

    # Ensemble combines semantic + keyword resutls
    base = EnsembleRetriever(retrievers=[dense, bm25], weights=[0.6, 0.4])

    if use_multi_query:
        llm = ChatOpenAI(model=CHAT_MODEL, temperature=0)
        base = MultiQueryRetriever.from_llm(retriever=base, llm=llm)

    # Add contextual compression (LLM extracts the most relevant sentences)
    compressor = LLMChainExtractor.from_llm(ChatOpenAI(model=CHAT_MODEL, temperature=0))
    compressed = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=base)
    return compressed

def format_docs_for_prompt(docs: List) -> str:
    lines = []
    for d in docs:
        src = d.metadata.get('source', 'unknown')
        page = d.metadata.get('page_number', d.metadata.get('page', '?'))
        lines.append(f"[{src}] | p.{page}\n{d.page_content}")
    return "\n\n---\n\n".join(lines)