# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import sys
import os
from dotenv import load_dotenv
from libs.Bitkub.App import Bitkub
from libs.Tradingview.Recommendation import Recommendation, TimeInterval
from libs.Notifications.Line import Line
import mysql.connector


# initialize env
load_dotenv()
API_HOST = os.getenv('API_BITKUB_HOST')
API_KEY = os.getenv('API_BITKUB_KEY')
API_SECRET = os.getenv('API_BITKUB_SECRET')
API_CURRENCY = os.getenv('API_BITKUB_CURRENCY')
API_TIMEFRAME = os.getenv('API_BITKUB_TIMEFRAME')

bitkub = Bitkub()

# initialize mysql db
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='marketcap'
)

def main():
    # Use a breakpoint in the code line below to debug your script.
    listSymbol = []
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
        percent_loop = int(((i + 1) * 100) / (len(symbols)))
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

    print(f'total: {percent_loop}%\n')

    # Add mysql cursor
    cursor = db.cursor()
    i = 0
    while i < len(docs):
        r = docs[i]
        last = bitkub.last_price(r['symbol'])
        last_price = float(last['last'])
        last_percent = float(last['percentChange'])
        weeks = []
        for a in r['timeframe']:
            w = TimeInterval().get_thai_language(a)
            weeks.append(w)

        time_frame = str(','.join(weeks))

        if last_percent < 2:
            # msg = f"SYMBOL: {r['symbol']}\nPRICE: {last_price}\nTREND: BUY\nTIMEFRAME: {time_frame}\nPERCENT: {last_percent}%\nAT: {str(datetime.datetime.now())[:19]}"
            msg = f"\nเหรียญ: {r['symbol']}\nราคาปัจจุบัน: {last_price:,}บาท\nเปอร์เซ็นต์: {last_percent}\nช่วงเวลา: {time_frame}\nสถานะ: BUY\n"
            # บันทึกข้อมูลใน mysql
            sql = f"INSERT INTO tbt_interesting(id, symbol, trend, timeframe, last_price, percent, is_check, last_update)VALUES(uuid(), '{r['symbol']}', 'BUY', '{time_frame}', {last_price}, {last_percent}, 0, CURRENT_TIMESTAMP);"
            cursor.execute(sql)
            print(cursor.rowcount, "record inserted.")
            # Line().notifications(msg)
            print(msg)
            # Append Symbol To ListSymbol
            listSymbol.append(r["symbol"])

        i += 1

    print(f"END LOAD: ({percent_loop})%\n")
    # Commit data
    db.commit()
    return listSymbol

def subscribe(symbols):
    interest_db = db.reference(f"crypto/interesting/")
    snapshot = interest_db.child(symbols[0])
    print(snapshot.order_by_key().get())



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # After run main process
    list_symbol = main()
    subscribe(list_symbol)
    sys.exit(0)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
