from sqlmodel import Session, select, func

from app.models.sale import SaleCreate, Sale, SalePublic

def create_sale(*, session: Session, sale_in: SaleCreate) -> Sale:
    db_item = Sale.model_validate(sale_in)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def get_sales(*, session: Session, offset: int, limit: int) -> list[SalePublic]:
    statement = (
        select(Sale)
        .offset(offset)
        .limit(limit)
    )
    return session.exec(statement).all()

def count_total_sales(*, session: Session) -> int:
    count_statement = (
        select(func.count())
        .select_from(Sale)
    )
    return session.exec(count_statement).one()