import json
from typing import Dict, List, Optional
from src.hr_saas.model.leave_request import LeaveRequest
from src.hr_saas.model.employee import Employee
from src.hr_saas.file_IO.logging import Logger
from src.hr_saas.file_IO.config_file import ERROR_LOG_FILE


class LeaveRepository:
    def __init__(self, storage_file):
        self._leave_storage_file = storage_file
        self._leave_database: Dict[str, Dict[str, LeaveRequest]] = {}
        self._load_leave_database()

    def get_all_leave_request(self):
        return self._leave_database

    def get_employee_requests_by_email(self, email: str) -> Dict[str, LeaveRequest]:
        return self._leave_database.get(email, {})

    def get_leave_balance(self, email: str) -> Optional[int]:
        if email not in self._leave_database:
            print("Employee has no previous leave_request")
            return None

        if not self._leave_database.get(email):
            print("Employee has no previous leave_request")
            return None

        total_leave_requested = 0
        total_available_leave_days = 0
        for requests in self._leave_database.get(email).values():
            total_available_leave_days = requests.total_leave_for_the_year
            if requests.leave_status.value == "Pending" or requests.leave_status.value == "Approved":
                total_leave_requested += requests.days

        balance = total_available_leave_days - total_leave_requested
        if balance == 0:
            raise ValueError("You have used up your leave for the year")

        return balance

    def save_leave_request(self, leave_request: LeaveRequest):
        email = leave_request.employee.email

        if email not in self._leave_database:
            self._leave_database[email] = {}

        # if leave_request.leave_id not in self._leave_database.get(email):
        self._leave_database[email][leave_request.leave_id] = leave_request

        # Serialization process
        return self._persist_to_disk()

    def _load_leave_database(self):
        self._leave_database.clear()

        if not self._leave_storage_file:
            return

        try:
            with open(self._leave_storage_file, mode="r", encoding="utf-8") as file_reader:
                data = json.load(file_reader)

                for email, requests_data in data.items():
                    self._leave_database[email] = {}
                    for leave_id, leave_obj in requests_data.items():
                        self._leave_database[email][leave_id] = LeaveRequest.from_to_dict(leave_obj)

        except FileNotFoundError as e:
            # First run - file does not exist yet
            Logger.error(f"Database file not found, starting fresh | {e}", ERROR_LOG_FILE)
            self._leave_database = {}
        except json.JSONDecodeError as e:
            # File exist but empty or corrupted
            Logger.error(f"Json Decode Error | {e}", ERROR_LOG_FILE)
            self._leave_database = {}
        except Exception as e:
            Logger.error(f"Error loading Leave_Request database | {e}", ERROR_LOG_FILE)
            self._leave_database = {}

    def _persist_to_disk(self):
        savable_data = {
            email: {
                leave_id: req.to_dict()
                for leave_id, req in requests.items()
            }

            for email, requests in self._leave_database.items()
        }

        try:
            with open(self._leave_storage_file, mode="w", encoding="utf-8") as file_writer:
                json.dump(savable_data, file_writer, indent=4)
            return True
        except Exception as e:
            Logger.error(f"Error saving leave_request | {e}", ERROR_LOG_FILE)
            return False
