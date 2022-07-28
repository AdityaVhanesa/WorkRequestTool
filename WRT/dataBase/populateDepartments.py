from WRT.models import departments as Departments


departmentList = ["Production",
                  "Software Engineering",
                  "Hardware Engineering",
                  "Mechanical Engineering",
                  "Administrative",
                  "Finance",
                  "Central Engineering",
                  "NPIE Engineering",
                  "Marketing",
                  "Supply Chain"
                  "Social",
                  "Legal",
                  "External Affairs",
                  "Security",
                  "General"
                  ]

if __name__ == '__main__':
    for department in departmentList:
        data = {
            "name": department
        }
        Departments.Department.save(data)