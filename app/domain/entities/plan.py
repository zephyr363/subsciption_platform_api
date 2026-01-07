from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class PlanEntity:
    id: UUID
    name: str
    features: str
    price: Decimal
    duration_days: int
    is_active: bool = True
    is_trial: bool = False

    @classmethod
    def create(
        cls,
        name: str,
        description: str,
        price: float,
        duration_days: int,
        is_trial: bool = False,
    ):
        return cls(
            id=uuid4(),
            name=name,
            features=description,
            price=Decimal(str(price)),
            duration_days=duration_days,
            is_trial=is_trial,
        )
