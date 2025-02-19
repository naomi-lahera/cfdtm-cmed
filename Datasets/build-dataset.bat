@echo off
python download-dataset-selenium.py 
python extract-text.py 
python pre-build-dataset.py 
python build-dataset.py 
pause