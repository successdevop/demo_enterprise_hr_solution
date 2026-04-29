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
        leave_balance = self._leave_repo.get_leave_balance(employee.email)

        if not leave_balance:
            if employee.role in [Role.ADMIN, Role.HR]:
                leave_balance = 30
            else:
                leave_balance = 21

        if days > leave_balance:
            raise ValidationError(f"You have {leave_balance} leave request remaining for the year")

        leave_request = LeaveRequest(employee, days, leave_t)
        self._leave_repo.save_leave_request(leave_request)

        Logger.success(f"{employee.name} applied for {days} days of {leave_t}", SUCCESS_LOG_FILE)
        print("Leave application successful")

        return leave_request

    def approve_leave(self, current_user, emp_email: str, leave_id: str):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR, Role.MANAGER])

        if emp_email not in self._leave_repo.get_all_leave_request():
            print("Email not found")
            return
        if not self._leave_repo.get_employee_requests_by_email(emp_email):
            print("No Leave Request found")
            return

        # Get the leave request
        leave = self._leave_repo.get_employee_requests_by_email(emp_email).get(leave_id)
        if not leave:
            print(f"Leave_Request with id {leave_id} not found")
            return

        if current_user.role == Role.ADMIN:
            leave.approve_leave(current_user)
            leave.approval_stage = 2
            self._leave_repo.save_leave_request(leave)
            Logger.success("Leave fully approved ✅", SUCCESS_LOG_FILE)

        else:
            if leave.approval_stage == 1:
                if current_user.role != Role.MANAGER:
                    raise AuthorizationError("Only Manager or Admin can approve at stage 1")

                if not set(leave.employee.department).intersection(current_user.department):
                    raise AuthorizationError("Not your team member. You can only approve your team member's leave")

                leave.approved_by.append({"name": current_user.name, "role": current_user.role.value})
                leave.approval_stage = 2
                self._leave_repo.save_leave_request(leave)
                Logger.info("Approved by Manager → moving to HR", INFO_LOG_FILE)

            elif leave.approval_stage == 2:
                if current_user.role != Role.HR:
                    raise AuthorizationError("Only HR or Admin can finalize approval")

                leave.approve_leave(current_user)
                self._leave_repo.save_leave_request(leave)
                Logger.info("Leave fully approved ✅", SUCCESS_LOG_FILE)

    def reject_leave(self, current_user, emp_email, leave_id: str):
        Authorization.authorized_roles(current_user, [Role.MANAGER, Role.HR, Role.ADMIN])
        # Get the leave request
        leave = self._leave_repo.get_employee_requests_by_email(emp_email).get(leave_id)
        if not leave:
            print(f"Leave_Request with id {leave_id} not found")
            return

        if current_user.role == Role.MANAGER:
            if not set(leave.employee.department).intersection(current_user.department):
                raise AuthorizationError("Not your team member. You can only approve your team member's leave")

        leave.reject_leave(current_user)
        self._leave_repo.save_leave_request(leave)
        Logger.info("Leave fully approved ✅", SUCCESS_LOG_FILE)





