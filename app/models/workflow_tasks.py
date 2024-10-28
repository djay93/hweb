from app.extensions import db
from datetime import datetime, UTC
from sqlalchemy import JSON

class WorkflowTask(db.Model):
    __tablename__ = 'workflow_tasks'

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, nullable=False)
    meta = db.Column(JSON, nullable=True)  
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    def __repr__(self):
        return f'<WorkflowTask {self.name}>'
