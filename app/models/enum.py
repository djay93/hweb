from enum import Enum, auto
from typing import List, Tuple

class JobStatus(Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    CANCELED = "CANCELED"

    @classmethod
    def choices(cls) -> List[dict]:
        return [{"name": type.name, "value": type.value} for type in cls]

class TaskStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    CANCELED = "CANCELED"
    SKIPPED = "SKIPPED"

    classmethod
    def choices(cls) -> List[dict]:
        return [{"name": type.name, "value": type.value} for type in cls]

class TriggerType(Enum):
    AUTO = "Automated"
    MANUAL = "Manual"

    @classmethod
    def choices(cls) -> List[dict]:
        return [{"name": type.name, "value": type.value} for type in cls]

class WorkflowType(Enum):
    HMDA = "HMDA"
    EWRA = "EWRA"
    QUARTERLY_REVIEW = "Quarterly Review"

    @classmethod
    def choices(cls) -> List[dict]:
        return [{"name": type.name, "value": type.value} for type in cls]

class ScheduleType(Enum):
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    YEARLY = "Yearly"

    @classmethod
    def choices(cls) -> List[dict]:
        return [{"name": type.name, "value": type.value} for type in cls]