from marshmallow import Schema, fields, validates, ValidationError, post_dump, post_load
from app.models.enum import TriggerType

class WorkflowTaskSchema(Schema):
    id = fields.Int()
    workflow_id = fields.Int(required=True)
    name = fields.Str(required=True, validate=lambda x: len(x) <= 100)
    description = fields.Str(allow_none=True, validate=lambda x: len(x) <= 255)
    order = fields.Int(required=True)
    task_type = fields.Str(allow_none=True)

    meta = fields.Dict(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('task_type')
    def validate_task_type(self, value):
        if value not in TriggerType._member_names_:
            raise ValidationError("Invalid task type.")

    @post_dump
    def convert_enums_for_ui(self, data, **kwargs):
        """Convert Enum name to Enum value for UI display after serialization."""
        if 'task_type' in data and data['task_type']:
            data['task_type'] = TriggerType[data['task_type']].value
        return data

    @post_load
    def convert_enums_for_storage(self, data, **kwargs):
        """Convert Enum value to Enum name for storage before deserialization."""
        if 'task_type' in data and data['task_type']:
            data['task_type'] = TriggerType(data['task_type']).name
        return data
