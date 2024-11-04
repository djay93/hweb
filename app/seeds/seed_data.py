from app.extensions import db
from app.models import Workflow, WorkflowTask, Job, JobStep, ActivityLog
from app.models.enum import WorkflowType, JobStatus, StepStatus, ScheduleType
from datetime import datetime, UTC

def seed_database():
    """Seed the database with initial data"""
    
    # Clear existing data
    JobStep.query.delete()
    Job.query.delete()
    WorkflowTask.query.delete()
    Workflow.query.delete()
    ActivityLog.query.delete()
    
    # Create timestamps for consistency
    workflow_timestamp = datetime(2024, 3, 1, tzinfo=UTC)
    task_timestamp = datetime(2024, 4, 11, tzinfo=UTC)
    job_timestamp = datetime(2024, 10, 28, tzinfo=UTC)
    step_timestamp = datetime(2024, 4, 11, tzinfo=UTC)
    
    # Create Workflows
    workflows = [
        Workflow(
            id=1,
            name="HMDA Weekly Processing",
            workflow_type=WorkflowType.HMDA_WEEKLY,
            description="Automated workflow for processing weekly HMDA data submissions, including validation, analysis, and report generation.",
            created_at=workflow_timestamp,
            updated_at=workflow_timestamp
        ),
        Workflow(
            id=2,
            name="Quarterly Compliance Review",
            workflow_type=WorkflowType.QUARTERLY_REVIEW,
            description="Comprehensive quarterly workflow for reviewing compliance metrics, generating reports, and identifying potential regulatory issues.",
            created_at=workflow_timestamp,
            updated_at=workflow_timestamp
        ),
        Workflow(
            id=3,
            name="EWRA Compliance Review",
            workflow_type=WorkflowType.EWRA,
            description="EWRA Compliance Review.",
            created_at=workflow_timestamp,
            updated_at=workflow_timestamp
        )
    ]
    
    # Add all workflows
    for workflow in workflows:
        try:
            db.session.add(workflow)
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding workflow {workflow.name}: {str(e)}")
            raise
    
    # Create Workflow Tasks
    workflow_tasks = [
        WorkflowTask(
            id=1,
            workflow_id=1,
            name="Data Collection",
            order=1,
            created_at=task_timestamp,
            updated_at=task_timestamp
        ),
        WorkflowTask(
            id=2,
            workflow_id=1,
            name="Data Validation",
            order=2,
            created_at=task_timestamp,
            updated_at=task_timestamp
        ),
        WorkflowTask(
            id=3,
            workflow_id=1,
            name="HMDA Format Conversion",
            order=3,
            created_at=task_timestamp,
            updated_at=task_timestamp
        ),
        WorkflowTask(
            id=4,
            workflow_id=1,
            name="Report Generation",
            order=4,
            created_at=task_timestamp,
            updated_at=task_timestamp
        ),
        WorkflowTask(
            id=5,
            workflow_id=1,
            name="Error Checking",
            order=5,
            created_at=task_timestamp,
            updated_at=task_timestamp
        ),
        WorkflowTask(
            id=6,
            workflow_id=1,
            name="Final Verification",
            order=6,
            created_at=task_timestamp,
            updated_at=task_timestamp
        )
    ]
    
    # Add all workflow tasks
    for task in workflow_tasks:
        try:
            db.session.add(task)
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding workflow task {task.name}: {str(e)}")
            raise
    
    # Create Jobs
    jobs = [
        Job(
            id=1,
            name="HMDA Weekly - 10/28/2024",
            workflow_id=1,
            workflow_type=WorkflowType.HMDA_WEEKLY,
            status=JobStatus.PENDING,
            start_time=None,
            end_time=None,
            created_at=job_timestamp,
            updated_at=job_timestamp
        )
    ]
    
    # Add all jobs
    for job in jobs:
        try:
            db.session.add(job)
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding job {job.name}: {str(e)}")
            raise
    
    # Create Job Steps
    job_steps = [
        JobStep(
            id=1,
            job_id=1,
            name="Data Collection",
            order=1,
            schedule_type=ScheduleType.MANUAL,
            status=StepStatus.PENDING,
            created_at=step_timestamp,
            updated_at=step_timestamp
        ),
        JobStep(
            id=2,
            job_id=1,
            name="Data Validation",
            order=2,
            schedule_type=ScheduleType.MANUAL,
            status=StepStatus.PENDING,
            created_at=step_timestamp,
            updated_at=step_timestamp
        ),
        JobStep(
            id=3,
            job_id=1,
            name="HMDA Format Conversion",
            order=3,
            schedule_type=ScheduleType.MANUAL,
            status=StepStatus.PENDING,
            created_at=step_timestamp,
            updated_at=step_timestamp
        ),
        JobStep(
            id=4,
            job_id=1,
            name="Report Generation",
            order=4,
            schedule_type=ScheduleType.MANUAL,
            status=StepStatus.PENDING,
            created_at=step_timestamp,
            updated_at=step_timestamp
        ),
        JobStep(
            id=5,
            job_id=1,
            name="Error Checking",
            order=5,
            schedule_type=ScheduleType.MANUAL,
            status=StepStatus.PENDING,
            created_at=step_timestamp,
            updated_at=step_timestamp
        ),
        JobStep(
            id=6,
            job_id=1,
            name="Final Verification",
            order=6,
            schedule_type=ScheduleType.MANUAL,
            status=StepStatus.PENDING,
            created_at=step_timestamp,
            updated_at=step_timestamp
        )
    ]

    # Add all job steps
    for step in job_steps:
        try:
            db.session.add(step)
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding job step {step.name}: {str(e)}")
            raise
    
    # Create Activity Log entries
    activity_logs = [
        ActivityLog(
            message="Database seeded with initial workflows",
            timestamp=workflow_timestamp,
            created_at=workflow_timestamp
        ),
        ActivityLog(
            message="Database seeded with workflow tasks",
            timestamp=task_timestamp,
            created_at=task_timestamp
        ),
        ActivityLog(
            message="Database seeded with initial jobs",
            timestamp=job_timestamp,
            created_at=job_timestamp
        ),
        ActivityLog(
            message="Database seeded with job steps",
            timestamp=step_timestamp,
            created_at=step_timestamp
        )
    ]
    
    for log in activity_logs:
        db.session.add(log)
    
    try:
        db.session.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error committing changes: {str(e)}")
        raise