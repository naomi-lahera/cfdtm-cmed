import joblib
import os
import random
import json

def build_jsonlist(year_label_text_jsons, subset, output_path):
    jsonlist = [{"label": doc["label"], "text": doc["text"]} for doc in year_label_text_jsons]
    with open(os.path.join(output_path, f"{subset}.jsonlist"), "w") as f:
        for record in jsonlist:
            f.write(json.dumps(record) + "\n")
    
def build_subset_times(year_label_text_jsons: list, time2id, subset, output_path):
    times = [time2id[doc["year"]] for doc in year_label_text_jsons]
    with open(os.path.join(output_path, f"{subset}_times.txt"), "w") as f:
        for elemento in times:
            f.write(str(elemento) + "\n")

def shuffle_set(jsonlist_per_year: dict):
    year_label_text_json = [{"year": year, "label": doc["label"], "text": doc["text"]} for year, list_ in jsonlist_per_year.items() for doc in list_]
    return random.shuffle(year_label_text_json)

def train_test_split(jsonlists_per_year: dict):
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
            
    return train_jsonlist_per_year, test_jsonlist_per_year
                
            
def build_time2id(years):
    time2id = dict()
    for i, year in enumerate(years):
        time2id[year] = i
    return time2id

if __name__ == '__main__':
    input_path = 'Ciencias-Médicas/jsonlists'
    metadata_output_path = 'Ciencias-Médicas/CMed'
    os.makedirs(metadata_output_path, exist_ok=True)
    
    jsonlists_per_year: dict = joblib.load(os.path.join(input_path, 'pre-jsonlist.joblib'))
    
    time2id = build_time2id(jsonlists_per_year.keys())
    train_jsonlist_per_year, test_jsonlist_per_year = train_test_split(jsonlists_per_year)
    
    train_year_label_text_jsons, test_year_label_text_jsons = shuffle_set(train_jsonlist_per_year), shuffle_set(test_jsonlist_per_year)
    
    build_subset_times(train_year_label_text_jsons, time2id, 'train', metadata_output_path)
    build_subset_times(test_year_label_text_jsons, time2id, 'test', metadata_output_path)
    
    build_jsonlist(train_year_label_text_jsons, 'train', input_path)
    build_jsonlist(test_year_label_text_jsons, 'test', input_path)
    