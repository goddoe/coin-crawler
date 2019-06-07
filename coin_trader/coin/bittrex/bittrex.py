import time
import hmac
from datetime import datetime

import dateparser
from bittrex.bittrex import *

from datetime import datetime
import simplejson as json
import requests

## class
class BittrexWrapper(object):

    def __init__(self, api_key=None, api_version=API_V1_1):
        self.access_token = None
        self.secret_key = None
        if api_key:
            self.access_token = api_key['ACCESS_TOKEN']
            self.secret_key = api_key['SECRET_KEY']

        self.bittrex = Bittrex(self.access_token,
                               self.secret_key,
                               api_version=api_version)

    def get_response(self, url, payload):
        if self.access_token is None  or self.secret_key is None:
            return {"message":"there is no access_token or secret_key"}
    
        payload['access_token'] = self.access_token

        encoded_payload = get_encoded_payload(payload)
        headers = {
          'Content-type': 'application/json',
          'X-COINONE-PAYLOAD': encoded_payload,
          'X-COINONE-SIGNATURE': get_signature(encoded_payload, self.secret_key)
        }

        return requests.post(url, headers=headers, params=encoded_payload).json()

    def get_balance(self, currency):
        resp = self.bittrex.get_balance(currency)
        # TODO: Make convert
  
    def get_orderbook(self, currency='eth'):
        def get_orderbook_template():
            return {
                        'currency':'',
                        'bid':[], # {"price": "414000","qty": "11.4946"}
                        'ask':[], # {"price": "414000","qty": "11.4946"} 
                    } 
        def get_quote(price, qty):
            return {'price':price, 'qty':qty}
        orderbook = get_orderbook_template()

        orderbook_raw = self.bittrex.get_orderbook(market, depth_type=BOTH_ORDERBOOK)
        orderbook['currency'] = currency

        for ob in orderbook_raw['result']:
            orderbook['bid' if ob['OrderType'] == 'BUY' else 'ask' ].append(
                get_quote(price=ob['Price'],
                          qty=ob['Quantity']))
      
        return orderbook

    def get_tr(self, currency='BTC-ETH'):
        recent_complete_orders = {
                'currency': '',
                'complete_order_list' : [],
                }

        recent_complete_orders_raw = self.bittrex.get_market_history(currency)
        recent_complete_orders['currency'] = currency
        recent_complete_orders['tr_list'] = [ {"datetime": datetime.datetime(dateparser(row['TimeStamp'])), 
                                            "price" : float(row['Price']), 
                                            'qty': float(row['Quantity'])} 
                                            for row in recent_complete_orders_raw['result'] ] 

        return recent_complete_orders

def test():
    from pprint import pprint
    from config.sj import COINONE_API_KEY as API_KEY 

    from db_models.coin.model_tr_coinone import ModelTrCoinone
    from mysql.connector.pooling import MySQLConnectionPool
    from config.db_config import mysql_config as db_conf

    cnx_pool = MySQLConnectionPool(
        pool_name='default_cnx_pool', **db_conf)
    model = ModelTrCoinone(cnx_pool)
    coinone = Coinone(API_KEY)
    #coinone = Coinone()
    #pprint(coinone.get_balance())
    #pprint(coinone.get_orderbook(currency='eth'))
    model.insert_tr(1,coinone.get_tr(currency='eth')["tr_list"])
    

if __name__=='__main__':
    test() 
