import json
import requests
from config import keys


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f"Невозможно перевести одинаковые валюты {base}.")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {quote}.")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f"Не удалось обаботать валюту {base}")

        try:
            amount = int(amount)
        except ValueError:
            raise ConvertionException(f"Не удалось обработать количество {amount}")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = float(json.loads(r.content)[keys[base]])
        result = round(float(total_base * amount),2)
        return result
