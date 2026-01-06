from .base import DomainError


class UserAlreadySubscribed(DomainError):
    """User already has an active or trial subscription."""


class CannotCancelSubscriptionError(DomainError):
    """Raise when attempting to cancel a subscription that cannot be cancelled."""


class SubscriptiopnActivationError(DomainError):
    """Error occurred while activating the subscription."""


class ActiveSubscriptionExists(DomainError):
    """An active subscription already exists for the user."""
