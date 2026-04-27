from typing import List
from src.hr_saas.error_handling.exceptions import ValidationError, UserAlreadyExistError, NotFoundError
from src.hr_saas.model.employee import Employee


class Department:
    def __init__(self, name: str, manager: Employee):
        if not name:
            raise ValidationError("Department must have a name")

        if manager.role.value != "Manager":
            raise ValidationError("Department manager must have a manager role/position")

        self._name = name
        self._manager = manager
        self._dept_employees: List[Employee] = []

    @property
    def name(self):
        return self._name

    @property
    def manager(self):
        return self._manager

    def view_dept_employees(self):
        for emp in self._dept_employees:
            print(emp)

    def assign_employee(self, employee: Employee):
        if self._manager.employee_id == employee.employee_id:
            raise ValidationError(f"{employee.name} is the manager of {self._name} department, and cannot be assigned")

        if employee.role.value == "Manager":
            raise ValidationError(f"{employee.name} is a manager and cannot be assigned as a team member")

        if employee in self._dept_employees:
            raise UserAlreadyExistError(f"{employee.name} already in {self._name} Department")

        self._dept_employees.append(employee)
        print(f"Employee {employee.name} added to the department")

    def remove_employee(self, employee: Employee):
        if employee not in self._dept_employees:
            raise NotFoundError("Employee not found")

        self._dept_employees.remove(employee)
        print(f"Employee {employee.name} removed from {self._name} department")

    def to_dict(self):
        return {
            "dept_name": self._name,
            "dept_manager": self._manager.to_dict(show_all=False) if self._manager else None,
            "dept_employees": [emp.to_dict(show_all=False) for emp in self._dept_employees]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Department":
        # Reconstruct manager from dict
        manager_data = data.get("dept_manager")
        manager = Employee.from_dict(manager_data)

        # Create department
        department = cls(
            name=data.get("dept_name"),
            manager=manager if manager else None
        )

        department._dept_employees = [
            Employee.from_dict(emp)
            for emp in data.get("dept_employees", [])
        ]
        return department

    def __repr__(self):
        return f"<Department(name: {self._name} | manager: {self._manager.name})>"
