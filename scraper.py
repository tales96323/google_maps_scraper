import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def setup_driver():
    options = Options()
    options.headless = True  # Executa o navegador em modo headless
    service = Service('path/to/chromedriver')  # Altere para o caminho do seu chromedriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_google_maps(search_query):
    driver = setup_driver()
    driver.get(f"https://www.google.com/maps/search/{search_query}")
    time.sleep(5)  # Aguarda o carregamento da página

    businesses = []
    
    # Altere a seleção de acordo com a estrutura HTML da página
    elements = driver.find_elements(By.CLASS_NAME, "section-result")
    
    for element in elements:
        name = element.find_element(By.CLASS_NAME, "section-result-title").text
        address = element.find_element(By.CLASS_NAME, "section-result-location").text
        businesses.append({'name': name, 'address': address})
    
    driver.quit()
    return businesses

if __name__ == "__main__":
    query = "restaurantes em São Paulo"
    results = scrape_google_maps(query)
    
    for business in results:
        print(f"Nome: {business['name']}, Endereço: {business['address']}")
