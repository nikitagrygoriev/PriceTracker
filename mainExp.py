import datetime
import requests
import os
from bs4 import BeautifulSoup

urls = ['https://www.x-kom.pl/p/541187-smartfon-telefon-samsung-galaxy-s20-g980f-dual-sim-cosmic-grey.html',
'https://www.x-kom.pl/p/543211-smartfon-telefon-motorola-moto-g8-power-4-64gb-dual-sim-smoke-black.html',
'https://www.x-kom.pl/p/475814-desktop-x-kom-g4m3r-500-i5-9400f-16gb-2401tb-w10x-gtx1660.html']
headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,  like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

titles, prices, oldPrices, newPrices = [],[],[],[]
items = {}

time = str(datetime.datetime.now())
for url in urls:
    page = requests.get(url, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    title = soup2.find(class_='sc-1x6crnh-5 dRjaeJ').get_text().strip()
    words = title.split()
    titleShort = ' '.join(words[:3])
    price = soup2.find(class_="u7xnnm-4 gHPNug").get_text().strip()
    # print(price)
    price = float(price[:-6].replace(' ','').replace(',',''))
    # print(price)
	#print(title[:title.find(',')])
	#print(float(price[1:-3].replace(',','')))
    #titleEd = title[:title.find(',')]
    titles.append(titleShort)
    prices.append(price)

items = [titles, prices]
with open('file.txt', 'r') as f:
    for line in f.readlines()[-len(urls):]:
        data = line.split('$')
        oldPrice = data[1]
        oldPrice = oldPrice[:oldPrice.index('.')]
        oldName = data[0].split()
        oldName = ' '.join(oldName[:3])
        # print('price '+str(float(oldPrice)))
        oldPrices.append(float(oldPrice))

if not oldPrices:
    for item in prices:
        oldPrices.append(0)
itemsOld = [titles, oldPrices]
# print(items)
# print(itemsOld)
newNames = []
changed = ['','','']
for title1, price1  in zip(titles,prices):
    if  price1 != itemsOld[1][itemsOld[0].index(title1)]:
        changed[itemsOld[0].index(title1)] = ' NEW PRICE'
    newNames.append(title1)
    newPrices.append(price1)

if len(newPrices) > 0 :
	with open('file.txt', 'a') as f:
            for newName, newPrice, change in zip(newNames, newPrices, changed):
                line = newName + ' had a price of $' + str(newPrice) + ' at ' + time + change +'\n'
                f.write(str(line))

	#os.system("mail -s 'Test Subject' lalkaed@gmail.com < file.txt")
