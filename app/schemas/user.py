from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    phone_number: str = Field(
        min_length=11,
        max_length=11,
        description="Номер телефона: 11 цифр без пробелов и знаков, например 89161234567",
    )
    username: str = Field(min_length=2, max_length=20)
    password: str = Field(
        min_length=8,
        max_length=20,
        description="Используйте надёжный пароль: заглавные и строчные буквы, цифры, спецсимволы",
    )

    @field_validator("phone_number")
    @classmethod
    def phone_must_be_digits(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("Номер телефона должен состоять только из цифр")
        return value


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    phone_number: str
    username: str
    is_active: bool
    is_admin: bool
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
