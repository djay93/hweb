from app.extensions import db
from datetime import datetime, UTC
from sqlalchemy import Enum
from app.models.enum import StepStatus, ScheduleType   

class JobStep(db.Model):
    __tablename__ = 'job_steps'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('workflow_tasks.id'), nullable=False)
    status = db.Column(Enum(StepStatus), default=StepStatus.PENDING)
    schedule_type = db.Column(Enum(ScheduleType), nullable=False)
    started_at = db.Column(db.DateTime, default=None)
    completed_at = db.Column(db.DateTime, default=None)
    retries = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    def __repr__(self):
        return f'<JobStep {self.name}>'
