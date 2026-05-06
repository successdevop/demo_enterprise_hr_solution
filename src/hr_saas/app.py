from datetime import datetime

from src.hr_saas.repository.employee_repo import EmployeeRepo
from src.hr_saas.repository.department_repo import DepartmentRepo
from src.hr_saas.repository.leave_repo import LeaveRepository
from src.hr_saas.repository.payroll_repo import PayrollRepository
from src.hr_saas.repository.attendance_repo import AttendanceRepository
from src.hr_saas.strategy.tax_strategy import NigerianTaxStrategy, Pension
from src.hr_saas.strategy.currency_converter import CurrencyStrategy
from src.hr_saas.services.employee_service import EmployeeService
from src.hr_saas.services.department_service import DepartmentService
from src.hr_saas.services.leave_service import LeaveService
from src.hr_saas.services.payroll_service import PayrollServices
from src.hr_saas.services.attendance_service import AttendanceService
from src.hr_saas.auth.auth import Auth
from src.hr_saas.enums.role import Role
from src.hr_saas.enums.month import Month
from src.hr_saas.enums.week import WeekDay
from src.hr_saas.enums.employee_type import EmployeeType
from src.hr_saas.enums.leave import LeaveType, LeaveStatus
from src.hr_saas.file_IO.database_files import (EMPLOYEE_DATABASE, DEPARTMENT_DATABASE, LEAVE_REQUEST_DATABASE,
                                                PAYROLL_DATABASE, ATTENDANCE_DATABASE)
from src.hr_saas.app_files.department_names import ENGINEERING


def main():
    emp_repo = EmployeeRepo(EMPLOYEE_DATABASE)
    # dept_repo = DepartmentRepo(DEPARTMENT_DATABASE)
    leave_repo = LeaveRepository(LEAVE_REQUEST_DATABASE)
    # payroll_repo = PayrollRepository(PAYROLL_DATABASE)
    # attendance_repo = AttendanceRepository(ATTENDANCE_DATABASE)
    # tax_strategy = NigerianTaxStrategy()
    # pension = Pension()
    # currency_converter = CurrencyStrategy()

    # emp_service = EmployeeService(emp_repo)
    # dept_service = DepartmentService(dept_repo, emp_repo)
    leave_service = LeaveService(leave_repo)
    # payroll_service = PayrollServices(payroll_repo, currency_converter, tax_strategy, pension)
    # attendance_service = AttendanceService(attendance_repo)
    auth = Auth(emp_repo)

    auth.login("succeSs@gmail.com", "mynewpassword123@/.com")
    # auth.login("john.doe@company.com", "JohnDoe2024#Secure")
    # auth.login("victor.ndukwe@company.com", "VicNduk@Manager1")
    # auth.login("esther.adeleke@company.com", "EstherAdeleke@Dev#1")

    # ======== DEPARTMENT SERVICE ========
    # dept_service.create_department(auth.get_current_user(), ENGINEERING, emp_repo.get_employee_by_email("esther.adeleke@company.com"))
    # dept_service.assign_employee(auth.get_current_user(), ENGINEERING, emp_repo.get_employee_by_email("femi.adeyemi@company.com"))
    # # dept_service.remove_employee(auth.get_current_user(), ENGINEERING, emp_repo.get_employee_by_email("esther.adeleke@company.com"))
    #
    # dept_service.create_department(auth.get_current_user(), "Sales", emp_repo.get_employee_by_email("victor.ndukwe@company.com"))
    # dept_service.assign_employee(auth.get_current_user(), "Sales", emp_repo.get_employee_by_email("linda.brown@company.com"))
    # # dept_service.remove_employee(auth.get_current_user(), "Sales", emp_repo.get_employee_by_email("linda.brown@company.com"))
    #
    # dept_service.create_department(auth.get_current_user(), "TECH", emp_repo.get_employee_by_email("adamu.ibrahim@company.com"))
    # dept_service.assign_employee(auth.get_current_user(), "TECH", emp_repo.get_employee_by_email("precious.eze@company.com"))
    # # dept_service.remove_employee(auth.get_current_user(), "TECH", emp_repo.get_employee_by_email("precious.eze@company.com"))

    # department = dept_service.assign_a_new_department_manager(auth.get_current_user(), ENGINEERING, emp_repo.get_employee_by_email("sarah.williams@company.com"))
    # print(department)

    # all_dept = dept_service.get_all_department(auth.get_current_user())
    # print(all_dept)

    # all_dept = dept_service.get_all_department_managers(auth.get_current_user())
    # print(all_dept)

    # number = dept_service.count_all_dept(auth.get_current_user())
    # print(number)

    # dept_service.delete_dept(auth.get_current_user(), ENGINEERING)

    # dept_service.delete_all_dept(auth.get_current_user())

    # ======== LEAVE SERVICE ========
    full_time_1 = emp_repo.get_employee_by_email("esther.adeleke@company.com")
    full_time_2 = emp_repo.get_employee_by_email("victor.ndukwe@company.com")
    full_time_3 = emp_repo.get_employee_by_email("adamu.ibrahim@company.com")

    contract = emp_repo.get_employee_by_email("femi.adeyemi@company.com")
    contract_1 = emp_repo.get_employee_by_email("linda.brown@company.com")
    contract_2 = emp_repo.get_employee_by_email("precious.eze@company.com")

    # leave_1 = leave_service.apply_for_leave(full_time_1, 25, LeaveType.ANNUAL)
    # print(leave_1)
    # leave_1 = leave_service.apply_for_leave(full_time_2, 22, LeaveType.UNPAID)
    # print(leave_1)
    # leave_1 = leave_service.apply_for_leave(full_time_3, 19, LeaveType.SICK)
    # print(leave_1)
    # leave_2 = leave_service.apply_for_leave(contract, 14, LeaveType.ANNUAL)
    # print(leave_2)
    # leave_2 = leave_service.apply_for_leave(contract_1, 11, LeaveType.MATERNITY)
    # print(leave_2)
    # leave_2 = leave_service.apply_for_leave(contract_2, 8, LeaveType.EMERGENCY)
    # print(leave_2)

    # leave_service.approve_leave(auth.get_current_user(), full_time_1, "8777")
    # leave_service.approve_leave(auth.get_current_user(), contract, "8182")
    # leave_service.approve_leave(auth.get_current_user(), full_time_2, "1585")
    # leave_service.approve_leave(auth.get_current_user(), contract_1, "4258")
    #
    # leave_service.reject_leave(auth.get_current_user(), contract_1, "4258")
    # leave_service.reject_leave(auth.get_current_user(), full_time_2, "1585")
    #
    # output = leave_service.get_all_leave_by_status(auth.get_current_user(), LeaveStatus.REJECTED)
    # print(output)
    #
    # output = leave_service.get_all_employee_leave(auth.get_current_user(), full_time_1)
    # print(output)
    # leave_service.get_all_employee_leave(auth.get_current_user(), contract)
    #
    # out = leave_service.get_employee_leave_balance(auth.get_current_user(), full_time_1)
    # print(out)
    # leave_service.get_employee_leave_balance(auth.get_current_user(), contract)
    #
    leave_service.delete_all_leave_request(auth.get_current_user())


if __name__ == "__main__":
    main()
    # print(datetime.now().date())
    # t = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S").date()
    # print(t)
    # today = datetime.now().date().year
    # dob = "21/06/1992"
    # age = datetime.now().strptime(dob, "%d/%m/%Y").date().year
    # age_cla = today - age
    # print(today)
    # print(dob)
    # print(age)
    # print()
    # print(age_cla)

    # employee_1 = auth.register_user(
    #     first_name="succeSS ifeANYi",
    #     last_name="RaPHAel",
    #     dob="21/06/1990",
    #     email="succeSs@gmail.com",
    #     origin="imo state, nigeria",
    #     role=Role.ADMIN,
    #     salary=100000,
    #     password="mynewpassword123@/.com"
    # )
    #
    # employee_2 = auth.register_user(
    #     first_name="JOhN",
    #     last_name="DOE",
    #     dob="15/03/1985",
    #     email="john.doe@company.com",
    #     origin="lagos state, nigeria",
    #     role=Role.HR,
    #     salary=65000,
    #     password="JohnDoe2024#Secure"
    # )
    #
    # employee_3 = auth.register_user(
    #     first_name="jAnE",
    #     last_name="sMiTh",
    #     dob="22/11/1992",
    #     email="jane.smith@company.com",
    #     origin="abuja, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=75000,
    #     password="JaneSmith@789Tech"
    # )
    #
    # employee_4 = auth.register_user(
    #     first_name="MICHAEL",
    #     last_name="JOHNSON",
    #     dob="03/08/1988",
    #     email="michael.j@company.com",
    #     origin="rivers state, nigeria",
    #     role=Role.MANAGER,
    #     salary=90000,
    #     password="MikeJ2024!Pass"
    # )
    #
    # employee_5 = auth.register_user(
    #     first_name="sarah",
    #     last_name="williams",
    #     dob="17/12/1995",
    #     email="sarah.williams@company.com",
    #     origin="kano state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=55000,
    #     password="SarahW@123Dev"
    # )
    #
    # employee_6 = auth.register_user(
    #     first_name="CHIEF",
    #     last_name="OKONKWO",
    #     dob="09/04/1980",
    #     email="chief.okonkwo@company.com",
    #     origin="anambra state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=20000,
    #     password="ChiefOkon@2024#"
    # )
    #
    # employee_7 = auth.register_user(
    #     first_name="abiGail",
    #     last_name="mba",
    #     dob="30/09/1998",
    #     email="abigail.mba@company.com",
    #     origin="enugu state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=48000,
    #     password="AbbyMba!Design987"
    # )
    #
    # employee_8 = auth.register_user(
    #     first_name="OLUWAFEMI",
    #     last_name="ADEYEMI",
    #     dob="12/06/1991",
    #     email="femi.adeyemi@company.com",
    #     origin="oyo state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=82000,
    #     password="FemiAde@2024Secure"
    # )
    #
    # employee_9 = auth.register_user(
    #     first_name="grace",
    #     last_name="okoro",
    #     dob="25/02/1993",
    #     email="grace.okoro@company.com",
    #     origin="delta state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=58000,
    #     password="GraceOkoro#HR2024"
    # )
    #
    # employee_10 = auth.register_user(
    #     first_name="VICTOR",
    #     last_name="NDUKWE",
    #     dob="07/10/1987",
    #     email="victor.ndukwe@company.com",
    #     origin="imo state, nigeria",
    #     role=Role.MANAGER,
    #     salary=95000,
    #     password="VicNduk@Manager1"
    # )
    #
    # employee_11 = auth.register_user(
    #     first_name="linda",
    #     last_name="brown",
    #     dob="18/07/1996",
    #     email="linda.brown@company.com",
    #     origin="cross river state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=62000,
    #     password="LindaBrownDev#2024"
    # )
    #
    # employee_12 = auth.register_user(
    #     first_name="ADAMU",
    #     last_name="IBRAHIM",
    #     dob="14/05/1983",
    #     email="adamu.ibrahim@company.com",
    #     origin="kaduna state, nigeria",
    #     role=Role.MANAGER,
    #     salary=90000,
    #     password="AdamIbrahim@Admin2024"
    # )
    #
    # employee_13 = auth.register_user(
    #     first_name="pReCiOuS",
    #     last_name="eZE",
    #     dob="01/01/2000",
    #     email="precious.eze@company.com",
    #     origin="abia state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=46000,
    #     password="PreciousEze!2000"
    # )
    #
    # employee_14 = auth.register_user(
    #     first_name="TOBILOBA",
    #     last_name="AKINDELE",
    #     dob="29/08/1994",
    #     email="tobi.akindele@company.com",
    #     origin="ogun state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=78000,
    #     password="TobiAkindele@789Tech"
    # )
    #
    # employee_15 = auth.register_user(
    #     first_name="faith",
    #     last_name="oseni",
    #     dob="11/11/1989",
    #     email="faith.oseni@company.com",
    #     origin="kwara state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=54000,
    #     password="FaithOseni#HR2024"
    # )
    #
    # employee_16 = auth.register_user(
    #     first_name="CHUKWUEBUKA",
    #     last_name="OKAFOR",
    #     dob="23/03/1986",
    #     email="ebuka.okafor@company.com",
    #     origin="anambra state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=102000,
    #     password="EbukaOkafor@Manager#1"
    # )
    #
    # employee_17 = auth.register_user(
    #     first_name="amara",
    #     last_name="okonkwo",
    #     dob="05/06/1997",
    #     email="amara.okonkwo@company.com",
    #     origin="enugu state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=59000,
    #     password="AmaraOkonkwo@Dev2024"
    # )
    #
    # employee_18 = auth.register_user(
    #     first_name="SULEIMAN",
    #     last_name="ABBA",
    #     dob="19/09/1982",
    #     email="suleiman.abba@company.com",
    #     origin="borno state, nigeria",
    #     role=Role.MANAGER,
    #     salary=105000,
    #     password="SuleimanAbba@Admin#1"
    # )
    #
    # employee_19 = auth.register_user(
    #     first_name="ifeoma",
    #     last_name="nwosu",
    #     dob="27/04/1999",
    #     email="ifeoma.nwosu@company.com",
    #     origin="imo state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=52000,
    #     password="IfeomaNwosu@Design99"
    # )
    #
    # employee_20 = auth.register_user(
    #     first_name="AYOMIDE",
    #     last_name="BALOGUN",
    #     dob="13/12/1990",
    #     email="ayo.balogun@company.com",
    #     origin="lagos state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=85000,
    #     password="AyomideBalo@Engineer1"
    # )
    #
    # employee_21 = auth.register_user(
    #     first_name="ngozi",
    #     last_name="uche",
    #     dob="31/07/1994",
    #     email="ngozi.uche@company.com",
    #     origin="rivers state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=61000,
    #     password="NgoziUche@HR2024"
    # )
    #
    # employee_22 = auth.register_user(
    #     first_name="IBRAHEEM",
    #     last_name="YUSUF",
    #     dob="08/01/1988",
    #     email="ibraheem.yusuf@company.com",
    #     origin="kogi state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=98000,
    #     password="IbraheemYusuf@Manager1"
    # )
    #
    # employee_23 = auth.register_user(
    #     first_name="esther",
    #     last_name="adeleke",
    #     dob="24/10/1993",
    #     email="esther.adeleke@company.com",
    #     origin="osun state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=64000,
    #     password="EstherAdeleke@Dev#1"
    # )
    #
    # employee_24 = auth.register_user(
    #     first_name="GODSWILL",
    #     last_name="AKPAN",
    #     dob="16/02/1985",
    #     email="godswill.akpan@company.com",
    #     origin="akwa ibom state, nigeria",
    #     role=Role.MANAGER,
    #     salary=115000,
    #     password="GodswillAkpan@Admin#2024"
    # )
    #
    # employee_25 = auth.register_user(
    #     first_name="zainab",
    #     last_name="muhammad",
    #     dob="02/08/1996",
    #     email="zainab.muhammad@company.com",
    #     origin="niger state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=50000,
    #     password="ZainabM@Design2024"
    # )

