import unittest

from WRT.config.queryConstrctor import query


class testQueryBuilder(unittest.TestCase):

    def setUp(self) -> None:
        self.query = query()

        self.removeQueryTestDir_string = {
            self.query.buildRemoveQuery("user", "id"): "DELETE FROM user WHERE id = %(id)s;",
            self.query.buildRemoveQuery("user", "id",
                                        "value"): "DELETE FROM user WHERE id = %(id)s AND value = %(value)s;",
        }
        self.removeQueryTestList_bool_false = [
            self.query.buildRemoveQuery("user"),
        ]

        self.gelAllQueryTestDir_string = {
            self.query.buildGetAllQuery("user"): "SELECT * FROM user;",
            self.query.buildGetAllQuery("user", "id"): "SELECT * FROM user WHERE id = %(id)s;",
            self.query.buildGetAllQuery("user", "id",
                                        "food"): "SELECT * FROM user WHERE id = %(id)s AND food = %(food)s;",
        }

        self.saveQueryTestDir_string = {
            self.query.buildSaveQuery("user", "id"):
                "INSERT INTO user ( id ) VALUE ( %(id)s );",
            self.query.buildSaveQuery("user", "id", "item", "food"):
                "INSERT INTO user ( id, item, food ) VALUE ( %(id)s, %(item)s, %(food)s );"
        }

        self.updateQueryTestDir_string = {
            self.query.buildUpdateQuery("user", values=["id"], location=["id"]):
                "UPDATE user SET id = %(id)s WHERE id = %(id)s;",
            self.query.buildUpdateQuery("user", values=["food", "item", "location", "test1"], location=["item", "id"]):
                "UPDATE user SET food = %(food)s , item = %(item)s , location = %(location)s , test1 = %(test1)s "
                "WHERE item = %(item)s AND id = %(id)s;"
        }

    def test_buildRemoveQuery(self):
        for key, value in self.removeQueryTestDir_string.items():
            self.assertEqual(key, value)

        for value in self.removeQueryTestList_bool_false:
            self.assertFalse(value)

    def test_buildGetAllQuery(self):
        for key, value in self.gelAllQueryTestDir_string.items():
            self.assertEqual(key, value)

    def test_buildSaveQuery(self):
        for key, value in self.saveQueryTestDir_string.items():
            self.assertEqual(key, value)

    def test_buildUpdateQuery(self):
        for key, value in self.updateQueryTestDir_string.items():
            self.assertEqual(key, value)


if __name__ == '__main__':
    unittest.main()
