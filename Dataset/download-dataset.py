from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import os
import joblib

path = 'PDFs'
path_temporary_files = 'temporary-files/'

# Configurar Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Ejecuta el navegador en segundo plano
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# url = "https://revistas.uh.cu/rcm/issue/archive"
# driver.get(url)

# # # Esperar a que la página cargue completamente
# # time.sleep(10) 

# time_periods = driver.find_elements(By.CLASS_NAME, "obj_issue_summary")
# periods_link = [(item.find_element(By.TAG_NAME, 'h2').find_element(By.TAG_NAME, 'a').text, item.find_element(By.TAG_NAME, 'h2').find_element(By.TAG_NAME, 'a').get_attribute('href')) for item in time_periods]
# joblib.dump(periods_link, f'{path_temporary_files}periods_link.joblib')
# print(periods_link)

periods_link = joblib.load(f'{path_temporary_files}periods_link.joblib')

time_art_dict = dict()
for time_slice, link in periods_link:
    print('link: ', link)
    driver.get(link)
    
    articles = driver.find_elements(By.CLASS_NAME, "obj_article_summary")
    print('Counted Articles: ', len(articles))
    
    for article in articles:        
        title = article.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').text
        print(title)

        pdf_link = article.find_element(By.CLASS_NAME, "obj_galley_link").get_attribute('href')
        print(pdf_link)

        driver.get(pdf_link)
        download_link = driver.find_element(By.CLASS_NAME, 'download').get_attribute('href')
        print(download_link)
        
        try:
            time_art_dict[time_slice].append(download_link)
        except:
            time_art_dict[time_slice] = [download_link]
            
        print('-'*50)
        
    print(time_art_dict)
    joblib.dump(time_art_dict, f'{path}time_art_dict.joblib')
    break
    
        # joblib.dump(download_link, f'{path_temporary_files}download_link.joblib')
        
        # download_link = joblib.load(f'{path_temporary_files}download_link.joblib')
        # print(download_link)
        
        # # driver.get(download_link)
        # print("Descargando:", download_link)

        # # Descargar el PDF usando requests
        # response = requests.get(download_link)

        # # Generar un nombre único para cada archivo basado en el enlace o índice
        # filepath = os.path.join(path, f'{path}{title}.pdf')

        # # Guardar el PDF en la carpeta especificada
        # with open(filepath, "wb") as f:
            # f.write(response.content)

        # print(f"PDF descargado con éxito en {filepath}.")
# 
# # Cierra el navegador
# driver.quit()
    
    
    
    # total_links += 1 
    # print(link)
    
# print(total_links)

# # Encuentra los botones de descarga de los PDFs
# pdf_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'clase-boton-pdf')]")

# # Descargar cada PDF encontrado
# for i, button in enumerate(pdf_buttons, start=1):
    # try:
        # # Hacer clic en el botón para descargar el PDF

        # ActionChains(driver).move_to_element(button).click(button).perform()
        
        # # Esperar un momento para que el PDF se descargue
        # time.sleep(20)
        
        # # Guardar el PDF en la carpeta, renombrando si es necesario
        # pdf_name = f"articulo_{i}.pdf"
        # pdf_path = os.path.join("PDFs/", pdf_name)
        
        # # Aquí puedes agregar lógica para mover el archivo desde la carpeta de descargas predeterminada
        # print(f"Descargado: {pdf_name}")
        
    # except Exception as e:
        # print(f"Error al intentar descargar el PDF {i}: {e}")

# # Cerrar el navegador
# driver.quit()

# print("Descarga completada.")