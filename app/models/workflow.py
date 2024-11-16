from datetime import datetime, timezone
from typing import List
from app.extensions import db
from .workflow_task import WorkflowTask

class Workflow(db.Model):
    __tablename__ = 'workflows'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    workflow_type = db.Column(db.String(50), nullable=False)
    tasks = db.relationship('WorkflowTask', backref='workflow', lazy=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Workflow {self.name}>'
