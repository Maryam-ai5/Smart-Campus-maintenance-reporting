from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Report, Category, ReportUpdate
from app.utils.decorators import role_required
from app.utils.notifications import create_notification

maintenance_bp = Blueprint('maintenance', __name__)


@maintenance_bp.route('/maintenance/panel')
@role_required('maintenance', 'admin')
def panel():
    status_filter = request.args.get('status', '')
    category_filter = request.args.get('category', '')
    urgency_filter = request.args.get('urgency', '')
    sort = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)

    query = Report.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if category_filter:
        query = query.filter_by(category_id=int(category_filter))
    if urgency_filter:
        query = query.filter_by(urgency=urgency_filter)

    if sort == 'oldest':
        query = query.order_by(Report.created_at.asc())
    elif sort == 'priority':
        from sqlalchemy import case
        priority_order = case(
            (Report.urgency == 'high', 1),
            (Report.urgency == 'medium', 2),
            (Report.urgency == 'low', 3),
        )
        query = query.order_by(priority_order, Report.created_at.desc())
    else:
        query = query.order_by(Report.created_at.desc())

    reports = query.paginate(page=page, per_page=15, error_out=False)

    open_count = Report.query.filter(Report.status.in_(['submitted', 'assigned', 'in_progress'])).count()
    high_priority = Report.query.filter(Report.urgency == 'high', Report.status != 'resolved').count()
    resolved_today = Report.query.filter(
        Report.status == 'resolved',
        db.func.date(Report.updated_at) == date.today()
    ).count()

    categories = Category.query.filter_by(is_active=True).all()
    return render_template('maintenance/panel.html',
        reports=reports, categories=categories,
        open_count=open_count, high_priority=high_priority, resolved_today=resolved_today,
        status_filter=status_filter, category_filter=category_filter,
        urgency_filter=urgency_filter, sort=sort)


@maintenance_bp.route('/maintenance/update-status/<int:report_id>', methods=['POST'])
@role_required('maintenance', 'admin')
def update_status(report_id):
    report = Report.query.get_or_404(report_id)
    new_status = request.form.get('status', '')
    note = request.form.get('note', '').strip()

    valid_statuses = ['submitted', 'assigned', 'in_progress', 'resolved']
    if new_status not in valid_statuses:
        flash('Invalid status.', 'danger')
        return redirect(request.referrer or url_for('maintenance.panel'))

    old_status = report.status
    report.status = new_status
    db.session.commit()

    update = ReportUpdate(
        report_id=report.id, updated_by=current_user.id,
        old_status=old_status, new_status=new_status,
        note=note or f"Status changed to {new_status.replace('_', ' ').title()}"
    )
    db.session.add(update)
    db.session.commit()

    status_label = new_status.replace('_', ' ').title()
    create_notification(report.user_id, report.id,
        f"Report #{report.id} has been updated to {status_label}")

    flash(f'Report #{report.id} updated to {status_label}.', 'success')
    return redirect(request.referrer or url_for('maintenance.panel'))
