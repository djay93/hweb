from marshmallow import Schema, fields, validates, ValidationError
from app.models.enum import WorkflowType
from .workflow_task_schema import WorkflowTaskSchema

class WorkflowSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=lambda x: len(x) <= 100)
    description = fields.Str(allow_none=True, validate=lambda x: len(x) <= 255)
    workflow_type = fields.Str(required=True)
    tasks = fields.Nested(WorkflowTaskSchema, many=True, dump_only=True)  
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('workflow_type')
    def validate_workflow_type(self, value):
        if value not in WorkflowType._member_names_:
            raise ValidationError("Invalid workflow type.")

