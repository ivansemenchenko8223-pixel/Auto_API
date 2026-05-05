from pydantic import BaseModel, Field


class DetalData(BaseModel):
        def conversion_of_text(self, article:str):
                self.new_text = article.replace(" ", "").upper()
                return self.new_text
        
        
        article_number = conversion_of_text("article")

        id:int
        name:str=Field(description="Название детали")            
        manufacturer:str=Field(min_length=2,
                               max_length=20,
                               description="Наименование производителя детали")
        article_number:str=Field(description="Артикул включает себя латинские буквы и цифры")
        price:float
        quantity_in_stock:int