from datetime import datetime
from time import sleep
import math
from mysql.connector import Error
from mysql.connector.errors import PoolError

from db_models.db_model import DbModel

from config.project_config import src_path
from libs.utils.various_utils import generateLogger

logger = generateLogger(src_path + '/logs/app.log', __name__)


class ModelTrCoinone(DbModel):
    def insert_tr(self, currency, tr_list):
        alarm_list = []

        try:
            cursor = self.conn.cursor()
            sql_base = """INSERT IGNORE INTO tr_coinone(currency, price, qty, date_time)
                     VALUES {}
            """
            
            sql_bulk_list = [] 
            
            for tr in tr_list:
                sql_data = "( {}, {}, {}, '{}' )".format(currency, tr['price'], tr['qty'], tr['datetime'])
                sql_bulk_list.append(sql_data)

            sql_bulk = ", ".join(sql_bulk_list)

            sql = sql_base.format(sql_bulk)

            cursor.execute(sql)
            self.conn.commit()
        except Error as e:
            self.conn.rollback()
            logger.error(e)
            raise Error(msg=e)
        finally:
            cursor.close()

        return alarm_list

    def get_tr(self, currency, rows=100, page=0):
        tr_list = []

        try:
            cursor = self.conn.cursor(dictionary=True)
            sql = """SELECT price, qty, date_time
                          FROM tr_coinone
                          WHERE currency = {}
                          ORDER BY date_time DESC
                          LIMIT {}, {}
            """.format(currency, rows*page, rows)
            cursor.execute(sql)
            tr_list = cursor.fetchall()
        except Error as e:
            logger.error(e)
            raise Error(msg=e)
        finally:
            cursor.close()

        return tr_list




def test():
    from mysql.connector.pooling import MySQLConnectionPool
    from config.db_config import mysql_config as db_conf

    cnx_pool = MySQLConnectionPool(
        pool_name='default_cnx_pool', **db_conf)
    model = ModelTrCoinone(cnx_pool)
    #model.insert_tr(1, [{'price':355, 'qty':10, 'datetime':datetime.now() },{'price':355, 'qty':12, 'datetime':datetime.now() }] )
    print(model.get_tr(1))


if __name__ == '__main__':
    test()
