import time
import base64
import hashlib
import hmac

from datetime import datetime
import simplejson as json
import requests

try:
    import api_urls as api
except:
    from . import api_urls as api


## utils
def get_encoded_payload(payload):
  payload['nonce'] = int(time.time()*1000)
  dumped_json = json.dumps(payload)
  encoded_json = base64.b64encode(bytes(dumped_json,'utf-8'))
  return encoded_json


def get_signature(encoded_payload, secret_key):
  signature = hmac.new(bytes(secret_key.upper(),"utf-8"), encoded_payload, hashlib.sha512);
  return signature.hexdigest()


## class
class Coinone(object):

    def __init__(self, api_key=None):
        self.access_token = None
        self.secret_key = None
        if api_key:
            self.access_token = api_key['ACCESS_TOKEN']
            self.secret_key = api_key['SECRET_KEY']

        currency_id_dict = {
                    
                }

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


    def get_balance(self):
        return self.get_response(api.balance, payload={})
  

    def get_orderbook(self, currency='eth'):
        return requests.get(api.orderbook, params={'currency': currency}).json()

    def get_tr(self, currency='eth', period='hour'):
        recent_complete_orders = {
                'currency': '',
                'complete_order_list' : [],
                }
        
        recent_complete_orders_raw = requests.get(api.recent_complete_orders,  
                                                    params={'currency': currency, 'period':period}).json()
 

        recent_complete_orders['currency'] = recent_complete_orders_raw['currency']
        recent_complete_orders['tr_list'] = [ {"datetime": datetime.fromtimestamp(int(row['timestamp'])), 
                                            "price" : float(row['price']), 
                                            'qty': float(row['qty'])} 
                                            for row in recent_complete_orders_raw['completeOrders'] ] 

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
