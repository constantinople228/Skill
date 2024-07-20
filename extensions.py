import requests
import json
from config import  keys

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote : str, base: str, amount: str):

        if quote == base:
            raise  APIException('Вы пытфетесь перевести в тужу валюту.')

        try:
            quote_key = keys[quote]
        except KeyError:
            raise APIException(f'Нет такой валюты {quote}')

        try:
            base_key = keys[base]
        except KeyError:
            raise APIException(f'Нет такой валюты {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество валюты')

        r = requests.get((f'https://min-api.cryptocompare.com/data/price?fsym={quote_key}&tsyms={base_key}'))
        total_base = json.loads(r.content)[keys[base]]
        return total_base * amount