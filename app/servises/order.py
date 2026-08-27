from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.models.detal import Detal
from app.schemas.order import OrderCreate, OrderResponse, OrderItemResponse

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_user_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()

def create_order(db: Session, order_data: OrderCreate, user_id: int) -> OrderResponse:
    db_order = Order(user_id=user_id)
    db.add(db_order)
    db.flush()

    total_price = 0.0
    order_items = []

    for item in order_data.items:
        detal = db.query(Detal).filter(Detal.id == item.detal_id).first()
        if not detal:
            raise ValueError(f"Деталь с id {item.detal_id} не найдена")
        price = detal.price * item.quantity
        total_price += price
        db_item = OrderItem(
            order_id=db_order.id,
            detal_id=item.detal_id,
            quantity=item.quantity,
            price=price
        )
        db.add(db_item)
        order_items.append(db_item)

    db_order.total_price = total_price
    db.commit()
    db.refresh(db_order)

    items_response = []
    for item in order_items:
        detal = db.query(Detal).filter(Detal.id == item.detal_id).first()
        items_response.append(OrderItemResponse(
            id=item.id,
            name=detal.name if detal else "",
            manufacturer=detal.manufacturer if detal else "",
            article_number=detal.article_number if detal else "",
            price=item.price,
            quantity=item.quantity
        ))

    return OrderResponse(
        id=db_order.id,
        user_id=db_order.user_id,
        total_price=db_order.total_price,
        items=items_response
    )
