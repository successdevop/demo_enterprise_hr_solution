import json
from typing import Dict, List, Optional
from datetime import datetime
from src.hr_saas.model.attendance import Attendance
from src.hr_saas.model.employee import Employee
from src.hr_saas.file_IO.logging import Logger
from src.hr_saas.file_IO.config_file import ERROR_LOG_FILE


class AttendanceRepository:
    def __init__(self, storage_file: str):
        self._attendance_storage_file = storage_file
        self._attendance_database: Dict[str, List[Attendance]] = {}
        self._load_attendance_database()

    def get_employee_today_attendance(self, employee: Employee) -> Optional[Attendance]:
        attendance_history = self._attendance_database.get(employee.email, [])
        for attendance in attendance_history:
            if datetime.strptime(attendance.date, "%Y-%m-%d %H:%M:%S").date() == datetime.now().date():
                return attendance
        return None

    def get_employee_attendance(self, employee: Employee) -> List[Attendance]:
        return self._attendance_database.get(employee.email, [])

    def get_all_today_attendance(self) -> List[Attendance]:
        today_attendance = []
        for attendance in self._attendance_database.values():
            today_attendance.extend(attendance)

        today_attendance[:] = [attend for attend in today_attendance if attend.date.today() == datetime.today()]
        return today_attendance

    def save_attendance(self, attendance: Attendance):
        email = attendance.employee.email
        if email not in self._attendance_database:
            self._attendance_database[attendance.employee.email] = []

        new_attendance = next((other_attendance for other_attendance in self._attendance_database[email]
                               if AttendanceRepository._compare_string_time(other_attendance.date, attendance.date)),
                              None)

        if not new_attendance:
            self._attendance_database.get(email).append(attendance)

        return self._save_to_disk()

    def _save_to_disk(self):
        savable_data = {
            email: [attendance.to_dict() for attendance in attendance_list]
            for email, attendance_list in self._attendance_database.items()
        }

        try:
            with open(self._attendance_storage_file, mode="w", encoding="utf-8") as file_writer:
                json.dump(savable_data, file_writer, indent=4)
                return True
        except Exception as e:
            Logger.error(f"Error saving Attendance data | {e}", ERROR_LOG_FILE)
            return False

    @classmethod
    def _compare_string_time(cls, time_1: str, time_2) -> bool:
        from datetime import datetime
        return (datetime.now().strptime(time_1, "%Y-%m-%d %H:%M:%S") == datetime.now()
                .strptime(time_2, "%Y-%m-%d %H:%M:%S"))

    def _load_attendance_database(self):
        self._attendance_database.clear()

        if not self._attendance_storage_file:
            print("Attendance json file not found")
            return

        try:
            with open(self._attendance_storage_file, mode="r", encoding="utf-8") as file_reader:
                data = json.load(file_reader)

                if isinstance(data, dict):
                    for email, attendance_data in data.items():
                        self._attendance_database[email] = [
                            Attendance.from_to_dict(attendance) for attendance in attendance_data
                        ]
        except FileNotFoundError as e:
            # First run - database file doesn't exist
            Logger.error(f"Database file does not exist yet, starting fresh | {e}", ERROR_LOG_FILE)
        except json.JSONDecodeError as e:
            # Database file exists but either empty or corrupted
            Logger.error(f"JSON Decode Error | {e}", ERROR_LOG_FILE)
        except Exception as e:
            Logger.error(f"Error loading attendance_database | {e}", ERROR_LOG_FILE)