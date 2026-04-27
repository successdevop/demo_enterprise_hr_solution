from src.hr_saas.repository.department_repo import DepartmentRepo
from src.hr_saas.repository.employee_repo import EmployeeRepo
from src.hr_saas.model.employee import Employee
from src.hr_saas.model.department import Department
from src.hr_saas.utils.utils import Utils
from src.hr_saas.file_IO.logging import Logger
from src.hr_saas.file_IO.config_file import SUCCESS_LOG_FILE
from src.hr_saas.error_handling.exceptions import UserAlreadyExistError, NotFoundError
from src.hr_saas.auth.authorization import Authorization
from src.hr_saas.enums.role import Role


class DepartmentService:
    def __init__(self, dept_repo: DepartmentRepo, emp_repo: EmployeeRepo):
        self._dept_repo = dept_repo
        self._emp_repo = emp_repo

    def create_department(self, current_user, dept_name: str, manager: Employee):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        Utils.validate_name(dept_name)

        if self._dept_repo.get_dept_by_name(dept_name.capitalize()):
            raise UserAlreadyExistError(f"{dept_name} Department: already exists")

        department = Department(dept_name, manager)

        self._dept_repo.save_department(department)
        manager.department.append(dept_name)
        self._emp_repo.save_employee(manager)

        Logger.success(f"{dept_name} Department: created successfully", SUCCESS_LOG_FILE)
        print(f"{dept_name} Department created successfully")
        return department

    def assign_employee(self, current_user, dept_name: str, employee: Employee):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])

        department = self._dept_repo.get_dept_by_name(dept_name)
        if not department:
            raise NotFoundError(f"{dept_name} department not found")

        department.assign_employee(employee)
        self._dept_repo.save_department(department)

        employee.department.append(dept_name)
        self._emp_repo.save_employee(employee)

    def remove_employee(self, current_user, dept_name: str, employee: Employee):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])

        department = self._dept_repo.get_dept_by_name(dept_name)
        if not department:
            raise NotFoundError(f"{dept_name} department not found")

        department.remove_employee(employee)
        self._dept_repo.save_department(department)

        employee.department.remove(dept_name)
        self._emp_repo.save_employee(employee)

    def assign_a_new_department_manager(self, current_user, dept_name: str, manager: Employee):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])

        department = self._dept_repo.get_dept_by_name(dept_name)
        if not department:
            raise NotFoundError(f"{dept_name} department not found")
        print(department.manager.department)

        if manager.role.value != "Manager":
            manager.role = Role.MANAGER
            manager.department.clear()
            manager.department.append(dept_name)
            self._emp_repo.save_employee(manager)
            self._emp_repo.update_employee_database()

        department.manager = manager
        self._dept_repo.save_department(department)
    #     still working on this method-----

    def get_all_department(self, current_user):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])

        departments = self._dept_repo.get_all_department()
        print(departments)

    def get_all_department_managers(self, current_user):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        managers = self._dept_repo.get_dept_managers()
        print(managers)

    def delete_dept(self, current_user, dept_name: str):
        Authorization.authorized_roles(current_user, [Role.ADMIN])
        self._dept_repo.delete_dept_by_name(dept_name)

        for employee in self._emp_repo.get_all_employee().values():
            if dept_name in employee.department:
                employee.department.remove(dept_name)
        self._emp_repo.update_employee_database()

    def delete_all_dept(self, current_user):
        Authorization.authorized_roles(current_user, [Role.ADMIN])
        self._dept_repo.delete_all_department()

        for employee in self._emp_repo.get_all_employee().values():
            employee.department.clear()
        self._emp_repo.update_employee_database()

    def count_all_dept(self, current_user):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        print(self._dept_repo.count_dept())




