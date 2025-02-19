from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import requests
from tqdm import tqdm
import json
from utils import *

index = 0
errors = 0

def get_docs(url, download_path, errors_path, i):
    global index
    global errors
    driver.get(url)
    
    div_issues_per_year = []
    j = 1
    while j <= 11:
        try:
            div_issues_per_year.append(driver.find_element(By.XPATH, f'//*[@id="issues"]/div[{j}]'))
            j+=2
        except:
            break
        
    years_issues_dict = dict()
    # years_issues_dict = joblib.load(f'{path}/years_issues_dict_{i}.joblib')
    
    for item in div_issues_per_year:
        year = item.find_element(By.TAG_NAME, 'h3').text
        print(year)
        os.makedirs(os.path.join(download_path, year), exist_ok=True)
        years_issues_dict[year] = []
        
        for element in tqdm(item.find_elements(By.XPATH, './/*[starts-with(@id, "issue-")]'), desc="Descargando los enlaces para accedera cada una de las paginas correspondientes a cada documento"):
            href = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            print(href)
            years_issues_dict[year].append(href)
            
        print(len(years_issues_dict[year]))
        
    # joblib.dump(years_issues_dict, f'{path}/years_issues_dict_{i}.joblib')
    
    year_doclink_dict = dict()
    # year_doclink_dict = joblib.load(f'{path}/year_doclink_dict.joblib')
    
    for year, links in list(years_issues_dict.items()):
        print(year)
        
        year_doclink_dict[year] = []
        
        # En caso de que luego se quiera evaluar pero con time slices en funcion de los meses la modificacion seria aqui
        for link in links:
            driver.get(link)
            
            articles = driver.find_elements(By.CLASS_NAME, "tocGalleys")
                        
            for article in articles:
                article_links = [item for item in article.find_elements(By.TAG_NAME, 'a') if item.text == 'PDF']
                if len(article_links) == 0:  continue
                article_link = article_links[0].get_attribute('href')
                                
                try:
                    ancestor = article.find_element(By.XPATH, './ancestor::*[preceding-sibling::h4[@class="tocSectionTitle"]][last()][1]')
                    category = ancestor.find_elements(By.XPATH, './preceding-sibling::h4[@class="tocSectionTitle"]')[-1].text
                except:
                    print(f"No se encontró categoría para el artículo: {article_link}")
                    category = '?'
                    
                category = category.lower().replace(' ', '-')  
                year_doclink_dict[year].append({"label": category, "link": article_link})
        
    # joblib.dump(year_doclink_dict, f'{path}/year_doclink_dict_{i}.joblib')
    
    for label in [json_['label'] for year, jsons in year_doclink_dict.items() for json_ in jsons]:
        os.makedirs(os.path.join(download_path, year, label), exist_ok=True)
    
    year_jsonlist_dict = dict()
    for year, jsons in tqdm(year_doclink_dict.items(), desc="Processing timeslices"):
        index = 0
        jsonlist = []
        for json_ in jsons:
            os.makedirs(os.path.join(download_path, year, json_['label']), exist_ok=True)
            driver.get(json_['link'])
            link = driver.find_element(By.ID, 'pdfDownloadLink').get_attribute('href')
            pdf_path = os.path.join(download_path, year, json_['label'], f"{index}.pdf")
            
            if not os.path.isfile(pdf_path): 
                try:
                    text = requests.get(link).content
                    with open(pdf_path, "wb") as f:
                        f.write(text)
                except Exception as e:
                    print(f"❌ Error al descargar el PDF para '{link}': {e}")
                    print('\\'*50)
                    
                    with open(os.path.join(errors_path, f"error_{errors}.json"), 'w')as file:
                        json.dump({"year": year, "label": json_['label'], "index": index, "downliadLink": link}, file)

                    if os.path.isfile(pdf_path):
                        os.remove(pdf_path)                
                    errors +=1
                    
            index+=1
            
        year_jsonlist_dict[year] = jsonlist
    
    # joblib.dump(year_jsonlist_dict, f'{path}/year_jsonlist_dict_{i}.joblib')  
    return year_jsonlist_dict

def fix_errors(path):
    for file in [f for f in os.scandir(path) if f.is_file()]:
        with open(file, 'r') as f:
            art = json.load(f)
            pdf_path = os.path.join(art['year'], art['label'], f"{art['index']}.pdf")
            if not os.path.isfile(pdf_path): 
                try:
                    text = requests.get(art['downliadLink']).content
                    with open(pdf_path, "wb") as f:
                        f.write(text)
                    os.remove(file)
                    print(f"PDF descargado con éxito en {pdf_path}. ✅")
                except Exception as e:
                    print(f"❌ Error al descargar el PDF para '{art['downliadLink']}': {e}")
                    print('\\'*50)
                    

if __name__ == '__main__':
    args = get_args_json(files.download_dataset_selenium)
    
    download_path = args['download_path']
    errors_path = args['errors_path']
    os.makedirs(download_path, exist_ok=True)
    os.makedirs(errors_path, exist_ok=True)
    
    urls = [
        'https://revhabanera.sld.cu/index.php/rhab/issue/archive?issuesPage=1#issues', 
        'https://revhabanera.sld.cu/index.php/rhab/issue/archive?issuesPage=2#issues',
        'https://revhabanera.sld.cu/index.php/rhab/issue/archive?issuesPage=3#issues',
        'https://revhabanera.sld.cu/index.php/rhab/issue/archive?issuesPage=4#issues'
        ]
    
    print('Configurando WebDriver')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    
    for i, url in enumerate(urls):
        print(f'Descargando elementos: {url}')
        get_docs(url, download_path, errors_path, i)