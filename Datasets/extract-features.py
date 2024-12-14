# import topmost

# import joblib
import json
import os

import nltk
from nltk.corpus import stopwords

# from topmost.data import download_20ng
from topmost.preprocessing import Preprocessing

# import os
from topmost.data import file_utils
from topmost.utils.logger import Logger


def time2id(_texts: dict, output_path):
    time2id = dict()
    time_index = 0
    
    for time in list(_texts.keys()):
        time2id[time] = time_index
        time_index += 1
    print(time2id)
    with open(os.path.join(output_path, "time2id.txt"), "w") as f:
        f.write(str(time2id))

    return time2id

def build_times(time2id, _texts, output_path, subset: str = 'train'):    
    # Construyendo archivo de tiempos -train -test
    train_time = [time2id[time] for time, info in _texts.items()]

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
    
    return _jsonlist
    

if __name__ == '__main__':
    input_path = 'Ciencias-Médicas/data/Texts'
    jsonlist_path = 'Ciencias-Médicas/jsonlists'
    output_path = 'Ciencias-Médicas/CMed'
    
    os.makedirs(jsonlist_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)

    with open(os.path.join(input_path, 'train_texts.json'), 'r') as f:
        train_texts: dict = json.load(f)
    
    with open(os.path.join(input_path, 'train_texts.json'), 'r') as f:
        test_texts: dict = json.load(f)
    
    _time2id = time2id(train_texts, output_path)
    
    build_times(_time2id, train_texts, output_path)
    build_jsonlist(jsonlist_path, train_texts)
    
    build_times(_time2id, test_texts, output_path, 'test')
    build_jsonlist(jsonlist_path, test_texts, 'test')

    
    nltk.download('stopwords')
    stopwords_es = set(stopwords.words('spanish'))

    preprocessing = Preprocessing(min_term=5, stopwords=stopwords_es)
    logger = Logger("WARNING")
    
    train_items = file_utils.read_jsonlist(os.path.join(jsonlist_path, 'train.jsonlist'))
    test_items = file_utils.read_jsonlist(os.path.join(jsonlist_path, 'test.jsonlist'))
    
    logger.info(f"Found training documents {len(train_items)} testing documents {len(test_items)}")
    
    raw_train_texts = []
    train_labels = None
    raw_test_texts = []
    test_labels = None
    
    for item in train_items:
        raw_train_texts.append(item['text'])
    for item in test_items:
        raw_test_texts.append(item['text'])
        
    rst = preprocessing.preprocess(raw_train_texts, None, raw_test_texts, None)
    preprocessing.save(output_path, **rst)
    
    
        