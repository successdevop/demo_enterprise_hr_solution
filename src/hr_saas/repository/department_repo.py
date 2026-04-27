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
        return self._department_database.get(dept_name)

    def get_dept_managers(self):
        box = []
        if len(self._department_database) > 0:
            for dept_name, dept_manager in self._department_database.items():
                val = {"dept_name": dept_name, "manager": dept_manager.manager.name}
                box.append(val)
            return box
        raise NotFoundError("No department created yet")

    def get_all_department(self) -> Optional[List[str]]:
        return list(self._department_database.keys())

    def count_dept(self):
        return len(self._department_database)

    def delete_dept_by_name(self, dept_name: str):
        if dept_name in self._department_database:
            del self._department_database[dept_name]
            DictionaryDatabase.save(self._storage_file, "Department", self._department_database)
            print(f"{dept_name} department deleted")
        else:
            raise NotFoundError(f"{dept_name} department not found")

    def delete_all_department(self):
        if len(self._department_database) > 0:
            self._department_database.clear()
            DictionaryDatabase.save(self._storage_file, "Department", self._department_database)
            print(f"All department deleted")
        else:
            raise NotFoundError("No department found")

    def save_department(self, dept: Department):
        self._department_database[dept.name] = dept
        DictionaryDatabase.save(self._storage_file, "Department", self._department_database)

    def _load_department_database(self):
        DictionaryDatabase.load_data(self._storage_file, self._department_database,
                                     Department, "Department")
