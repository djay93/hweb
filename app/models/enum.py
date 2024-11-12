from enum import Enum as PyEnum
from typing import List, Tuple

class JobStatus(PyEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    CANCELED = "CANCELED"

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        """Return choices for forms"""
        return [(status.name, status.value) for status in cls]


class StepStatus(PyEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    CANCELED = "CANCELED"
    SKIPPED = "SKIPPED"

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        """Return choices for forms"""
        return [(status.name, status.value) for status in cls]

class ScheduleType(PyEnum):
    AUTO = "Automated"
    MANUAL = "Manual"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        """Return choices for forms"""
        return [(type.name, type.value) for type in cls]

class WorkflowType(PyEnum):
    HMDA = "HMDA"
    EWRA = "EWRA"
    QUARTERLY_REVIEW = "Quarterly Review"

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        """Return choices for forms"""
        return [(type.name, type.value) for type in cls]

class WorkflowTaskType(PyEnum):
    AUTO = "Automated"
    MANUAL = "Manual"

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        """Return choices for forms"""
        return [(type.name, type.value) for type in cls]
