import requests
import json
from config import *


class APIException(Exception):
    pass





class CurrencyConverter:
    def __init__(self, base, quote, amount):
        self.base = base
        self.quote = quote
        self.amount = amount

    @staticmethod
    def get_price(base: str, quote:str, amount:str):
        #  проверяем можем ли мы с ними работать
        if base == quote:
            raise APIException('Невозможно перевести одинаковые валюты')


        try:
            base_ticker = available_dict[base]
        except KeyError:
            raise APIException(f'Не удалость обработать валюту {base}')
        try:
            quote_ticker = available_dict[quote]
        except KeyError:
            raise APIException(f'Не удалость обработать валюту {quote}')
        
        
        #  проверяем правильность кол-ва
        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Неверно указано кол-во')

        if amount <= 0:
            raise APIException('Неверно указано кол-во')



        # конвертация валюты
        if base == 'евро':
            r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={access_key}&symbols=USD,RUB&format=1')
            total_base = float(json.loads(r.content)['rates'][available_dict[quote]]) * float(amount)

        elif quote ==  'евро':
            r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={access_key}&symbols=USD,RUB&format=1')
            total_base = float(json.loads(r.content)['rates'][available_dict[base]])**(-1) * float(amount)

        else:
            r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={access_key}&symbols=USD,RUB&format=1')
            total_base = (float(json.loads(r.content)['rates'][available_dict[quote]]) / float(json.loads(r.content)['rates'][available_dict[base]])) * float(amount)
        

        return total_base