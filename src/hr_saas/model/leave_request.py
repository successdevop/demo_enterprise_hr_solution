import random
from datetime import datetime
from src.hr_saas.model.employee import Employee
from src.hr_saas.error_handling.exceptions import ValidationError
from src.hr_saas.enums.leave import LeaveType, LeaveStatus
from src.hr_saas.enums.role import Role


class LeaveRequest:
    def __init__(self, employee: Employee, days: int, leave_type: LeaveType):
        if days <= 0:
            raise ValidationError("days must be greater than zero")
        if employee.role in [Role.HR, Role.MANAGER]:
            self.total_leave_for_the_year = 30
        else:
            self.total_leave_for_the_year = 21

        self.leave_id = ''.join(str(random.randint(0, 9)) for _ in range(4))
        self.days = days
        self.employee = employee
        self.leave_status = LeaveStatus.PENDING
        self.leave_type = leave_type
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_approved = None
        self.reviewed_by = []
        self.approval_stage = 1

    def increase_total_leave_for_the_year(self, days):
        self.total_leave_for_the_year += days

    def approve_leave(self, executive: Employee):
        if self.leave_status != LeaveStatus.PENDING:
            raise ValidationError("Leave request already processed")

        self.leave_status = LeaveStatus.APPROVED
        self.time_approved = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.reviewed_by.append({"name": executive.name, "role": executive.role.value})

    def reject_leave(self, executive: Employee):
        if self.leave_status != LeaveStatus.PENDING:
            raise ValidationError("Leave request already processed")

        self.leave_status = LeaveStatus.REJECTED
        self.time_approved = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.reviewed_by.append({"name": executive.name, "role": executive.role.value})

    def to_dict(self):
        return {
            "leave_id": self.leave_id,
            "days": self.days,
            "total_leave": self.total_leave_for_the_year,
            "leave_status": self.leave_status.value if hasattr(self.leave_status, "value") else self.leave_status,
            "leave_type": self.leave_type.value if hasattr(self.leave_type, "value") else self.leave_type,
            "time_created": self.created_at,
            "time_approved": self.time_approved,
            "reviewed_by": self.reviewed_by,
            "approval_stage": self.approval_stage,
            "employee": self.employee.to_dict(show_all=False) if self.employee else None
        }

    @classmethod
    def from_to_dict(cls, data) -> "LeaveRequest":
        status = data.get("leave_status")
        if isinstance(status, str) and hasattr(LeaveStatus, status.upper()):
            status = LeaveStatus[status.upper()]

        l_type = data.get("leave_type")
        if isinstance(l_type, str) and hasattr(LeaveType, l_type.upper()):
            l_type = LeaveType[l_type.upper()]

        leave_request = cls(
            days=data.get("days"),
            leave_type=l_type,
            employee=Employee.from_dict(data.get("employee"))
        )
        leave_request.leave_id = data.get("leave_id")
        leave_request.leave_status = status
        leave_request.total_leave_for_the_year = data.get("total_leave")
        leave_request.created_at = data.get("time_created")
        leave_request.time_approved = data.get("time_approved")
        leave_request.reviewed_by = data.get("reviewed_by")
        leave_request.approval_stage = data.get("approval_stage")
        return leave_request

    def __eq__(self, other):
        if not isinstance(other, LeaveRequest):
            return False
        return self.leave_id == other.leave_id

    def __hash__(self):
        return hash(self.leave_id)

    def __repr__(self):
        return (f"<LeaveRequest(name:{self.employee.name} | days:{self.days} | leave_type:{self.leave_type} | "
                f"leave_status:{self.leave_status.value})>")
