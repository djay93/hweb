from app import db
from app.models import Job
from app.models.enum import WorkflowType

class JobService:
    @staticmethod
    def get_hmda_jobs():
        return (Job.query.filter(Job.workflow_type == WorkflowType.HMDA)
                .order_by(Job.name.asc())
                .all())
