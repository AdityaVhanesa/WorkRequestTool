import pymysql.cursors


# noinspection PyBroadException
class SQL:
    def __init__(self, db):
        self.db = db
        self.connection = None
        self.cursor = None
        self.__user = 'root'
        self.__password = 'Friday@4241'
        self.__host = 'localhost'

    def __openConnection(self):
        self.connection = pymysql.connect(host=self.__host,
                                          user=self.__user,
                                          password=self.__password,
                                          db=self.db,
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor,
                                          autocommit=True)
        self.cursor = self.connection.cursor()

    def __closeConnection(self):
        if self.connection and self.cursor:
            self.cursor.close()
            self.connection.close()
            self.cursor = None
            self.connection = None

    def query(self, query, data=None):
        self.__openConnection()
        try:
            query = self.cursor.mogrify(query, data)
            self.cursor.execute(query, data)
            if query.lower().__contains__("insert"):
                self.connection.commit()
            elif query.lower().__contains__("select"):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
        except Exception as E:
            print(E)
            return False
        finally:
            self.__closeConnection()





