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
# ✅ IMPORTS
# ============================================================
from src.dataloader import load_all_data
from src.datasplitter import split_docs
from src.embedding import huggingface_embeddings
from src.vectorstore import create_vectorstore, load_vectorstore
from src.chain import create_rag_chain


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
    try:
        vectorstore = load_vectorstore(embeddings, "faiss_index")
        print("\n✅ Existing vectorstore loaded.")

    except:
        print("\n⚙️ Creating new FAISS vectorstore...")
        vectorstore = create_vectorstore(chunked_docs, embeddings)

    # 5️⃣ Build RAG chain
    rag_chain = create_rag_chain(vectorstore)

    # 6️⃣ Ask a question
    query = input("\n💬 Enter your question: ")
    response = rag_chain.invoke({"input": query})

    # 7️⃣ Display answer
    print("\n🧠 AI Answer:")
    print(response["answer"])
    print("=" * 60)


# ============================================================
# 🏁 ENTRY POINT
# ============================================================
if __name__ == "__main__":
    main()
