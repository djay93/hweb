from flask import current_app as app
from app import db
from app.models import Job, Workflow, JobStep
from app.models.enum import WorkflowType, ScheduleType
from sqlalchemy import or_, func, String

class HMDAService:
    @staticmethod
    def get_hmda_jobs(page=1, per_page=10, search=''):
        query = Job.query.filter(Job.workflow_type == WorkflowType.HMDA)

        if search:
            search_lower = f"%{search.lower()}%"
            query = query.filter(
                or_(
                    func.lower(Job.name).like(search_lower),
                    func.cast(Job.id, String).like(search_lower)
                )
            )
        
        return query.order_by(Job.name.asc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
    
    @staticmethod
    def create_hmda_job(name, workflow_id, workflow_type, start_time, end_time, status, next_run_time):
        print(f"Received start_time: {start_time}, type: {type(start_time)}")
        job = Job(name=name, workflow_id=workflow_id, workflow_type=workflow_type, 
                 start_time=start_time, end_time=end_time, status=status, 
                 next_run_time=next_run_time)
        print(f"Job start_time before commit: {job.start_time}")
        db.session.add(job)
        db.session.commit()
        print(f"Job start_time after commit: {job.start_time}")
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


    @staticmethod
    def get_hmda_job_by_id(hmda_id):
        return Job.query.options(db.joinedload(Job.steps)).get(hmda_id)
    
    @staticmethod
    def create_hmda_job_steps(job_id, tasks):
        if not tasks:
            return
        
        try:
            for task in tasks:
                step = JobStep.from_workflow_task(task, job_id)
                db.session.add(step)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to create job steps: {str(e)}")

    @staticmethod
    def get_hmda_workflows():
        return (Workflow.query
                .filter(Workflow.workflow_type == WorkflowType.HMDA)
                .order_by(Workflow.name.asc())
                .options(db.joinedload(Workflow.tasks))
                .all())
    
    @staticmethod
    def update_hmda_job(id, **data):
        """Update a job by its ID with the provided data"""
        job = Job.query.get(id)
        if not job:
            raise ValueError(f"Job with ID {id} not found")
        
        for key, value in data.items():
            setattr(job, key, value)
            
        db.session.commit()
        return job
