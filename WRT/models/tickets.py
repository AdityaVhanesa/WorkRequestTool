from WRT.config.dateTime import dateTime
from WRT.config.model import Model
from WRT.models import departments as Departments
from WRT.models import users as Users
from WRT.models import reports as Reports


class Ticket(Model):
    tableName = "tickets"

    def __init__(self, data):
        super(Ticket, self).__init__(data)
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.created_at = dateTime(data["created_at"])
        self.updated_at = dateTime(data["updated_at"])
        self.start_at = dateTime(data["start_at"])
        self.closed_at = dateTime(data["closed_at"])
        self.status = data["status"]
        self.assigned_to = self._getUser({
            "id": data["assigned_to"]
        }, "id")
        self.closed_by = self._getUser({
            "id": data["closed_by"]
        }, "id")
        self.raised_by = self._getUser({
            "id": data["raised_by"]
        }, "id")
        self.functional_group = self._getDepartment({
            "id": data["functional_group"]
        }, "id")
        self.report = self._getReport({
            "id": data["report_id"]
        }, "id")

    def _getUser(self, data, *args):
        if data["id"] is None:
            return False
        return Users.User.get(data, *args)[0]

    def _getReport(self, data, *args):
        if data["id"] is None:
            return False
        return Reports.Report.get(data, *args)[0]

    def _getDepartment(self, data, *args):
        return Departments.Department.get(data, *args)[0]

    @classmethod
    def save(cls, data, *args):
        return super().save(data, "title", "description", "raised_by", "functional_group")

    @classmethod
    def update(cls, data, **kwargs):
        if "values" in kwargs:
            return super().update(data, **kwargs)
        return super().update(data, values=["title", "description", "functional_group"], location = ["id"])

    @classmethod
    def delete(cls, data, *args):

        deleteObjects = super().get(data, *args)

        if not deleteObjects:
            return

        for deleteObject in deleteObjects:
            data["posted_on"] = deleteObject.id
            Tickets.Ticket.delete(data, "posted_on")

        return super().delete(data, *args)


if __name__ == '__main__':
    data = {
        "title": "Test Ticket",
        "description": "This ment to be test",
        "raised_by": 1,
        "functional_group": 1,
        "id": 5
    }

    Ticket.update(data)
