from flask import Blueprint, render_template, redirect, session, url_for, flash, request

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard?<string:user>', methods=['GET'])
def home(user):
    if 'user' in session:
        return f"<h1>Welcome {user}, to the dashboard</h1>"
    else: 
        flash('You must be loggedin before accessing this url')
        return redirect(url_for('auth.login'))