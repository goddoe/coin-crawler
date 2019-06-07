from bittrex.bittrex import *

b = Bittrex(None, None, api_version=API_V2_0)

b.get_balance('ETH')
{'success': True, 
 'message': '',
 'result': {'Currency': 'ETH', 'Balance': 0.0, 'Available': 0.0, 
            'Pending': 0.0, 'CryptoAddress': None}
}

b1 = Bittrex(None, None, api_version=API_V1_1)

b1.get_market_history("BTC-ETH")
