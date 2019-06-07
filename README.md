coin trader

## Set Temporal environments
```
$ source path/to/virtualenv
$ source ./source_it_to_set_envs.sh

```


```
from libs.coin.coinone.coinone import CoinOne
from pprint import pprint

"""
# when use private api
from config.sj import COINONE_API_KEY as API_KEY  
coinone = CoinOne(API_KEY)
"""

# when use only public api
coinone = CoinOne()

pprint(coinone.get_balance())
pprint(coinone.get_orderbook(currency='eth'))
pprint(coinone.get_recent_complete_orders(currency='eth'))

```
