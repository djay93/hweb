from app.extensions import db
from datetime import datetime, UTC
from sqlalchemy import Enum
from app.models.enum import JobStatus, WorkflowType

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=False)
    workflow_type = db.Column(Enum(WorkflowType), nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(Enum(JobStatus), default=JobStatus.PENDING)
    next_run_time = db.Column(db.DateTime, nullable=True) 
    
    steps = db.relationship('JobStep', backref='job', lazy=True)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    def __repr__(self):
        return f'<Job {self.name}>'
