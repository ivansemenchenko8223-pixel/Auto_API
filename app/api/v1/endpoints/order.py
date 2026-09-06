from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.order import Order as OrderModel, OrderItem as OrderItemModel
<<<<<<< HEAD
from app.schemas.order import OrderItemsResponce as OrderData, OrderItem as OrderItemSchema
from app.models.detal import Detal
from app.core.config import config
from app.schemas.order import OrderCreate, OrderItem, OrderItemCreate, OrderItemsResponce
=======
from app.models.detal import Detal
from app.core.config import config
>>>>>>> 8860929115287add61d8bfc6ecb21363bdda5a75
from app.db.session import get_db
from app.servises.user import get_user_by_username, get_user_by_email
from datetime import timedelta
from app.core.depences import get_current_user
from app.servises.detal import create_detal as create_new_detal


router = APIRouter(prefix="/orders")


from app.schemas.order import OrderCreate, OrderResponse
from app.servises.order import create_order as create_new_order

@router.post("/order", tags=["Заказы"], summary="Создание заказа", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return create_new_order(db, order, current_user.id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    