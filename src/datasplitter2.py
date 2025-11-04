from langchain_classic.text_splitter import RecursiveCharacterTextSplitter


# 2.SPLITTING DOCUMENTS INTO CHUNKS

# splitting loaded documents into smaller chunks
def split_docs(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    chunked_documents = text_splitter.split_documents(documents)

    print("\n✅✅ Document Splitted successfully!")

    print(
        f"\n[INFO] Splitted <{len(documents)}> documents into <{len(chunked_documents)}> chunks.")
    
    print("=" * 50)

    return chunked_documents
