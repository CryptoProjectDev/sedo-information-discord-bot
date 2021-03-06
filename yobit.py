import time
import logging
import socket
try:
    from urllib.request import urlopen, Request
except:
    from urllib import urlopen, Request

from urllib.error import URLError

import json

import pprint

from weighted_average import WeightedAverage


class YobitAPI():
    def __init__(self, currency_symbol="SEDO"):
        self._SERVER_URL = "https://yobit.io/api/3/ticker"
        self.currency_symbol = currency_symbol
        self.api_name = "Yobit"
        self.short_url = "https://bit.ly/2Kpk77B"
        self.last_updated_time = 0

        self.price_eth = None
        self.price_usd = None
        self.price_btc = None
        self.volume_usd = None
        self.volume_eth = None
        self.volume_btc = None
        self.change_24h = None
        self.eth_price_usd = None
        self.btc_price_usd = None

    def _update(self, timeout=10.0):
        method = "/sedo_btc-sedo_eth-eth_usd-btc_usd"

        req = Request(
            self._SERVER_URL+method, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )

        response = urlopen(req, timeout=timeout)
        response = response.read().decode("utf-8") 
        try:
            data = json.loads(response)
        except json.decoder.JSONDecodeError:
            raise TimeoutError("bad reply from server ({})".format(repr(response)))

        volume_usd = 0

        self.price_btc = float(data['sedo_btc']['last'])
        self.volume_btc = float(data['sedo_btc']['vol'])
        self.price_eth = float(data['sedo_eth']['last'])
        self.volume_eth = float(data['sedo_eth']['vol'])
        self.eth_price_usd = float(data['eth_usd']['last'])
        self.btc_price_usd = float(data['btc_usd']['last'])

    def update(self, timeout=10.0):
        try:
            self._update(timeout=timeout)
        except (TimeoutError,
                ConnectionResetError,
                ConnectionRefusedError,
                socket.timeout,
                socket.gaierror,
                URLError) as e:
            logging.warning('api timeout {}: {}'.format(self.api_name, str(e)))
        else:
            self.last_updated_time = time.time()
            logging.info('successfully updated Yobit')

    def print_all_values(self):
        print(self.api_name, self.currency_symbol, 'price_eth    ', repr(self.price_eth))
        print(self.api_name, self.currency_symbol, 'price_usd    ', repr(self.price_usd))
        print(self.api_name, self.currency_symbol, 'price_btc    ', repr(self.price_btc))
        print(self.api_name, self.currency_symbol, 'volume_usd   ', repr(self.volume_usd))
        print(self.api_name, self.currency_symbol, 'volume_eth   ', repr(self.volume_eth))
        print(self.api_name, self.currency_symbol, 'volume_btc   ', repr(self.volume_btc))
        print(self.api_name, self.currency_symbol, 'change_24h   ', repr(self.change_24h))
        print(self.api_name, self.currency_symbol, 'eth_price_usd', repr(self.eth_price_usd))
        print(self.api_name, self.currency_symbol, 'btc_price_usd', repr(self.btc_price_usd))

if __name__ == "__main__":

    sedo_api = YobitAPI('SEDO')
    sedo_api.update()
    sedo_api.print_all_values()
