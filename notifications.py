{% extends 'base.html' %}
{% block title %}Register — CampusFix{% endblock %}
{% block auth_content %}
<div class="auth-card">
    <div class="auth-logo">
        <i class="bi bi-buildings"></i>
        <h2>Create Account</h2>
        <p>Join the Campus Maintenance System</p>
    </div>
    <form method="POST" action="{{ url_for('auth.register') }}" novalidate>
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        <div class="mb-3">
            <label for="name" class="form-label">Full Name</label>
            <div class="input-group">
                <span class="input-group-text"><i class="bi bi-person"></i></span>
                <input type="text" class="form-control" id="name" name="name" placeholder="Ahmed Khan" value="{{ name|default('') }}" required minlength="2" maxlength="100">
            </div>
        </div>
        <div class="mb-3">
            <label for="email" class="form-label">Email Address</label>
            <div class="input-group">
                <span class="input-group-text"><i class="bi bi-envelope"></i></span>
                <input type="email" class="form-control" id="email" name="email" placeholder="you@university.edu" value="{{ email|default('') }}" required>
            </div>
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <div class="input-group">
                <span class="input-group-text"><i class="bi bi-lock"></i></span>
                <input type="password" class="form-control" id="password" name="password" placeholder="Min 8 characters" required minlength="8">
            </div>
        </div>
        <div class="mb-4">
            <label for="confirm_password" class="form-label">Confirm Password</label>
            <div class="input-group">
                <span class="input-group-text"><i class="bi bi-lock-fill"></i></span>
                <input type="password" class="form-control" id="confirm_password" name="confirm_password" placeholder="Repeat password" required>
            </div>
        </div>
        <button type="submit" class="btn btn-primary-custom w-100 mb-3">
            <i class="bi bi-person-plus me-2"></i>Create Account
        </button>
        <p class="text-center mb-0" style="font-size:0.875rem; color:var(--text-secondary);">
            Already have an account? <a href="{{ url_for('auth.login') }}" style="color:var(--primary); font-weight:600;">Sign in</a>
        </p>
    </form>
</div>
{% endblock %}
