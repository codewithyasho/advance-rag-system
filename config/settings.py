"""
Configuration settings for RAG system
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Paths
WEB_URLS = [

]
PDF_DATA_PATH = "./data/pdf_data"
TEXT_DATA_PATH = "./data/text_data"
NEW_PDF_PATH = "./data/new_pdfs"
NEW_TEXT_PATH = "./data/new_texts"
MODELS_CACHE_PATH = "./models"
