import json
import requests
from datetime import date

API_KEY = "61bfcbf31791dbc5404450267bcc23bd"
AVAILABLE_CURRENCIES = ['USD', 'EUR', 'CAD', 'JPY']
API_URL = "http://api.exchangeratesapi.io/v1"

class ExchangeRate:
    """
    A class exchange money from one currency to destination currency

    Attributes
    ----------
    base_currency : str (accept list AVAILABLE_CURRENCIES)
       base currency you want to convert
    amount : float
        amount to convert 
    

    Methods
    -------
    setup_amount_and_base_currency(): void
        set up amount and base currency
    exchange_to_destination_currency(): object
        return result as json format
    exchange_date_currency(): object
        Returns result as json format.
    
    """
    def __init__(self, base_currency='', amount=0):
        self.base_currency = base_currency
        self.amount = amount
        
    #set up amount and base currency
    def setup_amount_and_base_currency(self, base_currency='', amount=0):
        self.base_currency = base_currency
        self.amount = amount
    
    #exchange currency to destination currency
    def exchange_to_destination_currency(self, des_currency=''):
        try:
            if des_currency:
                exchange_url = f'{API_URL}/latest?access_key={API_KEY}&base={self.base_currency}&symbols={des_currency}'
                response = requests.get(exchange_url)
                if response.status_code == 200:
                    response_result = response.json()

                    return json.dumps({
                        'baseCurrency': self.base_currency,
                        'amount': self.amount,
                        'exchangeRateDate': response_result['date'],
                        'exchangeValues': {
                            des_currency: self.amount * response_result['rates'][des_currency]
                        }
                    })
                else:
                    response.raise_for_status()
            else:
                other_currencies = [currency for currency in AVAILABLE_CURRENCIES if currency != self.base_currency]
                exchange_url = f'{API_URL}/latest?access_key={API_KEY}&base={self.base_currency}&symbols={",".join(other_currencies)}'
                response = requests.get(exchange_url)
                if response.status_code == 200:
                    response_result = response.json()

                    return json.dumps({
                        'baseCurrency': self.base_currency,
                        'amount': self.amount,
                        'exchangeRateDate': response_result['date'],
                        'exchangeValues': [{
                            picked_currency: self.amount * response_result['rates'][picked_currency]
                        } for picked_currency in other_currencies]
                    })
                else:
                    response.raise_for_status()
        except requests.exceptions.HTTPError as he:
            print(he)
            raise
        except requests.exceptions.ConnectionError as ce:
            print(ce)
        except requests.exceptions.Timeout as t:
            print(t)
        except requests.exceptions.RequestException as re:
            print(re)
    
    #exchange currency with special day
    def exchange_date_currency(self, day='', des_currency=''):
        specific_day = day if day else date.today().strftime('%Y-%m-%d')
        try:
            if des_currency:
                exchange_url = f'{API_URL}/{specific_day}?access_key={API_KEY}&base={self.base_currency}&symbols={des_currency}'
                response = requests.get(exchange_url)
                if response.status_code == 200:
                    response_result = response.json()

                    return json.dumps({
                        'baseCurrency': self.base_currency,
                        'exchangeRateDate': response_result['date'],
                        'rates': {
                            des_currency: response_result['rates'][des_currency]
                        }
                    })
                else:
                    response.raise_for_status()
            else:
                other_currencies = [currency for currency in AVAILABLE_CURRENCIES if currency != self.base_currency]
                exchange_url = f'{API_URL}/{specific_day}?access_key={API_KEY}&base={self.base_currency}&symbols={",".join(other_currencies)}'
                response = requests.get(exchange_url)
                if response.status_code == 200:
                    response_result = response.json()

                    return json.dumps({
                        'baseCurrency': self.base_currency,
                        'exchangeRateDate': response_result['date'],
                        'rates': [{
                            picked_currency: response_result['rates'][picked_currency]
                        } for picked_currency in other_currencies]
                    })
                else:
                    response.raise_for_status()
        except requests.exceptions.HTTPError as he:
            print(he)
        except requests.exceptions.ConnectionError as ce:
            print(ce)
        except requests.exceptions.Timeout as t:
            print(t)
        except requests.exceptions.RequestException as re:
            print(re)

if __name__ == "__main__":
    er = ExchangeRate(base_currency='EUR', amount=2)
    print('Destination currency is USD:')
    print(er.exchange_to_destination_currency('USD'))
    print('Destination currency is empty:')
    print(er.exchange_to_destination_currency())
    print('Exchange rate at 2021-06-01 of CAD:')
    print(er.exchange_date_currency(day='2021-06-01', des_currency='CAD'))
    print('Exchange rates at 2021-01-01:')
    print(er.exchange_date_currency(day='2021-01-01'))
    
    
    