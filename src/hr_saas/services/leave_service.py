from src.hr_saas.repository.leave_repo import LeaveRepository
from src.hr_saas.enums.leave import LeaveType
from src.hr_saas.enums.role import Role
from src.hr_saas.model.employee import Employee
from src.hr_saas.model.leave_request import LeaveRequest
from src.hr_saas.error_handling.exceptions import ValidationError
from src.hr_saas.file_IO.logging import Logger
from src.hr_saas.file_IO.config_file import SUCCESS_LOG_FILE


class LeaveService:
    def __init__(self, repo: LeaveRepository):
        self._leave_repo = repo

    def apply_for_leave(self, employee: Employee, days: int, leave_t: LeaveType):
        total_days_taken = 0

        if employee.email in self._leave_repo.get_all_leave_request():
            requests = self._leave_repo.get_employee_requests(employee.email)
            for request in requests:
                total_days_taken += request.days
            balance = requests[0].total_leave_for_the_year - total_days_taken
            if balance == 0:
                raise ValueError("You have used up your leave for the year")
        else:
            if employee.role in [Role.HR, Role.MANAGER]:
                balance = 30
            else:
                balance = 21

        if days > balance:
            raise ValidationError(f"You have {balance} leave request remaining for the year")

        leave_request = LeaveRequest(employee, days, leave_t)
        self._leave_repo.save_leave_request(leave_request)

        Logger.success(f"{employee.name} applied for {days} days of {leave_t}", SUCCESS_LOG_FILE)
        print("Leave application successful")

        return leave_request

    def approve_leave(self, ):
