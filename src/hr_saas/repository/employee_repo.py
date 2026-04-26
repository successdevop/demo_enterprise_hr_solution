import json
from typing import Dict, Optional
from src.hr_saas.model.employee import Employee
from src.hr_saas.file_IO.logging import Logger
from src.hr_saas.file_IO.config_file import ERROR_LOG_FILE


class EmployeeRepo:
    def __init__(self, employee_storage_file: str):
        self._employee_storage_file = employee_storage_file
        self._employee_database: Dict[str, Employee] = {}
        self._load_employee_database()

    def save_employee(self, employee: Employee):
        # Add to in-memory databases
        self._employee_database[employee.email] = employee

        # Prepare data for JSON serialization
        savable_data = {
            email: employee.to_dict()
            for email, employee in self._employee_database.items()
        }

        try:
            with open(self._employee_storage_file, mode="w", encoding="utf-8") as file_writer:
                json.dump(savable_data, file_writer, indent=4)
        except Exception as e:
            Logger.error(f"Error saving employee | {e}", ERROR_LOG_FILE)

    def get_employee_by_email(self, email: str) -> Optional[Employee]:
        return self._employee_database.get(email)

    def _load_employee_database(self):
        self._employee_database.clear()

        try:
            with open(self._employee_storage_file, mode="r", encoding="utf-8") as emp_reader:
                data = json.load(emp_reader)

                if isinstance(data, dict):
                    for emp_email, emp_data in data.items():
                        if isinstance(emp_data, dict):
                            employee = Employee.from_dict(emp_data)
                        else:
                            employee = emp_data

                        self._employee_database[emp_email] = employee

        except FileNotFoundError as e:
            # First run - file doesn't exist yet
            Logger.error(f"Database file not found, starting fresh | {e}", ERROR_LOG_FILE)
            self._employee_database = {}
        except json.JSONDecodeError as e:
            # File exists but is empty or corrupted
            Logger.error(f"JSON Decode Error | {e}", ERROR_LOG_FILE)
            self._employee_database = {}
        except Exception as e:
            Logger.error(f"Error Loading Employee Database | {e}", ERROR_LOG_FILE)
            self._employee_database = {}
