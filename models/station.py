from enum import StrEnum

from sqlalchemy import DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, UTC

from bicity.models.dock import Dock
from bicity.db.base import Base
from bicity.db.types import enum_column

class StationStatus(StrEnum):
    AVAILABLE = "available"
    MAINTENANCE = "maintenance"

class Station(Base):
    __tablename__ = 'stations'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[StationStatus] = mapped_column(
        enum_column(StationStatus),
        default=StationStatus.AVAILABLE
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    docks: Mapped[list["Dock"]] = relationship(back_populates="station")

    @property
    def is_retired(self) -> bool:
            return self.retired_at is not None