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

exp = ['Culinary Nutrition',
		'Geriatric Nutrition',
		'Ketogenic Nutrition',
		'Nutrigenetics / Nutrigenomics',
		'Pediatric and Family Nutrition',
		'Personalized Nutrition / Medicine',
		'Sports Nutrition',
		'Therapeutic Food Plans']

# exp = ['Culinary Nutrition']

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
append_list_as_row(filepathHeaderCSV, fHeaderCSV)

err = 0
while err == 0:
	try:
		driver = webdriver.Chrome(options=options, service = Service(ChromeDriverManager().install()))
		driver.implicitly_wait(20)
		err = 1
	except Exception:
		err = 0
		time.sleep(5)

driver.get('https://portal.theana.org/s/professional-directory-list')
driver.implicitly_wait(20)
time.sleep(5)

Select(driver.find_element(By.XPATH, '//*[@id="62:2;a"]')).select_by_value('United States Of America (USA)')
time.sleep(2)
for x in exp:
	Select(driver.find_element(By.XPATH, '//*[@id="78:2;a"]')).select_by_value(x)
	time.sleep(5)

	users = driver.find_elements(By.CLASS_NAME, 'userProfile')
	for u in users:
		name=company=office=phone=email=website=specialties = ''

		link = u.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')

		##### NEW TAB
		driver.execute_script("window.open('');")
		driver.switch_to.window(driver.window_handles[1])
		driver.get(link)
		driver.implicitly_wait(20)
		time.sleep(5)

		name = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="CustomerPortalTemplate"]/div[1]/div/div[2]/div/div/c-professional-user-profile/div/div[2]/div[2]/div[1]/div/div/div'))).text

		right = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="CustomerPortalTemplate"]/div[1]/div/div[2]/div/div/c-professional-user-profile/div/div[2]/div[2]')))
		for i in right.find_elements(By.CLASS_NAME, 'pRow'):
			if i.find_element(By.TAG_NAME, 'span').text == 'Areas of Expertise':
				specialties = i.text.replace('Areas of Expertise\n','').replace('; ','\n')
				specialties = '' if specialties == 'N/A' else specialties

			if i.find_element(By.TAG_NAME, 'span').text == 'Email':
				email = i.text.replace('Email\n','').replace('Email','')
				email = '' if email == 'N/A' else email

			if i.find_element(By.TAG_NAME, 'span').text == 'Phone':
				p = i.text.replace('Phone\n','')
				phone = ''.join(re.findall("\d+", p))
				phone = '' if phone == 'N/A' else phone

			if i.find_element(By.TAG_NAME, 'span').text == 'Practice Name':
				company = i.text.replace('Practice Name\n','')
				company = '' if company == 'N/A' else company

			if i.find_element(By.TAG_NAME, 'span').text == 'Practice Website':
				website = i.text.replace('Practice Website\n','').replace('; ','\n')
				website = website.split('@')[1] if '@' in website else website
				website = '' if website == 'N/A' else website
				website = '' if website == 'None' else website

		driver.close()
		driver.switch_to.window(driver.window_handles[0])
		##### NEW TAB

		print('['+str(exp.index(x)+1)+'/'+str(len(exp))+'] - '+str(users.index(u)+1)+'/'+str(len(users)))
		append_list_as_row(filepathHeaderCSV, [name, company, office, phone, email, website, specialties])

driver.quit()
print('DONE')



