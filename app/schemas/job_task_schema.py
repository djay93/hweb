from marshmallow import Schema, fields, validates, ValidationError, post_dump, post_load
from app.models.enum import TaskStatus, TriggerType

class JobTaskSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True, validate=lambda x: len(x) <= 100)
    order = fields.Int(required=True)
    job_id = fields.Int(required=True)
    status = fields.Str(required=True)  
    job_task_type = fields.Str(required=True)  
    started_at = fields.DateTime(allow_none=True)
    completed_at = fields.DateTime(allow_none=True)
    retries = fields.Int(required=False)
    meta = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('status')
    def validate_status(self, value):
        if value not in TaskStatus._member_names_:
            raise ValidationError("Invalid status.")

    # @validates('job_task_type')
    # def validate_job_task_type(self, value):
    #     if value not in TriggerType._member_names_:
    #         raise ValidationError("Invalid schedule type.")

    @post_dump
    def convert_enums_for_ui(self, data, **kwargs):
        """Convert Enum name to Enum value for UI display after serialization."""
        if 'status' in data:
            data['status'] = TaskStatus[data['status']].value
        if 'job_task_type' in data:
            data['job_task_type'] = TriggerType[data['job_task_type']].value
        return data

    @post_load
    def convert_enums_for_storage(self, data, **kwargs):
        """Convert Enum value to Enum name for storage before deserialization."""
        if 'status' in data:
            data['status'] = TaskStatus(data['status']).name
        if 'job_task_type' in data:
            data['job_task_type'] = TriggerType(data['job_task_type']).name
        return data
