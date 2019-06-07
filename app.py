from libs.coin.coinone.coinone import CoinOne
from pprint import pprint

coinone = CoinOne()
pprint(coinone.get_balance())
pprint(coinone.get_orderbook(currency='eth'))
pprint(coinone.get_recent_complete_orders(currency='eth'))



