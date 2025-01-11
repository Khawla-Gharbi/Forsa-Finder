from marshmallow import Schema, fields, validate

class ProgramSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    eligibility_criteria = fields.Str(required=True)  
    application_deadline = fields.Date(required=True)
    duration = fields.Str(required=True)
    location = fields.Str(required=True)
    funding_details = fields.Str()
    application_link = fields.Url(required=True)
    category = fields.Str(required=True)
    tunisian_eligibility = fields.Str(required=True)