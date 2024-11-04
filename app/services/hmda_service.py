from app import db
from app.models import Job, Workflow
from app.models.enum import WorkflowType

class HMDAService:
    @staticmethod
    def get_hmda_jobs(page=1, per_page=10):
        return (Job.query.filter(Job.workflow_type == WorkflowType.HMDA_WEEKLY)
                .order_by(Job.name.asc())
                .paginate(
                    page=page, 
                    per_page=per_page,
                    error_out=False
                ))

    @staticmethod
    def get_hmda_weekly_workflows():
        return (Workflow.query
                .filter(Workflow.workflow_type == WorkflowType.HMDA_WEEKLY)
                .order_by(Workflow.name.asc())
                .options(db.joinedload(Workflow.tasks))
                .all())
    
    @staticmethod
    def create_hmda_job(name, workflow_id, workflow_type, start_time, end_time, status, next_run_time):
        job = Job(name=name, workflow_id=workflow_id, workflow_type=workflow_type, 
                 start_time=start_time, end_time=end_time, status=status, 
                 next_run_time=next_run_time)
        db.session.add(job)
        db.session.commit()
        return job
    
    @staticmethod
    def delete_hmda_job(job_id):
        """Delete a job by its ID"""
        job = Job.query.get(job_id)
        if job:
            db.session.delete(job)
            db.session.commit()
        else:
            raise ValueError(f"Job with ID {job_id} not found")

