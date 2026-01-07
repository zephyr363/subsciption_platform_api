"""
The exception classses here are should be used only in Domain Entities/
"""


class CannotCancelSubscriptionError(Exception):
    pass


class SubscriptiopnActivationError(Exception):
    pass


class ActiveSubscriptionExists(Exception):
    pass
