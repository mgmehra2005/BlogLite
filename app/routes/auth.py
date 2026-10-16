from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.forms import RegistrationForm, LoginForm
from app.models import User
from app import db
import hashlib

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    # print("Login form data:", login_form.data)  # Debugging statement to print form data
    if 'user' in session:
        return redirect(url_for('routes.home', user=session['user']))

    if login_form.validate_on_submit():
        # Handle login logic here
        username = login_form.username.data
        password = login_form.password.data

        if User.query.filter_by(username=username).first():
            user = User.query.filter_by(username=username).first()
            # print(str(user.password) == hashlib.md5(password.encode('utf-8')).hexdigest(), "-", hashlib.md5(password.encode('utf-8')).hexdigest() ,"-", user.password)
            if str(user.password) == hashlib.md5(password.encode('utf-8')).hexdigest():
                session['user'] = username
                return redirect(url_for('routes.home', user=username))
            else:
                flash('Invalid password. Please try again.', 'danger')
        else:
            flash('User not found.', 'info')
            return redirect(url_for('auth.login'))
    return render_template('login.html', form=login_form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    if 'user' in session:
            return redirect(url_for('routes.home', user=session['user']))
    
    if register_form.validate_on_submit():
        # Handle registration logic here
        username = register_form.username.data or "new_user"
        password = register_form.password.data or "default_password"
        email = register_form.email.data or 'none'


        if not User.query.filter_by(username=username).first():
            new_user = User(username=username, password=hashlib.md5(password.encode('utf-8')).hexdigest(), email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('User already exists.', 'info')
    return render_template('register.html', form=register_form)

@auth_bp.route('/logout')
def logout():
    if 'user' not in session:
        return redirect(url_for('auth.login'))    
    session.pop('user')
    return redirect(url_for('auth.login'))