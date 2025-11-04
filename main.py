"""
main.py
End-to-end RAG pipeline using:
- DataLoader
- DataSplitter
- Embeddings
- Vectorstore (FAISS)
- Groq LLM RAG Chain
"""

# ============================================================
# IMPORTS
# ============================================================
from src.dataloader import load_all_data
from src.datasplitter import split_docs
from src.embedding import huggingface_embeddings
from src.vectorstore import create_vectorstore, load_vectorstore
from src.chain import create_rag_chain
from dotenv import load_dotenv
import os
load_dotenv()


# ============================================================
# MAIN PIPELINE
# ============================================================
def main():
    print("\n============================")
    print("🚀 Starting RAG Pipeline...")
    print("============================")

    # 1️⃣ Load all documents
    data_dir = "data/"
    urls = []

    docs = load_all_data(data_dir, urls)

    if not docs:
        print("❌ No documents found. Exiting.")
        return

    # 2️⃣ Split into chunks
    chunked_docs = split_docs(docs)

    if not chunked_docs:
        print("❌ No chunks created. Exiting.")
        return

    # 3️⃣ Initialize embedding model (HuggingFace or Ollama)
    embeddings = huggingface_embeddings()

    # 4️⃣ Create or load FAISS vectorstore
    if os.path.exists("faiss_index"):
        vectorstore = load_vectorstore(
            embeddings, vectorstore_path="faiss_index")
    else:
        vectorstore = create_vectorstore(chunked_docs, embeddings)

    # 5️⃣ Build RAG chain
    rag_chain = create_rag_chain(vectorstore)

    while True:
        # 6️⃣ Ask a question
        query = input("\nEnter your question: ")
        if query.lower() == 'exit':
            print("👋 Exiting RAG Pipeline. Goodbye!")
            break

        # 7️⃣ Display answer
        response = rag_chain.invoke({"input": query})
        print("\n🧠 AI Answer:")
        print(response["answer"])
        print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    main()
