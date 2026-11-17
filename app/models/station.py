from sqlalchemy import DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, UTC

from app.models.dock import Dock
from app.db.types import Status
from app.db.base import Base

class Station(Base):
    __tablename__ = 'stations'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[Status] = mapped_column(
        SQLEnum(Status,
                native_enum=False,
                length=20,
                values_callable=lambda enum: [e.value for e in enum]),
        default=Status.AVAILABLE
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    retired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    docks: Mapped[list["Dock"]] = relationship(back_populates="station")