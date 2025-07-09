from utils import load_files_from_folder

def clear_text(text):
    pass

if __name__ == "__main__":
    data_path = "../../data/texts-jsonlists"

    texts = [f[1]["text"] for f in load_files_from_folder(data_path, "json")]
    print(len(texts))
    print(texts[0][:50])
