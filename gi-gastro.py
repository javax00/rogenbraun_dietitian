from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from fake_useragent import UserAgent
from twocaptcha import TwoCaptcha
from datetime import datetime
from pyhunter import PyHunter
from csv import writer
import pandas as pd
import threading
import requests
import random
import time
import json
import pytz
import os
import re

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

def accessLink():
	again = True
	while again == True:
		try:
			ua = UserAgent()

			prefs = {
				"download.open_pdf_in_system_reader": False,
				"download.prompt_for_download": True,
				"download.default_directory": "/dev/null",
				"plugins.always_open_pdf_externally": False,
				"download_restrictions": 3
			}

			options = Options()
			options.add_argument("--headless")
			options.add_argument('--no-sandbox')
			options.add_argument('--disable-gpu')
			options.add_argument('--start-maximized')
			options.add_argument('--disable-infobars')
			options.add_argument('--disk-cache-size=0')
			options.add_argument('--disable-extensions')
			options.add_argument('--disable-dev-shm-usage')
			options.add_argument("--disable-blink-features")
			options.add_argument('--disable-browser-side-navigation')
			options.add_argument('--ignore-certificate-errors-spki-list')
			options.add_argument('--disable-blink-features=AutomationControlled')
			options.add_experimental_option("prefs", prefs)
			options.add_experimental_option('useAutomationExtension', False)
			options.add_experimental_option("excludeSwitches", ["enable-automation"])
			options.add_experimental_option('excludeSwitches', ['enable-logging'])
			options.add_argument('--log-level=3')

			options.add_argument("window-size="+str(random.randint(1000, 2000))+","+str(random.randint(600, 1050)))
			options.add_argument(f'--user-agent={ua.random}')
			options.add_argument(f'user-agent={ua.random}')

			caps = DesiredCapabilities().CHROME
			caps["pageLoadStrategy"] = "normal" #or "eager" or "none"

			driver = webdriver.Chrome(options=options, desired_capabilities=caps, service=Service(ChromeDriverManager().install()))
			driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
			driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua.random})

			stealth(driver,
					languages=["en-US", "en"],
					vendor="Google Inc.",
					platform="Win32",
					webgl_vendor="Intel Inc.",
					renderer="Intel Iris OpenGL Engine",
					fix_hairline=True)
			again = False
		except Exception as e:
			again = True

	driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": f'{ua.random}'})
	return driver

states = ['Alabama',
			'Alaska',
			'Arizona',
			'Arkansas',
			'California',
			'Colorado',
			'Connecticut',
			'Delaware',
			'Florida',
			'Georgia',
			'Hawaii',
			'Idaho',
			'Illinois',
			'Indiana',
			'Iowa',
			'Kansas',
			'Kentucky',
			'Louisiana',
			'Maine',
			'Maryland',
			'Massachusetts',
			'Michigan',
			'Minnesota',
			'Mississippi',
			'Missouri',
			'Montana',
			'Nebraska',
			'Nevada',
			'New Hampshire',
			'New Jersey',
			'New Mexico',
			'New York',
			'North Carolina',
			'North Dakota',
			'Ohio',
			'Oklahoma',
			'Oregon',
			'Pennsylvania',
			'Rhode Island',
			'South Carolina',
			'South Dakota',
			'Tennessee',
			'Texas',
			'Utah',
			'Vermont',
			'Virginia',
			'Washington',
			'West Virginia',
			'Wisconsin',
			'Wyoming']

again = True
while again == True:
	driver = accessLink()
	driver.get('https://gi.org/patients/find-a-gastroenterologist/')
	time.sleep(5)

	try:
		driver.find_element(By.ID, 'cn-accept-cookie').click()
	except Exception as e:
		pass
	time.sleep(3)

	driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])
	if 'Google Maps JavaScript API' in driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'):
		driver.quit()
	else:
		again = False

filepathHeaderCSV = 'gi-gastro-final.csv'
fHeaderCSV = ['id', 'name', 'profession', 'company', 'office', 'phone', 'email', 'website', 'specialties', 'created_at']
try:
	os.remove(filepathHeaderCSV)
	time.sleep(1)
except Exception as e:
	pass
append_list_as_row(filepathHeaderCSV, fHeaderCSV)

c = 1
for state in states:
	print(str(states.index(state)+1),'-',str(len(states)),'\n')
	driver.find_element(By.ID, 'addressInput').clear()
	driver.find_element(By.ID, 'addressInput').send_keys(state)
	driver.find_element(By.ID, 'searchButton').click()
	time.sleep(5)
	if 'Total Results :0' not in driver.find_element(By.ID, 'totalcount').text:
		for doc in driver.find_element(By.ID, 'searchresults').find_elements(By.TAG_NAME, 'div'):
			print(c)

			name, company, office, phone, email, website, specialties = '','','','','','',''
			data = doc.find_elements(By.TAG_NAME, 'td')[0].text.split('\n')

			name = data[0]

			if data[1].count(',') == 2:
				office = data[1]

				num = re.sub('\D', '', data[2])
				if len(num) == 10:
					phone = num
			else:
				company = data[1]
				office = data[2]

				num = re.sub('\D', '', data[3])
				if len(num) == 10:
					phone = num

			for d in data:
				if 'www.' in d:
					website = d

			if office == ',,':
				office = ''

			append_list_as_row(filepathHeaderCSV, ['', name, 'gastro', company, office, phone, email, website, specialties, ''])
			c+=1

driver.quit()