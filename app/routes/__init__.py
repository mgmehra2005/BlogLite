from flask import Blueprint, render_template, flash, request, redirect, url_for
from app.models import User, Post

general_bp = Blueprint('routes', __name__)

@general_bp.route('/')
def home():
    # Fetching Posts in the order of latest date to the oldest
    posts = Post.query.order_by(Post.created_at.desc()).all()
    
    flash('Do you have something in your mind share it with others', 'announcement')
    return render_template('home.html', posts=posts)

@general_bp.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        user_query = request.args.get('query')
        query_results = Post.query.where(Post.title.like(f"%{user_query}%")).all()
        return render_template('search.html', posts=query_results)
    return redirect(url_for('routes.home'))