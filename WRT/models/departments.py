from WRT.config.model import Model


class Department(Model):
    tableName = "departments"

    def __init__(self, data):
        super().__init__(data)
        self.id = data["id"]
        self.name = data["name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data, *args):
        return super().save(data, "name")


if __name__ == '__main__':
    Department.get()
