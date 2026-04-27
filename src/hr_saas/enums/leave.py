from enum import Enum


class LeaveStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class LeaveType(Enum):
    SICK = "Sick_leave"
    ANNUAL = "Annual_leave"
    UNPAID = "Unpaid_leave"
    EMERGENCY = "Emergency_leave"
    MATERNITY = "Maternity_leave"
