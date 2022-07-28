from WRT.config.dateTime import dateTime
from WRT.config.model import Model
from WRT.models import tickets as Tickets
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
        return User.get(data, *args)[0]

    def _getTicket(self, data, *args):
        return Tickets.Ticket.get(data, *args)[0]

    @classmethod
    def save(cls, data, *args):
        return super().save(data, "comment", "posted_by", "posted_on")


if __name__ == '__main__':
    data = {
        "comment": "Hi Zeal Here.",
        "posted_by": 6,
        "posted_on": 1,
    }
    Comment.save(data)













