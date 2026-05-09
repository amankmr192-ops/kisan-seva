import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

SCHEMES_DIR      = "data/schemes"
VECTORSTORE_PATH = "vectorstore/faiss_index"

def load_all_pdfs(directory: str):
    all_docs = []
    pdf_files = [f for f in os.listdir(directory) if f.endswith(".pdf")]

    if not pdf_files:
        print("No PDFs found in data/schemes/ — please add scheme PDFs first.")
        return []

    for filename in pdf_files:
        filepath = os.path.join(directory, filename)
        print(f"Loading: {filename}")
        loader = PyMuPDFLoader(filepath)
        docs   = loader.load()

        scheme_name = filename.replace(".pdf", "").replace("_", " ").title()
        for doc in docs:
            doc.metadata["scheme_name"] = scheme_name
            doc.metadata["source_file"] = filename

        all_docs.extend(docs)
        print(f"  → {len(docs)} pages loaded")

    return all_docs


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_documents(docs)
    print(f"\nTotal chunks created: {len(chunks)}")
    return chunks


def build_vectorstore(chunks):
    print("\nLoading embedding model (first time ~2 min)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "mps"}
    )

    print("Building FAISS vector store...")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs("vectorstore", exist_ok=True)
    vectorstore.save_local(VECTORSTORE_PATH)
    print(f"✅ Vector store saved to {VECTORSTORE_PATH}")
    return vectorstore


if __name__ == "__main__":
    print("=== Kisan Seva — PDF Ingestion ===\n")
    docs = load_all_pdfs(SCHEMES_DIR)
    if not docs:
        print("No PDFs found. Please add PDFs to data/schemes/ folder.")
        exit(1)
    chunks = split_documents(docs)
    build_vectorstore(chunks)
    print("\nIngestion complete! You can now start the FastAPI server.")