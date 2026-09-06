from pydantic import BaseModel, Field
from typing import List


class OrderItemCreate(BaseModel):
    detal_id: int
    quantity: int = Field(gt=0, description="Количество должно быть больше 0")


class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(min_length=1)


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
