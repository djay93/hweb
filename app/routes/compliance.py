from flask import Blueprint, render_template

compliance_bp = Blueprint('compliance', __name__)

@compliance_bp.route('/test-scenarios')
def test_scenarios():
    return render_template('compliance/test_scenarios.html')

@compliance_bp.route('/test-library')
def test_library():
    return render_template('compliance/test_library.html')

@compliance_bp.route('/schedule-tests')
def schedule_tests():
    return render_template('compliance/schedule_tests.html')

@compliance_bp.route('/test-calendar')
def test_calendar():
    return render_template('compliance/test_calendar.html')

@compliance_bp.route('/issue-tracker')
def issue_tracker():
    return render_template('compliance/issue_tracker.html')
