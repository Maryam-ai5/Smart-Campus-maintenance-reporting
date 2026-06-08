from datetime import date, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user
from werkzeug.security import generate_password_hash
from app import db
from app.models import Report, Category, User, ReportUpdate
from app.utils.decorators import role_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/dashboard')
@role_required('admin')
def dashboard():
    total = Report.query.count()
    open_count = Report.query.filter(Report.status != 'resolved').count()
    resolved = Report.query.filter_by(status='resolved').count()
    resolution_rate = round((resolved / total * 100), 1) if total > 0 else 0

    # Reports by category
    cats = Category.query.all()
    cat_labels = [c.name for c in cats]
    cat_data = [Report.query.filter_by(category_id=c.id).count() for c in cats]

    # Urgency distribution
    urg_high = Report.query.filter_by(urgency='high').count()
    urg_med = Report.query.filter_by(urgency='medium').count()
    urg_low = Report.query.filter_by(urgency='low').count()

    # Reports over last 7 days
    today = date.today()
    daily_labels = []
    daily_submitted = []
    daily_resolved = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        daily_labels.append(d.strftime('%b %d'))
        daily_submitted.append(Report.query.filter(db.func.date(Report.created_at) == d).count())
        daily_resolved.append(Report.query.filter(Report.status == 'resolved', db.func.date(Report.updated_at) == d).count())

    # Open vs Closed by category
    open_by_cat = [Report.query.filter(Report.category_id == c.id, Report.status != 'resolved').count() for c in cats]
    closed_by_cat = [Report.query.filter(Report.category_id == c.id, Report.status == 'resolved').count() for c in cats]

    # Recent activity
    recent_activity = ReportUpdate.query.order_by(ReportUpdate.timestamp.desc()).limit(10).all()

    return render_template('admin/dashboard.html',
        total=total, open_count=open_count, resolved=resolved, resolution_rate=resolution_rate,
        cat_labels=cat_labels, cat_data=cat_data,
        urg_high=urg_high, urg_med=urg_med, urg_low=urg_low,
        daily_labels=daily_labels, daily_submitted=daily_submitted, daily_resolved=daily_resolved,
        open_by_cat=open_by_cat, closed_by_cat=closed_by_cat,
        recent_activity=recent_activity)


@admin_bp.route('/admin/users')
@role_required('admin')
def users():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    role_filter = request.args.get('role', '')

    query = User.query
    if search:
        query = query.filter(db.or_(User.name.ilike(f'%{search}%'), User.email.ilike(f'%{search}%')))
    if role_filter:
        query = query.filter_by(role=role_filter)

    users_page = query.order_by(User.created_at.desc()).paginate(page=page, per_page=15, error_out=False)
    return render_template('admin/users.html', users=users_page, search=search, role_filter=role_filter)


@admin_bp.route('/admin/users/add', methods=['POST'])
@role_required('admin')
def add_user():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    role = request.form.get('role', 'student')

    if not name or not email or not password:
        flash('All fields are required.', 'danger')
        return redirect(url_for('admin.users'))
    if User.query.filter_by(email=email).first():
        flash('Email already exists.', 'danger')
        return redirect(url_for('admin.users'))
    if role not in ('student', 'maintenance', 'admin'):
        flash('Invalid role.', 'danger')
        return redirect(url_for('admin.users'))

    user = User(name=name, email=email, password_hash=generate_password_hash(password), role=role)
    db.session.add(user)
    db.session.commit()
    flash(f'User {name} created successfully.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/admin/users/<int:user_id>/role', methods=['POST'])
@role_required('admin')
def change_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role', '')
    if new_role not in ('student', 'maintenance', 'admin'):
        flash('Invalid role.', 'danger')
        return redirect(url_for('admin.users'))
    user.role = new_role
    db.session.commit()
    flash(f'{user.name} role changed to {new_role}.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/admin/users/<int:user_id>/toggle', methods=['POST'])
@role_required('admin')
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot deactivate your own account.', 'danger')
        return redirect(url_for('admin.users'))
    user.is_active_user = not user.is_active_user
    db.session.commit()
    status = 'activated' if user.is_active_user else 'deactivated'
    flash(f'{user.name} has been {status}.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/admin/categories')
@role_required('admin')
def categories():
    cats = Category.query.order_by(Category.name).all()
    return render_template('admin/categories.html', categories=cats)


@admin_bp.route('/admin/categories/add', methods=['POST'])
@role_required('admin')
def add_category():
    name = request.form.get('name', '').strip()
    icon = request.form.get('icon', '🔧').strip()
    description = request.form.get('description', '').strip()

    if not name:
        flash('Category name is required.', 'danger')
        return redirect(url_for('admin.categories'))
    if Category.query.filter_by(name=name).first():
        flash('Category already exists.', 'danger')
        return redirect(url_for('admin.categories'))

    cat = Category(name=name, icon=icon, description=description)
    db.session.add(cat)
    db.session.commit()
    flash(f'Category "{name}" added.', 'success')
    return redirect(url_for('admin.categories'))


@admin_bp.route('/admin/categories/<int:cat_id>/toggle', methods=['POST'])
@role_required('admin')
def toggle_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    cat.is_active = not cat.is_active
    db.session.commit()
    status = 'enabled' if cat.is_active else 'disabled'
    flash(f'Category "{cat.name}" {status}.', 'success')
    return redirect(url_for('admin.categories'))
