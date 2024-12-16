from selenium import webdriver
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import time


def get_proxies():
	co = webdriver.ChromeOptions()
	co.add_argument("log-level=3")
	# co.add_argument("--headless")

	driver = webdriver.Chrome(options=co, service=Service(ChromeDriverManager().install()))
	driver.get("https://free-proxy-list.net/")

	PROXIES = []
	proxies = driver.find_elements(By.TAG_NAME, 'tbody')[0].find_elements(By.TAG_NAME, 'tr')
	for p in proxies:
		result = p.find_elements(By.TAG_NAME, 'td')

		if result[6].text.strip() == "yes":
			PROXIES.append(result[0].text.strip()+":"+result[1].text.strip())
			print(result[0].text.strip()+":"+result[1].text.strip())

	driver.close()
	return PROXIES


ALL_PROXIES = get_proxies()


def proxy_driver(PROXIES):
	prox = Proxy()

	pxy = ''
	if PROXIES:
		pxy = PROXIES[-1]
	else:
		print("--- Proxies used up (%s)" % len(PROXIES))
		PROXIES = get_proxies()

	prox.proxy_type = ProxyType.MANUAL
	prox.http_proxy = pxy

	prox.ssl_proxy = pxy

	capabilities = webdriver.DesiredCapabilities.CHROME
	prox.add_to_capabilities(capabilities)

	co = webdriver.ChromeOptions()
	co.add_argument("log-level=3")
	# co.add_argument("--headless")

	driver = webdriver.Chrome(options=co, desired_capabilities=capabilities, service=Service(ChromeDriverManager().install()))

	return driver



# --- YOU ONLY NEED TO CARE FROM THIS LINE ---
# creating new driver to use proxy
pd = proxy_driver(ALL_PROXIES)

# code must be in a while loop with a try to keep trying with different proxies
running = True

while running:
	try:
		pd.get('https://health.usnews.com/doctors/gastroenterologists')
		time.sleep(5)
		if 'Access Denied' in pd.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'):
			int('abc')

		try:
			pd.find_element(By.ID, 'gdpr-modal-agree').click()
		except:
			pass

		###
	except:
		new = ALL_PROXIES.pop()
		
		# reassign driver if fail to switch proxy
		pd = proxy_driver(ALL_PROXIES)
		print("--- Switched proxy to: %s" % new)
		time.sleep(1)