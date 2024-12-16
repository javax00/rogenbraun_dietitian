from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
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
import getpass
import gspread
import pytz
import math
import time
import json
import os
import re

import sys
state = sys.argv[1].split(',')

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

filepathHeaderCSV = 'healthgrades-gastro-final.csv'

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

# CACHE
driver.get('https://www.healthgrades.com/gastroenterology-directory')
driver.implicitly_wait(20)
time.sleep(5)
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))).click()
time.sleep(2)

for stt in state:
	tot = 1
	printPage = str(state.index(stt)+1)+'/'+str(len(state))+' - '

	driver.get('https://www.healthgrades.com/gastroenterology-directory/'+stt)
	driver.implicitly_wait(20)
	time.sleep(3)

	if 'An error occurred when you requested this page.' in driver.find_element(By.TAG_NAME, 'body').text:
		print('Cant access: '+stt)
	else:
		try:
			driver.find_element(By.CLASS_NAME, 'sort-control__menu-btn').click()
			time.sleep(2)
			driver.find_elements(By.CLASS_NAME, 'sort-options')[-1].click()
			time.sleep(3)
		except Exception as e:
			pass

		nxt = 0
		links = []
		while nxt == 0:
			try:
				WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'results__results-cards')))

				lists = driver.find_element(By.CLASS_NAME, 'results__results-cards').find_elements(By.TAG_NAME, "li")
				for l in lists:
					if 'card-name' in l.get_attribute('innerHTML'):
						f = open("healthgrades-gastro-list.txt", "r")
						doc_names = f.read().split('\n')[:-1]

						new_name = []
						name = l.find_element(By.CLASS_NAME, 'card-name').text.strip().replace('Dr. ','').replace('Dr.','')
						for n in name.replace('\'','').split(' '):
							if not n.isupper():
								new_name.append(n.lower().split(',')[0])
						new_name = ' '.join(new_name)

						if new_name not in doc_names:
							links.append(l.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href'))

				if 'Page navigation' in driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'):
					nxtPage = driver.find_element(By.CLASS_NAME, 'results__pagination').find_elements(By.TAG_NAME, 'li')[-1]
					tot = driver.find_element(By.CLASS_NAME, 'results-title__results-title-count').text.split(' ')[0]
					pages = driver.find_element(By.CLASS_NAME, 'results__pagination').find_element(By.TAG_NAME, 'p').text.split(' ')

					print(printPage+'GETTING LINKS '+driver.find_element(By.CLASS_NAME, 'results__pagination').find_element(By.TAG_NAME, 'p').text.split(' ')[1]+' of '+str(math.ceil(int(tot)/22)))
					if driver.find_element(By.CLASS_NAME, 'results__pagination').find_element(By.TAG_NAME, 'p').text.split(' ')[1] == '99':
						nxt = 1
					elif 'heSiD' in nxtPage.get_attribute('outerHTML'):
						nxt = 1
					elif pages[1] == pages[3]:
						nxt = 1
					else:
						if 'is-bottom-ad-closed' in driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'):
							pass
						elif 'bottom-ad-close' in driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'):
							driver.find_element(By.CLASS_NAME, 'bottom-ad-close').click()
						nxtPage.find_element(By.TAG_NAME, 'a').click()
						time.sleep(3)
						nxt = 0
				else:
					nxt = 1
			except Exception as e:
				print('SKIP')
				nxt = 1
				pass

		for l in links:
			try:
				driver.get(l)
				WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
				name, company, office, phone, email, website, specialties = '','','','','','',''

				if 'ProviderDisplayName' in driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'):
					name = driver.find_element(By.TAG_NAME, 'h1').text

				if 'location-practice' in driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'):
					company = driver.find_element(By.CLASS_NAME, 'location-practice').text

				if 'location-row-address' in driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'):
					office = driver.find_element(By.CLASS_NAME, 'location-row-address').text

				if 'summary-standard-toggle-phone-number-button' in driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'):
					p = driver.find_elements(By.CLASS_NAME, 'summary-standard-toggle-phone-number-button ')[0].text
					phone = re.sub('\D', '', p)

				if 'about-me-subsection' in driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'):
					sp = driver.find_elements(By.CLASS_NAME, 'about-me-subsection')[0].find_elements(By.TAG_NAME, 'span')
					temp = []
					for ss in sp:
						if ss.text != '':
							temp.append(ss.text)
					specialties = ', '.join(temp)

				append_list_as_row(filepathHeaderCSV, [name, 'gastroenterologists',company, office, phone, email, website, specialties])
				print(printPage+'SCRAPING '+str(links.index(l)+1)+'/'+str(len(links)))

				new_name = []
				name = name.replace('Dr. ','').replace('Dr.','')
				for n in name.replace('\'','').split(' '):
					if not n.isupper():
						new_name.append(n.lower().split(',')[0])
				new_name = ' '.join(new_name)
				with open("healthgrades-gastro-list.txt", "a") as f:
					f.write(new_name+'\n')
			except Exception as e:
				pass

driver.quit()
print('\nDONE\n')








