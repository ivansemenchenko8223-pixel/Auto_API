from pydantic import BaseModel, Field, field_validator


class DetalData(BaseModel):
        id:int
        name:str=Field(description="Название детали")            
        manufacturer:str=Field(min_length=2,
                               max_length=20,
                               description="Наименование производителя детали")
        article_number:str=Field(description="Артикул включает себя латинские буквы и цифры")
        price:float
        quantity_in_stock:int


        @field_validator("article_number")
        @classmethod
        def conversion_of_text(cls, article:str):
                new_text = article.replace(" ", "").upper()
                return new_text


      
