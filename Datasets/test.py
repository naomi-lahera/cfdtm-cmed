import joblib
import json
import os
import re
from unicodedata import normalize
import pymupdf4llm
import traceback
import random

def time2id(_texts: dict, output_path):
    time2id = dict()
    time_index = 0
    
    for time in list(_texts.keys()):
        time2id[time] = time_index
        time_index += 1
        
    # print(time2id)
    with open(os.path.join(output_path, "time2id.txt"), "w") as f:
        f.write(str(time2id))

    return time2id

def build_times(time2id, _texts, output_path, subset: str = 'train'): 
    train_time = [] 
    # Construyendo archivo de tiempos -train -test
    for time, info in _texts.items():
        train_time.extend([time2id[time]]*len(info))
       
    # train_time = [time2id[time] for time, info in _texts.items()]

    with open(os.path.join(output_path, f"{subset}_times.txt"), "w") as f:
        for elemento in train_time:
            f.write(str(elemento) + "\n")

    
def build_jsonlist(_path: str, _texts: dict, subset: str = 'train'):
    _jsonlist = []
    for time, texts in _texts.items():
        _jsonlist.extend([{"text": text} for text in texts])

    with open(os.path.join(_path, f"{subset}.jsonlist"), "w") as f:
        for record in _jsonlist:
            f.write(json.dumps(record) + "\n")
    
    # print(_jsonlist)
    # print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
    return _jsonlist

def eliminar_tildes():
    label = 'caída-del-moño'
    current_label = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", label), flags=re.I
    )
    current_label = normalize('NFC', current_label)
    print(current_label)
    
def extract_text():
    pdf_path = 'Ciencias-Médicas/data/PDF/2010/ciencias-quirúrgicas/292.pdf'
    errors_path = 'Ciencias-Médicas/data/Texts/extract-text-errors'
    error_data = {"year": '2010', "label": 'ciencias-quirúrgicas'}
    os.makedirs(errors_path, exist_ok=True)
    
    md_read = pymupdf4llm.LlamaMarkdownReader()
    try:
        data = md_read.load_data(pdf_path)
    except Exception as e:
        # count = len(os.listdir(errors_path))
        error_info = {
        "error_type": type(e).__name__,  # Tipo de la excepción (e.g., ZeroDivisionError)
        "error_message": str(e),        # Mensaje del error
        "stack_trace": traceback.format_exc()  # Traza completa del error
        }
        new_error_path = os.path.join(errors_path, error_data["year"], error_data["label"])
        os.makedirs(new_error_path, exist_ok=True)
        try:
            with open(os.path.join(new_error_path, f'errors.json'), 'r') as f:
                errors: list = json.load(f)
        except:
            errors = []
                
        errors.append({"error": error_info, "pdf_path": pdf_path})
        
        with open(os.path.join(new_error_path, f'errors.json'), 'w') as f:
            json.dump(errors, f)
            
        return None
                
    text = ''
    for page in range(len(data)):
        text += data[page].to_dict()["text"]
        
    specialChars = "!#$%^&*()"
    for specialChar in specialChars:
        text = text.replace(specialChar, ' ')
        
    return text

def train_test_split():
    jsonlists_per_year = {"2001": 
                            [{"label": 1, "text": "text 1"}, {"label": 1, "text": "text 2"}],
                        "2002":
                            [{"label": 1, "text": "text 3"}, {"label": 2, "text": "text 4"}],
                        "2002":
                            [{"label": 3, "text": "text 5"}, {"label": 4, "text": "text 6"}, {"label": 3, "text": "text 5"}]}
    
    train_jsonlist_per_year, test_jsonlist_per_year = dict(), dict()
    
    for year, jsonlist in jsonlists_per_year.items():
        train_jsonlist_per_year[year] = []
        test_jsonlist_per_year[year] = []
        
        texts_per_label_dict = dict()
        
        for item in jsonlist:
            label = item["label"]
            text = item["text"]
            
            if label not in texts_per_label_dict:
                texts_per_label_dict[label] = [text]  # Crear una nueva lista con el elemento
            else:
                texts_per_label_dict[label].append(text)
                
        for label, texts in texts_per_label_dict.items():
            total_train_docs = int(0.7 * len(texts))
            train_jsonlist_per_year[year].extend([{"label": label, "text": text} for text in texts[:total_train_docs]])
            test_jsonlist_per_year[year].extend([{"label": label, "text": text} for text in texts[total_train_docs:]])
            
    print("Train: ", train_jsonlist_per_year)
    print("Test: ", test_jsonlist_per_year)

def shuffle_set():
    jsonlist_per_year = {"2001": 
                            [{"label": 1, "text": "text 1"}, {"label": 1, "text": "text 2"}],
                        "2002":
                            [{"label": 1, "text": "text 3"}, {"label": 2, "text": "text 4"}],
                        "2002":
                            [{"label": 3, "text": "text 5"}, {"label": 4, "text": "text 6"}, {"label": 3, "text": "text 5"}]}
    
    year_label_text_json = [{"year": year, "label": doc["label"], "text": doc["text"]} for year, list_ in jsonlist_per_year.items() for doc in list_]
    return random.shuffle(year_label_text_json)

def build_subset_times():
    year_label_text_jsons = [{"year": "2001", "label": 3, "text": "text 5"}]
    time2id = {"2001": 0, "2002": 1, "2003": 2}
    subset = 'train'
    output_path = path
    
    times = [time2id[doc["year"]] for doc in year_label_text_jsons]
    with open(os.path.join(output_path, f"{subset}_times.txt"), "w") as f:
        for elemento in times:
            f.write(str(elemento) + "\n")

def build_jsonlist():
    year_label_text_jsons = [{"year": "2001", "label": 3, "text": "text 5"}]
    subset = 'train'
    output_path = path
    
    jsonlist = [{"label": doc["label"], "text": doc["text"]} for doc in year_label_text_jsons]
    with open(os.path.join(output_path, f"{subset}.jsonlist"), "w") as f:
        for record in jsonlist:
            f.write(json.dumps(record) + "\n")

if __name__ == '__main__':
    path = './unittest'
    os.makedirs(path, exist_ok=True)
    
    # input_path = 'Ciencias-Médicas/data/Texts'
    # jsonlist_path = 'Ciencias-Médicas/jsonlists'
    # output_path = 'Ciencias-Médicas/CMed'
    
    # os.makedirs(jsonlist_path, exist_ok=True)
    # os.makedirs(output_path, exist_ok=True)

    # with open(os.path.join(input_path, 'train_texts.json'), 'r') as f:
        # train_texts: dict = json.load(f)
    
    # with open(os.path.join(input_path, 'test_texts.json'), 'r') as f:
        # test_texts: dict = json.load(f)
        
    # train_texts = joblib.load(os.path.join(input_path, 'train_texts.joblib'))
    # test_texts = joblib.load(os.path.join(input_path, 'test_texts.joblib'))
    
    # _time2id = time2id(train_texts, output_path)
    
    # build_times(_time2id, train_texts, output_path)
    # # build_jsonlist(jsonlist_path, train_texts)
    
    # build_times(_time2id, test_texts, output_path, 'test')
    # # build_jsonlist(jsonlist_path, test_texts, 'test')
    
    # eliminar_tildes()
    
    # extract_text()
    
    train_test_split()
    # shuffle_set()
