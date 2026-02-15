from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class AppointmentSchema(Schema):
    client_name = fields.String(required=True)
    service_type = fields.String(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
# feel free to add more entries, there are just what I can think of ATM

    @validates("end_time")
    def validate_end_time(self, value):
        if value <= datetime.utcnow():
            raise ValidationError("End time must be in the future.")
