@echo off
REM Paths
set DATASET_PAPERS_PATH=..\..\data\papers-pdf
set DATASET_XML_PATH=..\..\data\papers-xml
set DATASET_JSONLIST_PATH=..\..\data\texts-jsonlists
set DATASET_PATH=..\..\data\datasets\CMed

echo === Build Dataset ===

REM Step #1: Download papers
REM -

REM Step #2: Extract text from papers (pdfs)
REM python extract_text.py --input %DATASET_PAPERS_PATH% --output_xml %DATASET_XML_PATH% --output_jsonlists %DATASET_JSONLIST_PATH%

REM Step #2: Clear text (pdfs)
python clear_text.py --input %DATASET_JSONLIST_PATH% --output_jsonlists %DATASET_JSONLIST_PATH% --dataset_path %DATASET_PATH% --verbose True

REM echo === Done ✅ ===
REM pause
