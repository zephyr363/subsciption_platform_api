class PlanNotFoundError(Exception):
    pass


class PlanCreationError(Exception):
    pass


class SessionNotFoundError(Exception):
    pass


class SubscriptionNotFoundError(Exception):
    pass


class SubscriptionSaveError(Exception):
    pass


class SubscriptionAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass
