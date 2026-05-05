from typing import List
from src.hr_saas.error_handling.exceptions import ValidationError, UserAlreadyExistError, NotFoundError
from src.hr_saas.model.employee import Employee


class Department:
    def __init__(self, dept_name: str, dept_manager: Employee):
        if not dept_name:
            raise ValidationError("Department must have a name")

        if dept_manager.role.value != "Manager":
            raise ValidationError("Department manager must have a manager role/position")

        self._dept_name = dept_name
        self._dept_manager = dept_manager
        self._dept_employees: List[Employee] = []

    @property
    def dept_name(self):
        return self._dept_name

    @property
    def dept_manager(self):
        return self._dept_manager

    @dept_manager.setter
    def dept_manager(self, manager: Employee):
        self._dept_manager = manager

    @property
    def get_dept_employees(self):
        return self._dept_employees

    def view_dept_employees(self):
        for emp in self._dept_employees:
            print(emp.to_dict(show_all=False))

    def assign_employee(self, employee: Employee):
        if self._dept_manager.employee_id == employee.employee_id:
            raise ValidationError(f"{employee.first_name} is the manager of {self._dept_name} department, "
                                  f"and cannot be assigned")

        if employee.role.value == "Manager":
            raise ValidationError(f"{employee.first_name} is a manager and cannot be assigned as a team member")

        if employee in self._dept_employees:
            raise UserAlreadyExistError(f"{employee.first_name} already in {self._dept_name} Department")

        self._dept_employees.append(employee)
        print(f"Employee {employee.first_name} added to the department")

    def remove_employee(self, employee: Employee):
        if employee not in self._dept_employees:
            raise NotFoundError("Employee not found")

        self._dept_employees.remove(employee)
        print(f"Employee {employee.first_name} removed from {self._dept_name} department")

    def to_dict(self):
        return {
            "dept_name": self._dept_name,
            "dept_manager": self._dept_manager.to_dict(show_all=False) if self._dept_manager else None,
            "dept_employees": [emp.to_dict(show_all=False) for emp in self._dept_employees]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Department":
        # Reconstruct manager from dict
        manager_data = data.get("dept_manager")
        manager = Employee.from_dict(manager_data)

        # Create department
        department = cls(
            dept_name=data.get("dept_name"),
            dept_manager=manager if manager else None
        )

        department._dept_employees = [
            Employee.from_dict(emp)
            for emp in data.get("dept_employees", [])
        ]
        return department

    def __repr__(self):
        return f"<Department(name: {self._dept_name} | manager: {self._dept_manager.first_name})>"
