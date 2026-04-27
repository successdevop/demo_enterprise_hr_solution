import json
from typing import Dict, List
from src.hr_saas.model.leave_request import LeaveRequest
from src.hr_saas.file_IO.logging import Logger
from src.hr_saas.file_IO.config_file import ERROR_LOG_FILE


class LeaveRepository:
    def __init__(self, storage_file):
        self._leave_storage_file = storage_file
        self._leave_database: Dict[str, List[LeaveRequest]] = {}
        self._load_leave_database()

    def _load_leave_database(self):
        self._leave_database.clear()

        try:
            with open(self._leave_storage_file, mode="r", encoding="utf-8") as file_reader:
                data = json.load(file_reader)
                print(data)
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
