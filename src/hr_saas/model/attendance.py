from datetime import datetime
from src.hr_saas.model.employee import Employee
from src.hr_saas.error_handling.exceptions import UserAlreadyExistError, ValidationError


class Attendance:
    def __init__(self, employee: Employee):
        self.employee = employee
        self.clock_in = None
        self.clock_out = None
        self.date = datetime.now().date()

    def check_in(self):
        if self.clock_in:
            raise UserAlreadyExistError("Already checked in")
        self.clock_in = datetime.now()

    def check_out(self):
        if not self.clock_in:
            raise ValidationError("You must check in first before checking out")

        if self.clock_out:
            raise UserAlreadyExistError("Already checked out")

        self.clock_out = datetime.now()

    def total_hours_worked(self):
        if not self.clock_in or not self.clock_out:
            return 0

        delta = self.clock_out - self.clock_in
        return delta.total_seconds() / 3600

    def to_dict(self):
        return {
            "clock_in": self.clock_in,
            "clock_out": self.clock_out,
            "total_hours_worked": self.total_hours_worked(),
            "date": self.date,
            "employee": self.employee.to_dict(show_all=False) if self.employee else None
        }

    @classmethod
    def from_to_dict(cls, data: dict) -> "Attendance":
        attendance = cls(
            employee=Employee.from_dict(data.get("employee")),
        )
        attendance.clock_in = data.get("clock_in")
        attendance.clock_out = data.get("clock_out")
        attendance.total_hours_worked = data.get("total_hours_worked")
        attendance.date = data.get("date")
        return attendance

