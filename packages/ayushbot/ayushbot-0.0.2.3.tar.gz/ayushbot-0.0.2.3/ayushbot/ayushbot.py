import os
from .whatsapp import WhatsApp
import time
import json
import random
import re
import sys
import urllib.parse
import bs4
import requests
import chromedriver_autoinstaller


import time
import datetime as dt
import json
import os
import requests
import shutil
import pickle
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


from urllib.parse import urlencode
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print("Beautiful Soup Library is reqired to make this library work(For getting participants list for the specified group).\npip3 install beautifulsoup4")

chromedriver_autoinstaller.install()

def ayushbot(receiver):
    
    whatsapp = WhatsApp(100, session="mysession")
    whatsapp.send_message(receiver, "AyushBOT will serve you till Ayush comes online and answers your questions. As it is still very young AyushBOT can act very stupid sometimes. Please dont mind it. Start talking with AyushBOT below")
    newmessages=[]
    responses=[]
    chrome_options = Options()
    driver = webdriver.Chrome()

    driver.get("https://www.pandorabots.com/mitsuku/")
    content = driver.find_element_by_xpath("//button[@class='pb-widget__launcher pb-widget__launcher__open']")
    content.click()
    while 1==1:
        messages = whatsapp.get_last_message_for(receiver)
        newmessages.append(messages)
        if len(newmessages)>1:
            if len(newmessages)>10:
                newmessages=newmessages[:-5]

            if newmessages[-1][-1] != newmessages[-2][-1]:
                
                query=str(messages[-1])
                

                content2 = driver.find_element_by_xpath("//input[@class='pb-widget__input__message__input']")
                time.sleep(2)

                content2.send_keys(query)
                content2.submit()
                time.sleep(5)
                try:
                    content3 = driver.find_elements_by_xpath("//div[@class='pb-chat-bubble pb-chat-bubble__bot']")
                    answer=content3[-1].text

                except:
                    answer='Indeed'
                response=answer
                


                if '{"status": "error","message":"401 unauthorized"}' in response:
                    response=response.replace('{"status": "error","message":"401 unauthorized"}','')
                if 'Kuki' in response:
                    response=response.replace('Kuki','AyushBot')
                if 'Pandorabots' in response:
                    response=response.replace('Pandorabots','Ayush')    
                responses.append(response)

                if len(responses)>1:
                    if responses[-1]!=responses[-2]:
                        whatsapp.send_message(receiver, f'{responses[-1]}')
                elif len(responses)==1:
                    whatsapp.send_message(receiver, f'{responses[-1]}')


