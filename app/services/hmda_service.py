from flask import current_app as app
from app import db
from app.models import Job, Workflow, JobTask
from app.models.enum import WorkflowType, JobTaskStatus
from sqlalchemy import or_, func, String
from app.tasks.hmda_tasks import HmdaTasks

class HMDAService:
    # Create operations
    @staticmethod
    def create_hmda_job(job_data):
        """
        Create and save a new HMDA job.

        :param job_data: Dictionary containing data for a job
        :return: Created Job object
        """
        app.logger.info(f"Creating HMDA job with data:")
        
        # Create dict with only non-empty values
        job = Job(
            name=job_data.get('name'), 
            workflow_id=job_data.get('workflow_id'), 
            workflow_type=job_data.get('workflow_type'), 
            start_time=job_data.get('start_time'), 
            end_time=job_data.get('end_time'), 
            status=job_data.get('status'), 
            next_run_time=job_data.get('next_run_time')
        )
        
        db.session.add(job)
        db.session.commit()
        return job
    
    @staticmethod
    def create_hmda_job_tasks(job_id, job_tasks_data):
        """
        Create and save job tasks for a given HMDA job.

        :param job_id: The ID of the job to associate the tasks with
        :param job_tasks_data: A list of dictionaries, each containing data for a job task
        """
        
        job_tasks = []
        for task_data in job_tasks_data:
            job_tasks.append(
                JobTask(
                    job_id=job_id,
                    name=task_data['name'],
                    order=task_data['order'],
                    job_task_type=task_data['job_task_type'],   
                    status=task_data.get('status', "PENDING"),
                    started_at=task_data.get('started_at'),
                    completed_at=task_data.get('completed_at'),
                    retries=task_data.get('retries', 0),
                    meta=task_data.get('meta')
                )
            )
            
        # Save job tasks in bulk
        db.session.bulk_save_objects(job_tasks)
        db.session.commit()

    # Read operations
    @staticmethod
    def get_hmda_job_by_id(hmda_id):
        """
        Retrieve a job by its ID, including its associated tasks.

        :param hmda_id: ID of the HMDA job to retrieve
        :return: Job object with tasks loaded or None if not found
        """
        return Job.query.options(db.joinedload(Job.tasks)).get(hmda_id)
    
    @staticmethod
    def get_hmda_jobs(page=1, per_page=10, search=''):
        """
        Retrieve paginated HMDA jobs with optional search by job name or ID.

        :param page: Page number for pagination
        :param per_page: Number of items per page
        :param search: Optional search query for job name or ID
        :return: Paginated query result of HMDA jobs
        """
        query = Job.query.filter(Job.workflow_type == WorkflowType.HMDA.name)

        if search:
            search_lower = f"%{search.lower()}%"
            query = query.filter(
                or_(
                    func.lower(Job.name).like(search_lower),
                    func.cast(Job.id, String).like(search_lower)
                )
            )
        
        return query.order_by(Job.name.asc(), Job.id.asc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    @staticmethod
    def get_hmda_workflows():
        """
        Retrieve all workflows of type HMDA.

        :return: List of Workflow objects
        """
        return (Workflow.query
                .filter(Workflow.workflow_type == WorkflowType.HMDA.name)
                .order_by(Workflow.name.asc())
                .all())
      
    # Update operations
    @staticmethod
    def update_hmda_job(job_id, job_data):
        """
        Update a job with the provided data.

        :param job_id: ID of the job to update
        :param job_data: Fields to update on the job
        :return: Updated Job object
        """
        job_data['id'] = job_id
        job = Job(**job_data)
        db.session.merge(job)
        db.session.commit()
        return job

    @staticmethod
    def update_hmda_job_tasks(job_id, job_tasks_data):
        """
        Update job tasks for a given HMDA job.

        :param job_id: The ID of the job associated with the tasks
        :param job_tasks_data: A list of dictionaries containing task data to update
        """
        for task_data in job_tasks_data:
            task_id = task_data.pop('id')
            task = JobTask(
                id=task_id,
                job_id=job_id,
                name=task_data.get('name'),
                order=task_data.get('order'),
                job_task_type=task_data.get('job_task_type'),
                status=task_data.get('status'),
                started_at=task_data.get('started_at'),
                completed_at=task_data.get('completed_at'),
                retries=task_data.get('retries'),
                meta=task_data.get('meta')
            )
            db.session.merge(task)
        
        db.session.commit()

    # Delete operations
    @staticmethod
    def delete_hmda_job(job_id):
        """
        Delete a job by its ID.

        :param job_id: ID of the job to be deleted
        :raises ValueError: If job with the given ID is not found
        """
        job = Job.query.get(job_id)
        if not job:
            raise ValueError(f"Job with ID {job_id} not found")

        db.session.delete(job)
        db.session.commit()

    @staticmethod
    def execute_hmda_job_task(job_task_id):
        """
        Execute a HMDA job task.

        :param job_task_id: ID of the job task to execute
        """
        try:
            # Update the job task status to RUNNING first
            task = JobTask(id=job_task_id, status=JobTaskStatus.RUNNING.name)
            db.session.merge(task)
            db.session.commit()

            # Then dispatch the task
            HmdaTasks.process_hmda_error_checking({'job_task_id': job_task_id})
        except Exception as e:
            # If dispatch fails, update status to ERROR
            task = JobTask(id=job_task_id, status=JobTaskStatus.ERROR.name)
            db.session.merge(task)
            db.session.commit()
            app.logger.error(f"Failed to execute HMDA job task {job_task_id}: {str(e)}")
            raise  # Re-raise the exception after handling
        