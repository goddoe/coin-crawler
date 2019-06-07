from datetime import datetime
from time import sleep
import math
from mysql.connector import Error
from mysql.connector.errors import PoolError

from db_models.db_model import DbModel

from config.project_config import src_path
from libs.utils.various_utils import generateLogger

logger = generateLogger(src_path + '/logs/app.log', __name__)


class ModelExchange(DbModel):
    def get_exchange_dict(self):
        id_exchange_dict= {}
        exchange_id_dict = {}

        try:
            cursor = self.conn.cursor(dictionary=True)
            sql = """SELECT id as exchange_id, name as exchange_name
                     FROM exchange
            """

            cursor.execute(sql)
            for row in cursor:
                id_exchange_dict[row['exchange_id']] = row['exchange_name'] 
                exchange_id_dict[row['exchange_name']] = row['exchange_id']
        except Error as e:
            logger.error(e)
            raise Error(msg=e)
        finally:
            cursor.close()

        return id_exchange_dict, exchange_id_dict

def test():
    from mysql.connector.pooling import MySQLConnectionPool
    from config.db_config import mysql_config as db_conf

    cnx_pool = MySQLConnectionPool(
        pool_name='default_cnx_pool', **db_conf)
    model = ModelExchange(cnx_pool)

    print(model.get_exchange_dict())


if __name__ == '__main__':
    test()
