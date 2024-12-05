from flask import Blueprint, render_template

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/compliance-reports')
def compliance_reports():
    return render_template('reports/compliance_reports.html')

@reports_bp.route('/outcome-analysis')
def outcome_analysis():
    return render_template('reports/outcome_analysis.html')

@reports_bp.route('/audit-logs')
def audit_logs():
    return render_template('reports/audit_logs.html')