import joblib
import json
import os

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


if __name__ == '__main__':
    input_path = 'Ciencias-Médicas/data/Texts'
    jsonlist_path = 'Ciencias-Médicas/jsonlists'
    output_path = 'Ciencias-Médicas/CMed'
    
    os.makedirs(jsonlist_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)

    # with open(os.path.join(input_path, 'train_texts.json'), 'r') as f:
        # train_texts: dict = json.load(f)
    
    # with open(os.path.join(input_path, 'test_texts.json'), 'r') as f:
        # test_texts: dict = json.load(f)
        
    train_texts = joblib.load(os.path.join(input_path, 'train_texts.joblib'))
    test_texts = joblib.load(os.path.join(input_path, 'test_texts.joblib'))
    
    _time2id = time2id(train_texts, output_path)
    
    build_times(_time2id, train_texts, output_path)
    # build_jsonlist(jsonlist_path, train_texts)
    
    build_times(_time2id, test_texts, output_path, 'test')
    # build_jsonlist(jsonlist_path, test_texts, 'test')
