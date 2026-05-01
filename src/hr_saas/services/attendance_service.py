from datetime import datetime, time
from src.hr_saas.repository.attendance_repo import AttendanceRepository
from src.hr_saas.model.employee import Employee
from src.hr_saas.model.attendance import Attendance
from src.hr_saas.enums.week import WeekDay
from src.hr_saas.enums.role import Role
from src.hr_saas.error_handling.exceptions import UserAlreadyExistError, ValidationError
from src.hr_saas.file_IO.logging import Logger
from src.hr_saas.file_IO.config_file import SUCCESS_LOG_FILE
from src.hr_saas.auth.authorization import Authorization


class AttendanceService:
    def __init__(self, attendance_repo: AttendanceRepository):
        self._attendance_repo = attendance_repo
        self._work_start_time = time(9, 0)
        self._work_end_time = time(17, 0)

    def clock_in(self, current_user: Employee, day: WeekDay):
        attendance = self._attendance_repo.get_employee_today_attendance(current_user)
        if attendance:
            raise UserAlreadyExistError("Already clocked in")

        attendance = Attendance(employee=current_user, day_of_the_week=day)
        attendance.check_in()

        self._attendance_repo.save_attendance(attendance)
        Logger.success(f"{current_user.name} just clocked in", SUCCESS_LOG_FILE)

        return attendance

    def clock_out(self, current_user: Employee):
        attendance = self._attendance_repo.get_employee_today_attendance(current_user)
        if not attendance:
            raise ValidationError("No check-in record found")

        attendance.check_out()
        self._attendance_repo.save_attendance(attendance)
        Logger.success(f"{current_user.name} just clocked out", SUCCESS_LOG_FILE)
        return attendance

    def is_late(self, current_user: Employee, attendance: Attendance) -> bool:
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        return datetime.now().strptime(attendance.clocked_in,
                                       "%Y-%m-%d %H:%M:%S").time() > self._work_start_time

    def calculate_overtime(self, current_user: Employee, attendance: Attendance) -> float:
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        if not attendance.clocked_out:
            return 0

        overtime = datetime.now().strptime(attendance.clocked_out,
                                           "%Y-%m-%d %H:%M:%S").time() > self._work_end_time

        if overtime:
            extra_hours = attendance.total_hours_worked_per_day - 8
            return max(extra_hours, 0)
        return 0

    def get_all_employee_attendance(self, current_user: Employee, employee: Employee):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        attendance = self._attendance_repo.get_employee_attendance(employee)
        return attendance

    def get_employee_today_attendance(self, current_user: Employee, employee: Employee):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        attendance = self._attendance_repo.get_employee_today_attendance(employee)
        return attendance

    def get_all_attendance(self, current_user: Employee):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        attendance = self._attendance_repo.get_all_attendance()
        return attendance

    def get_all_today_attendance(self, current_user: Employee):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        attendance = self._attendance_repo.get_all_today_attendance()
        return attendance




