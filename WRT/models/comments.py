from WRT.config.dateTime import dateTime
from WRT.config.model import Model
from WRT.models.tickets import Ticket
from WRT.models.users import User


class Comment(Model):
    tableName = "comments"

    def __init__(self, data):
        super(Comment, self).__init__(data)
        self.comment = data["comment"]
        self.posted_by = self._getUser({
            "id": data["posted_by"]
        }, "id")
        self.posted_on = self._getTicket({
            "id": data["posted_on"]
        }, "id")
        self.created_at = dateTime(data["created_at"])
        self.updated_at = dateTime(data["updated_at"])

    def _getUser(self, data, *args):
        return User.get(data, *args)

    def _getTicket(self, data, *args):
        return Ticket.get(data, *args)

    @classmethod
    def save(cls, data, *args):
        return super().save(data, "comment", "posted_by", "posted_on")
