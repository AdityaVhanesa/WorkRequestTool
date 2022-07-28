from WRT.config.connection import SQL
from WRT.config.queryConstrctor import query as queryConstructor


class Model:
    dataBase = "WRT"
    tableName = None
    query = queryConstructor()

    def __init__(self, data):
        self.data = data

    @classmethod
    def _executeQuery(cls, query, data):
        return SQL(cls.dataBase).query(query, data)

    @classmethod
    def save(cls, data, *args):
        query = cls.query.buildSaveQuery(cls.tableName, *args)
        return SQL(cls.dataBase).query(query, data)

    @classmethod
    def delete(cls, data, *args):
        query = cls.query.buildRemoveQuery(cls.tableName, *args)
        return SQL(cls.dataBase).query(query, data)

    @classmethod
    def update(cls, data, **kwargs):
        query = cls.query.buildUpdateQuery(cls.tableName, **kwargs)
        return SQL(cls.dataBase).query(query, data)

    @classmethod
    def getLatest(cls):
        query = f"SELECT * FROM {cls.tableName} order by id DESC LIMIT 1;"
        results = SQL(cls.dataBase).query(query)

        resultsObjectList = []
        if not results:
            return False
        if results and len(results) == 1:
            resultsObjectList.append(cls(results[-1]))
        else:
            for result in results:
                resultsObjectList.append(cls(result))
        return resultsObjectList

    @classmethod
    def get(cls, data=None, *args):
        if data is None:
            query = cls.query.buildGetAllQuery(cls.tableName)
        else:
            query = cls.query.buildGetAllQuery(cls.tableName, *args)

        results = cls._executeQuery(query, data)
        resultsObjectList = []
        if not results:
            return False
        if results and len(results) == 1:
            resultsObjectList.append(cls(results[-1]))
        else:
            for result in results:
                resultsObjectList.append(cls(result))
        return resultsObjectList


