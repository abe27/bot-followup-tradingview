from tradingview_ta import TA_Handler

class TimeInterval:
    def __init__(self):
        self.INTERVAL_1_MINUTE = "1m"
        self.INTERVAL_5_MINUTES = "5m"
        self.INTERVAL_15_MINUTES = "15m"
        self.INTERVAL_30_MINUTES = "30m"
        self.INTERVAL_1_HOUR = "1h"
        self.INTERVAL_2_HOURS = "2h"
        self.INTERVAL_4_HOURS = "4h"
        self.INTERVAL_1_DAY = "1d"
        self.INTERVAL_1_WEEK = "1W"
        self.INTERVAL_1_MONTH = "1M"

    def get_interval(self):
        list_of_intervals = [
            # self.INTERVAL_30_MINUTES,
            # self.INTERVAL_1_HOUR,
            self.INTERVAL_2_HOURS,
            self.INTERVAL_4_HOURS,
            self.INTERVAL_1_DAY,
            self.INTERVAL_1_WEEK,
            self.INTERVAL_1_MONTH,
        ]

        return list_of_intervals

    def get_thai_language(self, time_interval):
        if time_interval == self.INTERVAL_1_MINUTE:
            return '1นาที'

        elif time_interval == self.INTERVAL_5_MINUTES:
            return '5นาที'

        elif time_interval == self.INTERVAL_15_MINUTES:
            return '15นาที'

        elif time_interval == self.INTERVAL_30_MINUTES:
            return '30นาที'

        elif time_interval == self.INTERVAL_1_HOUR:
            return '1ชั่วโมง'

        elif time_interval == self.INTERVAL_2_HOURS:
            return '2ชั่วโมง'

        elif time_interval == self.INTERVAL_4_HOURS:
            return '4ชั่วโมง'

        elif time_interval == self.INTERVAL_1_DAY:
            return '1วัน'

        elif time_interval == self.INTERVAL_1_WEEK:
            return '1สัปดาห์'

        elif time_interval == self.INTERVAL_1_MONTH:
            return '1เดือน'



class Recommendation:
    def __init__(self):
        print(f"*******************************")
        print(f"🤫 starting get recommendation.")
        print(f"*******************************")
        self.__VERSION__ = '0.1b'
        self.__DATA__INIT__ = {
            'SYMBOL': "",
            'CURRENCY': "",
            'EXCHANGE': "",
            'RECOMMENDATION': "",
            'BUY': 0,
            'SELL': 0,
            'NEUTRAL': "",
            'TIMEFRAME': "",
            'VERSION': self.__VERSION__
        }

    def summary(self, exchange='Bitkub', symbol='BTC', currency='THB', time=TimeInterval().INTERVAL_1_DAY):
        try:
            obj = TA_Handler(
                symbol=f'{symbol}{currency}',
                screener='crypto',
                exchange=exchange,
                interval=time
            )
            data = obj.get_analysis().summary
            if len(data) <= 0:
                return self.__DATA__INIT__

            obj = {
                'SYMBOL': symbol,
                'CURRENCY': currency,
                'EXCHANGE': exchange,
                'RECOMMENDATION': data['RECOMMENDATION'],
                'BUY': data['BUY'],
                'SELL': data['SELL'],
                'NEUTRAL': data['NEUTRAL'],
                'TIMEFRAME': time,
                'VERSION': self.__VERSION__
            }

            # print(obj)
            return obj

        except Exception as e:
            self.__DATA__INIT__['error'] = e
            return self.__DATA__INIT__

    def oscillators(self, exchange='Bitkub', symbol='BTC', currency='THB', time=TimeInterval().INTERVAL_1_DAY):
        try:
            obj = TA_Handler(
                symbol=f'{symbol}{currency}',
                screener='crypto',
                exchange=exchange,
                interval=time
            )
            data = obj.get_analysis().oscillators
            if len(data) <= 0:
                return self.__DATA__INIT__

            self.__DATA__INIT__['SYMBOL'] = symbol
            self.__DATA__INIT__['CURRENCY'] = currency
            self.__DATA__INIT__['EXCHANGE'] = exchange
            self.__DATA__INIT__['TIMEFRAME'] = time
            self.__DATA__INIT__['COMPUTE'] = data['COMPUTE']
            self.__DATA__INIT__['VERSION'] = self.__VERSION__
            print(data)
            return data

        except Exception as e:
            self.__DATA__INIT__['error'] = e
            return self.__DATA__INIT__

    def moving_averages(self, exchange='Bitkub', symbol='BTC', currency='THB', time=TimeInterval().INTERVAL_1_DAY):
        try:
            obj = TA_Handler(
                symbol=f'{symbol}{currency}',
                screener='crypto',
                exchange=exchange,
                interval=time
            )
            data = obj.get_analysis().moving_averages
            if len(data) <= 0:
                return self.__DATA__INIT__

            self.__DATA__INIT__['SYMBOL'] = symbol
            self.__DATA__INIT__['CURRENCY'] = currency
            self.__DATA__INIT__['EXCHANGE'] = exchange
            self.__DATA__INIT__['TIMEFRAME'] = time
            self.__DATA__INIT__['COMPUTE'] = data['COMPUTE']
            self.__DATA__INIT__['VERSION'] = self.__VERSION__
            print(self.__DATA__INIT__)
            return data

        except Exception as e:
            self.__DATA__INIT__['error'] = e
            return self.__DATA__INIT__

    def indicators(self, exchange='Bitkub', symbol='BTC', currency='THB', time=TimeInterval().INTERVAL_1_DAY):
        try:
            obj = TA_Handler(
                symbol=f'{symbol}{currency}',
                screener='crypto',
                exchange=exchange,
                interval=time
            )
            data = obj.get_analysis().indicators["RSI"]
            if len(data) <= 0:
                return self.__DATA__INIT__

            self.__DATA__INIT__['SYMBOL'] = symbol
            self.__DATA__INIT__['CURRENCY'] = currency
            self.__DATA__INIT__['EXCHANGE'] = exchange
            self.__DATA__INIT__['TIMEFRAME'] = time
            self.__DATA__INIT__['COMPUTE'] = data['COMPUTE']
            self.__DATA__INIT__['VERSION'] = self.__VERSION__
            print(self.__DATA__INIT__)
            return data

        except Exception as e:
            self.__DATA__INIT__['error'] = e
            return self.__DATA__INIT__