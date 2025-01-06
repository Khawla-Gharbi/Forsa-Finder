from marshmallow import Schema, fields, validate

class ProgramSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=100))
    description = fields.Str(required=True)
    eligibility_criteria = fields.List(fields.Str(), required=True)  
    application_deadline = fields.Date(required=True)
    duration = fields.Str(required=True, validate=validate.Length(max=50))
    location = fields.Str(required=True, validate=validate.Length(max=100))
    funding_details = fields.Str()
    application_link = fields.Url(required=True, validate=validate.Length(max=255))
    category = fields.Str(required=True, validate=validate.Length(max=100))
    tunisian_eligibility = fields.Str(required=True, validate=validate.Length(max=50))