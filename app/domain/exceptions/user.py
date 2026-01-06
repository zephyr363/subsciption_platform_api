class UserNotFound(Exception):
    """Exception raised when a user is not found."""

    pass


class UserAlreadyExists(Exception):
    """Exception raised when trying to create a user that already exists."""

    pass
