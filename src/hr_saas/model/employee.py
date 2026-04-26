import uuid
import hashlib
from typing import List
from datetime import datetime
from abc import ABC, abstractmethod
from src.hr_saas.enums.role import Role
from src.hr_saas.error_handling.exceptions import ValidationError


class Person(ABC):
    @abstractmethod
    def __init__(self, name: str, email: str, age: int, state_of_origin: str):
        self._name = name
        self._email = email
        self._state_of_origin = state_of_origin
        self._age = age

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def age(self):
        return self._age

    @property
    def state_of_origin(self):
        return self._state_of_origin


class Employee(Person):
    def __init__(self, name, email, age, state_of_origin, role: Role, salary: float):
        super().__init__(name=name, email=email, age=age, state_of_origin=state_of_origin)
        self._employee_id = str(uuid.uuid4())
        self.role = role
        self._salary = salary
        self.type = None
        self.isActive = True
        self._password = None
        self.department: List[str] = []
        self.hire_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def employee_id(self):
        return self._employee_id

    @property
    def salary(self):
        return self._salary

    def _get_password(self):
        return self._password

    def set_password(self, password):
        password = password.strip()
        if password and len(password) >= 8:
            self._password = hashlib.sha256(password.encode()).hexdigest()
        else:
            raise ValidationError("Password must be at least 8 characters long")

    def check_password(self, password):
        check = hashlib.sha256(password.encode()).hexdigest()
        return check == self._get_password()

    def to_dict(self) -> dict:
        return {
            "employee_id": self._employee_id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "origin": self.state_of_origin,
            "salary": self._salary,
            "role": self.role.value if hasattr(self.role, "value") else self.role,
            "is_active": self.isActive,
            "department": self.department,
            "hire_date": self.hire_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Employee":

        role = data.get("role")
        if isinstance(role, str) and hasattr(Role, role.upper()):
            role = Role[role.upper()]

        employee = cls(
            name=data.get("name"),
            email=data.get("email"),
            age=data.get("age"),
            state_of_origin=data.get("origin"),
            salary=data.get("salary"),
            role=role,
        )

        employee._employee_id = data.get("employee_id")
        employee.isActive = data.get("is_active")
        employee.department = data.get("department")
        employee._get_password()
        employee.type = data["type"]
        return employee

