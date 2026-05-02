from typing import Optional
from src.hr_saas.repository.employee_repo import EmployeeRepo
from src.hr_saas.model.employee import Employee
from src.hr_saas.error_handling.exceptions import UserAlreadyExistError, ValidationError
from src.hr_saas.utils.utils import Utils
from src.hr_saas.file_IO.logging import Logger
from src.hr_saas.file_IO.config_file import SUCCESS_LOG_FILE, ERROR_LOG_FILE, INFO_LOG_FILE


class Auth:
    def __init__(self, emp_repo: EmployeeRepo):
        self._emp_repo = emp_repo
        self._current_user: Optional[Employee] = None

    def get_current_user(self):
        return self._current_user

    def register_user(self, first_name, last_name, dob, email, origin, role, salary, password):
        email = email.strip().lower()
        Utils.validate_email(email)

        if self._emp_repo.get_employee_by_email(email):
            raise UserAlreadyExistError(f"{email} already exists")

        first_name = first_name.strip().title()
        last_name = last_name.strip().title()
        origin = origin.strip().title()

        Utils.validate_name(first_name)
        Utils.validate_name(last_name)
        Utils.validate_name(origin)
        Utils.validate_amount_input(salary)

        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            email=email,
            state_of_origin=origin,
            role=role,
            salary=salary
        )

        employee.set_password(password)

        self._emp_repo.save_employee(employee)
        Logger.success(f"Congratulations {first_name}, Registration Successful!!!", SUCCESS_LOG_FILE)
        print("Registration successful")

        return employee

    def login(self, email, password):
        email = email.strip().lower()
        Utils.validate_email(email)
        user = self._emp_repo.get_employee_by_email(email)

        if not user:
            Logger.error(f"user not found | {email}", ERROR_LOG_FILE)
            raise ValidationError("user not found")

        if not user.check_password(password):
            Logger.error(f"Invalid password for email | {email}", ERROR_LOG_FILE)
            raise ValidationError("Invalid email or password")

        if not user.isActive:
            Logger.error(f"user account deactivated: {email}", ERROR_LOG_FILE)
            raise ValidationError("Account deactivated, please contact support center/agents")

        self._current_user = user
        Logger.success(f"Login successful | {email}", SUCCESS_LOG_FILE)
        print(f"Login successful | {email}")
        return user

    def logout(self):
        if self._current_user:
            Logger.info(f"{self._current_user.email} logged out", INFO_LOG_FILE)
            print(f"{self._current_user.email} logged out")
            self._current_user = None

    def forgot_password(self, email):
        email = email.strip().lower()

        user = self._emp_repo.get_employee_by_email(email)
        if not user:
            Logger.error(f"Unknown/unregistered user trying to change password | {email}", ERROR_LOG_FILE)
            print(f"{email} not found")

        password = str(input("enter new password: "))
        verify_password = str(input("verify new password: "))
        if password != verify_password:
            Logger.error(f"Password change does not match for {user.email}", ERROR_LOG_FILE)
            raise ValidationError("Password does not match, try again")

        user.set_password(password)

        self._emp_repo.save_employee(user)
        Logger.info("Password changed successfully", INFO_LOG_FILE)
        print("Password changed successfully")
        return user


