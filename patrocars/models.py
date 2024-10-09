import uuid
from datetime import datetime

from sqlalchemy import func, types
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class UUIDModel(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        types.UUID,
        primary_key=True,
        init=False,
        default="uuid.uuid4",
    )


class TimestampMixin(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())


class CarModel(TimestampMixin, UUIDModel):
    __tablename__ = "car_model"


class CarManufacter(TimestampMixin, UUIDModel):
    __tablename__ = "car_manufacturer"
    name: Mapped[str] = mapped_column(types.String(100))
