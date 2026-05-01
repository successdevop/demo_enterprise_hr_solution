from datetime import datetime
from src.hr_saas.model.employee import Employee
from src.hr_saas.enums.week import WeekDay
from src.hr_saas.error_handling.exceptions import UserAlreadyExistError, ValidationError


class Attendance:
    def __init__(self, employee: Employee, day_of_the_week: WeekDay):
        self.day_of_the_week = day_of_the_week
        self.employee = employee
        self.clocked_in = None
        self.clocked_out = None
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def check_in(self):
        if self.clocked_in:
            raise UserAlreadyExistError("Already checked in")
        self.clocked_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def check_out(self):
        if not self.clocked_in:
            raise ValidationError("You must check in first before checking out")

        if self.clocked_out:
            raise UserAlreadyExistError("Already checked out")

        self.clocked_out = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def total_hours_worked(self) -> float:
        if not self.clocked_in or not self.clocked_out:
            return 0.0

        delta = (datetime.now().strptime(self.clocked_out, "%Y-%m-%d %H:%M:%S") -
                 datetime.now().strptime(self.clocked_in, "%Y-%m-%d %H:%M:%S"))
        return delta.total_seconds() / 3600

    @property
    def total_hours_worked_per_day(self):
        return self.total_hours_worked()

    def to_dict(self):
        return {
            "day_of_the_week": self.day_of_the_week.value if hasattr(self.day_of_the_week, "value") else None,
            "clocked_in": self.clocked_in,
            "clocked_out": self.clocked_out,
            "total_hours_worked_per_day": self.total_hours_worked_per_day,
            "date": self.date,
            "employee": self.employee.to_dict(show_all=False) if self.employee else None
        }

    @classmethod
    def from_to_dict(cls, data: dict) -> "Attendance":
        day = data.get("day_of_the_week")
        if isinstance(day, str) and hasattr(WeekDay, day.upper()):
            day = WeekDay[day.upper()]

        attendance = cls(
            day_of_the_week=day,
            employee=Employee.from_dict(data.get("employee")),
        )
        attendance.clocked_in = data.get("clocked_in")
        attendance.clocked_out = data.get("clocked_out")
        attendance.date = data.get("date")
        return attendance

    def __repr__(self):
        return f"<Attendance(name:{self.employee.name}) | clocked_in:{self.clocked_in} | clocked_out:{self.clocked_out}>"

