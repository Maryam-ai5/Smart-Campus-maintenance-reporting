{% extends 'base.html' %}
{% block title %}Login — CampusFix{% endblock %}
{% block auth_content %}
<div class="auth-card">
    <div class="auth-logo">
        <i class="bi bi-buildings"></i>
        <h2>CampusFix</h2>
        <p>Smart Campus Maintenance System</p>
    </div>
    <form method="POST" action="{{ url_for('auth.login') }}" novalidate>
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        <div class="mb-3">
            <label for="email" class="form-label">Email Address</label>
            <div class="input-group">
                <span class="input-group-text"><i class="bi bi-envelope"></i></span>
                <input type="email" class="form-control" id="email" name="email" placeholder="you@university.edu" required>
            </div>
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <div class="input-group">
                <span class="input-group-text"><i class="bi bi-lock"></i></span>
                <input type="password" class="form-control" id="password" name="password" placeholder="Enter your password" required>
            </div>
        </div>
        <div class="mb-3 form-check">
            <input type="checkbox" class="form-check-input" id="remember" name="remember">
            <label class="form-check-label" for="remember" style="font-size:0.85rem;">Remember me</label>
        </div>
        <button type="submit" class="btn btn-primary-custom w-100 mb-3">
            <i class="bi bi-box-arrow-in-right me-2"></i>Sign In
        </button>
        <p class="text-center mb-0" style="font-size:0.875rem; color:var(--text-secondary);">
            Don't have an account? <a href="{{ url_for('auth.register') }}" style="color:var(--primary); font-weight:600;">Register here</a>
        </p>
    </form>
</div>
{% endblock %}
