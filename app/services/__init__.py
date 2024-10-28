from .workflow_service import WorkflowService
from .job_service import JobService

workflow_service = WorkflowService()
job_service = JobService()

__all__ = [
    'WorkflowService',
    'JobService'
]
