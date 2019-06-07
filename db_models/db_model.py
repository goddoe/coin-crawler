from time import sleep
from mysql.connector import Error
from mysql.connector.errors import PoolError


class DbModel(object):
    def __init__(self, cnx_pool):
        while True:
            try:
                self.conn = cnx_pool.get_connection()
                break
            except PoolError as e:
                sleep(1)


    def __del__(self):
        if hasattr(self.conn, 'is_connected'):
            if self.conn.is_connected():
                self.conn.close()


def test():
    from mysql.connector.pooling import MySQLConnectionPool
    from config.db_config import mysql_config as db_conf

    cnx_pool = MySQLConnectionPool(
        pool_name='default_cnx_pool', **db_conf)
    model = DbModel(cnx_pool)

if __name__ == '__main__':
    test()
