import os
import pandas as pd
import json
import hmac
import hashlib
import requests
from termcolor import colored

# set plotting with plotly
pd.options.plotting.backend = "plotly"
char_length = 60

class Bitkub:
    def __init__(self):
        """
        Library for mine!
        """
        print(u"{}[2J{}[;H".format(chr(27), chr(27)))
        print(f"\n{colored(''.rjust(char_length, '*'), 'red')}")
        print(colored("\n😚 F-San Bitkub Lib v.1 🥰\nCreateBy 👻: F San\nE-Mail 💌: krumii.it@gmail.com\nGitHub: "
                           "🌤: https://github.com/abe27\nLicense: MIT", "blue"))
        print(f"\n{colored(''.rjust(char_length, '*'), 'red')}")

        # API info
        self.API_HOST = os.getenv('API_BITKUB_HOST')
        self.API_KEY = os.getenv('API_BITKUB_KEY')
        self.API_SECRET = (os.getenv('API_BITKUB_SECRET')).encode('utf8')
        self.API_CURRENCY = os.getenv('API_BITKUB_CURRENCY')
        self.API_TIMEFRAME = (os.getenv('API_BITKUB_TIMEFRAME')).split(',')
        self.API_BALANCE = os.getenv('API_BALANCE')
        self.API_LIMIT = int(os.getenv('API_LIMIT'))
        self.API_EMA_FAST = int(os.getenv('API_EMA_FAST'))
        self.API_EMA_SLOW = int(os.getenv('API_EMA_SLOW'))

        self.API_HEADER = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-APIKEY': self.API_KEY,
        }

    @staticmethod
    def __json_encode(data):
        return json.dumps(data, separators=(',', ':'), sort_keys=True)

    def sign(self, data):
        j = self.__json_encode(data)
        # print('Signing payload: ' + j)
        h = hmac.new(self.API_SECRET, msg=j.encode(), digestmod=hashlib.sha256)
        return h.hexdigest()

    # # check server time
    def timeserver(self):
        response = requests.get(self.API_HOST + '/api/servertime')
        ts = int(response.text)
        # print('Server time: ' + response.text)
        return ts

    def balance(self):
        # check timestamp on server
        data = {
            'ts': self.timeserver(),
        }
        signature = self.sign(data)
        data['sig'] = signature

        # print('Payload with signature: ' + json_encode(data))
        response = requests.post(self.API_HOST + '/api/market/balances',
                                 headers=self.API_HEADER, data=self.__json_encode(data))
        obj = json.loads(response.text)

        msg = f"ยอดเงินคงเหลือของคูณคือ: {int(obj['result'][self.API_CURRENCY]['available'])}"
        data = [{
            'available': obj['result'][self.API_CURRENCY]['available'],
            'reserved': obj['result'][self.API_CURRENCY]['reserved'],
            'symbol': self.API_CURRENCY,
            'message': msg
        }]

        if obj['error'] == 0:
            currency = obj['result']
            for i in currency:
                if currency[i]['reserved'] > 0:
                    currency[i]['symbol'] = i
                    currency[i]['message'] = ""
                    data.append(currency[i])

        return data

    def symbols(self):
        docs = []
        response = requests.get(self.API_HOST + "/api/market/symbols", headers={}, data={})
        obj = json.loads(response.text)
        if obj['error'] == 0:
            i = 0
            while i < len(obj['result']):
                symbol = str(obj['result'][i]['symbol'])
                docs.append(symbol[4:])
                i += 1

            docs.sort()
            return docs

        return obj['error']

    def last_price(self, symbol):
        try:
            sym = f'{self.API_CURRENCY}_{symbol}'
            ticker = requests.get(f'{self.API_HOST}/api/market/ticker?sym={sym}')
            ticker = ticker.json()
            price = ticker[sym]
            return price

        except Exception as e:
            print(f"Error: {e}")

        return False
