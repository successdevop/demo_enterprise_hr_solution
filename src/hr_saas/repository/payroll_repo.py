import json
from typing import Dict, List, Optional
from src.hr_saas.model.payroll import Payslip
from src.hr_saas.file_IO.logging import Logger
from src.hr_saas.file_IO.config_file import ERROR_LOG_FILE


class PayrollRepository:
    def __init__(self, payslip_storage_file):
        self._payroll_storage_file = payslip_storage_file
        self._payroll_database: Dict[str, List[Payslip]] = {}
        self._load_payslip_database()

    def save_payslip(self, payslip: Payslip):
        month = payslip.month.value

        if month not in self._payroll_database:
            self._payroll_database[month] = []

        self._payroll_database[month].append(payslip)
        return self._persist_to_disk()

    def get_employee_payslip(self, email: str, month: str) -> Optional[Payslip]:
        if month not in self._payroll_database:
            print(f"Payslips for the month of {month} not yet processed")
            return None

        for payslip in self._payroll_database[month]:
            if payslip.employee.email == email:
                print(f"Employee payslip for the month of {month} already processed")
                return payslip

        print(f"Employee has no payslip for the month of {month}")
        return None

    def get_payslip_for_each_month(self, month: str):
        if month not in self._payroll_database:
            print(f"Payslips for the month of {month} not yet processed")
            return
        return self._payroll_database.get(month)

    def _persist_to_disk(self):
        savable_data = {
            month: [slips.to_dict() for slips in payslip_data]
            for month, payslip_data in self._payroll_database.items()
        }

        try:
            with open(self._payroll_storage_file, mode="w", encoding="utf-8") as file_writer:
                json.dump(savable_data, file_writer, indent=4)
                return True
        except Exception as e:
            Logger.error(f"Error saving Payslip | {e}", ERROR_LOG_FILE)
            return False

    def _load_payslip_database(self):
        self._payroll_database.clear()

        if not self._payroll_storage_file:
            print("JSON file not present")
            return

        try:
            with open(self._payroll_storage_file, mode="r", encoding="utf-8") as file_reader:
                data = json.load(file_reader)

                if not isinstance(data, dict):
                    print(f"Invalid data format in {self._payroll_storage_file}")
                    return

                self._payroll_database = {
                    month: [Payslip.from_to_dict(payslip_data.to_dict()) for payslip_data in payslips]

                    for month, payslips in self._payroll_database.items()
                    if isinstance(payslips, list)
                }

        except FileNotFoundError as e:
            # First run - file does not exist yet
            Logger.error(f"Database file does not exist, starting fresh | {e}", ERROR_LOG_FILE)
        except json.JSONDecodeError as e:
            # File exist but empty or corrupted
            Logger.error(f"Json Decode Error | {e}", ERROR_LOG_FILE)
        except Exception as e:
            Logger.error(f"Error loading Payroll Database | {e}", ERROR_LOG_FILE)
