import joblib
import json
import os

output_path = 'features'
os.makedirs(output_path, exist_ok=True)

input_path = 'Datasets (manual)'
train_texts_path = os.path.join(input_path, 'train', 'train_texts.joblib')
test_texts_path = os.path.join(input_path, 'test', 'test_texts.joblib')

# Cargando textos
train_texts = joblib.load(train_texts_path)
test_texts = joblib.load(test_texts_path)

#Asigando id a cada uno de los segmentos de tiempo
time2id = dict()
time_index = 0
for time in set(list(train_texts.keys()) + list(test_texts.keys())):
    time2id[time] = time_index
    time_index += 1
print(time2id)
with open(os.path.join(output_path, "time2id.txt"), "w") as f:
    f.write(str(time2id))
    
# Construyendo archivo de tiempos -train -test
train_time = [time2id[time] for time, info in train_texts.items()]
test_time = [time2id[time] for time, info in test_texts.items()]

with open(os.path.join(output_path, "train_times.txt"), "w") as f:
    for elemento in train_time:
        f.write(str(elemento) + "\n")
with open(os.path.join(output_path, "test_times.txt"), "w") as f:
    for elemento in test_time:
        f.write(str(elemento) + "\n")

# Construyendo train.jsonlist y test.jsonlist
train_jsonlist = []
for time, texts in train_texts.items():
    train_jsonlist.extend([{"text": text} for text in texts])
# train_texts = [{"text": info} for time, info in train_texts.items()]


test_jsonlist = []
for time, texts in train_texts.items():
    test_jsonlist.extend([{"text": text} for text in texts])
# test_texts = [{"text": info} for time, info in test_texts.items()]


with open(os.path.join(input_path, "train.jsonlist"), "w") as f:
    for record in train_jsonlist:
        # Convertir el diccionario a JSON y escribir una línea
        f.write(json.dumps(record) + "\n")
        
with open(os.path.join(input_path, "test.jsonlist"), "w") as f:
    for record in test_jsonlist:
        f.write(json.dumps(record) + "\n")
        
        
#-----------------------------------------------TopMOst------------------------------------------------------------#
import nltk
from nltk.corpus import stopwords

from topmost.data import download_20ng
from topmost.preprocessing import Preprocessing

nltk.download('stopwords')
stopwords_es = set(stopwords.words('spanish'))
# print(stopwords_es) 


# preprocess raw data
preprocessing = Preprocessing(min_term=5, stopwords=stopwords_es)
import os
from topmost.data import file_utils
from topmost.utils.logger import Logger


logger = Logger("WARNING")

def preprocess_jsonlist(dataset_dir, label_name=None):
      train_items = file_utils.read_jsonlist(os.path.join(dataset_dir, 'train.jsonlist'))
      test_items = file_utils.read_jsonlist(os.path.join(dataset_dir, 'test.jsonlist'))

      logger.info(f"Found training documents {len(train_items)} testing documents {len(test_items)}")

      raw_train_texts = []
      train_labels = None
      raw_test_texts = []
      test_labels = None
      
      for item in train_items:
          raw_train_texts.append(item['text'])
          if label_name is not None:
              train_labels.append(item[label_name])

      for item in test_items:
          raw_test_texts.append(item['text'])
          if label_name is not None:
              test_labels.append(item[label_name])

      rst = preprocessing.preprocess(raw_train_texts, train_labels, raw_test_texts, test_labels)
      return rst

rst = preprocess_jsonlist(dataset_dir='./datasets/CMedjsonlist')

preprocessing.save('./datasets/CMed', **rst)
        