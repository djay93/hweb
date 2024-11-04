from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, HiddenField,DateTimeField, DateField
from wtforms.validators import DataRequired, Optional
from app.models.enum import WorkflowType, JobStatus

class HmdaProcessForm(FlaskForm):
    id = HiddenField('ID')
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])

    workflow_id = SelectField('Workflow', validators=[DataRequired()], coerce=int)
    workflow_type = SelectField(
        'Workflow Type',
        validators=[DataRequired()],
        choices=[(type.name, type.value) for type in WorkflowType])

    start_time = DateTimeField('Start Time', format='%Y-%m-%d %H:%M:%S', validators=[Optional()])
    end_time = DateTimeField('End Time', format='%Y-%m-%d %H:%M:%S', validators=[Optional()])

    status = SelectField(
        'Status',
        choices=[(status.name, status.value) for status in JobStatus],
        validators=[Optional()]
    )

    next_run_time = DateField('Next Run Time', format='%Y-%m-%d', validators=[Optional()])
