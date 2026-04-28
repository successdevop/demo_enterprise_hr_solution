from src.hr_saas.repository.leave_repo import LeaveRepository
from src.hr_saas.auth.authorization import Authorization
from src.hr_saas.enums.leave import LeaveType
from src.hr_saas.enums.role import Role
from src.hr_saas.model.employee import Employee
from src.hr_saas.model.leave_request import LeaveRequest
from src.hr_saas.error_handling.exceptions import ValidationError, AuthorizationError
from src.hr_saas.file_IO.logging import Logger
from src.hr_saas.file_IO.config_file import SUCCESS_LOG_FILE, INFO_LOG_FILE


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

    def approve_leave(self, current_user, leave: LeaveRequest):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR, Role.ADMIN])

        if current_user.role == Role.ADMIN:
            leave.approved_by.append(current_user)
            leave.approve_leave(current_user)
            Logger.success("Leave fully approved ✅", SUCCESS_LOG_FILE)
        else:
            if leave.approval_stage == 1:
                if current_user.role != Role.MANAGER:
                    raise AuthorizationError("Only Manager or Admin can approve at stage 1")

                if not set(leave.employee.department).intersection(current_user.department):
                    raise AuthorizationError("Not your team member. You can only approve your team member's leave")

                leave.approved_by.append(current_user)
                leave.approval_stage = 2
                Logger.info("Approved by Manager → moving to HR", INFO_LOG_FILE)

            elif leave.approval_stage == 2:
                if current_user != Role.HR:
                    raise AuthorizationError("Only HR or Admin can finalize approval")

                leave.approved_by.append(current_user)
                leave.approve_leave(current_user)
                Logger.info("Leave fully approved ✅", SUCCESS_LOG_FILE)




