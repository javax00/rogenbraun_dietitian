from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

def has_numbers(inputString):
	return any(char.isdigit() for char in inputString)

options = Options()
# options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

filepathHeaderCSV = 'dietitiancentral.csv'
fHeaderCSV = ['id', 'name', 'profession', 'company', 'office', 'phone', 'email', 'website', 'specialties', 'created_at']
try:
	os.remove(filepathHeaderCSV)
	time.sleep(1)
except Exception as e:
	pass
append_list_as_row(filepathHeaderCSV, fHeaderCSV)

err = 0
while err == 0:
	try:
		driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
		driver.implicitly_wait(20)
		err = 1
	except Exception:
		err = 0
		time.sleep(5)

driver.get('https://www.dietitiancentral.com/rd/rd_search_results.cfm')
time.sleep(5)

lastPage = driver.find_element(By.CLASS_NAME, 'pagination').find_elements(By.TAG_NAME, 'li')[-1].text
for i in range(0, int(lastPage)):
	page = driver.find_element(By.CLASS_NAME, 'pagination').find_elements(By.TAG_NAME, 'li')[i].find_element(By.TAG_NAME, 'a')
	print(page.get_attribute('id'))
	page.click()
	time.sleep(5)

	name, company, office, phone, email, website, specialties = '','','','','','',''

	con = driver.find_elements(By.CLASS_NAME, 'content')[1].find_elements(By.CLASS_NAME, 'container-fluid')
	for c in con:
		row = c.find_elements(By.CLASS_NAME, 'Row')
		name = row[1].text.strip()
		for r in row:
			if 'Company:' in r.text:
				com = r.text.replace('Company:', '').strip()
				if com == 'NA':
					company = ''
				else:
					company = com
			elif 'OFFICE 1:' in r.text:
				o = r.text.replace('OFFICE 1:', '').replace('\n', ', ').strip()
				if o[0:2] == ', ':
					office = o[2:]
				else:
					office = o
			elif 'PHONE:' in r.text:
				p = r.text.replace('PHONE:', '').strip()

				if has_numbers(p) == False:
					phone = ''
				elif 'x' in p:
					pp = re.sub('\D', '', p.split('x')[0])
					if len(pp) == 10:
						phone = pp
					elif len(pp) == '11':
						phone = pp
					else:
						phone = pp
				elif 'op' in p:
					pp = re.sub('\D', '', p.split('op')[0])
					if len(pp) == 10:
						phone = pp
					elif len(pp) == '11':
						phone = pp
					else:
						phone = pp
				else:
					pp = re.sub('\D', '', p.split('op')[0])
					if len(pp) == 10:
						phone = pp
					elif len(pp) == '11':
						phone = pp
					else:
						phone = pp
			elif 'SPECIALTIES:' in r.text:
				specialties = r.text.replace('SPECIALTIES:', '').replace('\n','').strip()

		row = c.find_element(By.CLASS_NAME, 'col-md-2').find_elements(By.TAG_NAME, 'div')
		try:
			email = row[0].find_element(By.TAG_NAME, 'button').get_attribute('onclick').split('\',\'')[-1][:-2]
		except Exception:
			pass

		try:
			website = row[1].find_element(By.TAG_NAME, 'a').get_attribute('href')
		except Exception:
			pass

		print(name)
		append_list_as_row(filepathHeaderCSV, ['', name, 'dietitian', company, office, phone, email, website, specialties, ''])
		# time.sleep(3)
	print('~')
driver.quit()


























