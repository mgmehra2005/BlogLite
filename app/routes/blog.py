from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.forms import NewBlog
from app.models import Post, User
from app import db

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/post/new', methods=['GET', 'POST'])
def new_post():
    new_blog = NewBlog()

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if new_blog.validate_on_submit():
        title = new_blog.title.data
        body = new_blog.blog.data

        post = Post(title=title, body=body, author_id=User.query.filter_by(username=session['user']).first().id)
        db.session.add(post)
        db.session.commit()
        # flash('New Blog Created')
        return redirect(url_for('routes.home'))
    return render_template('new_post.html', blog_form=new_blog)