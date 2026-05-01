from pydantic import BaseModel, Field


class OrderData(BaseModel):
    id:int
    total_price:float=Field(description="Общая сумма заказа")
    code_of_receipt:int=Field(min_length=4,
                            max_length=4, 
                            description="При формировании заказа генерируется рандомный четырехзначный код получения")
    
    
class OrderItem(BaseModel):
     id:int
     name:str
     manufacturer:str
     article_number:str
     price:float
     quantity:int
    