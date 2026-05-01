import random

from src.hr_saas.model.employee import Employee
from src.hr_saas.enums.month import Month


class Payslip:
    def __init__(self, employee: Employee, base_salary: float, net_salary: float, pension: float, month: Month,
                 currency: str, deductions: float, bonus: float):
        self.payslip_id = "".join(str(random.randint(0, 9)) for _ in range(5))
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
            "payslip_id": self.payslip_id,
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
        payslip.payslip_id = data.get("payslip_id")
        return payslip

    def __repr__(self):
        currency_list = {"NGN": "#", "USD": "$", "EUR": "€", "GBP": "£"}
        currency = currency_list.get(self.currency, "")
        return (f"<Payslip(name: {self.employee.name} | net_salary:{currency}{self.net_salary} | status: "
                f"{self.employee.role.value})>")
