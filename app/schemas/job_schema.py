from datetime import datetime
from marshmallow import Schema, fields, validates, ValidationError, pre_load
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
    tasks = fields.Nested(JobTaskSchema, many=True, required=False) 

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
        
    @pre_load
    def remove_readonly_fields(self, data, **kwargs):
        """Remove read-only fields before loading."""
        data.pop('created_at', None)  
        data.pop('updated_at', None)
        return data

class JobSchemaWithoutTasks(JobSchema):
    class Meta:
        exclude = ('tasks',)

