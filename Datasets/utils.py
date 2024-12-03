import joblib
from enum import Enum
import json
import sys
import os
import csv

class Path(Enum):
    dataset_path = 'data/dataset.joblib'
    nlp_path = 'data/nlp_model.joblib'
    lda_model_path = 'data/ldaModel.joblib'
    different_alphas = 'data/different_alphas.joblib'
    dataset = 'data/dataset.joblib'
    data = 'data/'
    result = 'results/'
    result_topics_hiper = 'results/fixed-hyperparameters/topics.csv'
    result_default_hiper = 'results/default-hyperparameters/'
    result_fixed_hiper = 'results/fixed-hyperparameters/'
    result_word_cloud = 'results/fixed-hyperparameters/word_cloud/'
    result_topics_hiper_default = 'results/default-hyperparameters/topics.csv'
    result_word_cloud_default = 'results/default-hyperparameters/word_cloud/'
    
def save_result_csv(lda_model, num_topics, filepath):
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        header = ['Topic'] + [f'Word_{i}' for i in range(1, 51)]  # 50 palabras por cada tópico
        writer.writerow(header)
        
        for topic_id in range(num_topics):
            topic = lda_model.show_topic(topic_id, topn=50)  # Obtener las 50 palabras más representativas del tópico
            row = [f'Topic {topic_id}'] + [f'{word}: {weight:.4f}' for word, weight in topic]
            writer.writerow(row)
    
def load_config(config_path):
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"✅ Archivo de configuración no encontrado: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("'❌ Error al leer el archivo de configuración. Asegúrate de que es un JSON válido.")
        sys.exit(1)
    
def create_folder_if_not_exists(path):
    try:
        os.makedirs(path)
        print(f"✅ Created foler: {path}")
    except FileExistsError:
        print(f"Folder {path} already exists.")
    except OSError as error:
        print(f"Error creating folder: {error}")

def load_file(path: str):
    try: 
        return joblib.load(path)
    except Exception as e :
        return Exception(f'❌ Error loading file. {e}')

def save_file(data, path: str):
    try:
        joblib.dump(data, path)
    except FileNotFoundError:
        joblib.dump(data, path)
    except Exception as e:
        Exception(f'❌ Error saving file. {e}')
        
if __name__ == '__main__':        
    load_file('cdfvybguihnjm')