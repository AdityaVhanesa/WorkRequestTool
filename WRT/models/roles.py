from WRT.config.dateTime import dateTime
from WRT.config.model import Model


class Role(Model):
    tableName = "roles"

    def __init__(self, data):
        super().__init__(data)
        self.role_name = data["role_name"]
        self.created_at = dateTime(data["created_at"])
        self.updated_at = dateTime(data["updated_at"])

    @classmethod
    def save(cls, data, *args):
        return super().save(data, "role_name")

    def __str__(self):
        return f"Role --> {self.role_name}"


if __name__ == '__main__':
    data = {
        "role_name": "Electrical Engineer"
    }
    print(Role.get())
