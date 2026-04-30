from abc import ABC, abstractmethod


class TaxStrategy(ABC):
    @abstractmethod
    def calculate(self, salary):
        pass


class NigerianTaxStrategy(TaxStrategy):
    def calculate(self, salary):
        if salary <= 3000:
            return salary * 0.1
        elif salary <= 10000:
            return salary * 0.15
        else:
            return salary * 0.2


class Pension:
    @staticmethod
    def calculate(salary):
        employee_contribution = salary * 0.08
        employer_contribution = salary * 0.10
        total_pension = employee_contribution + employer_contribution
        return employee_contribution, employer_contribution, total_pension
