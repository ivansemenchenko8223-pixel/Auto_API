from pydantic import BaseModel, Field, field_validator


class DetalData(BaseModel):
    name: str = Field(description="Название детали")
    manufacturer: str = Field(
        min_length=2, max_length=20, description="Наименование производителя детали"
    )
    article_number: str = Field(description="Артикул: латинские буквы и цифры")
    price: float = Field(gt=0, description="Цена должна быть больше 0")
    quantity_in_stock: int = Field(ge=0, description="Количество на складе, не может быть отрицательным")

    @field_validator("article_number")
    @classmethod
    def conversion_of_text(cls, article: str) -> str:
        return article.replace(" ", "").upper()
