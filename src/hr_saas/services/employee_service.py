from src.hr_saas.repository.employee_repo import EmployeeRepo
from src.hr_saas.model.employee import Employee
from src.hr_saas.auth.authorization import Authorization
from src.hr_saas.enums.role import Role
from src.hr_saas.enums.employee_type import EmployeeType


class EmployeeService:
    def __init__(self, emp_repo: EmployeeRepo):
        self._emp_repo = emp_repo

    def update_employee_type(self, current_user: Employee, employee: Employee, emp_type: EmployeeType):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])

        employee.type = emp_type
        self._emp_repo.save_employee(employee)

    def increase_leave(self, current_user: Employee, employee: Employee, day: int):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])

        employee.increase_leave_day(day)
        self._emp_repo.save_employee(employee)

    def deactivate_employee(self, current_user: Employee, employee: Employee):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        employee.deactivate()
        self._emp_repo.save_employee(employee)

    def activate_employee(self, current_user: Employee, employee: Employee):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        employee.activate()
        self._emp_repo.save_employee(employee)

    def promote_employee(self, current_user: Employee, employee: Employee, increase: float):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        employee.promote(salary_increase=increase)
        self._emp_repo.save_employee(employee)

    def delete_employee(self, current_user: Employee, employee: Employee):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        self._emp_repo.delete_employee(employee)

    def get_all_employee(self, current_user: Employee):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        return self._emp_repo.get_all_employee()

    def get_employee_by_email(self, current_user: Employee, email: str):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        return self._emp_repo.get_employee_by_email(email).to_dict()

    def count_employees(self, current_user: Employee):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        return len(self._emp_repo.get_all_employee())





