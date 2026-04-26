from src.hr_saas.repository.employee_repo import EmployeeRepo
from src.hr_saas.auth.auth import Auth
from src.hr_saas.enums.role import Role
from src.hr_saas.file_IO.database_files import EMPLOYEE_DATABASE


def main():
    emp_repo = EmployeeRepo(EMPLOYEE_DATABASE)
    auth = Auth(emp_repo)

    # auth.login("success@gmail.com", "mynewpassword123@/.com")
    # auth.forgot_password("success@gmail.com")

    # employee_1 = auth.register_user(
    #     name="succeSS ifeANYi raPHaEl",
    #     email="success@gmail.com",
    #     age=30,
    #     origin="imo state, nigeria",
    #     role=Role.ADMIN,
    #     salary=50000,
    #     password="ehez123@/.com|mynewpassword123@/.com"
    # )
    #
    # employee_1 = auth.register_user(
    #     name="oluchi favour",
    #     email="umah@gmail.com",
    #     age=34,
    #     origin="ebonyi state, nigeria",
    #     role=Role.HR,
    #     salary=30000,
    #     password="eoluch123@/.com"
    # )
    #
    # employee_1 = auth.register_user(
    #     name="Obi joy",
    #     email="obiageli@gmail.com",
    #     age=28,
    #     origin="ebonyi state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=10000,
    #     password="obyski123@/.com"
    # )


if __name__ == "__main__":
    main()
