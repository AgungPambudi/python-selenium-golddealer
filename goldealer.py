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


import csv
import ssl
import time
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#chrome settings

PROXY_STR = "154.49.216.33:3128"
options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=%s' % PROXY_STR)
chrome = webdriver.Chrome("C:\Applications\chromedriver_win32\chromedriver", options=options)
#function for gold price

def gold_price():
    chrome.get("https://www.golddealer.com/product-category/products-2/bullion/gold-bullion-coins-bars/?orderby=price-desc")
    chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.slee(10)
    data = list()
    gold = {}

    results = chrome.find_elements_by_xpath('//*[@id="content"]/div[2]/p')
    r = results[0].text.split()
    for k in range(int(r[2])):
        
        if k == 27:
        
            title = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/h2')
            buyprice = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/span[2]')
            price = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/span[3]')
            data = [title[0].text, buyprice[0].text, price[0].text]
            gold[k] = data
    
        if k < 32 and k!=27:
    
            title = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/h2')
            buyprice = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/span[1]')
            price = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/span[2]')
            data = [title[0].text, buyprice[0].text, price[0].text]
            gold[k] = data
            
        elif k >= 32 and k!=37:
      
            title = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/h2')
            buyprice = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/span[2]')
            price = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/span[3]')
            data = [title[0].text, buyprice[0].text, price[0].text]
            gold[k] = data
        
        
        elif k == 37:
        
            title = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/h2')
            buyprice = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/span[2]')
            price = chrome.find_elements_by_xpath('//*[@id="content"]/ul/li['+ str(k+1) +']/a/span[1]')
            data = [title[0].text, buyprice[0].text, price[0].text]
            gold[k] = data
            
    #create a dataframe and csv file
    import pandas as pd
    df = pd.DataFrame(columns=['Title', 'Buy Price', 'Price'])
    for i in range(len(gold)):
        df.loc[i,:] = gold[i]

    with open('gold_price.csv', 'w') as csvfile:
        df.to_csv('gold_price.csv')



#this will trigger the job on a specific time

sched = BackgroundScheduler()
              
trigger = CronTrigger(
    year="*", month="*", 
    day="*", hour="0",             #you can adjust the time here 
    minute="46", second="0"
)
sched.add_job(
    gold_price,
    trigger=trigger,
)

sched.start()



