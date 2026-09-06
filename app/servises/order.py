from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.models.detal import Detal
from app.schemas.order import OrderCreate, OrderResponse, OrderItemResponse


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_user_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()


def create_order(db: Session, order_data: OrderCreate, user_id: int) -> OrderResponse:
    requested: dict[int, int] = {}
    for item in order_data.items:
        if item.quantity <= 0:
            raise ValueError("Количество должно быть больше 0")
        requested[item.detal_id] = requested.get(item.detal_id, 0) + item.quantity

    detal_ids = list(requested.keys())
    detals = {
        d.id: d for d in db.query(Detal).filter(Detal.id.in_(detal_ids)).all()
    }

    for detal_id, qty in requested.items():
        detal = detals.get(detal_id)
        if not detal:
            raise ValueError(f"Деталь с id {detal_id} не найдена")
        if detal.quantity_in_stock < qty:
            raise ValueError(
                f"Недостаточно на складе для детали {detal.article_number}: "
                f"есть {detal.quantity_in_stock}, запрошено {qty}"
            )

    db_order = Order(user_id=user_id)
    db.add(db_order)
    db.flush()

    total_price = 0.0
    items_response: list[OrderItemResponse] = []

    for detal_id, qty in requested.items():
        detal = detals[detal_id]
        line_price = detal.price * qty
        total_price += line_price

        db_item = OrderItem(
            order_id=db_order.id,
            detal_id=detal_id,
            quantity=qty,
            price=line_price,
        )
        db.add(db_item)
        detal.quantity_in_stock -= qty
        db.flush()

        items_response.append(
            OrderItemResponse(
                id=db_item.id,
                name=detal.name,
                manufacturer=detal.manufacturer,
                article_number=detal.article_number,
                price=line_price,
                quantity=qty,
            )
        )

    db_order.total_price = total_price
    db.commit()
    db.refresh(db_order)

    return OrderResponse(
        id=db_order.id,
        user_id=db_order.user_id,
        total_price=db_order.total_price,
        items=items_response,
    )
