from src.hr_saas.repository.leave_repo import LeaveRepository
from src.hr_saas.auth.authorization import Authorization
from src.hr_saas.enums.leave import LeaveType
from src.hr_saas.enums.role import Role
from src.hr_saas.model.employee import Employee
from src.hr_saas.model.leave_request import LeaveRequest
from src.hr_saas.error_handling.exceptions import ValidationError, AuthorizationError, NotFoundError
from src.hr_saas.file_IO.logging import Logger
from src.hr_saas.file_IO.config_file import SUCCESS_LOG_FILE, INFO_LOG_FILE


class LeaveService:
    def __init__(self, repo: LeaveRepository):
        self._leave_repo = repo

    def apply_for_leave(self, employee: Employee, days: int, leave_t: LeaveType):
        total_leave = self._leave_repo.get_leave_balance(employee.email)
        if total_leave:
            leave_balance = employee.total_leave_days_for_the_year - total_leave

            if leave_balance == 0:
                raise ValidationError("You have used up your leave for the year")

            if days > leave_balance:
                raise ValidationError(f"You have {leave_balance} leave request days remaining for the year")
        else:

            leave_balance = employee.total_leave_days_for_the_year
            if days > leave_balance:
                raise ValidationError(f"You have {leave_balance} leave request days remaining for the year")

        leave_request = LeaveRequest(employee, days, leave_t)
        self._leave_repo.save_leave_request(leave_request)

        Logger.success(f"{employee.first_name} applied for {days} days of {leave_t}", SUCCESS_LOG_FILE)
        print("Leave application successful")

        return leave_request

    def approve_leave(self, current_user, employee: Employee, leave_id: str):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR, Role.MANAGER])
        emp_email = employee.email

        if (emp_email not in self._leave_repo.get_all_leave_request() or
                not self._leave_repo.get_employee_requests_by_email(emp_email)):
            raise NotFoundError("No Leave Request found")

        # Get the leave request
        leave = self._leave_repo.get_employee_requests_by_email(emp_email).get(leave_id)
        if not leave:
            print(f"Leave_Request with id {leave_id} not found")
            raise NotFoundError(f"Leave_Request with id {leave_id} not found")

        if current_user.role != Role.ADMIN:
            if current_user.role == employee.role:
                if current_user.role == Role.MANAGER:
                    raise AuthorizationError("You can't approve your own leave request, pass it to HR")
                else:
                    raise AuthorizationError("You can't approve your own leave request, pass it to Admin")

        if current_user.role == Role.ADMIN or (current_user.role == Role.HR and employee.role == Role.MANAGER):
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

                leave.reviewed_by.append({"name": current_user.first_name, "role": current_user.role.value})
                leave.approval_stage = 2
                self._leave_repo.save_leave_request(leave)
                Logger.info("Approved by Manager → moving to HR", INFO_LOG_FILE)

            elif leave.approval_stage == 2:
                if current_user.role != Role.HR:
                    raise AuthorizationError("Only HR or Admin can finalize approval")

                leave.approve_leave(current_user)
                self._leave_repo.save_leave_request(leave)
                Logger.info("Leave fully approved ✅", SUCCESS_LOG_FILE)

    def reject_leave(self, current_user, employee: Employee, leave_id: str):
        Authorization.authorized_roles(current_user, [Role.MANAGER, Role.HR, Role.ADMIN])
        emp_email = employee.email

        # Get the leave request
        leave = self._leave_repo.get_employee_requests_by_email(emp_email).get(leave_id)
        if not leave:
            raise NotFoundError(f"Leave_Request with id {leave_id} not found")

        if current_user.role != Role.ADMIN:
            if current_user.role == employee.role:
                if current_user.role == Role.MANAGER:
                    raise AuthorizationError("You can't reject your own leave request, pass it to HR")
                else:
                    raise AuthorizationError("You can't reject your own leave request, pass it to Admin")

        if current_user.role == Role.MANAGER:
            if not set(leave.employee.department).intersection(current_user.department):
                raise AuthorizationError("Not your team member. You can only reject your team member's leave")

        leave.reject_leave(current_user)
        self._leave_repo.save_leave_request(leave)
        Logger.info("Leave rejected", SUCCESS_LOG_FILE)

    def get_all_leave_by_status(self, current_user, leave_status):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR, Role.MANAGER])

        return self._leave_repo.get_all_leave_by_status(leave_status)

    def get_all_employee_leave(self, current_user, employee: Employee):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR, Role.MANAGER])

        leave = self._leave_repo.get_employee_requests_by_email(employee.email)
        if not leave:
            raise NotFoundError(f"{employee.first_name} has no leave request")

        return leave

    def get_employee_leave_balance(self, current_user, employee: Employee):
        Authorization.authorized_roles(current_user, [Role.ADMIN, Role.HR])
        leave_balance = self._leave_repo.get_leave_balance(employee.email)

        if not leave_balance:
            return employee.total_leave_days_for_the_year

        return employee.total_leave_days_for_the_year - leave_balance

    def delete_all_leave_request(self, current_user):
        Authorization.authorized_roles(current_user, [Role.ADMIN])
        self._leave_repo.delete_all_request()





