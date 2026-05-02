from src.hr_saas.repository.payroll_repo import PayrollRepository
from src.hr_saas.strategy.tax_strategy import NigerianTaxStrategy
from src.hr_saas.strategy.tax_strategy import Pension
from src.hr_saas.strategy.currency_converter import CurrencyStrategy
from src.hr_saas.model.employee import Employee
from src.hr_saas.model.payroll import Payslip
from src.hr_saas.file_IO.logging import Logger
from src.hr_saas.file_IO.config_file import SUCCESS_LOG_FILE
from src.hr_saas.enums.role import Role
from src.hr_saas.enums.month import Month
from src.hr_saas.error_handling.exceptions import AuthorizationError, NotFoundError
from src.hr_saas.auth.authorization import Authorization


class PayrollServices:
    def __init__(self, payroll_repo: PayrollRepository, currency_converter: CurrencyStrategy,
                 tax_strategy: NigerianTaxStrategy, pension: Pension):
        self._payroll_repo = payroll_repo
        self._currency_converter = currency_converter
        self._tax_strategy = tax_strategy
        self._pension = pension

    def process_salary(self, current_user, employee: Employee, month: Month, currency: str, deduction: float,
                       bonus: float):
        Authorization.authorized_roles(current_user, [Role.HR, Role.ADMIN])

        payslip = self._payroll_repo.get_employee_payslip(employee, month.value)
        if payslip:
            print(f"Payslip already processed for {employee.first_name} in {month.value}")
            return payslip

        base_salary = employee.salary

        tax = self._tax_strategy.calculate(base_salary)
        emp_pension, employer_pension, total_pension = self._pension.calculate(base_salary)
        net_salary = base_salary - tax - deduction + bonus - emp_pension

        converted_salary = self._currency_converter.convert(net_salary, "NGN", currency)

        payslip = Payslip(employee=employee, base_salary=base_salary, net_salary=converted_salary,
                          pension=total_pension, month=month, currency=currency, deductions=deduction, bonus=bonus)

        self._payroll_repo.save_payslip(payslip)
        Logger.success(f"Payroll processed for {employee.first_name}", SUCCESS_LOG_FILE)
        return payslip

    def get_employee_payslip(self, current_user, employee: Employee, month: Month):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR, Role.EMPLOYEE])

        if current_user.role == Role.EMPLOYEE:
            if employee.email != current_user.email:
                raise AuthorizationError("You are not allowed to perform this action")

        payslip = self._payroll_repo.get_employee_payslip(employee, month.value)
        if not payslip:
            raise NotFoundError(f"{employee.first_name} has no payslip for the month of {month.value}")
        return payslip

    def get_payslip_for_each_month(self, current_user, month: Month):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])

        payslip = self._payroll_repo.get_payslip_for_each_month(month.value)
        return payslip

    def delete_payslip(self, current_user, month: Month, payslip_id: str):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])

        self._payroll_repo.delete_payslip(month.value, payslip_id)

    def get_all_payslips(self, current_user):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        return self._payroll_repo.get_all_payslip()
