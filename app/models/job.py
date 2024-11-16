from datetime import datetime, timezone
from app.extensions import db
from app.models.enum import JobStatus

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=False)
    workflow_type = db.Column(db.String(50), nullable=False) 
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False)  
    next_run_time = db.Column(db.DateTime, nullable=False)
    
    tasks = db.relationship('JobTask', backref='job', lazy=True, cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Job {self.name}>'
