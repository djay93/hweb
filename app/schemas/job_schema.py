from datetime import datetime
from marshmallow import Schema, fields, validates, ValidationError, post_dump, post_load, pre_load
from app.models.enum import JobStatus, WorkflowType
from app.schemas.job_task_schema import JobTaskSchema  

class JobSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True, validate=lambda x: len(x) <= 255)
    workflow_id = fields.Int(required=True)
    workflow_type = fields.Str(required=True)  
    start_time = fields.DateTime(allow_none=True)
    end_time = fields.DateTime(allow_none=True)
    status = fields.Str(required=True)
    next_run_time = fields.DateTime(format='%Y-%m-%d', required=True)
    tasks = fields.Nested(JobTaskSchema, many=True, dump_only=True) 

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('workflow_type')
    def validate_workflow_type(self, value):
        if value not in WorkflowType._member_names_:
            raise ValidationError("Invalid workflow type.")

    @validates('status')
    def validate_status(self, value):
        if value not in JobStatus._member_names_:
            raise ValidationError("Invalid job status.")

    @post_dump
    def convert_enums_for_ui(self, data, **kwargs):
        """Convert Enum name to Enum value for UI display after serialization."""
        if 'workflow_type' in data:
            data['workflow_type'] = WorkflowType[data['workflow_type']].value
        if 'status' in data:
            data['status'] = JobStatus[data['status']].value
        return data

    @post_load
    def convert_enums_for_storage(self, data, **kwargs):
        """Convert Enum value to Enum name for storage before deserialization."""
        if 'workflow_type' in data:
            data['workflow_type'] = WorkflowType[data['workflow_type']].name
        if 'status' in data:
            data['status'] = JobStatus[data['status']].name
        return data
    

