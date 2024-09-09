from sqlalchemy.orm import Session
from database import db
from circuitbreaker import circuit
from sqlalchemy import select
from models.product import Product


def save(product_data):
  with Session(db.engine) as session:
    with session.begin():
      new_product = Product(name=product_data["name"],price=product_data["price"],quantity=product_data["quantity"])
      session.add(new_product)
      session.commit()
    session.refresh(new_product)
    return new_product
  
def find_all(page=1,per_page=10):
  products = db.paginate(select(Product),page=page,per_page=per_page)
  return products