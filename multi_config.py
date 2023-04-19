import os

NEW_FILES_DIR_LOCAL = f"NEW_FILES"
NEW_FILES_DIR_SERVER = f"{os.sep}home{os.sep}chatbot_root{os.sep}Zayed-Chatbot-Server{os.sep}zu_data"
SAVE_FILES_DIR = "CSV"
SAVE_FILE_NAME = "MAIN.csv"
SAVE_ARABIC_FILE_NAME = "ARABIC.csv"
DOWNLOAD_FILES = True
NUMBER_OF_PROCESSES = 2

FILES_TO_FETCH = [
    "https://www.zu.ac.ae/main/en/all_pages_json.json",
    "https://www.zu.ac.ae/main/en/all_pages.xml",
    "https://www.zu.ac.ae/main/ar/all_pages_ar.xml",
    "https://www.zu.ac.ae/main/en/all_news.xml",
    "https://www.zu.ac.ae/main/ar/all_news_ar.xml",
    "https://www.zu.ac.ae/main/en/all_files.xml",
    "https://eservices.zu.ac.ae/WebService/GetServices"
]

EXTENSION_LIST = [".JS", ".XLT", ".DOCX", ".DOT", ".CSS", ".JBG", ".PPTX", ".NBD", ".DB", 
    ".JPG", ".PNG", ".XLSX", ".XSLX", ".PDF", ".DOC", ".JPEG", ".GIF", ".CSV", ".SWF", ".PPT",
    ".XLS", ".PPSX", ".PSD", ".MP3", ".BMP", ".RTF", ".MP4", ".ACAD", 
]