#author          : Agung Pambudi
#email           : mail@agungpambudi.com
#linkedin        : http://linkedin.com/in/agungpambudi
#version         : 0.4
#
#
#==============================================================================
#                                   _         _ _
# ___ ___ _ _ ___ ___ ___ ___ _____| |_ _ _ _| |_|  ___ ___ _____
#| .'| . | | |   | . | . | .'|     | . | | | . | |_|  _| . |     |
#|__,|_  |___|_|_|_  |  _|__,|_|_|_|___|___|___|_|_|___|___|_|_|_|
#    |___|       |___|_|


import pandas as pd
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlencode

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
http = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

# data
data = list()
gold = {}

API_KEY = '83489fe80b28c8e99d0cf855048ef40c'

def get_scraperapi_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


while True:

    link = "https://www.golddealer.com/product-category/products-2/bullion/gold-bullion-coins-bars/"

    http.get(get_scraperapi_url(link))
    http.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(10)

    # Try to get data
    try:

        # Get data
        results = http.find_elements(by=By.XPATH, value="//*[@id='content']/div[2]/p")
        r = results[0].text.split()

        for k in range(int(r[2])):

            if k == 27:

                title = http.find_elements(by=By.XPATH, value="//*[@id='content']/ul/li[" + str(k+1) + "]/a/h2")
                buyprice = http.find_elements(by=By.XPATH, value="//*[@id='content']/ul/li[" + str(k+1) + "]/a/span[2]")
                price = http.find_elements(by=By.XPATH, value="//*[@id='content']/ul/li[" + str(k+1) + "]/a/span[3]")
                data = [title[0].text, buyprice[0].text, price[0].text]
                gold[k] = data

            if k < 32 and k != 27:

                title = http.find_elements(by=By.XPATH, value="//*[@id='content']/ul/li[" + str(k+1) + "]/a/h2")
                buyprice = http.find_elements(by=By.XPATH, value="//*[@id='content']/ul/li[" + str(k+1) + "]/a/span[1]")
                price = http.find_elements(by=By.XPATH, value="//*[@id='content']/ul/li[" + str(k+1) + "]/a/span[2]")
                data = [title[0].text, buyprice[0].text, price[0].text]
                gold[k] = data

            elif k >= 32 and k != 37:

                title = http.find_elements(by=By.XPATH, value="//*[@id='content']/ul/li[" + str(k+1) + "]/a/h2")
                buyprice = http.find_elements(by=By.XPATH, value="//*[@id='content']/ul/li[" + str(k+1) + "]/a/span[2]")
                price = http.find_elements(by=By.XPATH, value="//*[@id='content']/ul/li[" + str(k+1) + "]/a/span[3]")
                data = [title[0].text, buyprice[0].text, price[0].text]
                gold[k] = data

            elif k == 37:

                title = http.find_elements(by=By.XPATH, value="//*[@id='content']/ul/li[" + str(k+1) + "]/a/h2")
                buyprice = http.find_elements(by=By.XPATH, value="//*[@id='content']/ul/li[" + str(k+1) + "]/a/span[2]")
                price = http.find_elements(by=By.XPATH, value="//*[@id='content']/ul/li[" + str(k+1) + "]/a/span[1]")
                data = [title[0].text, buyprice[0].text, price[0].text]
                gold[k] = data

    except NoSuchElementException:
        # If fails then we dump the source code then break the loop (sad)
        print(http.page_source)
        break
    except:
        print("...")
        break



df = pd.DataFrame(columns=['Title', 'Buy Price', 'Price'])
for i in range(len(gold)):
    df.loc[i,:] = gold[i]

df.to_csv('data/gold_price.csv', index=False)

http.quit()
