from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import pandas as pd

def handle_price(array):
    for i in range(len(array)):
        array[i] = array[i].replace("\\", "")
        array[i] = array[i].replace("₽", "")
        array[i] = ''.join(array[i].split())
    return array

def get_price_from_one_page(url):
    price = []
    page = requests.get(url)
    filteredPrice = []

    soup = BeautifulSoup(page.text, "html.parser")
    all_items = soup.findAll('div', class_='iva-item-priceStep-uq2CQ')

    for data in all_items:
        if data.find('span', class_='price-text-_YGDY text-text-LurtD text-size-s-BxGpL') is not None:
            filteredPrice.append(data.text)

    filteredPrice = handle_price(filteredPrice)

    return filteredPrice

def plotting(array):
    x = [i for i in range(len(array))]
    y = array
    plt.plot(x, y)
    plt.show()




url = "https://www.avito.ru/ekaterinburg/avtomobili/vaz_lada/2107-ASgBAgICAkTgtg3GmSjitg3Omig?cd=1&radius=200"

array = get_price_from_one_page(url)

print(plotting(array))





