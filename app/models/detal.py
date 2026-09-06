from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from app.db.session import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class Detal(Base):
    __tablename__ = "detals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    article_number = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)
    
    order_items = relationship("app.models.order.OrderItem", back_populates="detals")


