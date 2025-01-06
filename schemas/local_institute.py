from marshmallow import Schema, fields, validate

class LocalInstituteSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=100))
    type = fields.Str(required=True, validate=validate.Length(max=50))
    service_offered = fields.Str(required=True)
    location = fields.Str(required=True, validate=validate.Length(max=100))
    contact_email = fields.Email()
    phone_number = fields.Str(validate=validate.Length(max=20))
    website = fields.Url(validate=validate.Length(max=255))
    target_audience = fields.Str(required=True, validate=validate.Length(max=100))
    cost = fields.Str(validate=validate.Length(max=50))