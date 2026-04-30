from src.hr_saas.model.employee import Employee
from src.hr_saas.enums.month import Month


class Payslip:
    def __init__(self, employee: Employee, base_salary: float, deductions: float, bonus: float,
                 net_salary: float, pension: float, month: Month, currency):
        self.month = month
        self.employee = employee
        self.base_salary = base_salary
        self.deductions = deductions
        self.bonus = bonus
        self.net_salary = net_salary
        self.pension = pension
        self.currency = currency

    def to_dict(self):
        return {
            "month": self.month.value if hasattr(self.month, "value") else None,
            "base_salary": self.base_salary,
            "deductions": self.deductions,
            "bonus": self.bonus,
            "net_salary": self.net_salary,
            "pension": self.pension,
            "currency": self.currency,
            "employee": self.employee.to_dict(show_all=False) if self.employee else None
        }

    @classmethod
    def from_to_dict(cls, data: dict) -> "Payslip":
        month = data.get("month")
        if isinstance(month, str) and hasattr(Month, month.upper()):
            month = Month[month.upper()]

        payslip = cls(
            month=month,
            base_salary=data.get("base_salary"),
            deductions=data.get("deductions"),
            bonus=data.get("bonus"),
            net_salary=data.get("net_salary"),
            pension=data.get("pension"),
            currency=data.get("currency"),
            employee=Employee.from_dict(data.get("employee"))
        )
        return payslip

    def __repr__(self):
        return f"<Payslip(name: {self.employee.name} | net_salary: {self.net_salary} | status: {self.employee.role.value})>"
