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

def remove_statistical_outliers(array):
    array = pd.Series(array)
    lower_bound = array.quantile(0.05)
    upper_bound = array.quantile(0.95)
    array = array[(array > lower_bound) & (array < upper_bound)]
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

    return remove_statistical_outliers(map(int, filteredPrice))

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
    return remove_statistical_outliers(map(int, price))

def get_links_from_multiple_pages(url):
    page = requests.get(url)
    links_text = []
    req = requests.get(url + '&p=' + str(page))
    soup = BeautifulSoup(req.text, 'html.parser')

    for a in soup.find_all('a', class_='link-link-MbQDP link-design-default-_nSbv title-root-zZCwT '
                                       'iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH'):
        links_text.append(a['href'])

    for i in range(len(links_text)):
        links_text[i] = 'https://www.avito.ru' + links_text[i]
    return links_text

def plotting(array):
    fig, ax = plt.subplots()
    ax.hist(array, bins=20, linewidth=0.5, edgecolor="white")
    ax.set_xlabel('Цена')
    ax.set_ylabel('Количество')
    plt.show()

def get_statistic_information(array):
    array = pd.Series(array)
    return array.describe()

def get_below_market_price(url, count_of_pages, percentile):
    array = get_price_from_multiple_pages(url, count_of_pages)
    df = pd.Series(array)
    fixed_price_value = df.quantile(percentile)
    below_market_price = []
    for elem in array:
        if elem < fixed_price_value:
            below_market_price.append(elem)
    return below_market_price



url = "https://www.avito.ru/ekaterinburg/avtomobili/vaz_lada/2107-ASgBAgICAkTgtg3GmSjitg3Omig?cd=1&radius=200"

array = get_price_from_multiple_pages(url, 1)

print(get_statistic_information(array))

print(plotting(array))

print(get_below_market_price(url, 3, 0.4))

print(get_links_from_multiple_pages(url, 3))

print(get_links_from_multiple_pages(url))
