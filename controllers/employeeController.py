from flask import request, jsonify
from models.schemas.employeeSchema import employee_schema,employees_schema,employees_production_schema
from services import employeeService
from marshmallow import ValidationError
from caching import cache

def save():
  try:
    employee_data = employee_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  
  employee_save = employeeService.save(employee_data)
  print(employee_save)
  if employee_save is not None:
    return employee_schema.jsonify(employee_save),201
  else:
    return jsonify({"message": "Fallback method error activated", "body":employee_data}), 400

@cache.cached(timeout=60)
def find_all():
  employees = employeeService.find_all()
  return employees_schema.jsonify(employees), 200

def employee_production_analyses_query():
  analyses = employeeService.employee_production_analyses_query()
  return employees_production_schema.jsonify(analyses), 200
  