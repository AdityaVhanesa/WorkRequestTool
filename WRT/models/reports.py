from WRT.config.dateTime import dateTime
from WRT.config.model import Model


class Report(Model):
    tableName = "reports"

    def __init__(self, data):
        super().__init__(data)
        self.id = data["id"]
        self.reportLink = data["report_link"]
        self.created_at = dateTime(data["created_at"])
        self.updated_at = dateTime(data["updated_at"])

    @classmethod
    def save(cls, data, *args):
        super().save(data, "report_link")

    def __str__(self):
        return self.reportLink
