from .base import DomainError


class TrialPlanNotFound(DomainError):
    """No trial plan found in the system."""
