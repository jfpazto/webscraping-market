from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def fetch_dynamic_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Para que no abra el navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get(url)
    driver.implicitly_wait(5)  # Esperar a que cargue
    
    html = driver.page_source
    driver.quit()
    return html

if __name__ == "__main__":
    URL = "https://tienda.makro.com.co"
    html = fetch_dynamic_page(URL)
    
    if html:
        print(html[:1000])  # Verifica que se carga correctamente
