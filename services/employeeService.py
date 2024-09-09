from sqlalchemy.orm import Session
from database import db
from circuitbreaker import circuit
from sqlalchemy import select,func,within_group

from models.employee import Employee
from models.production import Production
from models.product import Product

def fallback_function(employee):
  pass

@circuit(failure_threshold=1,recovery_timeout=10,fallback_function=fallback_function)
def save(employee_data):
  try:
    if employee_data['name'] == "Failure":
      raise Exception("Failure condition triggered")
    
    with Session(db.engine) as session:
      with session.begin():
        new_employee = Employee(name=employee_data['name'], position=employee_data['position'])
        session.add(new_employee)
        session.commit()
      session.refresh(new_employee)
      return new_employee
      
  except Exception as e:
    raise e
  
def find_all():
  query = select(Employee)
  employees = db.session.execute(query).scalars().all()
  return employees

def employee_production_analyses_query():
  # subquery = select(Production.product_id).join(
  #   Product,Production.product_id == Product.id
  #   ).subquery()
  query = select(Employee).join(Production,
                Employee.id == Production.employee_id).join(Product, 
                Production.product_id == Product.id
                ).group_by(
                Employee.name)
  # func.sum(Production.quantity).label('total')
 
                # , func.sum(Production.quantity,Production.id==Product.id).label('total')
  report = db.session.execute(query).scalars().all()
  print(report)
  # breakpoint()
  return report