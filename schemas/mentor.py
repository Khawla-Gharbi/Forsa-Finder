from marshmallow import Schema, fields, validate

class MentorSchema(Schema):
    id = fields.Int(dump_only=True)
    full_name = fields.Str(required=True, validate=validate.Length(max=50))
    email = fields.Email(required=True)
    contact_link = fields.Str(validate=validate.Length(max=255))
    field_of_expertise = fields.Str(required=True, validate=validate.Length(max=100))
    previous_attended_program = fields.Str(validate=validate.Length(max=100))
    type_of_mentorship = fields.Str(required=True, validate=validate.Length(max=50))
    organization = fields.Str(validate=validate.Length(max=100))
    availability = fields.Str(required=True, validate=validate.Length(max=50))