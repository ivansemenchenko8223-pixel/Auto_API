from sqlalchemy.orm import Session
from app.servises.user import get_user_by_username
from app.db.session import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.config import config
from app.schemas.token import Token, TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неправильные входные данные",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms = ["HS256"])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        
        token_data = TokenData(username=username)

    except:
        raise credentials_exception
    

    user = get_user_by_username(token_data.username, db)

    if not user:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь не активен")
    
    return user


            