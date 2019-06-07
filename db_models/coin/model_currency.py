from datetime import datetime
from time import sleep
import math
from mysql.connector import Error
from mysql.connector.errors import PoolError

from db_models.db_model import DbModel

from config.project_config import src_path
from libs.utils.various_utils import generateLogger

logger = generateLogger(src_path + '/logs/app.log', __name__)


class ModelCurrency(DbModel):
    def get_exchange_currency_dict(self, exchange_id):
        id_currency_dict= {}
        currency_id_dict = {}

        try:
            cursor = self.conn.cursor(dictionary=True)
            sql = """SELECT currency_id, currency_name
                     FROM exchange_currency
                     WHERE exchange_id = {} 
            """.format(exchange_id)

            cursor.execute(sql)
            for row in cursor:
                id_currency_dict[row['currency_id']] = row['currency_name'] 

                currency_id_dict[row['currency_name']] = row['currency_id']
        except Error as e:
            logger.error(e)
            raise Error(msg=e)
        finally:
            cursor.close()

        return id_currency_dict, currency_id_dict

    def get_currency_dict(self,):
        id_currency_dict= {}
        currency_id_dict = {}

        try:
            cursor = self.conn.cursor(dictionary=True)
            sql = """SELECT id as currency_id, name as currency_name
                     FROM currency
            """.format(exchange_id)

            cursor.execute(sql)
            for row in cursor:
                id_currency_dict[row['currency_id']] = row['currency_name'] 

                currency_id_dict[row['currency_name']] = row['currency_id']
        except Error as e:
            logger.error(e)
            raise Error(msg=e)
        finally:
            cursor.close()

        return id_currency_dict, currency_id_dict

def test():
    from mysql.connector.pooling import MySQLConnectionPool
    from config.db_config import mysql_config as db_conf

    cnx_pool = MySQLConnectionPool(
        pool_name='default_cnx_pool', **db_conf)
    model = ModelCurrency(cnx_pool)

    print(model.get_currency_dict(1))


if __name__ == '__main__':
    test()
