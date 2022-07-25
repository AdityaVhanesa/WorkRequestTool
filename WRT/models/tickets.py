from WRT.config.dateTime import dateTime
from WRT.config.model import Model
from WRT.models.roles import Role
from WRT.models.users import User


class Ticket(Model):
    tableName = "tickets"

    def __init__(self, data):
        super(Ticket, self).__init__(data)
        self.title = data["title"]
        self.description = data["description"]
        self.created_at = dateTime(data["created_at"])
        self.updated_at = dateTime(data["updated_at"])
        self.closed_at = dateTime(data["closed_at"])
        self.closed_by = self._getUser({
            "id": data["closed_by"]
        })
        self.raised_by = self._getUser({
            "id": data["raised_by"]
        })
        self.functional_group = self._getRole({
            "id": data["functional_group"]
        })

    def _getUser(self, data, *args):
        return User.get(data, *args)

    def _getRole(self, data, *args):
        return Role.get(data, *args)

    @classmethod
    def save(cls, data, *args):
        return super().save(data, "title", "description", "raised_by", "functional_group")

    