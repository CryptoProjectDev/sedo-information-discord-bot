""" Manage multiple apis at once - allows calculating better values by
incorporating multiple sources. """

import time
import logging
from weighted_average import WeightedAverage

# data older than this is completely ignored
_OLDEST_ALLOWED_DATA_SECONDS = 600

class MultiApiManager():
    def __init__(self, api_obj_list):
        self.api_obj_list = api_obj_list
    
    def update(self):
        for api_obj in self.api_obj_list:
            try:
                api_obj.update()
                #logging.debug('updated {} successfully'.format(api_obj.api_name))
            except:
                logging.exception('Unhandled Exception updating {}'.format(api_obj.api_name))

    @property
    def alive_apis(self):
        time_now = time.time()
        for a in self.api_obj_list:
            # skip apis that have never been updated
            if a.last_updated_time == None or a.last_updated_time == 0:
                continue
            # skip apis that have too old/stale data
            if time_now - a.last_updated_time > _OLDEST_ALLOWED_DATA_SECONDS:
                continue
            yield a

    @property
    def alive_api_names(self):
        all_names = []
        for a in self.alive_apis:
            all_names.append(a.api_name)

        # convert to set to remove duplicates 
        return list(set(all_names))

    def short_url(self, api_name='aggregate'):
        default_url = "https://bit.ly/2Kpk77B"
        if api_name == "aggregate":
            return default_url

        for a in self.api_obj_list:
            if a.api_name == api_name:
                return a.short_url
        return default_url

    def price_eth(self, currency_symbol='SEDO', api_name='aggregate'):
        result = WeightedAverage()
        for a in self.alive_apis:
            if a.currency_symbol != currency_symbol:
                continue
            if a.price_eth == None:
                continue
            if a.volume_eth == None:
                continue
            if api_name == 'aggregate' or a.api_name == api_name:
                result.add(a.price_eth, a.volume_eth)
        return result.average()

    def price_usd(self, currency_symbol='SEDO', api_name='aggregate'):
        result = WeightedAverage()
        for a in self.alive_apis:
            if a.currency_symbol != currency_symbol:
                continue
            if a.price_usd == None:
                continue
            if a.volume_eth == None:
                continue
            if api_name == 'aggregate' or a.api_name == api_name:
                result.add(a.price_usd, a.volume_eth)
        return result.average()

    def volume_usd(self, currency_symbol='SEDO', api_name='aggregate'):
        result = 0
        for a in self.alive_apis:
            if a.currency_symbol != currency_symbol:
                continue
            if a.volume_usd == None:
                continue
            if api_name == 'aggregate' or a.api_name == api_name:
                result += a.volume_usd
        return result

    def volume_eth(self, currency_symbol='SEDO', api_name='aggregate'):
        result = 0
        for a in self.alive_apis:
            if a.currency_symbol != currency_symbol:
                continue
            if a.volume_eth == None:
                continue
            if api_name == 'aggregate' or a.api_name == api_name:
                result += a.volume_eth
        return result

    def volume_btc(self, currency_symbol='SEDO', api_name='aggregate'):
        result = 0
        for a in self.alive_apis:
            if a.currency_symbol != currency_symbol:
                continue
            if a.volume_btc == None:
                continue
            if api_name == 'aggregate' or a.api_name == api_name:
                result += a.volume_btc
        return result

    def change_24h(self, currency_symbol='SEDO', api_name='aggregate'):
        result = WeightedAverage()
        for a in self.alive_apis:
            if a.currency_symbol != currency_symbol:
                continue
            if a.change_24h == None:
                continue
            if api_name == 'aggregate' or a.api_name == api_name:
                result.add(a.change_24h, a.volume_eth)
        return result.average()

    def rank(self, currency_symbol='SEDO', api_name='aggregate'):
        result = None
        for a in self.alive_apis:
            if a.currency_symbol != currency_symbol:
                continue
            if api_name == 'aggregate' or a.api_name == api_name:
                try:
                    result = a.rank
                except AttributeError:
                    pass
        return result

    def eth_price_usd(self, api_name='aggregate'):
        result = WeightedAverage()
        for a in self.alive_apis:
            if a.eth_price_usd == None:
                continue
            if api_name == 'aggregate' or a.api_name == api_name:
                if a.currency_symbol == 'ETH':
                    result.add(a.price_usd, a.volume_usd / a.price_usd)
                else:
                    result.add(a.eth_price_usd, a.volume_eth)
        return result.average()

    def btc_price_usd(self, api_name='aggregate'):
        result = WeightedAverage()
        for a in self.alive_apis:
            if a.btc_price_usd == None:
                continue
            if api_name == 'aggregate' or a.api_name == api_name:
                if a.currency_symbol == 'BTC':
                    result.add(a.price_usd, a.volume_usd / a.price_usd)
                else:
                    result.add(a.btc_price_usd, a.volume_btc)
        return result.average()

    def last_updated_time(self, api_name='aggregate'):
        result = 0
        for a in self.alive_apis:
            if api_name == 'aggregate' or a.api_name == api_name:
                # use the lowest last_updated time
                #if result == 0 or a.last_updated_time < result:
                # use the highest last_updated time as a hack for how
                if result == 0 or a.last_updated_time > result:
                    result = a.last_updated_time
        return result

if __name__ == "__main__":
    from coinmarketcap import CoinMarketCapAPI
    from enclavesdex import EnclavesAPI
    from livecoinwatch import LiveCoinWatchAPI
    from forkdelta import ForkDeltaAPI
    from mercatox import MercatoxAPI

    apis = [
        EnclavesAPI('SEDO'), 
        ForkDeltaAPI('SEDO'),
        MercatoxAPI('SEDO'),
        CoinMarketCapAPI('SEDO'),
        CoinMarketCapAPI('ETH')
    ]

    m = MultiApiManager(apis)
    m.update()

    print("m.price_eth", m.price_eth())
    print("m.price_usd", m.price_usd())
    print("m.volume_usd", m.volume_usd())
    print("m.volume_eth", m.volume_eth())
    print("m.volume_btc", m.volume_btc())
    print("m.change_24h", m.change_24h())

    print("m.eth_price_usd()", m.eth_price_usd())
    print("m.btc_price_usd()", m.btc_price_usd())

    print("m.price_eth('SEDO')", m.price_eth('SEDO'))
    print("m.price_usd('SEDO')", m.price_usd('SEDO'))
    print("m.volume_usd('SEDO')", m.volume_usd('SEDO'))
    print("m.volume_eth('SEDO')", m.volume_eth('SEDO'))
    print("m.volume_btc('SEDO')", m.volume_btc('SEDO'))
    print("m.change_24h('SEDO')", m.change_24h('SEDO'))

    print("m.change_24h('SEDO', api_name='Mercatox')",      m.change_24h('SEDO', api_name='Mercatox'))

