from typing import Dict
from src.hr_saas.model.department import Department
from src.hr_saas.file_IO.dictionary_database import DictionaryDatabase


class DepartmentRepo:
    def __init__(self, storage_file: str):
        self._storage_file = storage_file
        self._department_database: Dict[str, Department] = {}
        self._load_department_database()

    def save_department(self, dept: Department):
        self._department_database[dept.name] = dept
        DictionaryDatabase.save(self._storage_file, "Department", self._department_database)

    def _load_department_database(self):
        DictionaryDatabase.load_data(self._storage_file, self._department_database,
                                     Department, "Department")
