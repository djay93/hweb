from marshmallow import Schema, fields, validates, ValidationError, pre_load
from app.models.enum import TaskStatus, TriggerType

class JobTaskSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True, validate=lambda x: len(x) <= 100)
    order = fields.Int(required=True)
    job_id = fields.Int(required=True)
    status = fields.Str(required=True)  
    job_task_type = fields.Str(required=True)  
    started_at = fields.DateTime(format='%Y-%m-%dT%H:%M:%S', allow_none=True)
    completed_at = fields.DateTime(format='%Y-%m-%dT%H:%M:%S', allow_none=True)
    retries = fields.Int(required=False)
    meta = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('status')
    def validate_status(self, value):
        if value not in TaskStatus._member_names_:
            raise ValidationError("Invalid status.")

    @pre_load
    def remove_readonly_fields(self, data, **kwargs):
        """Remove read-only fields before loading."""
        data.pop('created_at', None)  
        data.pop('updated_at', None)
        return data
    

