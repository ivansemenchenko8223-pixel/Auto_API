from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.session import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = Column(String, default="pending")
    total_price = Column(Float, default=0.0)

    user = relationship("app.models.user.User", back_populates="orders")
    order_items = relationship(
        "app.models.order.OrderItem", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    detal_id = Column(Integer, ForeignKey("detals.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float)

    order = relationship("app.models.order.Order", back_populates="order_items")
    detals = relationship("app.models.detal.Detal", back_populates="order_items")
