
import argparse
import os
from grobid_client.grobid_client import GrobidClient
from lxml import etree
import json

client = GrobidClient(config_path="./extract-text-config.json")

def get_xmls(input_path, output_path):
    os.makedirs(output_path, exist_ok=True)
    client.process("processFulltextDocument", input_path=input_path, output=output_path, n=20, verbose=True)

def extract_xmls(input, output_xml):
    for year in os.scandir(input):
        if year.is_dir():
            for label in os.scandir(year.path):
                 if label.is_dir(): get_xmls(label.path, os.path.join(output_xml, year.name, label.name))
    
def extract_text_from_xml(xml_path):
    print(xml_path)
    parser = etree.XMLParser()
    with open(xml_path, "r", encoding="utf-8") as out:
        tree = etree.parse(out, parser)

    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

    # Extraer texto completo del <body>
    body_elements = tree.xpath('//tei:body//tei:p | //tei:body//tei:head', namespaces=ns)

    # Unir todo el texto del cuerpo, respetando títulos (<head>)
    article_text = '\n\n'.join(el.text.strip() for el in body_elements if el.text)

    # print("\n=== TEXTO DEL ARTÍCULO ===")
    # print(article_text)

    return article_text

def process_path(xml_paths, output_jsonlist):
    files = [{"year": year.name,
              "label": label.name,
              "text": extract_text_from_xml(xml.path)}
              
              for year in os.scandir(xml_paths) if year.is_dir() 
              for label in os.scandir(year.path) if label.is_dir()
              for xml in os.scandir(label.path) if xml.is_file() and xml.name.endswith("xml")]

    with open(os.path.join(output_jsonlist, "all_texts.jsonlist"), "w", encoding="utf-8") as f:
        json.dump(files, f)
            

def main():
    parser = argparse.ArgumentParser(description="Extract Text from Papers (PDFs)")
    parser.add_argument("--input", type=str, help="Papers path")
    parser.add_argument("--output_xml", type=str, help="Result (jsonlists) path")
    parser.add_argument("--output_jsonlists", type=str, help="Result (jsonlists) path")
    args = parser.parse_args()

    os.makedirs(args.output_xml, exist_ok=True)
    os.makedirs(args.output_jsonlists, exist_ok=True)

    extract_xmls(args.input, args.output_xml)
    process_path(args.output_xml, args.output_jsonlists)

if __name__ == "__main__":
    main()