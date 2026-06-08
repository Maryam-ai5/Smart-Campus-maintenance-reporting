from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # student, maintenance, admin
    is_active_user = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    reports = db.relationship('Report', backref='reporter', lazy='dynamic', foreign_keys='Report.user_id')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    updates = db.relationship('ReportUpdate', backref='updater', lazy='dynamic')

    @property
    def is_active(self):
        return self.is_active_user

    def __repr__(self):
        return f'<User {self.name} ({self.role})>'


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    icon = db.Column(db.String(10), default='🔧')
    description = db.Column(db.String(255), default='')
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    reports = db.relationship('Report', backref='category_ref', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.icon} {self.name}>'


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    urgency = db.Column(db.String(20), nullable=False, default='medium')  # low, medium, high
    photo_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='submitted')  # submitted, assigned, in_progress, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    updates = db.relationship('ReportUpdate', backref='report', lazy='dynamic', order_by='ReportUpdate.timestamp.asc()')
    notifications = db.relationship('Notification', backref='report', lazy='dynamic')

    @property
    def status_step(self):
        """Return numeric step for progress bar (1-4)."""
        steps = {'submitted': 1, 'assigned': 2, 'in_progress': 3, 'resolved': 4}
        return steps.get(self.status, 1)

    @property
    def status_label(self):
        """Return human-readable status label."""
        labels = {
            'submitted': 'Submitted',
            'assigned': 'Assigned',
            'in_progress': 'In Progress',
            'resolved': 'Resolved'
        }
        return labels.get(self.status, self.status)

    @property
    def urgency_label(self):
        """Return human-readable urgency label."""
        return self.urgency.capitalize()

    def __repr__(self):
        return f'<Report #{self.id} [{self.status}]>'


class ReportUpdate(db.Model):
    __tablename__ = 'report_updates'

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    old_status = db.Column(db.String(20), nullable=True)
    new_status = db.Column(db.String(20), nullable=False)
    note = db.Column(db.Text, default='')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ReportUpdate report={self.report_id} {self.old_status}->{self.new_status}>'


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=True)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Notification user={self.user_id} read={self.is_read}>'
