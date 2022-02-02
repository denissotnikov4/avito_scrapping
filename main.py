from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import pandas as pd


url = "https://www.avito.ru/ekaterinburg/avtomobili/vaz_lada/2107-ASgBAgICAkTgtg3GmSjitg3Omig?cd=1&p=1&radius=200"

page = requests.get(url)

filteredPrice = []

soup = BeautifulSoup(page.text, "html.parser")
all_items = soup.findAll('div', class_='iva-item-priceStep-uq2CQ')


for data in all_items:
    if data.find('span', class_='price-text-_YGDY text-text-LurtD text-size-s-BxGpL') is not None:
        filteredPrice.append(data.text)

# Нужно сделать как функцию
for i in range(len(filteredPrice)):
    filteredPrice[i] = filteredPrice[i].replace("\\", "")
    filteredPrice[i] = filteredPrice[i].replace("₽", "")
    filteredPrice[i] = ''.join(filteredPrice[i].split())
print(filteredPrice)
print(len(filteredPrice))

x = [i for i in range(len(filteredPrice))]
y = filteredPrice
plt.plot(x, y)
plt.show()






