from enum import Enum as PyEnum

class JobStatus(PyEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    CANCELED = "canceled"

class StepStatus(PyEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    CANCELED = "canceled"

class ScheduleType(PyEnum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    MANUAL = "manual"

class WorkflowType(PyEnum):
    HMDA = "hmda"
    MORTGAGE = "mortgage"
    TEST = "test"