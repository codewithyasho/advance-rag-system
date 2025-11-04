'''
contains all data loading functions for pdfs, text , word, excel, web pages, json and csv files for RAG system
'''

from pathlib import Path
from langchain_classic.document_loaders import PyMuPDFLoader, TextLoader, WebBaseLoader, CSVLoader, JSONLoader, UnstructuredWordDocumentLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from langchain_excel_loader import StructuredExcelLoader


# 1.DATA INGESTION FUNCTIONS


# 1. read all the pdfs inside the directory

def process_all_pdfs(directory):
    '''Process all pdfs in a directory using PyMuPDF'''

    all_documents = []
    pdf_dir = Path(directory)

    # finding all pdfs recursively
    pdf_files = list(pdf_dir.glob('**/*.pdf'))

    print(f"\n====== Found {len(pdf_files)} PDF files to process ======")

    for file in pdf_files:
        print(f"\n[INFO] Processing: {file.name} file")

        try:
            loader = PyMuPDFLoader(
                str(file)
            )
            documents = loader.load()

            # .extend() adds individual items to the list
            all_documents.extend(documents)

            print(
                f"\n✅ Successfully Loaded <{len(documents)}> pages from {file.name}")
            print("=" * 50)

        except Exception as e:
            print(f"❌ Error processing {file.name}: {e}")
            continue

    print(f"\n\n[INFO] Total PDF documents loaded: <{len(all_documents)}>\n")

    return all_documents


# ==========================================================================

# 2. read all the text files inside the directory

def process_all_texts(directory):
    '''Process all text files in a directory'''

    all_documents = []
    text_dir = Path(directory)

    # finding all text files recursively
    text_files = list(text_dir.glob('**/*.txt'))

    print(f"\n====== Found {len(text_files)} text files to process ======")

    for file in text_files:
        print(f"\n[INFO] Processing: {file.name} file")

        try:
            loader = TextLoader(
                str(file)
            )
            documents = loader.load()

            # .extend() adds individual items to the list
            all_documents.extend(documents)

            print(
                f"\n✅ Successfully Loaded <{len(documents)}> pages from {file.name}")
            print("=" * 50)

        except Exception as e:
            print(f"❌ Error processing {file.name}: {e}")
            continue

    print(f"\n\n[INFO] Total TEXT documents loaded: <{len(all_documents)}>\n")

    return all_documents


# ==========================================================================

# 3. read all the web pages from a list of urls

def process_all_webpages(urls):
    '''Process all web pages in a list'''

    all_documents = []

    print(f"\n====== Found {len(urls)} web pages to process ======")

    for url in urls:
        print(f"\n[INFO] Processing: {url} web page")

        try:
            loader = WebBaseLoader(
                url
            )
            documents = loader.load()

            # .extend() adds individual items to the list
            all_documents.extend(documents)

            print(
                f"\n✅ Successfully Loaded <{len(documents)}> pages from {url}")
            print("=" * 50)

        except Exception as e:
            print(f"❌ Error processing {url}: {e}")
            continue

    print(
        f"\n\n[INFO] Total WEBPAGE documents loaded: <{len(all_documents)}>\n")

    return all_documents


# ==========================================================================

# 5. load all csv files in a directory

def process_all_csvs(directory):
    '''Process all csv files in a directory'''

    all_documents = []
    csv_dir = Path(directory)

    # finding all csv files recursively
    csv_files = list(csv_dir.glob('**/*.csv'))

    print(f"\n====== Found {len(csv_files)} CSV files to process ======")

    for file in csv_files:
        print(f"\n[INFO] Processing: {file.name} file")

        try:
            loader = CSVLoader(str(file))
            documents = loader.load()

            # .extend() adds individual items to the list
            all_documents.extend(documents)

            print(
                f"\n✅ Successfully Loaded <{len(documents)}> pages from {file.name}")
            print("=" * 50)

        except Exception as e:
            print(f"❌ Error processing {file.name}: {e}")
            continue

    print(f"\n\n[INFO] Total CSV documents loaded: <{len(all_documents)}>\n")

    return all_documents


# ==========================================================================

# 6. load all excel files in a directory using langchain_excel_loader

def process_all_excels(directory):
    '''Process all excel files in a directory'''

    all_documents = []
    excel_dir = Path(directory)

    # finding all excel files recursively
    excel_files = list(excel_dir.glob('**/*.xlsx'))

    print(f"\n====== Found {len(excel_files)} Excel files to process ======")

    for file in excel_files:
        print(f"\n[INFO] Processing: {file.name} file")

        try:
            loader = StructuredExcelLoader(str(file))
            documents = loader.load()

            # .extend() adds individual items to the list
            all_documents.extend(documents)

            print(
                f"\n✅ Successfully Loaded <{len(documents)}> pages from {file.name}")
            print("=" * 50)

        except Exception as e:
            print(f"❌ Error processing {file.name}: {e}")
            continue

    print(f"\n\n[INFO] Total EXCEL documents loaded: <{len(all_documents)}>\n")

    return all_documents


# ==========================================================================

# 7. load all word files in a directory UnstructuredWordDocumentLoader

def process_all_word_docs(directory):
    '''Process all word files in a directory'''

    all_documents = []
    word_dir = Path(directory)

    # finding all word files recursively
    word_files = list(word_dir.glob('**/*.docx'))

    print(f"\n====== Found {len(word_files)} Word files to process ======")

    for file in word_files:
        print(f"\n[INFO] Processing: {file.name} file")

        try:
            loader = UnstructuredWordDocumentLoader(str(file))
            documents = loader.load()

            # .extend() adds individual items to the list
            all_documents.extend(documents)

            print(
                f"\n✅ Successfully Loaded <{len(documents)}> pages from {file.name}")
            print("=" * 50)

        except Exception as e:
            print(f"❌ Error processing {file.name}: {e}")
            continue

    print(f"\n\n[INFO] Total WORD documents loaded: <{len(all_documents)}>\n")

    return all_documents


# ==========================================================================


# 8. load all the pptx files inside the directory

def process_all_pptx(directory):
    '''Process all pptx files in a directory using UnstructuredPowerPointLoader'''

    all_documents = []
    pptx_dir = Path(directory)

    # finding all pptx files recursively
    pptx_files = list(pptx_dir.glob('**/*.pptx'))

    print(f"\n====== Found {len(pptx_files)} PPTX files to process ======")

    for file in pptx_files:
        print(f"\n[INFO] Processing: {file.name} file")

        try:
            loader = UnstructuredPowerPointLoader(
                str(file)
            )
            documents = loader.load()

            # .extend() adds individual items to the list
            all_documents.extend(documents)

            print(
                f"\n✅ Successfully Loaded <{len(documents)}> pages from {file.name}")
            print("=" * 50)

        except Exception as e:
            print(f"❌ Error processing {file.name}: {e}")
            continue

    print(f"\n\n[INFO] Total PPTX documents loaded: <{len(all_documents)}>\n")

    return all_documents


# ==========================================================================

# ====================================================================
# COMBINED DATA LOADER (Optional)
# ====================================================================

def load_all_data(directory, urls=None):
    """
    Load all supported file types + optional web pages from a directory.
    """
    all_docs = []
    all_docs += process_all_pdfs(directory)
    all_docs += process_all_texts(directory)
    all_docs += process_all_word_docs(directory)
    all_docs += process_all_csvs(directory)
    all_docs += process_all_excels(directory)
    all_docs += process_all_pptx(directory)
    if urls:
        all_docs += process_all_webpages(urls)

    print(f"🎯 Total documents loaded from all sources: {len(all_docs)}")

    return all_docs


# =====================================================================
# END OF FILE
