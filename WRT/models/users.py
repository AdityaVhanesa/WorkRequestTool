from WRT.config.model import Model
from WRT.config.dateTime import dateTime
from WRT.models.roles import Role


class User(Model):
    tableName = "users"

    def __init__(self, data):
        super(User, self).__init__(data)
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = dateTime(data["created_at"])
        self.updated_at = dateTime(data["updated_at"])
        self.role = self._getRole({
            "id": data["roles_id"]
        }, "id")

    def _getUser(self, data, *args):
        return User.get(data, *args)

    def _getRole(self, data, *args):
        return Role.get(data, *args)

    @classmethod
    def save(cls, data, *args):
        return super().save(data, "first_name", "last_name", "email", "password", "roles_id")

    def __str__(self):
        return f"User Object --> {self.first_name} {self.last_name}"


if __name__ == '__main__':
    data = {
        "first_name": "Jaini",
        "last_name": "Shah",
        "email": "adityaVha@gmail.com",
        "password": "Marky",
        "roles_id": 1,
    }
    print(User.get())
