from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    """Redirect root to login or dashboard based on auth status."""
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'maintenance':
            return redirect(url_for('maintenance.panel'))
        else:
            return redirect(url_for('student.dashboard'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            if not user.is_active_user:
                flash('Your account has been deactivated. Contact an administrator.', 'danger')
                return render_template('auth/login.html')

            login_user(user, remember=remember)
            flash(f'Welcome back, {user.name}!', 'success')

            # Redirect based on role
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'maintenance':
                return redirect(url_for('maintenance.panel'))
            else:
                return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration (student role only)."""
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        errors = []
        if not name or len(name) < 2 or len(name) > 100:
            errors.append('Name must be between 2 and 100 characters.')
        if not email or '@' not in email:
            errors.append('Please enter a valid email address.')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        if password != confirm_password:
            errors.append('Passwords do not match.')

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            errors.append('An account with this email already exists.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html', name=name, email=email)

        # Create new user
        new_user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            role='student'
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Log the user out."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
