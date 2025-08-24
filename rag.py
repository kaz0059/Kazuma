# rag.py

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

DB_DIR = "knowledge_base"


def build_knowledge_base():
    """
    Build (or reload) a knowledge base from files in knowledge_base/.
    Supports PDF and TXT for now.
    If no files found, returns None (so the AI still works).
    """
    docs = []

    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    # Load docs
    for fname in os.listdir(DB_DIR):
        path = os.path.join(DB_DIR, fname)
        if fname.endswith(".pdf"):
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        elif fname.endswith(".txt"):
            loader = TextLoader(path, encoding="utf-8")
            docs.extend(loader.load())

    if not docs:  # 🚨 nothing found
        print("⚠️ No documents found in knowledge_base/. Skipping RAG.")
        return None

    # Split docs into smaller chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(docs)

    # Use HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create Chroma vectorstore
    db = Chroma.from_documents(split_docs, embeddings, persist_directory=DB_DIR)
    db.persist()
    return db


def query_knowledge_base(db, query: str, k: int = 3):
    """
    Query the Chroma knowledge base for relevant context.
    If db is None, return empty context.
    """
    if db is None:
        return ""  # no knowledge base yet
    results = db.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in results])
