from typing import Protocol


class IUnitOfWork(Protocol):
    async def commit(self) -> None:
        """Подтвердить все изменения атомарно"""
        ...

    async def rollback(self) -> None:
        """Откатить изменения"""
        ...
