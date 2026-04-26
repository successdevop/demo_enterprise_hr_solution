import re
from src.hr_saas.error_handling.exceptions import ValidationError


class Utils:
    @staticmethod
    def validate_email(email: str) -> str | None:
        # Stricter pattern that prevents leading/trailing dots
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]*[a-zA-Z0-9]@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        # Additional check for consecutive dots
        local_part = email.split('@')[0]
        if re.match(pattern, email) and '..' not in local_part:
            return email
        raise ValidationError("Invalid email format. Enter a correct email")

    @staticmethod
    def validate_name(name: str) -> str:
        if name and len(name) >= 3:
            return name
        raise ValidationError("Name value cannot be empty and must be at-least 3 characters")

    @staticmethod
    def validate_age(age: int) -> int:
        if isinstance(age, int):
            if age >= 18:
                return age
            else:
                raise ValidationError("You must be at-least 18 years")
        else:
            raise ValidationError("Invalid age value")

    @staticmethod
    def validate_amount_input(amount: float) -> float | None:
        """
        this function takes the user input and checks if it is an actually number
        and that the number is also not negative
        :param amount: user input
        :return: float number
        """
        if amount > 0:
            return float(amount)
        else:
            raise ValidationError(f"Amount cannot be negative and must be greater than 0")

