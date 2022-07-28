from WRT.config.dateTime import dateTime
from WRT.config.model import Model
from WRT.models import users as Users
from WRT.models import roles as Roles


class Manager(Model):
    tableName = "managers"

    def __init__(self, data):
        super().__init__(data)
        self.id = data["id"]
        self.user = self._getUser({"id": data["users_id"]}, "id")
        self.created_at = dateTime(data["created_at"])
        self.updated_at = dateTime(data["updated_at"])

    def _getUser(self, data, *args):
        return Users.User.get(data, *args)[0]

    @classmethod
    def save(cls, data, *args):
        super().save(data, "users_id")
        managerObject = cls.get(data, 'users_id')[0]
        data["id"] = managerObject.user.role.id
        data["managers_id"] = managerObject.id
        Roles.Role.update(data, values=["managers_id"], location=["id"])

    @classmethod
    def delete(cls, data, *args):
        deleteObjects = super().get(data, *args)

        if not deleteObjects:
            return

        for deleteObject in deleteObjects:
            data["roles_id"] = deleteObject.id
            Users.User.delete(data, "roles_id")

        return super().delete(data, *args)

    def __str__(self):
        return f"{self.user}"


if __name__ == '__main__':
    data = {
        "id": 7
    }
    Role.delete(data, "id")
