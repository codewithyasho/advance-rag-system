"""
Streamlit Web Application for Advanced RAG Pipeline
Interactive UI for document Q&A with multi-format support
"""

import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

# Import RAG pipeline components
from src.dataloader import load_all_data
from src.datasplitter import split_docs
from src.embedding import huggingface_embeddings
from src.vectorstore import create_vectorstore, load_vectorstore
from src.chain import create_rag_chain

# Load environment variables
load_dotenv()

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Advanced RAG System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #E8F4F8;
        border-left: 5px solid #2E86AB;
    }
    .assistant-message {
        background-color: #F0F0F0;
        border-left: 5px solid #FF4B4B;
    }
    .source-box {
        background-color: #FFF9E6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 3px solid #FFD700;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pipeline_ready" not in st.session_state:
    st.session_state.pipeline_ready = False
if "total_docs" not in st.session_state:
    st.session_state.total_docs = 0
if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0

# ============================================================
# HELPER FUNCTIONS
# ============================================================


def initialize_pipeline(data_dir, urls=None):
    """Initialize the RAG pipeline with documents"""
    try:
        with st.spinner("🔄 Loading documents..."):
            # Load documents
            docs = load_all_data(data_dir, urls if urls else [])

            if not docs:
                st.error("❌ No documents found in the data directory!")
                return False

            st.session_state.total_docs = len(docs)

        with st.spinner("✂️ Splitting documents into chunks..."):
            # Split documents
            chunked_docs = split_docs(docs)

            if not chunked_docs:
                st.error("❌ Failed to create document chunks!")
                return False

            st.session_state.total_chunks = len(chunked_docs)

        with st.spinner("🧠 Generating embeddings..."):
            # Initialize embeddings
            embeddings = huggingface_embeddings()

        with st.spinner("💾 Creating/Loading vector store..."):
            # Create or load vectorstore
            if os.path.exists("faiss_index"):
                vectorstore = load_vectorstore(
                    embeddings, vectorstore_path="faiss_index")
                st.info("ℹ️ Loaded existing vector store")
            else:
                vectorstore = create_vectorstore(chunked_docs, embeddings)
                st.success("✅ Created new vector store")

            st.session_state.vectorstore = vectorstore

        with st.spinner("⚡ Building RAG chain..."):
            # Create RAG chain
            rag_chain = create_rag_chain(vectorstore)
            st.session_state.rag_chain = rag_chain
            st.session_state.pipeline_ready = True

        return True

    except Exception as e:
        st.error(f"❌ Error initializing pipeline: {str(e)}")
        return False


def process_query(query):
    """Process user query and return response"""
    try:
        if not st.session_state.pipeline_ready:
            return "⚠️ Please initialize the pipeline first!"

        # Get response from RAG chain
        response = st.session_state.rag_chain.invoke({"input": query})

        # Extract answer and context
        answer = response.get("answer", "No answer available")
        context = response.get("context", [])

        return answer, context

    except Exception as e:
        return f"❌ Error processing query: {str(e)}", []


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.title("⚙️ Configuration")

    st.markdown("---")

    # Data directory input
    st.subheader("📁 Data Source")
    data_dir = st.text_input(
        "Data Directory",
        value="data/",
        help="Directory containing your documents"
    )

    # Optional URLs
    st.subheader("🌐 Web Sources (Optional)")
    urls_input = st.text_area(
        "URLs (one per line)",
        help="Enter URLs to scrape (optional)",
        height=100
    )

    urls = [url.strip() for url in urls_input.split(
        "\n") if url.strip()] if urls_input else None

    st.markdown("---")

    # Initialize/Rebuild button
    if st.button("🚀 Initialize Pipeline"):
        st.session_state.chat_history = []  # Clear chat history
        success = initialize_pipeline(data_dir, urls)

        if success:
            st.success("✅ Pipeline initialized successfully!")
            st.balloons()

    # Reset button
    if st.button("🔄 Reset Chat"):
        st.session_state.chat_history = []
        st.rerun()

    # Rebuild vector store button
    if st.button("🗑️ Rebuild Vector Store"):
        if os.path.exists("faiss_index"):
            import shutil
            shutil.rmtree("faiss_index")
            st.success(
                "✅ Vector store deleted. Click 'Initialize Pipeline' to rebuild.")
        else:
            st.info("ℹ️ No vector store exists.")

    st.markdown("---")

    # Pipeline status
    st.subheader("📊 Pipeline Status")

    if st.session_state.pipeline_ready:
        st.success("✅ Ready")
        st.metric("Documents Loaded", st.session_state.total_docs)
        st.metric("Total Chunks", st.session_state.total_chunks)

        # Vector store info
        if st.session_state.vectorstore:
            st.metric("Vector Dimension", st.session_state.vectorstore.index.d)
            st.metric("Total Vectors",
                      st.session_state.vectorstore.index.ntotal)
    else:
        st.warning("⏸️ Not Initialized")
        st.info("Click 'Initialize Pipeline' to start")

    st.markdown("---")

    # Supported formats
    with st.expander("📄 Supported Formats"):
        st.markdown("""
        - 📕 PDF (.pdf)
        - 📝 Text (.txt)
        - 📘 Word (.docx)
        - 📊 Excel (.xlsx)
        - 📋 CSV (.csv)
        - 🎬 PowerPoint (.pptx)
        - 🌐 Web Pages (URLs)
        """)

    # About section
    with st.expander("ℹ️ About"):
        st.markdown("""
        **Advanced RAG System**
        
        Built with:
        - LangChain
        - FAISS Vector Store
        - Groq LLM
        - HuggingFace Embeddings
        
        Created by: Yasho
        """)

# ============================================================
# MAIN CONTENT AREA
# ============================================================

# Header
st.title("🤖 Advanced RAG System")
st.markdown("### Ask questions about your documents!")

st.markdown("---")

# Check if API key is set
if not os.getenv("GROQ_API_KEY"):
    st.error("⚠️ GROQ_API_KEY not found! Please set it in your .env file.")
    st.stop()

# Main chat interface
if not st.session_state.pipeline_ready:
    st.info("👈 Please initialize the pipeline using the sidebar to get started!")

    # Display instructions
    st.markdown("""
    ### 📋 Getting Started
    
    1. **Add Documents**: Place your files in the `data/` directory
    2. **Configure**: Set the data directory path in the sidebar
    3. **Initialize**: Click 'Initialize Pipeline' in the sidebar
    4. **Ask Questions**: Start chatting with your documents!
    
    ### 💡 Tips
    
    - You can add multiple file formats at once
    - Optionally add web URLs to scrape
    - The vector store is saved locally for faster subsequent loads
    - Use 'Rebuild Vector Store' if you add new documents
    """)

else:
    # Query input
    col1, col2 = st.columns([5, 1])

    with col1:
        user_query = st.text_input(
            "Your Question:",
            placeholder="Ask anything about your documents...",
            key="user_input",
            label_visibility="collapsed"
        )

    with col2:
        ask_button = st.button("🔍 Ask", use_container_width=True)

    # Process query
    if ask_button and user_query:
        # Add user message to chat history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_query
        })

        # Get response
        with st.spinner("🤔 Thinking..."):
            answer, context = process_query(user_query)

        # Add assistant response to chat history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "context": context
        })

    # Display chat history
    st.markdown("---")

    if st.session_state.chat_history:
        for i, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <b>👤 You:</b><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <b>🤖 Assistant:</b><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)

                # # Show sources if available
                # if "context" in message and message["context"]:
                #     with st.expander(f"📚 View Sources ({len(message['context'])} documents)"):
                #         for idx, doc in enumerate(message["context"], 1):
                #             st.markdown(f"""
                #             <div class="source-box">
                #                 <b>Source {idx}:</b><br>
                #                 {doc.page_content[:500]}...
                #                 <br><br>
                #                 <small><i>Metadata: {doc.metadata}</i></small>
                #             </div>
                #             """, unsafe_allow_html=True)
    else:
        st.info("💬 No messages yet. Ask a question to get started!")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 1rem;'>
    <small>Advanced RAG System | Built with ❤️ using Streamlit & LangChain</small>
</div>
""", unsafe_allow_html=True)
