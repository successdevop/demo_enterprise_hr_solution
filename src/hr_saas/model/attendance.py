from datetime import datetime
from src.hr_saas.model.employee import Employee
from src.hr_saas.error_handling.exceptions import UserAlreadyExistError, ValidationError


class Attendance:
    def __init__(self, employee: Employee, day_of_the_week: WeekDay):
        self.day_of_the_week = day_of_the_week
        self.employee = employee
        self.clock_in = None
        self.clock_out = None
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def check_in(self):
        if self.clock_in:
            raise UserAlreadyExistError("Already checked in")
        self.clock_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def check_out(self):
        if not self.clock_in:
            raise ValidationError("You must check in first before checking out")

        if self.clock_out:
            raise UserAlreadyExistError("Already checked out")

        self.clock_out = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def total_hours_worked(self) -> float:
        if not self.clock_in or not self.clock_out:
            return 0.0

        delta = (datetime.now().strptime(self.clock_out, "%Y-%m-%d %H:%M:%S") -
                 datetime.now().strptime(self.clock_in, "%Y-%m-%d %H:%M:%S"))
        return delta.total_seconds() / 3600

    @property
    def total_hours_worked_per_day(self):
        return self.total_hours_worked()

    def to_dict(self):
        return {
            "clock_in": self.clock_in,
            "clock_out": self.clock_out,
            "total_hours_worked_per_day": self.total_hours_worked_per_day,
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
        attendance.date = data.get("date")
        return attendance

