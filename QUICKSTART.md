# 🚀 Quick Start Guide - Web Application

## Running the Streamlit App

1. **Ensure all dependencies are installed:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Make sure your `.env` file is configured:**
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Start the web application:**
   ```bash
   streamlit run app.py
   ```

4. **Your browser will automatically open to:** `http://localhost:8501`

## Using the Web Interface

### Sidebar Controls

- **📁 Data Source**: Set the path to your documents folder (default: `data/`)
- **🌐 Web Sources**: Optionally add URLs to scrape (one per line)
- **🚀 Initialize Pipeline**: Load documents and build the RAG system
- **🔄 Reset Chat**: Clear the conversation history
- **🗑️ Rebuild Vector Store**: Delete and rebuild the FAISS index

### Main Interface

1. **Initialize the Pipeline** (first time):
   - Click "Initialize Pipeline" in the sidebar
   - Wait for documents to load and embeddings to generate
   - Status will show "✅ Ready" when complete

2. **Ask Questions**:
   - Type your question in the input box
   - Click "🔍 Ask" or press Enter
   - View the AI-generated answer

3. **View Sources**:
   - Expand "📚 View Sources" below any answer
   - See the exact document chunks used to generate the response

### Features

✨ **Beautiful UI** - Clean, modern interface with custom styling
📊 **Real-time Status** - Monitor pipeline state and vector store metrics
💬 **Chat History** - Conversation is preserved during your session
📚 **Source Citations** - See which documents were used for each answer
⚙️ **Easy Configuration** - Adjust settings without editing code
🔄 **Hot Reload** - Make changes and refresh to see updates

## Troubleshooting

### Port Already in Use
If port 8501 is busy, specify a different port:
```bash
streamlit run app.py --server.port 8502
```

### API Key Issues
Ensure your `.env` file exists in the project root and contains:
```env
GROQ_API_KEY=your_actual_api_key_here
```

### Memory Issues
If you get memory errors:
- Reduce the number of documents
- Lower the batch size in `src/embedding.py`
- Use CPU instead of GPU for embeddings

## Tips for Best Results

1. **Organize Your Documents**: Place all files in the `data/` directory
2. **Use Descriptive Names**: Name files clearly for better source tracking
3. **Specific Questions**: Ask focused questions for better answers
4. **Check Sources**: Review source documents to verify information
5. **Rebuild When Needed**: Add new docs? Rebuild the vector store!

## Keyboard Shortcuts

- **Ctrl + R** (or **Cmd + R**): Refresh the page
- **Ctrl + K**: Focus on the question input box

## Deployment Options

### Local Network Access
```bash
streamlit run app.py --server.address 0.0.0.0
```
Access from other devices on your network using your computer's IP address.

### Streamlit Cloud (Free Hosting)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets (GROQ_API_KEY) in the Streamlit dashboard
5. Deploy!

---

**Need Help?** Check the main README.md or open an issue on GitHub!
