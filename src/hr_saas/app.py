from datetime import datetime

from src.hr_saas.repository.employee_repo import EmployeeRepo
from src.hr_saas.repository.department_repo import DepartmentRepo
from src.hr_saas.repository.leave_repo import LeaveRepository
from src.hr_saas.repository.payroll_repo import PayrollRepository
from src.hr_saas.repository.attendance_repo import AttendanceRepository
from src.hr_saas.strategy.tax_strategy import NigerianTaxStrategy, Pension
from src.hr_saas.strategy.currency_converter import CurrencyStrategy
from src.hr_saas.services.department_service import DepartmentService
from src.hr_saas.services.leave_service import LeaveService
from src.hr_saas.services.payroll_service import PayrollServices
from src.hr_saas.services.attendance_service import AttendanceService
from src.hr_saas.auth.auth import Auth
from src.hr_saas.enums.role import Role
from src.hr_saas.enums.month import Month
from src.hr_saas.enums.week import WeekDay
from src.hr_saas.enums.leave import LeaveType, LeaveStatus
from src.hr_saas.file_IO.database_files import (EMPLOYEE_DATABASE, DEPARTMENT_DATABASE, LEAVE_REQUEST_DATABASE,
                                                PAYROLL_DATABASE, ATTENDANCE_DATABASE)
from src.hr_saas.app_files.files import ENGINEERING


def main():
    emp_repo = EmployeeRepo(EMPLOYEE_DATABASE)
    dept_repo = DepartmentRepo(DEPARTMENT_DATABASE)
    leave_repo = LeaveRepository(LEAVE_REQUEST_DATABASE)
    payroll_repo = PayrollRepository(PAYROLL_DATABASE)
    attendance_repo = AttendanceRepository(ATTENDANCE_DATABASE)
    tax_strategy = NigerianTaxStrategy()
    pension = Pension()
    currency_converter = CurrencyStrategy()

    dept_service = DepartmentService(dept_repo, emp_repo)
    leave_service = LeaveService(leave_repo)
    payroll_service = PayrollServices(payroll_repo, currency_converter, tax_strategy, pension)
    attendance_service = AttendanceService(attendance_repo)
    auth = Auth(emp_repo)

    # auth.login("success@gmail.com", "mynewpassword123@/.com")
    # auth.login("adewusi@gmail.com", "obyadew123@/.com")
    auth.login("umah@gmail.com", "eoluch123@/.com")

    # attendance_service.clock_in(emp_repo.get_employee_by_email("obiageli@gmail.com"), WeekDay.MONDAY)
    # attendance_service.clock_in(emp_repo.get_employee_by_email("francis@gmail.com"), WeekDay.TUESDAY)
    attendance_service.clock_out(emp_repo.get_employee_by_email("obiageli@gmail.com"))

    # payslip = payroll_service.get_all_payslips(auth.get_current_user())
    # print(payslip)
    # payslip = payroll_service.process_salary(auth.get_current_user(), emp_repo.get_employee_by_email("obiageli@gmail.com"),
    #                                          Month.JANUARY, "USD", 0, 0)
    # print(payslip)
    # payslip = payroll_service.process_salary(auth.get_current_user(), emp_repo.get_employee_by_email("francis@gmail.com"),
    #                                          Month.FEBRUARY, "GBP", 200, 179)
    # print(payslip)
    # payslip_1 = payroll_service.delete_payslip(auth.get_current_user(), Month.JANUARY, '23951')
    # print(payslip_1)
    # payslip_1 = payroll_service.get_payslip_for_each_month(auth.get_current_user(), Month.JANUARY)
    # print(payslip_1)
    # payslip_1 = payroll_service.get_employee_payslip(auth.get_current_user(), emp_repo.get_employee_by_email("obiageli@gmail.com"),
    #                                                  Month.JANUARY)
    # print(payslip_1)
    #
    # payslip_1 = payroll_service.get_employee_payslip(auth.get_current_user(), emp_repo.get_employee_by_email("francis@gmail.com"),
    #                                                  Month.JANUARY)
    # print(payslip_1)
    # leave1 = leave_service.apply_for_leave(emp_repo.get_employee_by_email("obiageli@gmail.com"), 5, LeaveType.UNPAID)
    # leave2 = leave_service.apply_for_leave(emp_repo.get_employee_by_email("obiageli@gmail.com"), 10, LeaveType.ANNUAL)
    # leave3 = leave_service.apply_for_leave(emp_repo.get_employee_by_email("francis@gmail.com"), 9, LeaveType.ANNUAL)
    # leave4 = leave_service.apply_for_leave(emp_repo.get_employee_by_email("francis@gmail.com"), 9, LeaveType.ANNUAL)
    # leave4 = leave_service.apply_for_leave(emp_repo.get_employee_by_email("francis@gmail.com"), 11, LeaveType.ANNUAL)
    # leave_service.approve_leave(auth.get_current_user(), "francis@gmail.com", "4955")
    # leave_service.reject_leave(auth.get_current_user(), "francis@gmail.com", "8115")
    # leave_service.reject_leave(auth.get_current_user(), "obiageli@gmail.com", "0554")
    # dept_service.get_all_department(auth.get_current_user())
    # dept_service.get_all_department_managers(auth.get_current_user())
    # dept_service.delete_dept(auth.get_current_user(), ENGINEERING)
    # dept_service.delete_all_dept(auth.get_current_user())
    # dept_service.assign_a_new_department_manager(auth.get_current_user(), ENGINEERING,
    #                                              emp_repo.get_employee_by_email("francis@gmail.com"))

    # dept_service.create_department(auth.get_current_user(), ENGINEERING,
    #                                emp_repo.get_employee_by_email("adewusi@gmail.com"))
    #
    # dept_service.assign_employee(auth.get_current_user(), ENGINEERING,
    #                                emp_repo.get_employee_by_email("francis@gmail.com"))

    # dept_service.remove_employee(auth.get_current_user(), ENGINEERING,
    #                                emp_repo.get_employee_by_email("francis@gmail.com"))

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
    # employee_2 = auth.register_user(
    #     name="oluchi favour",
    #     email="umah@gmail.com",
    #     age=34,
    #     origin="ebonyi state, nigeria",
    #     role=Role.HR,
    #     salary=30000,
    #     password="eoluch123@/.com"
    # )
    #
    # employee_3 = auth.register_user(
    #     name="Obi joy",
    #     email="obiageli@gmail.com",
    #     age=28,
    #     origin="ebonyi state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=10000,
    #     password="obyski123@/.com"
    # )

    # employee_3 = auth.register_user(
    #     name="adewusi tobi",
    #     email="adewusi@gmail.com",
    #     age=28,
    #     origin="osun state, nigeria",
    #     role=Role.MANAGER,
    #     salary=10000,
    #     password="obyadew123@/.com"
    # )
    #
    # employee_3 = auth.register_user(
    #     name="francis ebinabo",
    #     email="francis@gmail.com",
    #     age=32,
    #     origin="kogi state, nigeria",
    #     role=Role.EMPLOYEE,
    #     salary=10000,
    #     password="obyskfranco@/.com"
    # )

    # employee_3 = auth.register_user(
    #     name="oladimeji folakemi",
    #     email="folakemi.ola@gmail.com",
    #     age=24,
    #     origin="ekiti state, nigeria",
    #     role=Role.MANAGER,
    #     salary=15000,
    #     password="kemzyolas123@/.com"
    # )


if __name__ == "__main__":
    main()
    # print(datetime.now().date())
    # t = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S").date()
    # print(t)
