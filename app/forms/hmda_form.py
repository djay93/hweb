from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField, DateTimeField, DateField
from wtforms.validators import Optional
from app.models.enum import WorkflowType, JobStatus
from app.services import HMDAService
from datetime import datetime

class HmdaJobDetailsForm(FlaskForm):
    id = HiddenField('ID')
    name = StringField('Name', id='name', render_kw={"placeholder": "Enter process name"})
    
    # Define select fields with type coercion and initial choices from enums
    workflow_type = SelectField('Automation Type', choices=WorkflowType.choices(), coerce=str, default=WorkflowType.HMDA.name)
    workflow_id = SelectField('Workflow', coerce=int)
    status = SelectField('Status', choices=JobStatus.choices(), coerce=str, default=JobStatus.NEW.name)

    # Define date and datetime fields with formats
    start_time = DateTimeField('Start Time', format='%Y-%m-%d %H:%M:%S', validators=[Optional()])
    end_time = DateTimeField('End Time', format='%Y-%m-%d %H:%M:%S', validators=[Optional()])
    next_run_time = DateField('Job Start Date', format='%Y-%m-%d', validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = kwargs.get('obj')

        # Dynamically load workflow choices
        self.workflow_id.choices = [(w.id, w.name) for w in HMDAService.get_hmda_workflows()]

        # Convert next_run_time to date if it's a datetime object
        if self.next_run_time.data and isinstance(self.next_run_time.data, datetime):
            self.next_run_time.data = self.next_run_time.data.date()

        # Set initial dropdown values based on the provided object
        if self.obj:
            if hasattr(self.obj, 'status') and self.obj.status:
                self.status.data = self.obj.status.name
            if hasattr(self.obj, 'workflow_type') and self.obj.workflow_type:
                self.workflow_type.data = self.obj.workflow_type.name
