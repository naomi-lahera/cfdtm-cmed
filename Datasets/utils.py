import json
from enum import Enum

class files(Enum):
    download_dataset_selenium = 'download-dataset-selenium'
    extract_text = 'extract-text'
    pre_build_dataset = 'pre-build-dataset'
    build_dataset = 'build-dataset'

def get_args_json(file: files):
    with open('args.json', 'r') as f:
        args = json.load(f)
    
    return args[file.value]