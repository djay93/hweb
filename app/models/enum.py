from enum import Enum as PyEnum

class JobStatus(PyEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    CANCELED = "CANCELED"

class StepStatus(PyEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    CANCELED = "CANCELED"
    SKIPPED = "SKIPPED"

class ScheduleType(PyEnum):
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    MANUAL = "MANUAL"

class WorkflowType(PyEnum):
    HMDA_WEEKLY = "HMDA Weekly Processing"
    EWRA = "EWRA Processing"
    QUARTERLY_REVIEW = "Quarterly Review"
    TEST = "Test Workflow"