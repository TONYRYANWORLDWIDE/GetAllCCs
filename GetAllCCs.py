import pandas as pd
import os
import requests as req
from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time
from time import sleep 
from selenium.webdriver.common.keys import Keys
import urllib
import requests
from bs4 import BeautifulSoup
import pandas
from pandas import DataFrame
Balance_CSV  = 'C:/Users/tonyr/Desktop/BUDGET STUFF/KeyBalance.csv'

req = req.get('https://mint.com')

usr= 'tonyryanworldwide@gmail.com '#input('Enter Email Id:')  
pwd='Secret#8'#input('Enter Password:') 

url = "https://www.mint.com/"

path = 'C:/Users/tonyr/ChromeDriver/chromedriver_win32'
os.chdir(path)
cwd = os.getcwd()
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
driver = webdriver.Chrome(options=options)

driver.get(url)

sleep(1) 

Login = driver.find_element_by_xpath('/html/body/div[1]/div/section[1]/header/div/div[3]/a[2]')
Login.click()

username_box = driver.find_element_by_id('ius-userid') 
username_box.send_keys(usr) 

sleep(1) 
  
password_box = driver.find_element_by_id('ius-password') 
password_box.send_keys(pwd) 

SignInClick = driver.find_element_by_id('ius-sign-in-submit-btn-text') 
SignInClick.click() 

sleep(30)

x = driver.find_element_by_class_name('pageContentSection')
xtext = x.text
while xtext.lower().find('refreshing') >= 0:
    print('Waiting For Refresh')
    sleep(10)
    x = driver.find_element_by_class_name('pageContentSection')
    xtext = x.text
# transactions = driver.find_element_by_id('transaction')
# transactions.click()
sleep(3)

page = driver.find_element_by_class_name('AccountsView')
a = page.text

p2 = driver.find_element_by_id('moduleAccounts-credit')
p3 = p2.get_attribute('outerHTML')
p4 = BeautifulSoup(p3, 'html.parser')
CClist = p4.ul.find_all('h4')
CCDict = {}
for cc in range(0,len(CClist)):
    #print (CClist[cc])
    CCDict[CClist[cc].a.text] = CClist[cc].span.text


page = driver.find_element_by_id('moduleAccounts-bank')
pg = page.get_attribute('outerHTML')
pgfin = BeautifulSoup(pg, 'html.parser')
CU = pgfin.h4.span.text
CU = CU.replace('$','').replace(',','')

p2 = driver.find_element_by_id('moduleAccounts-investment')
p3 = p2.get_attribute('outerHTML')
p4 = BeautifulSoup(p3, 'html.parser')
Invest = p4.div.h3.span.next_sibling.text
Invest = Invest.replace('$','').replace(',','')
Invest = str(round((float(Invest) - 5847.85),2))

CCDict2 = {}
for i in CCDict.keys():
    print(i.find('Bank of America'))
    if i.find('Bank') != -1:
        CCDict2['BOA'] = float(CCDict[i].replace('$','').replace(',','')) * - 1
        continue        
    elif i.find('Amex') != -1:
        CCDict2['Amex'] = float(CCDict[i].replace('$','').replace(',','')) * - 1
        continue
    elif i.find('Quick') != -1:
        CCDict2['CAP'] = float(CCDict[i].replace('$','').replace(',',''))  * - 1 
        continue
    elif i.lower().find('amazon') != -1:
        CCDict2['Chase Amazon'] = float(CCDict[i].replace('$','').replace(',',''))  * - 1
        continue      
        
row = []
for i in CCDict2.values():
    row.append(i)    


import csv
import os
import datetime
path = 'C:/Users/Tonyr/Desktop/'
os.chdir(path)
cwd = os.getcwd()

csv.register_dialect('myDialect', delimiter = ',', lineterminator = '\n')

row = []

for i in CCDict2.values():
    row.append(i)
    
row2 = [CU,11976.05,datetime.datetime.now(),Invest]
#13286.31 is what we owe Don now
finrow = row + row2

with open('Assets.csv', 'a') as csvFile:
    writer = csv.writer(csvFile, dialect = 'myDialect')
    writer.writerow(finrow )

csvFile.close()