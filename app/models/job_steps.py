from flask import current_app as app
from app.extensions import db
from datetime import datetime, UTC
from sqlalchemy import Enum
from app.models.enum import StepStatus, ScheduleType   

class JobStep(db.Model):
    __tablename__ = 'job_steps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id', name='fk_job_steps_job_id'), nullable=False)
    status = db.Column(Enum(StepStatus), default=StepStatus.PENDING)
    schedule_type = db.Column(Enum(ScheduleType, native_enum=False), nullable=False)
    started_at = db.Column(db.DateTime, default=None)
    completed_at = db.Column(db.DateTime, default=None)
    retries = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    def to_dict(self):
        return {
            'order': self.order,
            'name': self.name,
            'job_id': self.job_id,
            'schedule_type': self.schedule_type.value if self.schedule_type else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'retries': self.retries,
            'status': self.status.value if self.status else None
        }
    
    @classmethod
    def from_workflow_task(cls, workflow_task, job_id):
        """Creates a JobStep from a WorkflowTask.
        
        Returns:
            JobStep: A new JobStep instance
        """
        # Convert from enum value ("Manual") to enum name ("MANUAL")
        schedule_type = next(type for type in ScheduleType if type.value == workflow_task['task_type'])
        return cls(
            name=workflow_task['name'],
            order=workflow_task['order'],
            job_id=job_id,
            schedule_type=schedule_type,
            status=StepStatus.PENDING
        )

    def __repr__(self):
        return f'<JobStep {self.name}>'
