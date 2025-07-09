@echo off
REM Paths
set DATASET_PAPERS_PATH=..\..\data\papers-pdf
set DATASET_JSONLIST_PATH=..\..\data\texts-jsonlists
set DATASET_PATH=..\..\data\CMed-dataset

echo === Build Dataset ===

REM Step #1: Download papers
REM -

REM Step #2: Extract text from papers (pdfs)
python extract_text.py --input %DATASET_PAPERS_PATH% --output %DATASET_JSONLIST_PATH% 

REM echo === Done ✅ ===
REM pause
