from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey
from datetime import datetime, UTC
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.types import Status
from app.db.base import Base
from app.models.station import Station
from app.models.bike import Bike


class Dock(Base):
    __tablename__ = 'docks'

    id: Mapped[int] = mapped_column(primary_key=True)
    station_id: Mapped[int] = mapped_column(ForeignKey("stations.id"))
    bike_id: Mapped[int | None] = mapped_column(ForeignKey("bikes.id"))
    status: Mapped[Status] = mapped_column(
            SQLEnum(Status,
                    native_enum=False,
                    length=20,
                    values_callable=lambda enum: [e.value for e in enum]),
        default=Status.AVAILABLE
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    station: Mapped["Station"] = relationship(back_populates="docks")
    bike: Mapped["Bike | None"] = relationship(back_populates="bikes")