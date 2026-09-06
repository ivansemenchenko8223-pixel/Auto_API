from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.depences import get_current_user
from app.schemas.order import OrderCreate, OrderResponse
from app.servises.order import create_order as create_new_order


router = APIRouter(prefix="/orders")


@router.post(
    "/order",
    tags=["Заказы"],
    summary="Создание заказа",
    response_model=OrderResponse,
)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return create_new_order(db, order, current_user.id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
