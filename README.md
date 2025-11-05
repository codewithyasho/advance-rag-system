# 🚀 Advanced RAG Pipeline

A professional Retrieval-Augmented Generation (RAG) system built with LangChain, FAISS, and Groq LLM. This pipeline supports multiple document formats and provides intelligent question-answering capabilities.

## ✨ Features

- 📄 **Multi-Format Support**: PDF, TXT, DOCX, CSV, PPTX, XLSX, and web pages
- 🧠 **Smart Document Chunking**: Recursive text splitting with optimal chunk sizes
- 🔍 **Vector Search**: FAISS-based similarity search with cosine distance
- ⚡ **Fast Inference**: Powered by Groq LLM for quick responses
- 🎯 **Flexible Embeddings**: Support for both HuggingFace and Ollama embeddings
- 💾 **Persistent Storage**: Save and load vector indices for efficiency
- 🖥️ **GPU Support**: Automatic GPU detection for faster embedding generation

## 📁 Project Structure

```
project14-Advance-rag-pipeline/
├── main.py                 # Main entry point for RAG pipeline
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project metadata
├── README.md              # This file
├── .env                   # Environment variables (create this)
├── config/
│   ├── __init__.py
│   └── settings.py        # Configuration settings
├── data/
│   └── pdf_files/         # Place your documents here
├── faiss_index/           # Vector store (auto-generated)
│   └── index.faiss
└── src/
    ├── __init__.py
    ├── dataloader.py      # Document loading utilities
    ├── datasplitter.py    # Text chunking logic
    ├── embedding.py       # Embedding model setup
    ├── vectorstore.py     # FAISS vector store operations
    ├── chain.py           # RAG chain configuration
    └── utils.py           # Utility functions
```

## 🛠️ Installation

### Prerequisites

- Python 3.12 or higher
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/codewithyasho/advance-rag-system.git
   cd advance-rag-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   .\venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here  # Optional
   ```

   Get your Groq API key from: https://console.groq.com/

5. **Add your documents**
   
   Place your documents in the `data/` directory:
   - PDFs → `data/pdf_files/`
   - Other formats supported: TXT, DOCX, CSV, PPTX, XLSX

## 🚀 Usage

### Option 1: Web Application (Recommended)

Run the Streamlit web interface:

```bash
streamlit run app.py
```

This will open a beautiful web interface in your browser where you can:
- 📊 Monitor pipeline status
- 💬 Chat with your documents
- 📚 View source documents for each answer
- ⚙️ Configure settings easily
- 🔄 Reset or rebuild the vector store

### Option 2: Command Line

Run the terminal-based pipeline:

```bash
python main.py
```

The pipeline will:
1. Load all documents from the `data/` directory
2. Split them into chunks
3. Create embeddings
4. Build/load FAISS vector store
5. Start an interactive Q&A session

### Interactive Mode (CLI)

Once running, you can ask questions about your documents:

```
Enter your question: What is this document about?

🧠 AI Answer:
[Response based on your documents]
============================================================

Enter your question: exit  # Type 'exit' to quit
```

### Adding More Documents

1. Add new files to the `data/` directory
2. Delete the `faiss_index/` folder to rebuild the vector store
3. Run `python main.py` again

## 🔧 Configuration

### Embedding Models

**HuggingFace (Default)**
```python
# In src/embedding.py
embeddings = huggingface_embeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

**Ollama Alternative**
```python
# Uncomment in main.py
from src.embedding import ollama_embeddings
embeddings = ollama_embeddings(model_name="nomic-embed-text")
```

### Chunk Size Configuration

Adjust in `src/datasplitter.py`:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Modify this
    chunk_overlap=200,    # Modify this
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)
```

### Retrieval Settings

Modify in `src/chain.py`:
```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}  # Number of chunks to retrieve
)
```

### LLM Configuration

Change model in `src/chain.py`:
```python
llm = ChatGroq(
    model="openai/gpt-oss-120b",  # Try: llama-3.3-70b-versatile, etc.
    temperature=0.7,               # Adjust creativity (0.0-1.0)
)
```

## 📚 Supported File Formats

| Format | Extension | Loader |
|--------|-----------|--------|
| PDF | `.pdf` | PyMuPDFLoader |
| Text | `.txt` | TextLoader |
| Word | `.docx` | UnstructuredWordDocumentLoader |
| Excel | `.xlsx` | StructuredExcelLoader |
| CSV | `.csv` | CSVLoader |
| PPTX | `.pptx` | UnstructuredPowerPointLoader |
| Web | URLs | WebBaseLoader |

## 🎯 Advanced Features

### Adding Web Pages

Edit `main.py`:
```python
urls = [
    "https://example.com/article1",
    "https://example.com/article2"
]
docs = load_all_data(data_dir, urls)
```

### Using GPU Acceleration

The system automatically detects and uses GPU if available:
- CUDA-enabled GPU for faster embeddings
- Falls back to CPU if GPU is unavailable

### Persistent Vector Store

- First run: Creates `faiss_index/`
- Subsequent runs: Loads existing index (much faster)
- To rebuild: Delete `faiss_index/` folder

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
pip install --upgrade langchain langchain-groq langchain-huggingface
```

**2. FAISS Installation Issues**
```bash
# For CPU
pip install faiss-cpu

# For GPU (if you have CUDA)
pip install faiss-gpu
```

**3. API Key Errors**
- Ensure `.env` file exists in root directory
- Check that `GROQ_API_KEY` is set correctly
- Restart terminal after setting environment variables

**4. Out of Memory**
- Reduce `chunk_size` in datasplitter.py
- Reduce `batch_size` in embedding.py
- Process fewer documents at once

## 📊 Performance Tips

1. **Use GPU**: Significantly faster embedding generation
2. **Batch Processing**: Increase `batch_size` for faster embedding (if memory allows)
3. **Persistent Index**: Keep `faiss_index/` folder for quick loading
4. **Optimize Chunks**: Balance between chunk_size (context) and retrieval speed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Yasho**
- GitHub: [@codewithyasho](https://github.com/codewithyasho)

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/) - Framework for LLM applications
- [Groq](https://groq.com/) - Fast LLM inference
- [FAISS](https://github.com/facebookresearch/faiss) - Efficient similarity search
- [HuggingFace](https://huggingface.co/) - Embedding models

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section above

---

Made with ❤️ by Yasho | Star ⭐ this repo if you find it helpful!
