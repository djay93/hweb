from marshmallow import Schema, fields
import logging
from app.core.decorators import with_app_context
from app.tasks.hmda_error_checking_service import ErrorCheckingService

# Set up logging
logger = logging.getLogger(__name__)

class ErrorInputSchema(Schema):
    input_file_path = fields.String(required=True)
    sheet_name = fields.String(required=True)
    target_columns = fields.List(fields.String(), required=True)
    replacer_file_path = fields.String(required=True)
    remove_empty_rows = fields.Boolean(required=False)
    sort_columns = fields.List(fields.String(), required=False)

class HMDAErrorCheckingTaskSchema(Schema):
    job_task_id = fields.Integer(required=True)
    acaps = fields.Nested(ErrorInputSchema, required=True)

class HmdaTasks:
    def __init__(self, huey):
        self.huey = huey
        # Register tasks during initialization
        self.process_hmda_error_checking = self.huey.task(name='process_hmda_error_checking')(self.process_hmda_error_checking)
    
    @staticmethod
    @with_app_context
    def process_hmda_error_checking(args_dict):
        try:
            schema = HMDAErrorCheckingTaskSchema()
            data = schema.load(args_dict)
            job_task_id = data.get('job_task_id')
        
            error_checking_service = ErrorCheckingService(job_task_id)

            # process acaps
            acaps = data.get('acaps')
            error_checking_service.process_error_checking(
                input_file_path=acaps.get('input_file_path'),
                sheet_name=acaps.get('sheet_name'),
                target_columns=acaps.get('target_columns'),
                replacer_file_path=acaps.get('replacer_file_path'),
                remove_empty_rows=acaps.get('remove_empty_rows'),
                sort_columns=acaps.get('sort_columns')
            )
        except Exception as e:
            logger.error(f"Error processing HMDA error checking for job_task_id={data.get('job_task_id', 'unknown')}: {str(e)}", exc_info=True)
            raise
