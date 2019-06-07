import os
import time
from pprint import pprint
from config.sj import COINONE_API_KEY as API_KEY

from coin_trader.coin.coinone.coinone import Coinone

from db_models.coin.model_tr_coinone import ModelTrCoinone
from db_models.coin.model_currency import ModelCurrency
from db_models.coin.model_exchange import ModelExchange
from mysql.connector.pooling import MySQLConnectionPool
from config.db_config import mysql_config as db_conf


class ExchangeDataCrawler(object):

    def __init__(self, cnx_pool):
        self.model_tr = ModelTrCoinone(cnx_pool)
        self.model_currency = ModelCurrency(cnx_pool)
        self.coinone = Coinone()

        self.id_currency_dict, self.currency_id_dict = self.model_currency.get_exchange_currency_dict(
            exchange_id=1)

    def run(self):
        while True:
            view = {}
            for currency_id, currency_name in self.id_currency_dict.items():
                tr_list = self.coinone.get_tr(currency=currency_name)["tr_list"]
                self.model_tr.insert_tr(currency_id, tr_list)
                view[currency_name] = tr_list[-1]['price']
            
            time.sleep(5)
            os.system('clear')
            print(view)


def run():
    cnx_pool = MySQLConnectionPool(
        pool_name='default_cnx_pool', **db_conf)

    exchange_data_crawler = ExchangeDataCrawler(cnx_pool)
    exchange_data_crawler.run()


if __name__ == '__main__':
    run()
