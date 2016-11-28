import pymysql
from features import BASE_DIR
import yaml

class DB(object):
    def __init__(self):
        print('Creating MySQL connection \n')
        settings = yaml.load(open(BASE_DIR + '/features/config.yaml').read())
        self._connection = pymysql.connect(host=settings['db_host'],
                                           port=int(settings['db_port']),
                                           user=settings['db_user'],
                                           password=settings['db_password'],
                                           db=settings['db_name'],
                                           charset=settings['db_charset'],
                                           cursorclass=pymysql.cursors.DictCursor)

    def select(self, sql):
        print('Executing sql = %s \n' % sql)
        db = self._connection.cursor()
        db.execute(sql)
        result = []
        row = db.fetchone()
        result.append(row)
        while row is not None:
            row = db.fetchone()
            if row is not None:
                result.append(row)
        return result

    def update(self, sql):
        print('Executing sql = %s \n' % sql)
        db = self._connection.cursor()
        db.execute(sql)
        self._connection.commit()

    def __del__(self):
        self._connection.close()
        print('MySQL connection is closed! \n')

