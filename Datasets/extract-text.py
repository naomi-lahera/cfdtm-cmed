import os
import fitz  # PyMuPDF
import joblib
import json

path = 'Datasets (manual)'

train_texts = dict()
test_texts = dict()

for time in os.listdir(os.path.join(path, 'train')): #time_slices:
    train_texts[time] = []
    
    print(f"Time: {time}")
    
    pdf_files = [os.path.join(path, 'train', time, file) for file in os.listdir(os.path.join(path, 'train', time)) if file.endswith('.pdf')]
    
    for file_path in pdf_files:
        print(f" - Archivo PDF: {file_path}")
        doc = fitz.open(file_path)
        text = ''
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text("text")  # Modo de extracción de texto
            print(f"Texto de la página {page_num + 1}:\n{text}\n")

        train_texts[time].append(text)
        
    print(f'Texts in {time}:  {train_texts[time]}')
        
joblib.dump(train_texts, os.path.join(path, 'train', 'train_texts.joblib'))

with open(os.path.join(path, "train", "train_texts.json"), 'w') as f:
    json.dump(train_texts, f)
# json.dump(train_texts, os.path.join(path, 'train_texts.json'))


for time in os.listdir(os.path.join(path, 'test')): #time_slices:
    test_texts[time] = []
    
    print(f"Time: {time}")
    
    pdf_files = [os.path.join(path, 'test', time, file) for file in os.listdir(os.path.join(path, 'test', time)) if file.endswith('.pdf')]
    
    for file_path in pdf_files:
        print(f" - Archivo PDF: {file_path}")
        doc = fitz.open(file_path)
        text = ''
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text("text")  # Modo de extracción de texto
            print(f"Texto de la página {page_num + 1}:\n{text}\n")

        test_texts[time].append(text)
        
    print(f'Texts in {time}:  {test_texts[time]}')
        
joblib.dump(test_texts, os.path.join(path, 'test', 'test_texts.joblib'))
# json.dump(test_texts, os.path.join(path, 'train_texts.json'))

with open(os.path.join(path, 'test', "test_texts.json"), 'w') as f:
    json.dump(test_texts, f)