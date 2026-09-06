from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.schemas.order import OrderItemsResponce, OrderItem
from app.models.detal import Detal
from app.models.order import Order as OrderModel, OrderItem as OrderItemModel
from app.schemas.order import OrderItemsResponce as OrderSchema, OrderItem as OrderItemSchema

def get_order(db:Session, order_id:int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_user_orders(db:Session, user_id:int):
    return db.query(Order).filter(user_id == Order.user_id).all()


def to_order_schema(db_order: OrderModel, db: Session):
    items = []
    for item in db_order.items:
        items.append(
            OrderItemSchema(
                id = items.id,
                name = items.name,
                manufacturer = item.manufacturer,
                article_number = item.article_number,
                price = item.price,
                quantity = item.quantity
            )
        )

      
    return OrderSchema(
        id=db_order.id,
        total_price=db_order.total_price,
        code_of_receipt=db_order.code_of_receipt
    )


def create_order(db: Session, order: OrderSchema, user_id: int):
    db_order = OrderModel(user_id=user_id)
    db.add(db_order)
    db.flush()

    total_price = 0
    order_items = []

    for item in order.items:
        detal = db.query(Detal).filter(Detal.article_number == item.article_number).first()
        if not detal:
            raise ValueError(f"Деталь с данным {item.article_number} не найдена")

        price = detal.price * item.quantity
        total_price += price
        db_item = OrderItemModel(
            id=db_order.id,
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
    return to_order_schema(db_order, db)