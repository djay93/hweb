from flask import Blueprint, render_template
test_runs_bp = Blueprint('test_runs', __name__)

@test_runs_bp.route('/execute-tests')
def execute_tests():
    return render_template('test_runs/execute_tests.html')

@test_runs_bp.route('/test-progress')
def test_progress():
    return render_template('test_runs/test_progress.html')

@test_runs_bp.route('/test-results')
def test_results():
    return render_template('test_runs/test_results.html')