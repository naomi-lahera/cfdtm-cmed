from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os
import joblib

path = 'PDFs'
os.makedirs(path, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument("--headless") 
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

url = "https://revmedicina.sld.cu/index.php/med/issue/archive"
driver.get(url)
time.sleep(10) 

time_slices = driver.find_element(By.ID, "issues").find_elements(By.CSS_SELECTOR, 'div')
time_slices_refs = []
for item in time_slices:
    element = item.find_element(By.CSS_SELECTOR, 'div').find_element(By.CLASS_NAME, 'a')
    time_slices_refs.append((element.text, element.get_attribute('href')))

print('Time Slaices Count: ', len(time_slices_refs))
print('Example: ', time_slices_refs[0])

# periods_link = [(item.find_element(By.TAG_NAME, 'h2').find_element(By.TAG_NAME, 'a').text, item.find_element(By.TAG_NAME, 'h2').find_element(By.TAG_NAME, 'a').get_attribute('href')) for item in time_periods]

# time_art_dict = dict()
# for time_slice, link in periods_link:
    # print('Link:', link)
    # driver.get(link)
    
    # time.sleep(10) 

    # articles = driver.find_elements(By.CLASS_NAME, "obj_article_summary")
    # print('Número de artículos encontrados:', len(articles))
    
    # article_links = []
    # pending_articles = []
    # for article in articles:
        # title = article.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').text
        
        # try:
            # pdf_link = article.find_element(By.CLASS_NAME, "obj_galley_link").get_attribute('href')
        # except:
            # pending_articles.append(article)
            # print('error')
            # print('\\'*50)
            
        # article_links.append((title, pdf_link))
    
    # current_path = f'{path}/{time_slice}'
    # os.makedirs(current_path, exist_ok=True)
    
    # pending_doc = []
    # for title, pdf_link in article_links:
        # pdf_path = os.path.join(current_path, f"{title}.pdf")
        # if os.path.exists(pdf_path): continue
        
        # driver.get(pdf_link)
        
        # try:
            # download_link = driver.find_element(By.CLASS_NAME, 'download').get_attribute('href')
            # print("Enlace de descarga:", download_link)
            
            # if time_slice not in time_art_dict:
                # time_art_dict[time_slice] = []
            # time_art_dict[time_slice].append(download_link)
            
            # response = requests.get(download_link)
            # # pdf_path = os.path.join(current_path, f"{title}.pdf")
            # with open(pdf_path, "wb") as f:
                # f.write(response.content)
                
            # print(f"PDF descargado con éxito en {pdf_path}.")
            
        # except Exception as e:
            # print(f"Error al descargar el PDF para '{title}': {e}")
            # print('\\'*50)
            # pending_doc.append(download_link)
        
        # print('-' * 50)
    
# driver.quit()
