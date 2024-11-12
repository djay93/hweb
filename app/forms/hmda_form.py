from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, HiddenField,DateTimeField, DateField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired, Optional
from app.models.enum import WorkflowType, JobStatus, ScheduleType, StepStatus
from app.services import HMDAService
from datetime import datetime

class HmdaJobDetailsForm(FlaskForm):
    id = HiddenField('ID')
    name = StringField('Name', id='name', render_kw={"placeholder": "Enter process name"})
    description = TextAreaField('Description', render_kw={"placeholder": "Enter process description"})

    workflow_type = SelectField('Automation Type', choices=WorkflowType.choices(), default=WorkflowType.HMDA.name)
    workflow_id = SelectField('Workflow', coerce=int)
    status = SelectField('Status', choices=JobStatus.choices())
    
    start_time = DateTimeField('Start Time', format='%Y-%m-%d')
    end_time = DateTimeField('End Time', format='%Y-%m-%d')
    next_run_time = DateField('Process Start Date', format='%Y-%m-%d')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = kwargs.get('obj')
        
        # Set dynamic choices
        self.workflow_id.choices = [(w.id, w.name) for w in HMDAService.get_hmda_workflows()]

        # Handle datetime conversion for next_run_time
        if self.next_run_time.data and isinstance(self.next_run_time.data, datetime):
            self.next_run_time.data = self.next_run_time.data.date()
        
        # Handle dropdown values
        if self.obj and hasattr(self.obj, 'status'):
            self.status.data = self.obj.status.name
