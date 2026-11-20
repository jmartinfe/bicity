from sqlalchemy import DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import StrEnum
from datetime import datetime, UTC

from bicity.db.base import Base
from bicity.db.types import enum_column
from bicity.models.dock import Dock

class BikeStatus(StrEnum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"

class Bike(Base):
    __tablename__ = 'bikes'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[BikeStatus] = mapped_column(
        enum_column(BikeStatus),
        default=BikeStatus.AVAILABLE
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    dock: Mapped["Dock | None"] = relationship(back_populates="bike")

    @property
    def is_retired(self) -> bool:
        return self.retired_at is not None