from marshmallow import Schema, fields, validate

class ApplicantSchema(Schema):
    id = fields.Int(dump_only=True)
    full_name = fields.Str(required=True, validate=validate.Length(max=100))
    email = fields.Email(required=True)
    university = fields.Str(required=True, validate=validate.Length(max=100))
    level_of_study = fields.Str(required=True, validate=validate.Length(max=50))
    field_of_study = fields.Str(required=True, validate=validate.Length(max=100))
    goals = fields.Str()
    languages_spoken = fields.Str(validate=validate.Length(max=100))
    location = fields.Str(validate=validate.Length(max=100))