"""
Simple and modern RAG chain setup using LangChain Classic (Groq + FAISS).
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain


def create_rag_chain(vectorstore):
    """
    Create and return a complete RAG chain.
    This function:
    - Creates retriever from FAISS vectorstore
    - Initializes Groq LLM
    - Builds the retrieval chain (retriever + LLM + prompt)
    """

    print("\n🚀 Initializing RAG chain...")

    # 1️⃣ Create retriever
    assert vectorstore is not None, "❌ Vectorstore not loaded or invalid."
    
    retriever = vectorstore.as_retriever(
        search_type="mmr",  # or "similarity"
        search_kwargs={"k": 3}
    )

    # 2️⃣ Initialize LLM (Groq)
    llm = ChatGroq(
        model="opeanai/gpt-oss-120b",
        temperature=0.7,
    )

    # 3️⃣ Define prompt template
    prompt = ChatPromptTemplate.from_template(
        """
        You are a helpful and factual AI assistant.
        Use the following retrieved context to answer the user's question.
        If the answer is not found in the context, reply with:
        "I'm not sure based on the provided information."

        <context>
        {context}
        </context>

        Question: {input}
    """
    )

    # 4️⃣ Build RAG chain
    document_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, document_chain)

    print("✅✅ RAG chain created successfully!\n" + "=" * 60)

    return rag_chain
