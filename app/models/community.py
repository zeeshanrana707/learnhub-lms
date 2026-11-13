from datetime import datetime, timezone
from app.extensions import db

def utcnow():
    return datetime.now(timezone.utc)

class ForumThread(db.Model):
    __tablename__ = 'forum_threads'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    is_pinned = db.Column(db.Boolean, default=False, nullable=False)
    is_locked = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    course = db.relationship('Course', back_populates='forum_threads')
    author = db.relationship('User', back_populates='forum_threads')
    posts = db.relationship('ForumPost', back_populates='thread', cascade='all, delete-orphan', lazy='select', order_by='ForumPost.created_at.asc()')

    def __repr__(self):
        return f'<ForumThread {self.title}>'


class ForumPost(db.Model):
    __tablename__ = 'forum_posts'

    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('forum_threads.id', ondelete='CASCADE'), nullable=False, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id', ondelete='CASCADE'), nullable=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    thread = db.relationship('ForumThread', back_populates='posts')
    author = db.relationship('User', back_populates='forum_posts')
    parent = db.relationship('ForumPost', remote_side=[id], back_populates='replies')
    replies = db.relationship('ForumPost', back_populates='parent', cascade='all, delete-orphan', lazy='select')
    likes = db.relationship('PostLike', back_populates='post', cascade='all, delete-orphan', lazy='select')

    @property
    def like_count(self) -> int:
        return len(self.likes)

    def is_liked_by(self, user_id: int) -> bool:
        return any(like.user_id == user_id for like in self.likes)

    def __repr__(self):
        return f'<ForumPost {self.id} on Thread {self.thread_id}>'


class PostLike(db.Model):
    __tablename__ = 'post_likes'
    __table_args__ = (
        db.UniqueConstraint('post_id', 'user_id', name='uq_post_like'),
    )

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    post = db.relationship('ForumPost', back_populates='likes')
    user = db.relationship('User', back_populates='post_likes')


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    subject = db.Column(db.String(150), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], back_populates='received_messages')

    def __repr__(self):
        return f'<Message from {self.sender_id} to {self.recipient_id}: {self.subject}>'
