from typing import Dict, Optional, List
from src.hr_saas.model.department import Department
from src.hr_saas.error_handling.exceptions import NotFoundError
from src.hr_saas.file_IO.dictionary_database import DictionaryDatabase


class DepartmentRepo:
    def __init__(self, storage_file: str):
        self._storage_file = storage_file
        self._department_database: Dict[str, Department] = {}
        self._load_department_database()

    def get_dept_by_name(self, dept_name: str) -> Optional[Department]:
        return self._department_database.get(dept_name, None)

    def get_dept_managers(self) -> List[dict]:
        box = []
        if self._department_database is None or len(self._department_database) == 0:
            raise NotFoundError("No department created yet")

        for dept_name, dept_manager in self._department_database.items():
            val = {"dept_name": dept_name, "manager": dept_manager.dept_manager.first_name}
            box.append(val)
        return box

    def get_all_department(self) -> Optional[List[str]]:
        return list(self._department_database.keys())

    def count_dept(self):
        return len(self._department_database)

    def delete_dept_by_name(self, dept_name: str):
        if dept_name not in self._department_database:
            raise NotFoundError(f"{dept_name} department not found")

        del self._department_database[dept_name]
        DictionaryDatabase.save(self._storage_file, "Department", self._department_database)
        print(f"{dept_name} department deleted")

    def delete_all_department(self):
        if self._department_database is None or len(self._department_database) == 0:
            raise NotFoundError("No department found")

        self._department_database.clear()
        DictionaryDatabase.save(self._storage_file, "Department", self._department_database)
        print(f"All department deleted")

    def save_department(self, dept: Department):
        self._department_database[dept.dept_name] = dept
        DictionaryDatabase.save(self._storage_file, "Department", self._department_database)

    def _load_department_database(self):
        DictionaryDatabase.load_data(self._storage_file, self._department_database,
                                     Department, "Department")
