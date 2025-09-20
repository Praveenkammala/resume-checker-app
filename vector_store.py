
"""vector_store.py
Helpers to create and query a vector store using FAISS or Chroma.
This is a template: adapt to your runtime (Chroma cloud, local FAISS, or Pinecone).
"""
from typing import List, Tuple

def build_faiss_index(embeddings):
    try:
        import faiss
    except Exception as e:
        raise ImportError('faiss-cpu is required. pip install faiss-cpu') from e
    import numpy as np
    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d)  # inner product for cosine if normalized
    index.add(embeddings)
    return index

def query_faiss(index, query_embedding, top_k=5):
    import numpy as np
    D, I = index.search(query_embedding, top_k)
    return D, I

# Chroma example (local)
def build_chroma_collection(embeddings, metadatas, ids):
    try:
        import chromadb
        from chromadb.config import Settings
    except Exception as e:
        raise ImportError('chromadb required. pip install chromadb') from e
    client = chromadb.Client(Settings(chroma_db_impl='duckdb+parquet', persist_directory='.chromadb'))
    collection = client.create_collection(name='resumes')
    collection.add(documents=[str(i) for i in range(len(embeddings))], embeddings=embeddings.tolist(), metadatas=metadatas, ids=ids)
    return collection

def query_chroma(collection, query_embedding, n=5):
    res = collection.query(query_embeddings=[query_embedding.tolist()], n_results=n, include=['metadatas','distances'])
    return res
