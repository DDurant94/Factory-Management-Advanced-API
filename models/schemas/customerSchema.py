from marshmallow import fields, validate
from schema import ma

class CustomerSchema(ma.Schema):
  id = fields.Integer(required=False)
  name = fields.String(required=True, validate=validate.Length(min=1))
  email = fields.String(required=True, validate=validate.Length(min=1))
  phone = fields.String(required=True, validate=validate.Length(min=10))
  
  class Meta:
    fields = ("id", "name", "email", "phone")
    
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)