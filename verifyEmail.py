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

def has_numbers(inputString):
	return any(char.isdigit() for char in inputString)

def scrapeGoogle(name, link):
	driver = accessLink()
	again = 0
	while again == 0:
		try:
			driver.get(link)
			time.sleep(random.randint(1, 2))

			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))

			if 'g-recaptcha-response' in driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'):
				print('			CAPTCHA FOUND')

				API_KEY = "c6c7ceffb1a10b7cdf72b572fef49eaf"
				data_s = driver.find_element(By.ID, 'recaptcha').get_attribute('data-s')
				data_sitekey = driver.find_element(By.ID, 'recaptcha').get_attribute('data-sitekey')

				########################
				u1 = f"https://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={link}&json=1&data-s={data_s}"

				try:
					r1 = requests.get(u1)
					rid = r1.json().get("request")
				except requests.exceptions.RequestException:
					print('ERROR: request exception')
				except requests.exceptions.ConnectionError:
					print('ERROR: connection error')

				time.sleep(20)
				while True:

					try:
						u2 = f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={int(rid)}&json=1"
						r2 = requests.get(u2)
					except requests.exceptions.RequestException:
						print('ERROR: request exception')
					except requests.exceptions.ConnectionError:
						print('ERROR: connection error')

					if r2.json().get("status") == 1:
						form_tokon = r2.json().get("request")
						break
					time.sleep(20)
				########################
				# solver = TwoCaptcha(API_KEY)

				# try:
				# 	result = solver.recaptcha(
				# 		sitekey=data_sitekey,
				# 		url=link,
				# 		datas=data_s)
				# except Exception as e:
				# 	print('ERROR DAW:',str(e))
				# else:
				# 	result = result['code']
				########################

				container = driver.find_element(By.ID, 'g-recaptcha-response')
				driver.execute_script("arguments[0].style.display = 'block';", container)
				driver.find_element(By.ID, 'g-recaptcha-response').send_keys(form_tokon)
				time.sleep(1)
				driver.find_element(By.ID, 'captcha-form').submit()

				again = 0
			else:
				print('			CAPTCHA DONE')
				again = 1
		except Exception as e:
			print(str(e))
			again = 0
			driver.quit()

	rLinks = []
	temp_emails = []
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))

	if 'Gx5Zad' in driver.find_element(By.TAG_NAME, 'html').get_attribute('innerHTML'):
		gLinks = driver.find_element(By.ID, 'main').find_elements(By.CLASS_NAME, 'egMi0')
		for gl in gLinks:
			try:
				rLinks.append('https://'+gl.find_element(By.TAG_NAME, 'a').get_attribute('href').split('://')[2].split('&ved')[0])
			except Exception:
				pass
	if 'ezO2md' in driver.find_element(By.TAG_NAME, 'html').get_attribute('innerHTML'):
		gLinks = driver.find_element(By.TAG_NAME, 'body').find_elements(By.CLASS_NAME, 'ezO2md')
		for gl in gLinks:
			try:
				rLinks.append('https://'+gl.find_element(By.TAG_NAME, 'a').get_attribute('href').split('://')[2].split('&ved')[0])
			except Exception:
				pass
	if 'MjjYud' in driver.find_element(By.TAG_NAME, 'html').get_attribute('innerHTML'):
		gLinks = driver.find_elements(By.CLASS_NAME, 'MjjYud')
		for gl in gLinks:
			try:
				rLinks.append('https://'+gl.find_element(By.TAG_NAME, 'a').get_attribute('href').split('://')[2].split('&ved')[0])
			except Exception:
				pass
	driver.quit()

	for rl in rLinks:
		if rl.split('/')[2] not in allLinks and 'google.com' not in rl and 'linkedin.com' not in rl:
			# print('		'+rl.split('/')[2].replace('www.',''))
			try:
				driver = accessLink()
				driver.get(rl)
				body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html'))).text.split(' ')
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				for b in body:
					if '@' in b:
						temp_emails.append(b)
			except Exception:
				pass

			allLinks.append(rl.split('/')[2])
			driver.quit()

	if temp_emails != []:
		temp = []
		for r in temp_emails:
			if str(r)[-1] == '.':
				r = str(r)[:-1]

			if str(r)[0] == '@':
				pass
			elif '\n' in str(r):
				for i in str(r).split('\n'):
					if '@' in i:
						if i.lower() not in temp:
							temp.append(i.lower())
			elif '@' in str(r):
				if r.lower() not in temp:
					temp.append(r.lower())

		final = []
		c = 0
		for t in temp:
			print('			',t)
			if c <= 10:
				try:
					driver = accessLink()
					driver.set_page_load_timeout(5)
					driver.implicitly_wait(5)
					driver.get('https://api.hunter.io/v2/email-verifier?email='+t+'&api_key='+api_key)
					time.sleep(.5)
					WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
					ve = json.loads(driver.find_element(By.TAG_NAME, 'body').text)['data']['status']
					if ve == 'valid' or ve == 'accept_all' or ve == 'webmail':
						print('			 -',ve)
						final.append(t)

					driver.quit()
				except Exception:
					driver.quit()
					pass
			c+=1
		return '\n'.join(final)
	return ''

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

def nospecial(text):
	import re
	text = re.sub("[^a-zA-Z ]+", "",text)
	return text

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

def main(lists, start, end, index):
	# starts = end-start
	for l in lists:
		# starts += 1
		new_name = []
		for n in l['name'].replace('\'','').split(' '):
			if not n.isupper():
				new_name.append(n.lower().split(',')[0])
		new_name = ' '.join(new_name).replace('dr. ','').replace('dr.','').replace('phd','').replace('msci','').replace('msc','').replace('(epi)','')

		try:
			f = open("DOCTORS-NAME-GASTRO.txt", "r")
			doc_names = f.read().split('\n')[:-1]
		except Exception:
			doc_names = []
			with open('DOCTORS-NAME-GASTRO.txt', 'w') as fp:
				pass

		if new_name not in doc_names:
			# print(index+' - '+str(starts)+'/'+str(end)+' - '+l['name'])
			print(index+' - '+str(lists.index(l)+1)+'/'+str(len(lists))+' - '+l['name'])

			name=profession=company=office=phone=email=website=specialties = ''

			if str(l['name']) != 'nan':
				name = l['name'].replace('\'','').replace('\n','')

			if str(l['profession']) != 'nan':
				profession = l['profession']

			if str(l['company']) != 'nan':
				company = l['company']

			if str(l['website']) != 'nan':
				website = l['website']

			if str(l['email']) != 'nan':
				em = l['email'].split(' ')
				if len(em) == 1:
					if '@' in em[0]:
						email = em[0].lower().strip()
				else:
					if (' @' in l['email'] or '@ ' in l['email']) and len(em) == 2:
						email = ''.join(em).lower().strip()
					else:
						for e in em:
							if '@' in e:
								email = e.lower().strip()
								break
				email = email.replace(',','.')

			if str(l['office']) != 'nan':
				office = l['office']

			if str(l['phone']) != 'nan':
				if len(str(l['phone'])) >= 9 and len(str(l['phone'])) <= 13:
					phone = str(l['phone'])

			if str(l['specialties']) != 'nan':
				specialties = l['specialties']

			if name == '' or name == 'nan' or has_numbers(name) == True:
				pass
			else:
				############### VERIFY EMAIL ###############
				if email != '':
					print('	Validating email')
					try:
						driver = accessLink()
						driver.set_page_load_timeout(5)
						driver.implicitly_wait(5)
						driver.get('https://api.hunter.io/v2/email-verifier?email='+email+'&api_key='+api_key)
						time.sleep(.5)
						WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
						ve = json.loads(driver.find_element(By.TAG_NAME, 'body').text)['data']['status']
						if ve == 'valid' or ve == 'accept_all' or ve == 'webmail':
							email = email.lower()
						else:
							email = ''
					except Exception:
						pass

				if email == None:
					email = ''

				############### 1 FIND EMAILS via GOOGLE ###############
				if email == '':
					print('	► Finding email via Google')
					if 'http' in website:
						web = website.split('/')[2]
					else:
						web = website.split('/')[0]

					global allLinks
					allLinks = []

					print('		Google operator 1/4')
					email = scrapeGoogle(name, 'https://google.com/search?q='+name)

					# if email == '':
					# 	print('		Google operator 2/4')
					# 	if website != '':
					# 		email = scrapeGoogle(name, 'https://google.com/search?q='+name+' '+website)

					# 	if email == '':
					# 		print('		Google operator 3/4')
					# 		if phone != '':
					# 			email = scrapeGoogle(name, 'https://google.com/search?q='+name+' '+phone)

					# 		if email == '':
					# 			print('		Google operator 4/4')
					# 			if office != '':
					# 				email = scrapeGoogle(name, 'https://google.com/search?q='+name+' '+office)

				############### 2 FIND EMAILS via COMBI ###############
				if has_numbers(name) == True:
					name = ''
				elif email == '':
					print('	► Finding email via Combi')
					domain = website.replace('https://','').replace('http://','').replace('www.','').split('/')[0].split('?')[0].split('&')[0]
					if len(new_name) == 1:
						combi = [''.join(new_name),
								'.'.join(new_name),
								'dr'+new_name[0],
								'dr.'+new_name[0]]
					else:
						combi = []
						try:
							combi.append(''.join(new_name))
						except:
							pass
						try:
							combi.append('.'.join(new_name))
						except:
							pass
						try:
							combi.append(new_name[0]+new_name[1][0])
						except:
							pass
						try:
							combi.append(new_name[0][0]+new_name[1])
						except:
							pass
						try:
							combi.append(new_name[0]+'.'+new_name[1][0])
						except:
							pass
						try:
							combi.append(new_name[0][0]+'.'+new_name[1])
						except:
							pass
						try:
							combi.append('dr'+new_name[0])
						except:
							pass
						try:
							combi.append('dr'+new_name[1])
						except:
							pass
						try:
							combi.append('dr.'+new_name[0])
						except:
							pass
						try:
							combi.append('dr.'+new_name[1])
						except:
							pass

					final_email = []
					for c in combi:
						if '.' in domain:
							new_email = c+'@'+domain
							try:
								driver = accessLink()
								driver.set_page_load_timeout(5)
								driver.implicitly_wait(5)
								driver.get('https://api.hunter.io/v2/email-verifier?email='+new_email+'&api_key='+api_key)
								time.sleep(.5)
								WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
								ve = json.loads(driver.find_element(By.TAG_NAME, 'body').text)['data']['status']
								if ve == 'valid' or ve == 'accept_all' or ve == 'webmail':
									final_email.append(new_email)
									break

								driver.quit()
							except Exception as e:
								print(str(e))
								driver.quit()
								pass
					email = '\n'.join(final_email)

				############### 3 FIND EMAILS via INFO ###############
				# if email == '':
				# 	print('	► Finding email via Info')
				# 	try:
				# 		driver = accessLink()
				# 		driver.set_page_load_timeout(5)
				# 		driver.implicitly_wait(5)
				# 		driver.get('''https://api.hunter.io/v2/email-finder?
				# 						domain='''+website+'''
				# 						&company='''+company+'''
				# 						&full_name='''+name+'''
				# 						&max_duration=10
				# 						&api_key='''+api_key)
				# 		time.sleep(.5)
				# 		WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
				# 		if 'reached the limit' in driver.find_element(By.TAG_NAME, 'body').text:
				# 			print('		Reached the limit')
				# 		else:
				# 			fe = json.loads(driver.find_element(By.TAG_NAME, 'body').text)['data']['email'].lower()
				# 			email = fe
				# 		driver.quit()
				# 	except Exception:
				# 		driver.quit()
				# 		pass

				########################################## END ##########################################

				if name != '':
					append_list_as_row(filepathHeaderCSV, ['', str(name), str(profession), str(company), str(office), str(phone), str(email), str(website), str(specialties), ''])
					with open("DOCTORS-NAME-GASTRO.txt", "a") as f:
						f.write(''.join(new_name)+'\n')

					if email == '':
						print('  ▐ No email found ▐')
					else:
						print('  √ Found an email')
		else:
			print(index+' - '+str(lists.index(l)+1)+'/'+str(len(lists))+' - '+l['name']+' - DONE')
			# print(index+' - '+str(starts)+'/'+str(end)+' - '+l['name']+' - DONE')
	print('DONE -',index)

####################################################################################
import sys
site_name = sys.argv[1]
num = sys.argv[2]
filepathHeaderCSV = sys.argv[3]

# hunter = PyHunter('fe5f6b39d36d01411c397c0eee2d3af8f0dc12a5')
api_key = 'fe5f6b39d36d01411c397c0eee2d3af8f0dc12a5'
df = pd.read_csv(site_name+'.csv', low_memory=False)#, nrows=100)

lists = []
for i in df.index:
	con = {}
	for x in df:
		if str(x) == 'name':
			con['name'] = str(df[x][i])

	for x in df:
		if str(x) == 'profession':
			con['profession'] = str(df[x][i])

	for x in df:
		if str(x) == 'company':
			con['company'] = str(df[x][i])

	for x in df:
		if str(x) == 'office':
			con['office'] = str(df[x][i])

	for x in df:
		if str(x) == 'phone':
			con['phone'] = str(df[x][i])

	for x in df:
		if str(x) == 'email':
			con['email'] = str(df[x][i])

	for x in df:
		if str(x) == 'website':
			con['website'] = str(df[x][i])

	for x in df:
		if str(x) == 'specialties':
			con['specialties'] = str(df[x][i])

	lists.append(con)

accessLink()
time.sleep(5)

div = int(len(lists)/10)

if num == '1':
	main(lists[:div*1], div, div*1, '1')
elif num == '2':
	main(lists[div*1:div*2], div, div*2, '2')
elif num == '3':
	main(lists[div*2:div*3], div, div*3, '3')
elif num == '4':
	main(lists[div*3:div*4], div, div*4, '4')
elif num == '5':
	main(lists[div*4:div*5], div, div*5, '5')
elif num == '6':
	main(lists[div*5:div*6], div, div*6, '6')
elif num == '7':
	main(lists[div*6:div*7], div, div*7, '7')
elif num == '8':
	main(lists[div*7:div*8], div, div*8, '8')
elif num == '9':
	main(lists[div*8:div*9], div, div*9, '9')
elif num == '10':
	main(lists[div*9:], div, div*10, '10')
# elif num == '10':
# 	main(lists[div*9:div*10], div, div*10, '10')
# elif num == '11':
# 	main(lists[div*10:div*11], div, div*11, '11')
# elif num == '12':
# 	main(lists[div*11:div*12], div, div*12, '12')
# elif num == '13':
# 	main(lists[div*12:div*13], div, div*13, '13')
# elif num == '14':
# 	main(lists[div*13:div*14], div, div*14, '14')
# elif num == '15':
# 	main(lists[div*14:div*15], div, div*15, '15')
# elif num == '16':
# 	main(lists[div*15:div*16], div, div*16, '16')
# elif num == '17':
# 	main(lists[div*16:div*17], div, div*17, '17')
# elif num == '18':
# 	main(lists[div*17:div*18], div, div*18, '18')
# elif num == '19':
# 	main(lists[div*18:div*19], div, div*19, '19')
# elif num == '20':
# 	main(lists[div*19:], div, div*20, '20')
# elif num == '20':
# 	main(lists[div*19:div*20], div, div*20, '20')
# elif num == '21':
# 	main(lists[div*20:div*21], div, div*21, '21')
# elif num == '22':
# 	main(lists[div*21:div*22], div, div*22, '22')
# elif num == '23':
# 	main(lists[div*22:div*23], div, div*23, '23')
# elif num == '24':
# 	main(lists[div*23:div*24], div, div*24, '24')
# elif num == '25':
# 	main(lists[div*24:div*25], div, div*25, '25')
# elif num == '26':
# 	main(lists[div*25:div*26], div, div*26, '26')
# elif num == '27':
# 	main(lists[div*26:div*27], div, div*27, '27')
# elif num == '28':
# 	main(lists[div*27:div*28], div, div*28, '28')
# elif num == '29':
# 	main(lists[div*28:div*29], div, div*29, '29')
# elif num == '30':
# 	main(lists[div*29:], div, div*30, '30')
