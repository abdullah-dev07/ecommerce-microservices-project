from enum import Enum

from tortoise import fields, models


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Order(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField(index=True)
    # Snapshot of line items at order time:
    # [{product_id, name, quantity, unit_price, line_total}, ...]
    items = fields.JSONField()
    total = fields.FloatField()
    status = fields.CharEnumField(OrderStatus, default=OrderStatus.PENDING, max_length=20)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "orders"
