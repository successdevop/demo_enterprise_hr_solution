from typing import List
from src.hr_saas.enums.role import Role
from src.hr_saas.model.employee import Employee
from src.hr_saas.error_handling.exceptions import AuthorizationError, ValidationError


class Authorization:
    @staticmethod
    def authorized_roles(user: Employee, allowed_roles: List[Role]):
        if not isinstance(user, Employee):
            raise ValidationError("Invalid user")

        if user.role not in allowed_roles:
            raise AuthorizationError(f"{user.role.value} is not allowed to perform this action")
