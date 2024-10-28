from flask import Blueprint, render_template
from app.services.job_service import JobService  

hmda_bp = Blueprint('hmda', __name__)

@hmda_bp.route('/', methods=['GET'])
def index():
    jobs = JobService.get_hmda_jobs()
    return render_template('hmda/index.html', jobs=jobs)
