from typing import Dict, Optional
from src.hr_saas.model.employee import Employee
from src.hr_saas.file_IO.dictionary_database import DictionaryDatabase


class EmployeeRepo:
    def __init__(self, employee_storage_file: str):
        self._employee_storage_file = employee_storage_file
        self._employee_database: Dict[str, Employee] = {}
        self._load_employee_database()

    def save_employee(self, employee: Employee):
        # Add to in-memory databases
        self._employee_database[employee.email] = employee
        DictionaryDatabase.save(self._employee_storage_file, "Employee", self._employee_database)

    def get_employee_by_email(self, email: str) -> Optional[Employee]:
        return self._employee_database.get(email)

    def _load_employee_database(self):
        DictionaryDatabase.load_data(self._employee_storage_file, self._employee_database,
                                     Employee, "Employee")