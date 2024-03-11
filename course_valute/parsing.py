import datetime
from django.shortcuts import get_object_or_404

import requests
from bs4 import BeautifulSoup

from .models import Valute


def parsing_course(time):
    print(f'start parsing')
    date_start_parsing = datetime.date.today()
    valute = Valute.objects.all().last()
    date_create_or_update_valute = valute.date_update
    print(f'Прошло: {date_start_parsing.day - date_create_or_update_valute.day} дней с последнего парсера')
    if date_start_parsing.day - date_create_or_update_valute.day >= time:
        url = 'https://finance.rambler.ru/currencies/?ysclid=ltlk6xol22210655915'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('a', class_="finance-currency-table__tr")

        for a in articles:
            code = str(a.find('div', class_="finance-currency-table__cell finance-currency-table__cell--code").text).replace('\n', '')
            nominale = a.find('div', class_="finance-currency-table__cell finance-currency-table__cell--denomination").text
            country_name = (str(a.find('div', class_="finance-currency-table__cell finance-currency-table__cell--currency").text).replace('\n', '')
                            .replace('их', 'ий')
                            .replace('ов', ''))
            course = str(a.find('div', class_="finance-currency-table__cell finance-currency-table__cell--value").text).replace('\n', '')
            course = round(float(course[:course.find('.')+3]) / int(nominale), 2)
            Valute.objects.update_or_create(country=country_name, country_code=code, value=course, date_update=datetime.date.today())
        print('update courses')

    print('stop parsing')


