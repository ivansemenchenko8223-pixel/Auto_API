from pydantic import BaseModel, EmailStr, Field



class UserCreate(BaseModel):
    email:EmailStr
    phone_number:int=Field(min_length=11,
                            max_length=11, 
                            description="Номер телефона должен включать 11 знаков, в формате '8 XXX YYY‑YY‑YY'")
    username:str=Field(min_length=2, max_length=12)
    password:str=Field(min_length=8, max_length=12,
                       description="Для безопасности используйте надежный пароль, включающий заглавные и строчные буквы, цифры, спецсимволы")
                       
                       
class UserData(UserCreate):
    pass
    

class UserLogin(BaseModel):
    email:EmailStr    #???нужно ли дуллировать Field, как в UserCreate
    phone_number:int  #???
    password:str      #???
    








    

