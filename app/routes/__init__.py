from flask import Blueprint, render_template, url_for, redirect, flash
from app.models import User, Post

general_bp = Blueprint('routes', __name__)

@general_bp.route('/')
def home():
    # Fetching Posts in the order of latest date to the oldest
    posts = Post.query.order_by(Post.created_at.desc()).all()
    
    flash('Do you have something in your mind share it with others', 'announcement')
    return render_template('home.html', posts=posts)