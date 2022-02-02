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
    page = requests.get(url)
    filteredPrice = []

    soup = BeautifulSoup(page.text, "html.parser")
    all_items = soup.findAll('div', class_='iva-item-priceStep-uq2CQ')

    for data in all_items:
        if data.find('span', class_='price-text-_YGDY text-text-LurtD text-size-s-BxGpL') is not None:
            filteredPrice.append(data.text)

    filteredPrice = handle_price(filteredPrice)

    return map(int, filteredPrice)

# 1 .. count_of_pages
def get_price_from_multiple_pages(url_general, count_of_pages):
    price = []
    for page in range(1, count_of_pages + 1):
        price_text = []
        req = requests.get(url + '&p=' + str(page))
        soup = BeautifulSoup(req.text, 'html.parser')
        all_items = soup.findAll('div', class_='iva-item-priceStep-uq2CQ')

        for data in all_items:
            if data.find('span', class_='price-text-_YGDY text-text-LurtD text-size-s-BxGpL') is not None:
                price_text.append(data.text)

        price_text = handle_price(price_text)

        price = price + price_text
    return map(int, price)

def plotting(array):
    fig, ax = plt.subplots()
    ax.hist(array, bins=20, linewidth=0.5, edgecolor="white")
    ax.set_xlabel('Цена')
    ax.set_ylabel('Количество')
    plt.show()

def get_statistic_information(array):
    array = pd.Series(array)
    return array.describe()


url = "https://www.avito.ru/ekaterinburg/avtomobili/vaz_lada/2107-ASgBAgICAkTgtg3GmSjitg3Omig?cd=1&radius=200"

array = sorted(get_price_from_multiple_pages(url, 4))
print(get_statistic_information(array))

print(plotting(array))
