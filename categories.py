import os

CATEGORY_MAP = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"},
    "Spreadsheets": {".xls", ".xlsx", ".csv"},
    "Presentations": {".ppt", ".pptx"},
    "Videos": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".webm"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".json", ".xml"},
    "Executables": {".exe", ".msi", ".bat", ".sh", ".app"},
}

CATEGORY_FOLDERS = set(CATEGORY_MAP.keys())
OTHERS = "Others"

SKIP_FILES = {"desktop.ini", "thumbs.db", ".ds_store"}


def get_category(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    for category, extensions in CATEGORY_MAP.items():
        if ext in extensions:
            return category
    return OTHERS
