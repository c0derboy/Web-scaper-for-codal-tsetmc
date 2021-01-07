import selenium
from selenium import webdriver
from unidecode import unidecode
import time

def numfix(num):
    a = num.replace(',', '')
    a = a.replace('(', '')
    a = a.replace(')', '')
    a = unidecode(a)
    try:
        a = int(a)
    except:
        print('Error!')
    return a


def get_data(link):
	mali = link + '&sheetId=0'
	naghdi = link+ '&sheetId=9'

	driver = webdriver.Chrome(executable_path = r'C:\Users\Sina\Desktop\chromedriver.exe')
	driver.get(mali)


	#Shares
	shares = driver.find_element_by_css_selector('#ctl00_lblListedCapital').text
	shares = numfix(shares)
	shares *= 1000
	print(shares)


	#Equity
	equity = driver.find_elements_by_css_selector('table>tbody>tr:nth-child(32) td')[1].text
	equity = numfix(equity)
	equity *= 1000000
	print(equity)


	#ChashFlow
	driver.get(naghdi)

	cashflow = driver.find_elements_by_css_selector('table>tbody>tr:nth-child(4) td')
	data = [i.text for i in list(cashflow)][1:4]
	data = [numfix(i) for i in data]
	cash = data[2] - data[1] + data[0]
	cash *= 1000000
	print(cash)
	cps = cash / shares
	bps = equity / shares
	print(f'BPS: {bps:.0f} | CPS: {cps:.0f}')

	driver.close()
#link = 'https://codal.ir/Reports/Decision.aspx?LetterSerial=1gr1Ya1g%2BpC0fcDqU5BnHw%3D%3D&rt=0&let=6&ct=0&ft=-1'
link = str(input('link='))

get_data(link)
#add readName

