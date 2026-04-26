import re
from src.hr_saas.error_handling.exceptions import ValidationError


class Utils:
    @staticmethod
    def validate_email(email: str):
        # Stricter pattern that prevents leading/trailing dots
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]*[a-zA-Z0-9]@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        # Additional check for consecutive dots
        local_part = email.split('@')[0]
        if re.match(pattern, email) and '..' not in local_part:
            return email
        raise ValidationError("Invalid email format. Enter a correct email")
