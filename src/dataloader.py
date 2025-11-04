'''
contains all data loading functions for pdfs, text , word, excel, web pages, json and csv files for RAG system
'''

from pathlib import Path
import json
from langchain_classic.document_loaders import PyMuPDFLoader, TextLoader, WebBaseLoader, CSVLoader, JSONLoader, UnstructuredWordDocumentLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from langchain_classic.docstore.document import Document
from langchain_excel_loader import StructuredExcelLoader


# 1.DATA INGESTION FUNCTIONS

# MAIN FUCTION TO PROCESS DIFFERENT FILE TYPES

def process_files(directory, pattern, loader_class, loader_kwargs=None):
    all_documents = []
    directory = Path(directory)
    loader_kwargs = loader_kwargs or {}

    files = list(directory.glob(f'**/*{pattern}'))
    print(
        f"\n====== Found {len(files)} {pattern.upper()} files to process ======")

    for file in files:
        print(f"\n[INFO] Processing: {file.name}")
        try:
            loader = loader_class(str(file), **loader_kwargs)
            docs = loader.load()
            all_documents.extend(docs)
            print(f"✅ Loaded <{len(docs)}> pages from {file.name}")
            print("=" * 50)
        except Exception as e:
            print(f"❌ Error processing {file.name}: {e}")
            continue

    print(
        f"\n[INFO] Total {pattern.upper()} docs loaded: <{len(all_documents)}>\n")
    return all_documents


# ====================================================================
# SPECIFIC FILE TYPE PROCESSING FUNCTIONS

# 1. read all the pdfs inside the directory
def process_all_pdfs(directory):
    return process_files(directory, ".pdf", PyMuPDFLoader)


# 2. read all the text files inside the directory
def process_all_texts(directory):
    # Add encoding and error handling for text files
    return process_files(
        directory,
        ".txt",
        TextLoader,
        loader_kwargs={"encoding": "utf-8", "autodetect_encoding": True}
    )


# 3. load all excel files in a directory using langchain_excel_loader
def process_all_excels(directory):
    return process_files(directory, ".xlsx", StructuredExcelLoader)


# 4. load all word files in a directory UnstructuredWordDocumentLoader
def process_all_word_docs(directory):
    return process_files(directory, ".docx", UnstructuredWordDocumentLoader)


# 5. load all csv files in a directory
def process_all_csvs(directory):
    # Add encoding for CSV files
    return process_files(
        directory,
        ".csv",
        CSVLoader,
        loader_kwargs={"encoding": "utf-8"}
    )


# 7. read all the web pages from a list of urls

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
