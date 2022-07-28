from WRT.models import roles as Roles


rolesName = [
    ["Test Engineer", "Supervisor", "Technician", "Assembler", "Merchandize expert", "Shipping", "Stocking", "Picking"],
    ["Infra Engineer", "IT Security", "Autotest Engineer", "QA Analysit", "Application Engineer", "FW Developer", "Data Scientist"],
    ["PCB Designer", "Layout Engineer", "Sustaining Engineer", "NPD Engineer"],
    ["Thermal Engineer", "Cad Designer", "Intern"],
    ["HR", "Administrative Assistant"],
    ["Financial Advisor"],
    ["EDVT", "MDVT", "Packaging", "ODVT"],
    ["Product Integration Engineer"],
    ["Sales Representative"],
    ["Supply Chain Expert"],
    ["Social Netowrk Specialist"],
    ["Advocate"],
    ["Foreign Relationship Expert"],
    ["Gaurd"],
    ["Cleaner", "Chef"]
]


if __name__ == '__main__':
    i = 1
    for roles in rolesName:
        for role in roles:
            data = {
                "role_name": role,
                "departments_id": i
            }
            Roles.Role.save(data)
        i += 1