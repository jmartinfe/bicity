from enum import StrEnum
from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey
from datetime import datetime, UTC
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bicity.db.base import Base
from bicity.models.station import Station
from bicity.models.bike import Bike
from bicity.db.types import enum_column

class DockStatus(StrEnum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    
class Dock(Base):
    __tablename__ = 'docks'

    id: Mapped[int] = mapped_column(primary_key=True)
    station_id: Mapped[int] = mapped_column(ForeignKey("stations.id"))
    bike_id: Mapped[int | None] = mapped_column(ForeignKey("bikes.id"))
    status: Mapped[DockStatus] = mapped_column(
            enum_column(DockStatus),
        default=DockStatus.AVAILABLE
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    station: Mapped["Station"] = relationship(back_populates="docks")
    bike: Mapped["Bike | None"] = relationship(back_populates="bikes")