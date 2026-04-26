class HRSystemError(Exception):
    """Base class for error handling"""
    pass


class ValidationError(HRSystemError):
    pass


class UserAlreadyExistError(HRSystemError):
    pass


class AuthorizationError(HRSystemError):
    pass


class AuthenticationError(HRSystemError):
    pass


class NotFoundError(HRSystemError):
    pass
