import enum
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, Enum as SQLEnum, Float, Integer

from app.db.base import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    items = Column(JSON, nullable=False)  # snapshot: [{product_id, name, quantity, unit_price, line_total}]
    total = Column(Float, nullable=False)
    status = Column(
        SQLEnum(OrderStatus, name="order_status"),
        default=OrderStatus.PENDING,
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
