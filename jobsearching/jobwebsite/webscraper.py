import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import lxml

# url = 'https://www.careerjet.com/jobad/us827927d1693748b79497a7207bcc7230'

def getSeeMore(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.execute_script("window.stop();")
    html = BeautifulSoup(driver.page_source, 'lxml')
    words = html.find_all('section', class_='content')
    lst = []
    for i in words:
        lst.append(i.get_text(strip=True))
    if len(lst) == 0:
        return [""]
    return lst


def getDescription(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.execute_script("window.stop();")
    html = BeautifulSoup(driver.page_source, 'lxml')
    words = html.find_all('section', class_='content')
    return words