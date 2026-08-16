from pydantic import BaseModel
from typing import List

class OrderItemCreate(BaseModel):
    detal_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    id: int
    name: str
    manufacturer: str
    article_number: str
    price: float
    quantity: int

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    items: List[OrderItemResponse]