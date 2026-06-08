from app import db
from app.models import Notification, User


def create_notification(user_id, report_id, message):
    """Create a single notification for a user."""
    notification = Notification(
        user_id=user_id,
        report_id=report_id,
        message=message
    )
    db.session.add(notification)
    db.session.commit()
    return notification


def notify_admins(report_id, message):
    """Send a notification to all admin users."""
    admins = User.query.filter_by(role='admin', is_active_user=True).all()
    for admin in admins:
        notif = Notification(
            user_id=admin.id,
            report_id=report_id,
            message=message
        )
        db.session.add(notif)
    db.session.commit()


def notify_maintenance(report_id, message):
    """Send a notification to all maintenance team members."""
    team = User.query.filter_by(role='maintenance', is_active_user=True).all()
    for member in team:
        notif = Notification(
            user_id=member.id,
            report_id=report_id,
            message=message
        )
        db.session.add(notif)
    db.session.commit()


def get_unread_count(user_id):
    """Return the count of unread notifications for a user."""
    return Notification.query.filter_by(user_id=user_id, is_read=False).count()
