from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired
from app.models.enum import WorkflowType 

class WorkflowForm(FlaskForm):
    id = HiddenField('ID')
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    workflow_type = SelectField(
        'Workflow Type',
        validators=[DataRequired()],
        choices=[(type.name, type.value) for type in WorkflowType]
    )  
