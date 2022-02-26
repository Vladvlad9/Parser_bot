import json

import requests
from bs4 import BeautifulSoup

url = 'https://www.wildberries.ru/catalog/18409417/detail.aspx?targetUrl=XS'

headers = {
    "Accept": "*/*",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

request = requests.get(url=url, headers=headers)

soup = BeautifulSoup(request.text, 'lxml')


def name_brand_product():
    name = soup.find_all(class_='same-part-kt__header-wrap hide-mobile')
    result = ''
    for item_name in name:
        name_brand = item_name.find(attrs={"data-link": "text{:product^brandName}"}).text
        article = item_name.find("span", id='productNmId').text
        result = f'Бренд:{name_brand}'

    with open('file3.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=3, ensure_ascii=False)

    return result


def img_prod():
    img = soup.find_all('img', class_='photo-zoom__preview j-zoom-preview')
    for image in img:
        src = image.get("src")
        if src:
            print(src)


def name_products():
    name = soup.find_all(class_='same-part-kt__header-wrap hide-mobile')
    for item_name in name:
        name_product = item_name.find(attrs={"data-link": "text{:product^goodsName}"}).text
        article = item_name.find("span", id='productNmId').text
        result = f'Название продукта:{name_product}'
        return result


def advantages_list():
    advantages_lis = soup.find_all(class_='same-part-kt__advantages advantages')
    advantages = ''
    for item_advantages in advantages_lis:
        delivery = item_advantages.find('li', class_='advantages__item advantages__item--delivery').text
        fitting_hide = item_advantages.find('li', class_='advantages__item advantages__item--fitting hide').text
        refund = item_advantages.find('li', class_="advantages__item advantages__item--refund").text
        rise_hide = item_advantages.find('li', class_="advantages__item advantages__item--rise hide").text
        advantages = "Преимущества: " + delivery, fitting_hide, refund, rise_hide

    with open('file3.json', 'w', encoding='utf-8') as file:
        json.dump(advantages, file, indent=3, ensure_ascii=False)

    return advantages


def price_product():
    price = soup.find_all(class_='price-block__content')
    for item in price:
        final_price = item.find('span', class_="price-block__final-price").text.split()
        old_price = item.find('del', class_="price-block__old-price j-final-saving").text.split()
        discount = item.find('span', class_="discount-tooltipster-value").text.split()
        resulr_price = f'Стоимость:{" ".join(final_price)}\nСтарая цена:{" ".join(old_price)}\nСкидка:{" ".join(discount)}'
        return resulr_price


def product_detail():
    show_product_detail = soup.find_all(class_='product-detail__details details')

    for item_product_detail in show_product_detail:
        description = item_product_detail.find('p', class_="collapsable__text").text
        return description


def prod_params():
    product_params = soup.find_all(class_='product-params')

    rows = soup.find_all('caption', class_="product-params__caption")
    ad = soup.find_all('tr', class_='product-params__row')
    res = {}

    for item_rows in ad:
        header = item_rows.find("span", class_="product-params__cell-decor").text
        header_description1 = item_rows.find('td', class_='product-params__cell').text

        res[header] = header_description1

    s = ''
    for r, t in res.items():
        s += f'{r} - {t}\n'
    return s
