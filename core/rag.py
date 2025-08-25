# core/rag.py

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# Use relative path from project root
DB_DIR = "knowledge_base"


def build_knowledge_base():
    """
    Build (or reload) a knowledge base from files in knowledge_base/.
    Supports PDF and TXT files.
    Returns None if no files found (so the AI still works).
    """
    docs = []

    # Create directory if it doesn't exist
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        print(f"📁 Created {DB_DIR} directory")

    # Load documents
    supported_files = []
    for fname in os.listdir(DB_DIR):
        path = os.path.join(DB_DIR, fname)
        
        try:
            if fname.lower().endswith(".pdf"):
                loader = PyPDFLoader(path)
                docs.extend(loader.load())
                supported_files.append(fname)
            elif fname.lower().endswith(".txt"):
                loader = TextLoader(path, encoding="utf-8")
                docs.extend(loader.load())
                supported_files.append(fname)
        except Exception as e:
            print(f"⚠️ Error loading {fname}: {e}")

    if not docs:
        print(f"ℹ️ No supported documents found in {DB_DIR}/")
        print("💡 Add .txt or .pdf files to enable knowledge base")
        return None

    print(f"📚 Loaded {len(supported_files)} files: {', '.join(supported_files)}")

    try:
        # Split documents into smaller chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        split_docs = splitter.split_documents(docs)
        print(f"✂️ Split into {len(split_docs)} chunks")

        # Use HuggingFace embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )

        # Create Chroma vectorstore
        persist_dir = os.path.join(DB_DIR, "chroma_db")
        db = Chroma.from_documents(
            documents=split_docs,
            embedding=embeddings,
            persist_directory=persist_dir
        )
        db.persist()
        return db

    except Exception as e:
        print(f"❌ Failed to build knowledge base: {e}")
        return None


def query_knowledge_base(db, query: str, k: int = 3) -> str:
    """
    Query the Chroma knowledge base for relevant context.
    Returns empty string if db is None or query fails.
    """
    if db is None:
        return ""
    
    try:
        results = db.similarity_search(query, k=k)
        if not results:
            return ""
        
        # Combine results with clear separation
        context_parts = []
        for i, doc in enumerate(results, 1):
            content = doc.page_content.strip()
            if content:
                context_parts.append(f"[Source {i}]: {content}")
        
        return "\n\n".join(context_parts)
    
    except Exception as e:
        print(f"⚠️ Knowledge base query error: {e}")
        return ""