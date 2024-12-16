from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
from time import sleep
from csv import writer
import pandas as pd
import pycountry
import requests
import gspread
from bs4 import BeautifulSoup
from dateutil.parser import parse
from fake_useragent import UserAgent
import platform
import random
import math
import pytz
import json
import pytz
import time
import json
import glob
import os
import re

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

err = 0
while err == 0:
	try:
		caps = DesiredCapabilities().CHROME
		# caps["pageLoadStrategy"] = "normal"  #  complete
		caps["pageLoadStrategy"] = "eager"  #  interactive
		#caps["pageLoadStrategy"] = "none"

		driver = webdriver.Chrome(options=options, service = Service(ChromeDriverManager().install()), desired_capabilities=caps)
		driver.implicitly_wait(20)
		err = 1
	except Exception:
		err = 0
		time.sleep(5)

print('Getting states and cities...')

driver.get('https://www.healthgrades.com/gastroenterology-directory')
driver.implicitly_wait(20)
time.sleep(5)

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))).click()

allState = []
allCity = []
state = driver.find_element(By.CLASS_NAME, 'link-list').find_elements(By.TAG_NAME, 'a')
for st in state:
	allState.append(st.get_attribute('href'))

for ast in allState:
	print('States: '+str(allState.index(ast)+1)+'/'+str(len(allState)))
	driver.get(ast)
	driver.implicitly_wait(20)
	time.sleep(5)

	if 'Oops...' not in driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'):
		state = driver.find_element(By.CLASS_NAME, 'link-list').find_elements(By.TAG_NAME, 'a')
		for st in state:
			allCity.append('/'.join(st.get_attribute('href').split('/')[4:]))

print('Done getting states and cities...')
driver.quit()

div = int(len(allCity)/10)

filepathHeaderCSV = 'healthgrades-gastro-final.csv'
fHeaderCSV = ['id', 'name', 'profession', 'company', 'office', 'phone', 'email', 'website', 'specialties', 'created_at']
append_list_as_row(filepathHeaderCSV, fHeaderCSV)

os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python healthgrades-gastro.py '+','.join(allCity[:div*1])+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python healthgrades-gastro.py '+','.join(allCity[div*1:div*2])+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python healthgrades-gastro.py '+','.join(allCity[div*2:div*3])+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python healthgrades-gastro.py '+','.join(allCity[div*3:div*4])+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python healthgrades-gastro.py '+','.join(allCity[div*4:div*5])+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python healthgrades-gastro.py '+','.join(allCity[div*5:div*6])+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python healthgrades-gastro.py '+','.join(allCity[div*6:div*7])+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python healthgrades-gastro.py '+','.join(allCity[div*7:div*8])+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python healthgrades-gastro.py '+','.join(allCity[div*8:div*9])+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python healthgrades-gastro.py '+','.join(allCity[div*9:])+'"')