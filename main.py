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
import sub_main

#time.sleep(120)
# instantiating the connection and load markets
exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({"api_key": "",
                           "api_secret": "",
                           'timeout': 30000,
                           'enableRateLimit': True,
                           })
exchange.loadMarkets()
api_key = "YrDGAnac0OnT4D6SHPkRqdvxpvM73Fm4F0b2fe5eStDsZbP3b6R1q2IikPtXjmBw"
api_secret = "TZ8TBQ1FHfwMnHiCZzjFBWaoCZDKxJT4BTLcAPxjjo5Yd1BJe18SsrrrffXUY4QFbmM"
client = Client(api_key, api_secret, {"timeout": 20})
# Request current-price and current-time
# collect server time
sub_main.get_server_time()
# collect average price data
sub_main.get_avg_price("BTCUSDT")
sub_main.get_avg_price("ETHUSDT")
# sub_main.req_fresh_kline('btc')
# sub_main.req_fresh_kline('eth')
BTC_dict = exchange.fetchOHLCV('BTC/USDT', timeframe='4h')[-1]
ETH_dict = exchange.fetchOHLCV('ETH/USDT', timeframe= '4h')[-1]
# create a dict from list
BTC_dict = sub_main.decon(BTC_dict)
ETH_dict = sub_main.decon(ETH_dict)
# Run conditionals
sub_main.req_fresh_kline("btc")
sub_main.req_fresh_kline("eth")
# Run strategies
# if datetime.fromtimestamp(data_feed[0]) > time_since_la# st_kline():
