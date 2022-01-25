# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import sys
import os
from dotenv import load_dotenv
from libs.Bitkub.App import Bitkub
from libs.Tradingview.Recommendation import Recommendation, TimeInterval
import firebase_admin
from firebase_admin import credentials, db


# initialize env
load_dotenv()
API_HOST = os.getenv('API_BITKUB_HOST')
API_KEY = os.getenv('API_BITKUB_KEY')
API_SECRET = os.getenv('API_BITKUB_SECRET')
API_CURRENCY = os.getenv('API_BITKUB_CURRENCY')
API_TIMEFRAME = os.getenv('API_BITKUB_TIMEFRAME')

bitkub = Bitkub()

# Fetch the service account key JSON file contents
cred = credentials.Certificate('keys.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('API_FIREBASE_URL')
})

def main():
    # Use a breakpoint in the code line below to debug your script.
    balance = bitkub.balance()
    # Show Assets in Account!
    print(balance[0]['message'])

    # Get Symbols from Bitkub
    symbols = bitkub.symbols()
    # print(list(symbols))

    # Get Recommendation from tradingview
    td = Recommendation()
    # Get Time Interval
    time_interval = TimeInterval().get_interval()
    docs = []
    percent_loop = 0
    i = 0
    while i < len(symbols):
        __symbol = symbols[i]
        # Start Loop with Time Interval
        percent_loop = int(((i + 1) * len(symbols)) / 100)
        print(f"\nStart Loop {__symbol}({percent_loop}%) with Time Interval")
        __interval = []
        symbol_count = 0
        x = 0
        while x < len(time_interval):
            __time_interval = time_interval[x]
            print(f"{(x + 1)}. Get Recommendation: {__symbol} with timeframe: {__time_interval}")
            data = td.summary(symbol=__symbol, time=__time_interval)
            if data['RECOMMENDATION'] == 'BUY':
                __interval.append(__time_interval)
                symbol_count += 1

            x += 1

        if symbol_count > 0:
            docs.append({'symbol': __symbol, 'total': symbol_count, 'timeframe': __interval})

        print(f"+++++++++++++++ END ++++++++++++++++++++\n")
        i += 1

    print(f'total: {percent_loop}%')
    i = 0
    while i < len(docs):
        r = docs[i]
        last = bitkub.last_price(r['symbol'])
        last_price = float(last['last'])
        last_percent = float(last['percentChange'])
        msg = f"""SYMBOL: {r['symbol']}\nPRICE: {last_price}\nACT.: BUY\nTIMEFRAME: {','.join(r['timeframe'])}\nPERCENT: {last_percent}%\nAT: {str(datetime.datetime.now())[:19]}"""
        print(msg)

        # บันทึกข้อมูลใน firebase
        if last_price < 2:
            interest_db = db.reference(
                f"crypto/interesting/{r['symbol']}/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}")
            interest_db.set({
                "percent": last_percent,
                "symbol": r["symbol"],
                "trend": "UP",
                "timeframe": r['timeframe'],
                "last_price": last_price,
                "last_update": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })

        print("\n")
        i += 1



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    sys.exit(0)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
