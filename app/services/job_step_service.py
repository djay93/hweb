from app import db
from app.models import JobStep, Job
from app.models.enum import WorkflowType

class JobStepService:
    @staticmethod
    def get_job_steps(job_id):
        return (JobStep.query
                .join(Job)
                .filter(job_id == JobStep.job_id)
                .order_by(JobStep.step_number.asc())  
                .all())
