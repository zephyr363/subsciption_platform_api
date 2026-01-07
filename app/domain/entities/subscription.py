from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from app.domain.exceptions import (
    CannotCancelSubscriptionError,
    SubscriptiopnActivationError,
)

from .plan import PlanEntity


class SubscriptionStatus(Enum):
    TRIAL = "trial"
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


@dataclass
class SubscriptionEntity:
    id: UUID
    user_id: UUID
    plan_id: UUID
    status: SubscriptionStatus
    started_at: datetime
    ends_at: datetime
    cancelled_at: Optional[datetime] = None
    plan: Optional[PlanEntity] = None  # Optional relationship to PlanEntity

    def cancel(self):
        if self.status == SubscriptionStatus.CANCELLED:
            raise CannotCancelSubscriptionError("Subscription is already cancelled.")
        self.status = SubscriptionStatus.CANCELLED

    def activate(self):
        if self.status != SubscriptionStatus.TRIAL:
            raise SubscriptiopnActivationError(
                "Only trial subscriptions can be activated."
            )
        self.status = SubscriptionStatus.ACTIVE

    @classmethod
    def create_trial(
        cls,
        user_id: UUID,
        plan: PlanEntity,
    ) -> "SubscriptionEntity":
        return cls(
            id=uuid4(),
            user_id=user_id,
            plan_id=plan.id,
            status=SubscriptionStatus.TRIAL,
            plan=plan,
            started_at=datetime.now(UTC),
            ends_at=datetime.now(UTC) + timedelta(days=plan.duration_days),
        )
