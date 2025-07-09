import os
import json
    
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"✅ File {file_path} successfully loaded")
    return data

def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = "/n".join(f.readlines())
    print(f"✅ File {file_path} successfully loaded")
    return text

def load_files_from_folder(folder_path, format):
    files = [(f.name, f.path) for f in os.scandir(folder_path) if f.is_file()]
    texts = [(f[0], file_formats[format](f[1])) for f in files]
    print(f"✅ {len(texts)} files successfully loaded from  {folder_path}")
    return texts

file_formats = {
    "txt": load_txt,
    "json": load_json}