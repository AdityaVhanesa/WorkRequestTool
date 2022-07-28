from WRT.config.dateTime import dateTime
from WRT.config.model import Model
from WRT.models import departments as Departments
from WRT.models import users as Users


class Role(Model):
    tableName = "roles"

    def __init__(self, data):
        super().__init__(data)
        self.id = data["id"]
        self.role_name = data["role_name"]
        self.department = self._getDepartment({"id": data["departments_id"]}, "id")
        self.created_at = dateTime(data["created_at"])
        self.updated_at = dateTime(data["updated_at"])

    def _getDepartment(self, data, *args):
        return Departments.Department.get(data, *args)

    @classmethod
    def save(cls, data, *args):
        return super().save(data, "role_name", "departments_id")
    
    @classmethod
    def update(cls, data, **kwargs):
        super().update(data, **kwargs)

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
        return f"Role --> {self.role_name}"


if __name__ == '__main__':
    data = {
        "id": 7
    }
    Role.delete(data, "id")
