import pymupdf4llm
import os
import re
from unicodedata import normalize
import joblib
import  json
from tqdm import tqdm
import traceback

def extract_text(pdf_path, errors_path, error_data):    
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
        text = text.replace(specialChar, '')
        
    return text if valid_text(text) > 0 else None

def valid_text(texto):
    try:
        texto.encode('utf-8').decode('utf-8')  # Verificar si es UTF-8 válido
        return True
    except UnicodeDecodeError:
        return False
    finally:
        patron_0 = r"[^\w\s,.áéíóúüñÁÉÍÓÚÜÑ]"
        patron_1 = r"[\u0000-\u0008\u000B-\u001F\u007F]"
        return bool(re.search(patron_0, texto)) and bool(re.search(patron_1, texto))

def remove_diacritics(label):
    current_label = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", label), flags=re.I
    )
    return normalize('NFC', current_label)

if __name__ == '__main__':
    input_path = 'Ciencias-Médicas/data/PDF'
    output_path = 'Ciencias-Médicas/jsonlists'
    errors_path = 'Ciencias-Médicas/data/Texts/extract-text-errors'
    os.makedirs(errors_path, exist_ok=True)
    
    jsonlist_per_year_dict = dict()
    for year in tqdm(os.listdir(input_path), desc='Extracting text from docs'):
        jsonlist = []
        for label in os.listdir(os.path.join(input_path, year)):
            current_label = remove_diacritics(label)
            for doc in os.listdir(os.path.join(input_path, year, label)):
                text = extract_text(os.path.join(input_path, year, label, doc), errors_path, error_data={"year": year, "label": label})
                if not text: continue
                jsonlist.append({"label": current_label, "text": text})
        jsonlist_per_year_dict[year] = jsonlist
        
    # print([item[:2] for item in list(jsonlist_per_year_dict.items())[:3]])
    joblib.dump(jsonlist_per_year_dict, os.path.join(output_path, f'pre-jsonlist.joblib'))
    with open(os.path.join(output_path, f'pre-jsonlist.json'), 'w') as f:
        json.dump(jsonlist_per_year_dict, f)