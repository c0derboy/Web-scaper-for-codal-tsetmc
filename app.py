import selenium
from selenium import webdriver
from unidecode import unidecode
import time

#fuctions
#fix the numbers and get integers
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

#convert persian into english
def namefix(name):
    persian = ['آ', 'ا', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز','ژ' , 'س', 'ش', 'ص', 'ض', 'ط', 'ظ','ع','غ','ف','ق','ک','گ','ل','م','ن','و', 'ه', 'ي']
    english = ['a', 'a', 'b', 'p', 't', 's', 'j', 'ch', 'kh', 'h', 'd', 'z', 'r', 'z', 'zh','s', 'sh','s','z','t','z','h','x','f','gh','k','g','l','m','n','v','h','i']
    fix = name
    for a in range(len(persian)):
        fix = fix.replace(persian[a], english[a])
    return fix

#render codal links
def renderlinks(list):
	for i in range(len(list)):
		list[i] = list[i].replace('\n', '')

#calculate bps and cps
def calculate_bps_cps(shares, equity, cash):
	cps = cash / shares
	bps = equity / shares
	return {'bps': bps, 'cps': cps}

#get data from tsetmc
def get_price(symbol):
	main = 'http://www.tsetmc.com/Loader.aspx?ParTree=15'
	driver.get(main)


	driver.execute_script("javascript:ShowSearchWindow();")
	driver.execute_script("SearchKey.value = arguments[0];", (symbol))
	driver.execute_script('GetSearchResult();')

	search_results = driver.find_element_by_id('SearchResult')

	while True:
	    try:
	        stock = search_results.find_element_by_css_selector('a').get_attribute('href')
	        break
	    except:
	        continue
	            
	driver.get(stock)
	#to fix
	while True:
	    price = driver.find_element_by_id('d02').text.split('  ')
	    if price == ['']:
	        continue
	    else:
	        break
	print(price)
	try:
		price_changes = price[2][1:-1]
	except:
		price_changes = 'None'
	price = int(price[0].replace(',', ''))

	yearly_lowhigh = driver.find_elements_by_css_selector('.box6:nth-child(2)>table>tbody>tr:nth-child(4) td')
	yearly_lowhigh = yearly_lowhigh[1:]
	yearly_lowhigh = [i.text for i in yearly_lowhigh]
	yearly_lowhigh = [numfix(i) for i in yearly_lowhigh]
	yearly_high = yearly_lowhigh[0]
	yearly_low = yearly_lowhigh[1]
	return {'price': price, 'price changes':price_changes, 'yearly high':yearly_high, 'yearly low':yearly_low}

#get data from codal
def get_data(link):
	mali = link + '&sheetId=0'
	naghdi = link+ '&sheetId=9'
	driver.get(mali)

	#get symbol
	symbol = driver.find_element_by_css_selector('#ctl00_txbSymbol').text
	fixedsymbol = namefix(symbol)

	#get name
	name = driver.find_element_by_css_selector('#ctl00_txbCompanyName').text
	name = namefix(name)
	#Shares
	shares = driver.find_element_by_css_selector('#ctl00_lblListedCapital').text
	shares = numfix(shares)
	shares *= 1000


	#Equity
	equity = driver.find_elements_by_css_selector('table>tbody>tr:nth-child(32) td')[1].text
	equity = numfix(equity)
	equity *= 1000000


	#ChashFlow
	driver.get(naghdi)

	cashflow = driver.find_elements_by_css_selector('table>tbody>tr:nth-child(4) td')
	data = [i.text for i in list(cashflow)][1:4]
	data = [numfix(i) for i in data]
	cash = data[2] - data[1] + data[0]
	cash *= 1000000
	return {'stock': {'symbol': fixedsymbol, 'name':name, 'shares':shares,'equity': equity,'cash': cash}, 'prices': get_price(symbol), 'ratios': calculate_bps_cps(shares, equity, cash)}


#mass input => output

#link = 'https://codal.ir/Reports/Decision.aspx?LetterSerial=1gr1Ya1g%2BpC0fcDqU5BnHw%3D%3D&rt=0&let=6&ct=0&ft=-1'
#link = str(input('link='))

#Main code
driver = webdriver.Chrome(executable_path = r'C:\Users\Sina\Desktop\chromedriver.exe')
input_file = open('input.txt')
output_file = open('output.txt', 'a+')

links = input_file.readlines()
renderlinks(links)

for e in links:
	data = get_data(e)
	sd = data['stock']
	pd = data['prices']
	rd = data['ratios']
	print(data)
	output = f"{sd['symbol']} | BPS: {rd['bps']} | CPS: {rd['cps']} | Price: {pd['price']} {pd['price changes']} | 52W-Low: {pd['yearly low']} | 52W-High: {pd['yearly high']}\n"
	output_file.write(output)


input_file.close()
output_file.close()
driver.close()
#get_data(link)
#add readName

