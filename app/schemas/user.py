from pydantic import BaseModel, EmailStr, Field



class UserCreate(BaseModel):
    email:EmailStr
    phone_number:str=Field(min_length=11,
                            max_length=11, 
                            description="Номер телефона должен включать 11 знаков, в формате '8 XXX YYY‑YY‑YY'")
    username:str=Field(min_length=2, max_length=20)
    password:str=Field(min_length=8, max_length=20,
                       description="Для безопасности используйте надежный пароль, включающий заглавные и строчные буквы, цифры, спецсимволы")
                       
                       
class UserData(BaseModel):
    email:EmailStr
    phone_number:int
    username:str
    password:str
    
class UserLogin(BaseModel):
    email:EmailStr
    phone_number:int
    password:str









    

