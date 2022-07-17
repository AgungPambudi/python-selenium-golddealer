#author          : Agung Pambudi
#email           : mail@agungpambudi.com
#linkedin        : http://linkedin.com/in/agungpambudi
#version         : 0.5
#
#
#==============================================================================
#                                   _         _ _
# ___ ___ _ _ ___ ___ ___ ___ _____| |_ _ _ _| |_|  ___ ___ _____
#| .'| . | | |   | . | . | .'|     | . | | | . | |_|  _| . |     |
#|__,|_  |___|_|_|_  |  _|__,|_|_|_|___|___|___|_|_|___|___|_|_|_|
#    |___|       |___|_|


import csv
import ssl
import time
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


# Ignore SSL certificate errors

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#chrome settings

PROXY_STR = "154.49.216.33:3128"
options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=%s' % PROXY_STR)
chrome = webdriver.Chrome("C:\Applications\chromedriver_win32\chromedriver", options=options)
#function for gold price

def silver_price():
    chrome.get("https://www.golddealer.com/product-category/products-2/bullion/silver-bullion-coins-bars/?orderby=price-desc")
    time.sleep(10)
    chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
   
    data = list()
    silver = {}

    results = chrome.find_elements_by_xpath('//*[@id="content"]/div[2]/p')
    r = results[0].text.split()
    for k in range(int(r[2])):
        
        if k == 10 or k==19:
            title = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/h2')
            buyprice = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/span[2]')
            price = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/span[3]')
            data = [title[0].text, buyprice[0].text, price[0].text]
            silver[k] = data
            
        elif (k >=13 and k <=17) or (k >=28 and k <=32):
            
            title = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/h2')
            buyprice = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/span[2]')
            price = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/span[3]')
            data = [title[0].text, buyprice[0].text, price[0].text]
            silver[k] = data
            
        else:
            
            title = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/h2')
            buyprice = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/span[1]')
            price = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/span[2]')
            data = [title[0].text, buyprice[0].text, price[0].text]
            silver[k] = data
    
            
    #create a dataframe and csv file
    import pandas as pd
    df = pd.DataFrame(columns=['Title', 'Buy Price', 'Price'])
    for i in range(len(silver)):
        df.loc[i,:] = silver[i]

    with open('silver_price.csv', 'w') as csvfile:
        df.to_csv('silver_price.csv')


#this will trigger the job on a specific time

sched = BackgroundScheduler()
              
trigger = CronTrigger(
    year="*", month="*", 
    day="*", hour="2",             #you can adjust the time here for silver price trigger 
    minute="18", second="0"         
)

sched.add_job(
    silver_price,
    trigger=trigger,
)

sched.start()