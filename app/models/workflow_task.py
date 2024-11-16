from app.extensions import db
from datetime import datetime, timezone
from sqlalchemy import JSON

class WorkflowTask(db.Model):
    __tablename__ = 'workflow_tasks'

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, nullable=False)
    task_type = db.Column(db.String(50), nullable=True)
    meta = db.Column(JSON, nullable=True)  
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<WorkflowTask {self.name}>'
