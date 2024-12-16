from datetime import datetime
from csv import writer
import time
import pytz
import sys
import os

site_name = 'healthgrades-gastro-final'

def append_list_as_row(file_name, list_of_elem):
	with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
		csv_writer = writer(write_obj)
		csv_writer.writerow(list_of_elem)

date = datetime.utcnow().replace(tzinfo=pytz.utc).strftime('%Y-%m-%d_%H-%M-%S')
filepathHeaderCSV = site_name+'-verified-'+str(date)+'.csv'
fHeaderCSV = ['id', 'name', 'profession', 'company', 'office', 'phone', 'email', 'website', 'specialties', 'created_at']
append_list_as_row(filepathHeaderCSV, fHeaderCSV)

os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 1 '+filepathHeaderCSV+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 2 '+filepathHeaderCSV+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 3 '+filepathHeaderCSV+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 4 '+filepathHeaderCSV+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 5 '+filepathHeaderCSV+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 6 '+filepathHeaderCSV+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 7 '+filepathHeaderCSV+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 8 '+filepathHeaderCSV+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 9 '+filepathHeaderCSV+'"')
os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 10 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 11 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 12 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 13 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 14 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 15 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 16 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 17 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 18 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 19 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 20 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 21 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 22 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 23 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 24 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 25 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 26 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 27 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 28 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 29 '+filepathHeaderCSV+'"')
# os.system('start cmd.exe /k "mode con cols=63 lines=14 & G: & cd \"Other computers\My MacBook Air\RogerBraun\" & python verifyEmail.py '+site_name+' 30 '+filepathHeaderCSV+'"')