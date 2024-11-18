from marshmallow import Schema, fields
from app.utils.huey_config import huey
import logging

# Set up logging
logger = logging.getLogger(__name__)

class HMDATaskArgsSchema(Schema):
    job_task_id = fields.Integer(required=True)

class HmdaTasks:
    @staticmethod
    @huey.task()
    def process_hmda_error_checking(args_dict):
        logging.info("Processing HMDA error checking")
        logging.info(args_dict)
        schema = HMDATaskArgsSchema()
        data = schema.load(args_dict)
        job_task_id = data.get('job_task_id')
        logging.info(f"Job task ID: {job_task_id}")
