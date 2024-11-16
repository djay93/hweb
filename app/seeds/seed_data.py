from app.extensions import db
from app.models import Workflow, WorkflowTask, Job, JobTask, ActivityLog
from app.models.enum import WorkflowType, TaskStatus, TriggerType, TriggerType
from datetime import datetime, UTC

def seed_database():
    """Seed the database with initial data"""
    
    # Clear existing data
    _clear_existing_data()
    
    # Create timestamps for consistency
    timestamps = _create_timestamps()
    
    # Create and add workflows
    _create_workflows(timestamps['workflow'])
    
    # Create and add workflow tasks
    _create_workflow_tasks(timestamps['task'])
    
    # Create and add jobs
    _create_jobs(timestamps['job'])
    
    # Create and add job tasks
    _create_job_tasks(timestamps['task'])
    
    # Create and add activity logs
    _create_activity_logs(timestamps)
    
    try:
        db.session.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error committing changes: {str(e)}")
        raise

def _clear_existing_data():
    """Clear all existing data from relevant tables"""
    JobTask.query.delete()
    Job.query.delete()
    WorkflowTask.query.delete()
    Workflow.query.delete()
    ActivityLog.query.delete()

def _create_timestamps():
    """Create consistent timestamps for all entities"""
    return {
        'workflow': datetime(2024, 3, 1, tzinfo=UTC),
        'task': datetime(2024, 4, 11, tzinfo=UTC),
        'job': datetime(2024, 10, 28, tzinfo=UTC),
        'task': datetime(2024, 4, 11, tzinfo=UTC)
    }

def _create_workflows(timestamp):
    """Create and add initial workflows"""
    workflows = [
        Workflow(
            id=1,
            name="HMDA Weekly Processing",
            workflow_type=WorkflowType.HMDA.name,
            description="Automated workflow for processing weekly HMDA data submissions, including validation, analysis, and report generation.",
            created_at=timestamp,
            updated_at=timestamp
        ),
        Workflow(
            id=2,
            name="Quarterly Compliance Review",
            workflow_type=WorkflowType.QUARTERLY_REVIEW.name,
            description="Comprehensive quarterly workflow for reviewing compliance metrics, generating reports, and identifying potential regulatory issues.",
            created_at=timestamp,
            updated_at=timestamp
        ),
        Workflow(
            id=3,
            name="EWRA Compliance Review",
            workflow_type=WorkflowType.EWRA.name,
            description="EWRA Compliance Review.",
            created_at=timestamp,
            updated_at=timestamp
        )
    ]
    
    for workflow in workflows:
        try:
            db.session.add(workflow)
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding workflow {workflow.name}: {str(e)}")
            raise

def _create_workflow_tasks(timestamp):
    """Create and add workflow tasks"""
    tasks = [
        # HMDA Weekly Processing Tasks (workflow_id=1)
        {"id": 1, "name": "Export HMDA", "task_type": TriggerType.MANUAL.name, "order": 1},
        {"id": 2, "name": "Export CRA", "task_type": TriggerType.MANUAL.name, "order": 2},
        {"id": 3, "name": "Run Weekly Batch Job #1", "task_type": TriggerType.AUTO.name, "order": 3},
        {"id": 4, "name": "Run CRA data creation EG Job (SAS Grid)", "task_type": TriggerType.AUTO.name, "order": 4},
        {"id": 5, "name": "Run Weekly Batch Job #2", "task_type": TriggerType.AUTO.name, "order": 5},
        {"id": 6, "name": "Download NMLSID from Workday", "task_type": TriggerType.MANUAL.name, "order": 6},
        {"id": 7, "name": "Update LITE Auto Spreadsheet & Save CSV", "task_type": TriggerType.MANUAL.name, "order": 7},
        {"id": 8, "name": "Run Lite Auto data creation EG job (SAS Grid)", "task_type": TriggerType.AUTO.name, "order": 8},
        {"id": 9, "name": "Import ACAPS into RISK_EXEC", "task_type": TriggerType.MANUAL.name, "order": 9},
        {"id": 10, "name": "Import DOTNET_HMDA22 into RISK_EXEC", "task_type": TriggerType.MANUAL.name, "order": 10},
        {"id": 11, "name": "Import Lite_Auto RISK_EXEC", "task_type": TriggerType.MANUAL.name, "order": 11},
        {"id": 12, "name": "Calculate ULI for Lite Auto", "task_type": TriggerType.MANUAL.name, "order": 12},
        {"id": 13, "name": "Manual Review by Terry, Amy and Laura", "task_type": TriggerType.MANUAL.name, "order": 13},
        {"id": 14, "name": "GeoCode HMDA and calculate HMDA Fields", "task_type": TriggerType.MANUAL.name, "order": 14},
        {"id": 15, "name": "Export HMDA", "task_type": TriggerType.MANUAL.name, "order": 15},
        {"id": 16, "name": "Import ACT (Ascentium) into RISK_EXEC", "task_type": TriggerType.MANUAL.name, "order": 16},
        {"id": 17, "name": "Import ACLS into RISK_EXEC", "task_type": TriggerType.MANUAL.name, "order": 17},
        {"id": 18, "name": "Import AFS into RISK_EXEC", "task_type": TriggerType.MANUAL.name, "order": 18},
        {"id": 19, "name": "Import TSYS into RISK_EXEC", "task_type": TriggerType.MANUAL.name, "order": 19},
        {"id": 20, "name": "Import AFS_Exclude into RISK_EXEC", "task_type": TriggerType.MANUAL.name, "order": 20},
        {"id": 21, "name": "GeoCode CRA and calculate CRA fields", "task_type": TriggerType.MANUAL.name, "order": 21},
        {"id": 22, "name": "Export CRA", "task_type": TriggerType.MANUAL.name, "order": 22},
        {"id": 23, "name": "Copy COMMDEV and RENEWALS to Q:", "task_type": TriggerType.MANUAL.name, "order": 23},
        {"id": 24, "name": "Run Data Integrity EG Job", "task_type": TriggerType.AUTO.name, "order": 24},
        {"id": 25, "name": "Run Weekly Errors Batch Job", "task_type": TriggerType.AUTO.name, "order": 25},
        {"id": 26, "name": "Perform ERROR CHECKING for ACAPS, EMPOWER, LITE AUTO", "task_type": TriggerType.AUTO.name, "order": 26},
        {"id": 27, "name": "Send Email", "task_type": TriggerType.AUTO.name, "order": 27},
    ]
    
    for task_data in tasks:
        task = WorkflowTask(
            id=task_data["id"],
            workflow_id=1,  # All tasks currently belong to HMDA Weekly workflow
            name=task_data["name"],
            task_type=task_data["task_type"],
            order=task_data["order"],
            created_at=timestamp,
            updated_at=timestamp
        )
        try:
            db.session.add(task)
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding workflow task {task.name}: {str(e)}")
            raise

def _create_jobs(timestamp):
    """Create and add initial jobs"""
    jobs = []
    
    for job in jobs:
        try:
            db.session.add(job)
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding job {job.name}: {str(e)}")
            raise

def _create_job_tasks(timestamp):
    """Create and add job tasks"""
    tasks = []
    
    for task_data in tasks:
        task = JobTask(
            id=task_data["id"],
            job_id=1,
            name=task_data["name"],
            order=task_data["order"],
            job_task_type=TriggerType.MANUAL,
            status=TaskStatus.PENDING,
            created_at=timestamp,
            updated_at=timestamp
        )
        try:
            db.session.add(task)
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding job task {task.name}: {str(e)}")
            raise

def _create_activity_logs(timestamps):
    """Create and add activity log entries"""
    logs = [
        {"message": "Database seeded with initial workflows", "timestamp": timestamps['workflow']},
        {"message": "Database seeded with workflow tasks", "timestamp": timestamps['task']},
        {"message": "Database seeded with initial jobs", "timestamp": timestamps['job']},
        {"message": "Database seeded with job tasks", "timestamp": timestamps['task']}
    ]
    
    # for log_data in logs:
    #     log = ActivityLog(
    #         message=log_data["message"],
    #         user_id=1,
    #         # timestamp=log_data["timestamp"],
    #         created_at=log_data["timestamp"]
    #     )
    #     db.session.add(log)