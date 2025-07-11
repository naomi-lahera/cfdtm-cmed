import argparse
import os
import json
import spacy
from tqdm import tqdm

nlp = spacy.load("es_core_news_lg")
stopwords = nlp.Defaults.stop_words

ner = set()
vocab = set()

def save_vocab(dataset_path):
    with open(os.path.join(dataset_path, "vocab.txt"), "w", encoding="utf-8") as f:
        for term in vocab:
            f.write(term.strip() + '\n')
    print("✅ The vocabulary was successfully saved")

def valid_token(token, delete):
    return token.is_alpha and token.pos_ not in delete and token.lemma_ not in stopwords

#TODO Corregir la extraccion de entidades nombradas. Usar modelo entrenado en NER en medicina
def preprocess_text(text: str, delete=["INTJ", "PUNCT", "SYM", "X", "SPACE"]):
    tokens = nlp(text)

    for entity in tokens.ents:
        ner.add(entity.text)

    ents = {ent.start: ent for ent in tokens.ents}  # Diccionario para detectar entidades

    terms = []

    for i in range(len(tokens)):
        if i in ents:  # Si el índice pertenece a una entidad
            terms.append(ents[i].text.replace(" ", "_").lower())
            vocab.add(ents[i].text.replace(" ", "_").lower())
            i = ents[i].end  # Saltar los tokens que forman la entidad
        elif valid_token(tokens[i], delete):
            vocab.add(tokens[i].lemma_.lower())  # Agregar palabra normal
            terms.append(tokens[i].lemma_)

    return " ".join(terms)

def process_path(input_path, output_jsonlist, verbose):
    with open(os.path.join(input_path, "all_texts.jsonlist"), "r", encoding="utf-8") as f:
        jsonlist = json.load(f)[:5]

    files = [{"year": item["year"],
              "label": item["label"],
              "text": preprocess_text(item["text"])}
              
              for item in tqdm(jsonlist, desc="Preprocessing Texts")]

    with open(os.path.join(output_jsonlist, "all_preprocessed_texts.jsonlist"), "w", encoding="utf-8") as f:
        json.dump(files, f)

    if verbose:
        print("\n👽 Named Netities")
        for ent in list(ner)[:20]:
            print(ent)
        print("...\n")

    print("✅ Done. The texts was successully preprocessed")

def main():
    parser = argparse.ArgumentParser(description="Extract Text from Papers (PDFs)")
    parser.add_argument("--input", type=str, help="Papers path")
    parser.add_argument("--output_jsonlists", type=str, help="Result (jsonlists) path")
    parser.add_argument("--dataset_path", type=str, help="Dataset path")
    parser.add_argument("--verbose", default=False, type=bool, help="Dataset path")
    args = parser.parse_args()

    os.makedirs(args.output_jsonlists, exist_ok=True)
    os.makedirs(args.dataset_path, exist_ok=True)
    verbose = args.verbose

    if verbose:
        print("⛔ Stop Words")
        for word in list(stopwords)[:20]: print(word)
        print("...\n")

    process_path(args.input, args.output_jsonlists, verbose)
    
    save_vocab(args.dataset_path)

if __name__ == "__main__":
    main()