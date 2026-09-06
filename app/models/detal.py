from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.session import Base


class Detal(Base):
    __tablename__ = "detals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    article_number = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)

    order_items = relationship("app.models.order.OrderItem", back_populates="detals")
