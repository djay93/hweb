from app.extensions import db
from datetime import datetime, UTC
from sqlalchemy import Enum
from app.models.enum import WorkflowType

class Workflow(db.Model):
    __tablename__ = 'workflows'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    type = db.Column(Enum(WorkflowType), nullable=False)
    tasks = db.relationship('WorkflowTask', backref='workflow', lazy=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    def __repr__(self):
        return f'<Workflow {self.name}>'
