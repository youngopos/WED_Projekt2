from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pickle


#options = Options()
#options.add_argument('--headless=new')
chr = Service(r"C:\Users\tomus\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe")
url = r'https://store.steampowered.com/search/?supportedlang=english&ndl=1'
def scroll(url,n):
    driver = webdriver.Chrome(service=chr,)
    driver.get(url)
    time.sleep(2)
    element = driver.find_element(By.TAG_NAME,'body')
    for i in range(n):
        element.send_keys(Keys.PAGE_DOWN)
    doc = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    driver.quit()
    return doc

def get_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find('div', {'id: search_results'}, class_ = 'search_results')
    rows = container.find_all('a')
    links = []
    for row in rows:
        link = row['href']
        if 'app' in link:
            links.append(link)
    return links
if __name__ == '__main__':
    lista = get_links(scroll(url,2*int(1e+4)))
    with open('list_links.pkl', 'wb') as f:
        pickle.dump(lista, f)

