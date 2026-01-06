from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, StringConstraints, Field
from typing import Annotated


class PlanBase(BaseModel):
    id: UUID
    name: Annotated[str, StringConstraints(max_length=255)]
    price: Decimal = Field(max_digits=10, decimal_places=2)
    features: Annotated[str, StringConstraints(max_length=600)]
    duration_days: int
    is_active: bool = True


class PlanCreate(BaseModel):
    name: Annotated[str, StringConstraints(max_length=255)]
    price: Decimal = Field(max_digits=10, decimal_places=2)
    features: Annotated[str, StringConstraints(max_length=600)]
    duration_days: int
