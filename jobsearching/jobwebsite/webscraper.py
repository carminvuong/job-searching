import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import lxml


url = 'https://www.careerjet.com/jobad/us827927d1693748b79497a7207bcc7230'


def getSeeMore(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.execute_script("window.stop();")
    html = BeautifulSoup(driver.page_source, 'lxml')
    words1 = html.find_all('div')
    words = html.find_all('section', class_='content')
    lst = []
    print(words1)
    for i in words:
        print(i)
        #lst.append(i.get_text(strip=True))
        lst.append(i.get_text())
    if len(lst) == 0:
        return [""]
    print(lst[0])
    text = lst[0]
    accum = ""
    if "Job Description" in text:
        index = text.find("Job Description")
        for i in range(index+14,len(text)):
            if text[i] == "\\":
                return list(accum)
            accum+=text[i]
    elif "JOB DESCRIPTION" in text:
        index = text.find("JOB DESCRIPTION")
        for i in range(index+14,len(text)):
            if text[i] == "\\":
                return list(accum)
            accum+=text[i]
    elif "job description" in text:
        index = text.find("job description")
        for i in range(index+14,len(text)):
            if text[i] == "\\":
                return list(accum)
            accum+=text[i]
    elif "JOB SUMMARY" in text:
        index = text.find("JOB SUMMARY")
        for i in range(index+10,len(text)):
            if text[i] == "\\":
                return list(accum)
            accum+=text[i]
    elif "Job Summary" in text:
        index = text.find("Job Summary")
        for i in range(index+10,len(text)):
            if text[i] == "\\":
                return list(accum)
            accum+=text[i]
    elif "job summary" in lst[0]:
        index = text.find("job summary")
        for i in range(index+10,len(text)):
            if text[i] == "\\":
                return list(accum)
            accum+=text[i]
    elif "About us" in lst[0]:
        index = text.find("About us")
        for i in range(index+7,len(text)):
            if text[i] == "\\":
                return list(accum)
            accum+=text[i]
    elif "About Us" in lst[0]:
        index = text.find("About Us")
        for i in range(index+7,len(text)):
            if text[i] == "\\":
                return list(accum)
            accum+=text[i]
    return lst


def getDescription(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.execute_script("window.stop();")
    html = BeautifulSoup(driver.page_source, 'lxml')
    words = html.find_all('section', class_='content')
    return words[0]
