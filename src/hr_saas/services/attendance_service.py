from datetime import datetime, time
from src.hr_saas.repository.attendance_repo import AttendanceRepository
from src.hr_saas.model.employee import Employee
from src.hr_saas.model.attendance import Attendance
from src.hr_saas.error_handling.exceptions import UserAlreadyExistError
from src.hr_saas.file_IO.logging import Logger
from src.hr_saas.file_IO.config_file import SUCCESS_LOG_FILE


class AttendanceService:
    def __init__(self, attendance_repo: AttendanceRepository):
        self._attendance_repo = attendance_repo
        self._work_start_time = time(9, 0)
        self._work_end_time = time(17, 0)

    def clock_in(self, current_user: Employee):
        attendance = self._attendance_repo.get_employee_today_attendance(current_user)
        if attendance:
            raise UserAlreadyExistError("Already clocked in")

        attendance = Attendance(employee=current_user)
        attendance.clock_in()

        self._attendance_repo.save_attendance(attendance)
        Logger.success(f"{current_user.name} just clocked in", SUCCESS_LOG_FILE)

        return attendance

