class query:
    def __init__(self):
        self.EOL = ";"

    def buildSaveQuery(self, tableName, *args):
        if len(args) < 1:
            return False

        basicQuery = f"INSERT INTO {tableName} "
        tableFields, tableValues = self._buildKeyValueLists(*args)

        basicQuery += tableFields + " VALUE " + tableValues + self.EOL
        return basicQuery

    def buildGetAllQuery(self, tableName, *args):
        basicQuery = f"SELECT * FROM {tableName}"
        if len(args) < 1:
            return basicQuery + self.EOL
        return basicQuery + " WHERE " + self._buildKeyValuePair("AND", list(args)) + self.EOL

    def buildUpdateQuery(self, tableName, **kwargs):
        if len(kwargs) < 1:
            return False

        if "values" not in kwargs and "location" not in kwargs:
            return False

        basicQuery = f"UPDATE {tableName} SET "
        updatePair = self.__buildKeyValuePair(",", kwargs["values"])
        locationPair = self.__buildKeyValuePair("AND", kwargs["location"])
        basicQuery += updatePair + " WHERE " + locationPair + self.EOL
        return basicQuery

    def buildRemoveQuery(self, tableName, *args):
        if len(args) < 1:
            return False

        basicQuery = f"DELETE FROM {tableName} WHERE "
        basicQuery += self.__buildKeyValuePair("AND", list(args)) + self.EOL
        return basicQuery

    def _buildKeyValueIndividual(self, item, isComma=False):
        if isComma:
            return f", {item}", f", %({item})s"
        return f"{item}", f"%({item})s"

    def _buildKeyValuePair(self, deliminator, itemList):
        if len(itemList) < 1:
            return ""

        basicClause = f"{itemList[0]} = %({itemList[0]})s"

        if len(itemList) > 1:
            for value in itemList[1::]:
                key, value = self.__buildKeyValueIndividual(value)
                basicClause += f" {deliminator} {key} = {value}"

        return basicClause

    def _buildKeyValueLists(self, *args):
        if len(args) < 1:
            return ""

        key, value = self._buildKeyValueIndividual(args[0])
        tableKey = f"{key}"
        tableValue = f"{value}"

        if len(args) > 1:
            for value in args[1::]:
                key, value = self._buildKeyValueIndividual(value, True)
                tableValue += value
                tableKey += key

        return f"( {tableKey} )", f"( {tableValue} )"
