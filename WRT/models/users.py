from WRT.config.dateTime import dateTime
from WRT.config.model import Model
from WRT.models import tickets as Tickets
from WRT.models import roles as Roles


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
        return User.get(data, *args)[0]

    def _getRole(self, data, *args):
        return Roles.Role.get(data, *args)[0]

    @classmethod
    def save(cls, data, *args):
        return super().save(data, "first_name", "last_name", "email", "password", "roles_id")

    @classmethod
    def delete(cls, data, *args):

        deleteObjects = super().get(data, *args)

        if not deleteObjects:
            return

        for deleteObject in deleteObjects:
            data["raised_by"] = deleteObject.id
            Tickets.Ticket.delete(data, "raised_by")

        return super().delete(data, *args)

    def __str__(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"


if __name__ == '__main__':
    data = {
        "first_name": "Bharati",
        "last_name": "Vhanesa",
        "email": "adityaVha@gmail.com",
        "password": "Marky",
        "roles_id": 1,
    }
    User.save(data)
