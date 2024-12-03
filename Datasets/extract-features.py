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

with open(os.path.join(output_path, "train_time.txt"), "w") as f:
    for elemento in train_time:
        f.write(str(elemento) + "\n")
with open(os.path.join(output_path, "test_time.txt"), "w") as f:
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


with open(os.path.join(input_path, "train_texts.jsonlist"), "w") as f:
    for record in train_jsonlist:
        # Convertir el diccionario a JSON y escribir una línea
        f.write(json.dumps(record) + "\n")
        
with open(os.path.join(input_path, "test_texts.jsonlist"), "w") as f:
    for record in test_jsonlist:
        f.write(json.dumps(record) + "\n")
        