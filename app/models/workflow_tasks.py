from app.extensions import db
from datetime import datetime, UTC
from sqlalchemy import JSON, Enum
from .enum import WorkflowTaskType

class WorkflowTask(db.Model):
    __tablename__ = 'workflow_tasks'

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, nullable=False)
    task_type = db.Column(Enum(WorkflowTaskType), nullable=True)
    meta = db.Column(JSON, nullable=True)  
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at: datetime = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    def __repr__(self):
        return f'<WorkflowTask {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'workflow_id': self.workflow_id,
            'name': self.name,
            'description': self.description,
            'order': self.order,
            'task_type': self.task_type.value if self.task_type else None,
            'meta': self.meta,
        }
