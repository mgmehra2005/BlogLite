from flask import Blueprint, render_template, redirect, session, url_for, flash, request
from app.models import Post, Comments, User

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
def home():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    return redirect(url_for('dashboard.user_stats'))

@dashboard_bp.route('/dashboard/stats')
def user_stats():
    def append_comment_count(posts):
        new_array = []
        for p in posts:
            n = [p, len(Comments.query.filter_by(post_id=p.id).all())]
            new_array.append(n)
        return new_array

    if 'user' not in session:
        flash('Login is required', 'info')
        return redirect(url_for('auth.login'))

    post = Post.query.filter_by(author_id = User.query.filter_by(username = session['user']).first().id).all()
    return render_template('stats.html', posts=append_comment_count(post), total_comments=0)


@dashboard_bp.route('/dashboard/blogs')
def user_blogs():
    post = Post.query.filter_by(author_id = User.query.filter_by(username = session['user']).first().id).all()
    return render_template('user-blogs.html', posts=post)
