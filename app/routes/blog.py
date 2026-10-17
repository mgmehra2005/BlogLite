from flask import Blueprint, render_template, redirect, url_for, flash, request, session, Response
from app.forms import NewBlog, Comment
from app.models import Post, User, Comments
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

@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def fetch_post(post_id): 
    com = Comment()
    try:
        post = Post.query.get_or_404(post_id)
    except Exception as e:
        post = None
    
    if request.method == 'POST':
        if 'user' not in session:
            return redirect(url_for('auth.login'))

        if com.validate_on_submit():
            comment = com.comment.data
            db.session.add(Comments(comment=comment, post_id=post_id, author_id=User.query.filter_by(username=session['user']).first().id))
            db.session.commit()
            return redirect(url_for('blog.fetch_post', post_id=post_id))
        return Response("<h1>Page Not Found</h1>", mimetype="text/html")
    else:
        return render_template('post.html', post=post, comment_form=com, comments=Comments.query.filter_by(post_id=post_id).order_by(Comments.created_at.desc()).all()) if post!=None else Response('<h1>Requested URL not found.</h1>', mimetype='text/html')

@blog_bp.route('/post/update/<type><int:pid>')
def update_post_param(type, pid):    
    if request.method == 'GET':
        if type == 'view':
            post = Post.query.filter_by(id=pid).first()
            # print('before update', post.views)
            post.views += 1
            print('updated views on post id ', post.id)
            db.session.commit()
            return redirect(url_for('blog.fetch_post', post_id=pid))
        if type == 'like':
            if 'user' not in session:
                    return redirect(url_for('auth.login'))
            post = Post.query.filter_by(id=pid).first()
            post.likes += 1
            print('updated likes on post id ', post.id)
            db.session.commit()
            print("update like data ", [pid, type])
            return redirect(url_for('blog.fetch_post', post_id=pid))
        else:
            return Response('<h1>worng lane choosen</h1>', mimetype='text/html')
    else: 
        return Response('<h1>You are on the wrong road.</h1>', status=404, mimetype='text/html')

@blog_bp.route('/post/delete/<int:pid>')
def delete_post(pid):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    post = Post.query.filter_by(id=pid).first()
    if not post:
        flash('No post to delete', 'info')
        return redirect(url_for('dashboard.user_blogs'))
    else:
        if post.author.username == session['user']:
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('dashboard.user_blogs'))
        else:
            flash("You're not permitted to perform this action", 'danger')
            return redirect(url_for('dashboard.user_blogs'))

    