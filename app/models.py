from app import db
from datetime import datetime, timezone

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.id} {self.username}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    views = db.Column(db.Integer, nullable=False, default=0)
    likes = db.Column(db.Integer, nullable=False, default=0)
    author = db.relationship('User', backref=db.backref('post', cascade='all, delete-orphan', lazy='dynamic'))

    def __repr__(self):
        return f'<Post {self.id} {self.title}>'


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    # The post_id column is a foreign key that references the id column of the Post model. This establishes a relationship between the Comments and Post models, allowing you to associate comments with specific posts. The post relationship allows you to access the associated Post object from a Comment instance, and the backref creates a dynamic relationship from Post to its associated comments.
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    # The post relationship allows you to access the associated Post object from a Comment instance, and the backref creates a dynamic relationship from Post to its associated comments. The cascade='all, delete-orphan' option ensures that when a Post is deleted, all its associated Comments are also deleted. The lazy='dynamic' option allows you to query the comments for a post without loading them all at once.
    post = db.relationship('Post', backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))
    author = db.relationship('User', backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))

    def __repr__(self):
        return f'<Comment {self.id} {self.author} - {self.comment} on Post {self.post_id}>'
