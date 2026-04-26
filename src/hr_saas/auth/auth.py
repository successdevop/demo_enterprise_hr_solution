from typing import Optional
from src.hr_saas.repository.employee_repo import EmployeeRepo
from src.hr_saas.model.employee import Employee
from src.hr_saas.error_handling.exceptions import UserAlreadyExistError
from src.hr_saas.utils.utils import Utils
from src.hr_saas.file_IO.logging import Logger
from src.hr_saas.file_IO.config_file import SUCCESS_LOG_FILE


class AuthN:
    def __init__(self, emp_repo: EmployeeRepo):
        self.emp_repo = emp_repo
        self.current_user: Optional[Employee] = None

    def register_user(self, name, email, age, origin, role, salary, password):
        email = email.strip().lower()
        Utils.validate_email(email)

        if self.emp_repo.get_employee_by_email(email):
            raise UserAlreadyExistError(f"{email} already exists")

        name = name.strip().title()
        origin = origin.strip().title()

        Utils.validate_name(name)
        Utils.validate_name(origin)
        Utils.validate_amount_input(salary)
        Utils.validate_age(age)

        employee = Employee(
            name=name,
            email=email,
            age=age,
            state_of_origin=origin,
            role=role,
            salary=salary
        )

        employee.set_password(password)

        self.emp_repo.save_employee(employee)
        Logger.success(f"Congratulations {name}, Registration Successful!!!", SUCCESS_LOG_FILE)

        return employee

