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

filepathHeaderCSV = 'theana-final.csv'
fHeaderCSV = ['Name', 'Company', 'Office', 'Phone', 'Email', 'Website', 'Specialties']

try:
	os.remove(filepathHeaderCSV)
	time.sleep(1)
except Exception as e:
	pass
# append_list_as_row(filepathHeaderCSV, fHeaderCSV)

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

driver.get('https://directory.net/doctors')
driver.implicitly_wait(20)

pc = 1
nxt = True
while nxt == True:
	allName = []
	nls = driver.find_elements(By.CLASS_NAME, 'names-list')
	for nl in nls:
		lis = nl.find_elements(By.TAG_NAME, 'a')
		for li in lis:
			allName.append(li.get_attribute('href'))

	for an in allName:
		##### NEW TAB
		driver.execute_script("window.open('');")
		driver.switch_to.window(driver.window_handles[1])
		driver.get(an)

		WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'person-table')))

		name=company=office=phone=email=website=specialties = ''

		sps = driver.find_elements(By.CLASS_NAME, 'person-table')
		for sp in sps:
			name = driver.find_element(By.TAG_NAME, 'h1').text.strip()
			if "Provider Profile Details:" in sp.get_attribute('innerHTML')
				Specialization
				Phone Number
			if "Provider Business Practice Location Address Details:" in sp.get_attribute('innerHTML')
				Address
				City
				State
				Zip
				Phone Number
			if "Provider Business Mailing Address Details:" in sp.get_attribute('innerHTML')
				Phone Number
			if "Provider's Primary Taxonomy Details:" in sp.get_attribute('innerHTML')
				Type
				Speciality

		if specialty == 'Dietitian, Registered' or specialty == 'Nutritionist':

		driver.close()
		driver.switch_to.window(driver.window_handles[0])
		##### NEW TAB

		print('['+str(pc)+'/85] - '+str(allName.index(an)+1)+'/'+str(len(allName))+' - '+specialties)

	page = driver.find_element(By.CLASS_NAME, 'pagination').find_elements(By.TAG_NAME, 'li')[-1]
	if 'next' in page.get_attribute('innerHTML'):
		page.find_element(By.TAG_NAME, 'a').click()
	else:
		nxt = False

	pc+=1

driver.quit()