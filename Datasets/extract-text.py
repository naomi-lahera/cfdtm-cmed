import os
import fitz 
import joblib
import json
import re

# import pdfplumber


def extract_text(path, subset: str):
    _texts = dict()
    time_slices = os.listdir(os.path.join(path, subset))
    # print(time_slices)
    
    for time in time_slices:
        _texts[time] = []
        
        pdf_files = [os.path.join(path, subset, time, file) for file in os.listdir(os.path.join(path, subset, time)) if file.endswith('.pdf')]

        # for file_path in pdf_files:
            # try:
                # with pdfplumber.open(file_path) as pdf:
                    # text = ""
                    # for page in pdf.pages:
                        # text += page.extract_text()
                    # _texts[time].append(text)
            # except Exception as e:
                # print(f"❌ Error procesando {file_path} con pdfplumber: {e}")
                # continue


        for file_path in pdf_files:
            # print(f" - Archivo PDF: {file_path}")
            try:
                doc = fitz.open(file_path)
                text = ""
                for page_num in range(doc.page_count):
                    page = doc[page_num]
                    text += page.get_text("text")  # Modo de extracción de texto
                    # print(f"Texto de la página {page_num + 1}:\n{text}\n")

                _texts[time].append(text)
            except fitz.fitz.FileDataError:
                print(f"❌ Error específico de MuPDF al procesar {file_path}: No default Layer config.")
                # Opcional: puedes guardar el nombre del archivo problemático en una lista para referencia
                # error_files.append(file_path)
            except Exception as e:
                print(f"❌ Error general al procesar {file_path}: {e}")
            

        print(f"{time} done ✅ - {len(_texts[time])} files" )
        
    return _texts if len(_texts) != 0 else None    
    
# def build_jsonlist(_path: str, _texts: dict, subset: str):
    # _jsonlist = []
    # for time, texts in _texts.items():
        # _jsonlist.extend([{"text": text} for text in texts])

    # with open(os.path.join(_path, f"{subset}.jsonlist"), "w") as f:
        # for record in _jsonlist:
            # f.write(json.dumps(record) + "\n")
                    
if __name__ == '__main__':
    input_path = 'Ciencias-Médicas/data/PDFs'
    # jsonlist_path = 'jsonlist'
    output_path = 'Ciencias-Médicas/data/Texts'
    os.makedirs(output_path, exist_ok=True)
    
    train_texts = extract_text(input_path, 'train')
    test_texts = extract_text(input_path, 'test')
    
    joblib.dump(train_texts, os.path.join(output_path, 'train_texts.joblib'))
    if train_texts: 
        with open(os.path.join(output_path, 'train_texts.json'), 'w') as f: 
            json.dump(train_texts, f)
                 
    joblib.dump(test_texts, os.path.join(output_path, 'test_texts.joblib'))        
    if test_texts: 
        with open(os.path.join(output_path, 'test_texts.json'), 'w') as f: 
            json.dump(test_texts, f)  
              
    # if train_texts: build_jsonlist(jsonlist_path, train_texts, 'train')
    # if test_texts: build_jsonlist(jsonlist_path, test_texts, 'test')    