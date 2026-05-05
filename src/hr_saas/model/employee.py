import uuid
import hashlib
from typing import List
from datetime import datetime
from src.hr_saas.enums.role import Role
from src.hr_saas.enums.employee_type import EmployeeType
from src.hr_saas.error_handling.exceptions import ValidationError
from src.hr_saas.utils.utils import Utils


class Person:
    def __init__(self, first_name: str, last_name: str, dob: str, email: str, state_of_origin: str):
        self._first_name = first_name
        self._last_name = last_name
        self._dob = datetime.strptime(dob, "%d/%m/%Y").date()
        self._email = email
        self._state_of_origin = state_of_origin

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def email(self):
        return self._email

    @property
    def dob(self):
        return self._dob

    @property
    def state_of_origin(self):
        return self._state_of_origin


class Employee(Person):
    def __init__(self, first_name, last_name, dob, email, state_of_origin, role: Role, salary: float):
        super().__init__(first_name=first_name, last_name=last_name, dob=dob, email=email,
                         state_of_origin=state_of_origin)
        self._employee_id = str(uuid.uuid4())
        self.role = role
        self._salary = salary
        self._age = datetime.now().date().year - self.dob.year
        self._type = None
        self.isActive = True
        self._password = None
        self._password_text = None
        self.department: List[str] = []
        self.hire_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self.role.value == "Admin" or self.role.value == "Hr" or self.role.value == "Manager":
            self._type = EmployeeType.FULL_TIME
            self.total_leave_days_for_the_year = 30
        else:
            self.total_leave_days_for_the_year = 14

        if self._salary:
            self._type = EmployeeType.CONTRACT if self._salary > 55000 else EmployeeType.INTERN

    @property
    def employee_id(self):
        return self._employee_id

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, salary: float):
        self._salary = Utils.validate_amount_input(salary)

    @property
    def emp_type(self):
        return self._type

    @emp_type.setter
    def emp_type(self, employee_type: str):
        self._type = employee_type

    def _get_password(self):
        return self._password

    def set_password(self, password):
        password = password.strip()
        if password and len(password) >= 8:
            self._password_text = password
            self._password = hashlib.sha256(password.encode()).hexdigest()
        else:
            raise ValidationError("Password must be at least 8 characters long")

    def check_password(self, password):
        check = hashlib.sha256(password.encode()).hexdigest()
        return check == self._get_password()

    def increase_leave_day(self, days):
        self.total_leave_days_for_the_year += days

    def promote(self, salary_increase: float):
        self._salary += salary_increase

    def deactivate(self):
        if self.isActive:
            self.isActive = False
        return

    def activate(self):
        if self.isActive:
            return
        self.isActive = True

    def to_dict(self, show_all: bool = True) -> dict:
        if show_all:
            return {
                "employee_id": self._employee_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "age": self._age,
                "origin": self.state_of_origin,
                "salary": self._salary,
                "role": self.role.value if hasattr(self.role, "value") else self.role,
                "emp_type": self._type.value if hasattr(self._type, "value") else self._type,
                "total_leave_days_for_the_year": self.total_leave_days_for_the_year,
                "is_active": self.isActive,
                "department": self.department,
                "hire_date": self.hire_date,
                "password_text": self._password_text,
                "password": self._password,
                "dob": self.dob.strftime("%d/%m/%Y")
            }
        else:
            return {
                "email": self.email,
                "first_name": self.first_name,
                "role": self.role.value if hasattr(self.role, "value") else self.role,
                "dob": self.dob.strftime("%d/%m/%Y"),
                "department": self.department
            }

    @classmethod
    def from_dict(cls, data: dict) -> "Employee":
        role = data.get("role")
        if isinstance(role, str) and hasattr(Role, role.upper()):
            role = Role[role.upper()]

        emp_type = data.get("emp_type")
        if isinstance(emp_type, str) and hasattr(EmployeeType, emp_type.upper()):
            emp_type = EmployeeType[emp_type.upper()]

        employee = cls(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            state_of_origin=data.get("origin"),
            salary=data.get("salary"),
            role=role,
            dob=data.get("dob")
        )
        employee._employee_id = data.get("employee_id")
        employee._age = data.get("age")
        employee.isActive = data.get("is_active")
        employee._password = data.get("password")
        employee._password_text = data.get("password_text")
        employee.emp_type = emp_type
        employee.total_leave_days_for_the_year = data.get("total_leave_days_for_the_year")
        employee.department = data.get("department")
        return employee

    def __eq__(self, other):
        if not isinstance(other, Employee):
            return False
        return self.email == other.email

    def __hash__(self):
        return hash(self.email)

    def __repr__(self):
        return f"<Employee email:{self.email} | first_name:{self.first_name} | role:{self.role.value}"
