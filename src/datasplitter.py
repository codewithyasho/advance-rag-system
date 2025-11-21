"""
Splits loaded documents into smaller, embedding-friendly chunks.
"""

from langchain_classic.text_splitter import RecursiveCharacterTextSplitter


def split_docs(documents):
    """
    Split loaded documents into chunks for embedding.
    """

    if not documents:
        print("⚠️ No documents to split.")
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    chunked_documents = text_splitter.split_documents(documents)

    print("\n✅✅ Documents split successfully!")
    print(
        f"\n[INFO] Splitted <{len(documents)}> documents into <{len(chunked_documents)}> chunks."
    )
    print("=" * 50)

    return chunked_documents
