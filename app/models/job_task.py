from datetime import datetime, timezone
from app.extensions import db
from app.models.enum import TaskStatus
class JobTask(db.Model):
    __tablename__ = 'job_tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id', name='fk_job_tasks_job_id'), nullable=False)
    status = db.Column(db.String(50), default=TaskStatus.PENDING.name, nullable=False) 
    job_task_type = db.Column(db.String(50), nullable=False)  
    started_at = db.Column(db.DateTime, default=None)
    completed_at = db.Column(db.DateTime, default=None)
    retries = db.Column(db.Integer, default=0)
    meta = db.Column(db.Text, nullable=True)  
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # @classmethod
    # def from_workflow_task(cls, workflow_task, job_id):
    #     """Creates a JobTask from a WorkflowTask."""
    #     # Convert from enum value to enum name
    #     job_task_type = next(type for type in TriggerType if type.value == workflow_task['task_type'])
    #     return cls(
    #         name=workflow_task['name'],
    #         order=workflow_task['order'],
    #         job_id=job_id,
    #         job_task_type=job_task_type.name,
    #         status=TaskStatus.PENDING.name
    #     )

    def __repr__(self):
        return f'<JobTask {self.name}>'
