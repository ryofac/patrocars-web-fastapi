import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, func, types
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class UUIDModel(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        types.UUID,
        primary_key=True,
        init=False,
        default=uuid.uuid4,
    )


class TimestampMixin(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        init=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(),
        init=False,
        nullable=True,
    )


class CarModel(TimestampMixin, UUIDModel):
    __tablename__ = "car_model"

    name: Mapped[str] = mapped_column(types.String(100))
    reference_value: Mapped[Decimal] = mapped_column(types.DECIMAL(2))
    motorization: Mapped[float] = mapped_column(types.Float(1))
    is_automatic: Mapped[bool]
    description: Mapped[str] = mapped_column(types.String(255), nullable=True)

    manufacturer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("manufacturer.id"),
        nullable=False,
    )

    manufacturer: Mapped["Manufacturer"] = relationship(
        "Manufacturer",
        back_populates="car_models",
        init=False,
    )

    cars: Mapped[list["Car"]] = relationship(
        "Car",
        back_populates="car_model",
        init=False,
    )


class Car(TimestampMixin, UUIDModel):
    __tablename__ = "car"

    car_model_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("car_model.id"),
        nullable=False,
    )
    car_model: Mapped["CarModel"] = relationship("CarModel", back_populates="cars")


class Manufacturer(TimestampMixin, UUIDModel):
    __tablename__ = "manufacturer"

    name: Mapped[str] = mapped_column(types.String(100))
    country: Mapped[str] = mapped_column(types.String(100))
    foundation_year: Mapped[int]

    car_models: Mapped[list["CarModel"]] = relationship(
        "CarModel",
        back_populates="manufacturer",
        init=False,
    )
