from grobid_client.grobid_client import GrobidClient
import argparse
import os

def extract_text_api(pdf_path, output_path):
    # import requests
    # url = "https://grobid.science-miner.com/api/processFulltextDocument"
    # with open(pdf_path, "rb") as f:
    #     response = requests.post(url, files={"input": f})
    # return response.text  # Retorna XML estructurado
    print("OK")

def main():
    parser = argparse.ArgumentParser(description="Extract Text from Papers (PDFs)")
    parser.add_argument("--input", type=str, help="Papers path")
    parser.add_argument("--output", type=str, help="Result (jsonlists) path")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    extract_text_api(pdf_path=args.input, output_path=args.output)

if __name__ == "__main__":
    main()