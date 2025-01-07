import pymupdf4llm
import os

def extract_text_test():
    # Uso del código
    path_base = "Ciencias-Médicas/data/PDF/2024/"
    pdf_paths = ["editorial/0.pdf", "ciencias-clínicas-y-patológicas/11.pdf"]
    for path in pdf_paths:
        # text_per_page = extract_text_from_pdf(os.path.join(path_base,path), use_ocr=True)
        # text_per_page = extract_text_from_pdf(os.path.join(path_base,path))
        print(f'{path_base}{path}')

        md_read = pymupdf4llm.LlamaMarkdownReader()
        data = md_read.load_data(os.path.join(path_base,path))
        text = ''
        for page in range(len(data)):
            text += data[page].to_dict()["text"]

        print(text)
        print('\n')
        
def join_dict_test():
    jsonlist_per_year_0 = {'a': [1,2,3], 'b': [1]}
    jsonlist_per_year_1 = {'a': [1,2,3], 'b': [1]}
    
    current_dict_0: dict = {'b': [2,3], 'c': [1,2,3]}
    current_dict_1: dict = {'c': [1,2,3], 'd': [1,2,3]}
    last_key_0 = list(jsonlist_per_year_0.items())[-1][0]
    last_key_1 = list(jsonlist_per_year_1.items())[-1][0]
    try:
        jsonlist_per_year_0[last_key_0].extend(current_dict_0[last_key_0])
        del current_dict_0[last_key_0]
        jsonlist_per_year_1[last_key_1].extend(current_dict_1[last_key_1])
        del current_dict_1[last_key_1]
    except:
        pass
    
    jsonlist_per_year_0.update(current_dict_0)
    print(jsonlist_per_year_0)
    jsonlist_per_year_1.update(current_dict_1)
    print(jsonlist_per_year_1)
    
def exist_file():
    print(os.path.isfile('Ciencias-Médicas/data/PDF/2024/ciencias-clínicas-y-patológicas/18.pdf'))

def remove_file():
    os.remove('Ciencias-Médicas/data/PDF/2024/ciencias-clínicas-y-patológicas/18.pdf')

import json
import requests 
def fix_errors(path):
    for file in [f for f in os.scandir(path) if f.is_file()]:
        with open(file, 'r') as f:
            art = json.load(f)
            pdf_path = os.path.join(art['year'], art['label'], f"{art['index']}.pdf")
            if not os.path.isfile(pdf_path): 
                try:
                    text = requests.get(art['downliadLink']).content
                    with open(pdf_path, "wb") as f:
                        f.write(text)
                    os.remove(file.name)
                    print(f"PDF descargado con éxito en {pdf_path}. ✅")
                except Exception as e:
                    print(f"❌ Error al descargar el PDF para '{art['downliadLink']}': {e}")
                    print('\\'*50)
                    
def ls(path):
    print('Scan Dir')
    for item in [f for f in os.scandir(path) if f.is_file()]:
        print(item.name)

errors_path = 'Ciencias-Médicas/data/PDF/errors'
fix_errors(errors_path)