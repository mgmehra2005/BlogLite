from flask import Blueprint, render_template, url_for, redirect

general_bp = Blueprint('routes', __name__)

@general_bp.route('/')
def home():
    return render_template('home.html')