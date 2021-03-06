"""
API for Enclaves distributed exchange (enclaves.io)

example token entry:
    {'addr': '0x0F00f1696218EaeFa2D2330Df3D6D1f94813b38f',
     'amountEther': '22230538924500000',
     'amountToken': '3293413174',
     'change': '-0.13460428979858716137',
     'priceEnclaves': '0.000675',
     'volumeEnclavesEther': '17921353316879564600',
     'volumeEther': '21737691009396312760'},
"""
import time
import logging
import socket
import websocket
import json
import pprint

try:
    from urllib.request import urlopen
except:
    from urllib import urlopen

from urllib.error import URLError


def wei_to_ether(amount_in_wei):
    return int(amount_in_wei) / 1000000000000000000.0

class EnclavesAPI():
    def __init__(self, currency_symbol="0xBTC"):
        self._WEBSOCKET_URL = "ws://app.enclaves.io:80/socket.io/?EIO=3&transport=websocket";

        if currency_symbol == "0xBTC":
            self._CONTRACT_ADDRESS = '0x0F00f1696218EaeFa2D2330Df3D6D1f94813b38f'
        else:
            raise RuntimeError("Unknown currency_symbol {}".format(currency_symbol))

        self.last_updated_time = 0

        self.currency_symbol = currency_symbol
        self.api_name = "Enclaves DEX"
        self.command_names = ['enclaves', 'encalves']
        self.short_url = "https://bit.ly/2rnYA7b"

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
        #print('connecting to', self._WEBSOCKET_URL)

        ws = websocket.create_connection(self._WEBSOCKET_URL, timeout=timeout)
        #print('connected')
        # TMP forks read session id etc first so we do the same
        #print('rcv')
        result = ws.recv()
        #print('result:')
        #pprint.pprint(result)
        #print('rcv')
        result = ws.recv()
        #print('result:')
        #pprint.pprint(result)
        #request miner data
        ws.send('42["getTokens"]')
        result = ws.recv()
        #print('result:')
        #pprint.pprint(result)

        try:
            all_data = json.loads(result[2:])
        except json.decoder.JSONDecodeError:
            if "be right back" in response:
                raise TimeoutError("api is down - got 404 page")
            else:
            	raise TimeoutError("api sent bad data ({})".format(repr(response)))
         

        data_was_updated = False
        #pprint.pprint(all_data)
        tokens = all_data[1]['tokens']
        for token in tokens:
            if token['addr'] == self._CONTRACT_ADDRESS:
                self.price_eth = float(token['priceEnclaves'])
                self.volume_eth = wei_to_ether(token['volumeEther'])
                self.change_24h = float(token['change'])
                data_was_updated = True

        if not data_was_updated:
            raise RuntimeError('Response from Enclaves did not include indicated currency ({}).'.format(self.currency_symbol))


    def update(self, timeout=10.0):
        try:
            self._update(timeout=timeout)
        # todo: may not need to check for URLError when using websockets
        except (websocket._exceptions.WebSocketTimeoutException,
                websocket._exceptions.WebSocketBadStatusException,
                websocket._exceptions.WebSocketAddressException,
                socket.gaierror,
                URLError) as e:
            logging.warning('api timeout {}'.format(self.api_name))
        else:
            self.last_updated_time = time.time()

    def print_all_values(self):
        print(self.api_name, self.currency_symbol, 'price_eth    ', self.price_eth)
        print(self.api_name, self.currency_symbol, 'price_usd    ', self.price_usd)
        print(self.api_name, self.currency_symbol, 'volume_usd   ', self.volume_usd)
        print(self.api_name, self.currency_symbol, 'volume_eth   ', self.volume_eth)
        print(self.api_name, self.currency_symbol, 'change_24h   ', self.change_24h)
        print(self.api_name, self.currency_symbol, 'eth_price_usd', self.eth_price_usd)
        print(self.api_name, self.currency_symbol, 'btc_price_usd', self.btc_price_usd)



if __name__ == "__main__":
    e = EnclavesAPI('0xBTC')

    e.update()
    e.print_all_values()
