import ccxt
import h5py
import asyncio
import arrow
import time
from dateutil import tz
import numpy as np
from datetime import datetime, timedelta
from binance.client import Client
import memoryCell


# Timesleep 120 seconds
# time.sleep(120)
# instantiating the connection and load markets
exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({"api_key": "YrDGAnac0OnT4D6SHPkRqdvxpvM73Fm4F0b2fe5eStDsZbP3b6R1q2IikPtXjmBw",
                           "api_secret": "TZ8TBQ1FHfwMnHiCZzjFBWaoCZDKxJT4BTLcAPxjjo5Yd1BJe18SsrrrffXUY4QFbmM",
                           'timeout': 30000,
                           'enableRateLimit': True,
                           })
exchange.loadMarkets()
api_key = "YrDGAnac0OnT4D6SHPkRqdvxpvM73Fm4F0b2fe5eStDsZbP3b6R1q2IikPtXjmBw"
api_secret = "TZ8TBQ1FHfwMnHiCZzjFBWaoCZDKxJT4BTLcAPxjjo5Yd1BJe18SsrrrffXUY4QFbmM"
client = Client(api_key, api_secret, {"timeout": 20})
# collect server time
def get_server_time():
    # this function requests server time using the client module and returns a datetime object
    server_time = client.get_server_time()
    server_time = server_time["serverTime"]
    server_time = server_time // 1000
    server_time = datetime.fromtimestamp(server_time)
    return server_time
# collect average price data
def get_avg_price(ticker):
    # x is the ticker symbol you are trying to get
    avg_price = client.get_avg_price(symbol= ticker )
    avg_price = avg_price["price"]
    return avg_price
def get_kline_data(ticker):
    if ticker.upper() == "BTC":
        ticker = "BTC/USDT"
    elif ticker.upper() == "ETH":
        ticker = "ETH/USDT"
    else:
        print("ticker not supported")
    four_hour_kline = exchange.fetchOHLCV(ticker, timeframe='4h')
    kline_data = four_hour_kline[-1]
    return kline_data
def decon(list):
    d = {"Time": list[0], "Open": list[1], "High": list[2], "Low": list[3], "Close": list[4],
         "Volume": list[5]}
    return d
def time_since_last_kline(tick):
    tick = tick.upper()
    if tick == "BTC":
        coll = memoryCell.btc_coll
    elif tick == "ETH":
        coll = memoryCell.eth_coll
    else:
        print("ticker not supported ")
    time_since_last_kline = memoryCell.get_last_updated_doc(coll)
    time_since_last_kline = time_since_last_kline[0]["Time"]//1000
    time_since_last_kline = datetime.utcfromtimestamp(time_since_last_kline)
    return time_since_last_kline
def req_fresh_kline(tick):
    # tick = BTC/ETH
    tick = tick.upper()
    if tick == "BTC":
        coll = memoryCell.btc_coll
    elif tick == "ETH":
        coll = memoryCell.eth_coll
    else:
        print("ticker not supported ")
    if get_server_time() >= time_since_last_kline(tick) + timedelta(hours= 4):
        four_hour_kline = exchange.fetchOHLCV(f"{tick}/USDT", timeframe='4h')  # , limit = undefined, params = {})
        data_feed = (four_hour_kline[-1])
        memory_dict = {"Time": data_feed[0], "Open": data_feed[1], "High": data_feed[2],
                       "Low": data_feed[3], "Close": data_feed[4]}
        time_data = data_feed[0]//1000
        if datetime.utcfromtimestamp(time_data) != time_since_last_kline(tick):
            memoryCell.memory_update(memory_dict, coll )
        else:
            print("update unavailable")
    else:
        print("not yet $")
#btc_memory_dict = {"Time" : btc_data_feed[0], "Open" : btc_data_feed[1], "High" : btc_data_feed[2], "Low" : btc_data_feed[3], "Close" : btc_data_feed[4]}

#time_since_last_candle = btc_data_feed[0]
#current_data_feed = [btc_data_feed, eth_data_feed]
# def time_since_last_kline(ticker):
#     four_hour_kline = exchange.fetchOHLCV(ticker, timeframe='4h')  # , limit = undefined, params = {})
#     time_since_last_kline = (four_hour_kline[-1][0])//1000
#     time_since_last_kline = datetime.utcfromtimestamp(time_since_last_kline)


# time_since_last_candle = time_since_last_candle // 1000
# time_since_last_candle = datetime.fromtimestamp(time_since_last_candle)
# print(time_since_last_candle)
# def conditionals_001 (x, y):
#     # x is the current time, y is the time since last candle stick
#     x = server_time
#     y = time_since_last_candle
#     if time_since_last_candle + timedelta(hours= 4) >= server-time:
#         # update new row in dataset
#         "stream"
#print(btc_memory_dict)
#print(eth_memory_dict)
