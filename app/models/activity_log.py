from datetime import datetime, timezone
from app.extensions import db

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflows.id', name='fk_activity_logs_workflow'), nullable=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id', name='fk_activity_logs_job'), nullable=True)
    activity_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=True, default="IN_PROGRESS")
    execution_time = db.Column(db.Float, nullable=True)
    triggered_by = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    message = db.Column(db.Text, nullable=True)
    payload = db.Column(db.JSON, nullable=True)  

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<ActivityLog id={self.id}, activity_type='{self.activity_type}', status='{self.status}'>"
