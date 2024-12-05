from flask import Blueprint, render_template
help_bp = Blueprint('help', __name__)

@help_bp.route('/documentation')
def documentation():
    return render_template('help/documentation.html')

@help_bp.route('/faqs')
def faqs():
    return render_template('help/faqs.html')

@help_bp.route('/contact')
def contact_support():
    return render_template('help/contact_support.html')