{% extends 'base.html' %}
{% block title %}Profile — CampusFix{% endblock %}
{% block page_title %}My Profile{% endblock %}
{% block content %}
<div class="animate-in" style="max-width:720px;">
    <div class="content-card mb-4">
        <div class="card-header-custom"><h5><i class="bi bi-person-circle me-2"></i>Profile Information</h5></div>
        <div class="card-body-custom">
            <form method="POST">
                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                <input type="hidden" name="action" value="update_profile">
                <div class="mb-3">
                    <label for="name" class="form-label">Full Name</label>
                    <input type="text" class="form-control" id="name" name="name" value="{{ current_user.name }}" required minlength="2" maxlength="100">
                </div>
                <div class="mb-3">
                    <label class="form-label">Email Address</label>
                    <input type="email" class="form-control" value="{{ current_user.email }}" disabled>
                    <div class="form-text">Email cannot be changed.</div>
                </div>
                <div class="mb-3">
                    <label class="form-label">Role</label>
                    <div><span class="badge-status badge-role-{{ current_user.role }}">{{ current_user.role|capitalize }}</span></div>
                </div>
                <div class="mb-3">
                    <label class="form-label">Member Since</label>
                    <p class="mb-0">{{ current_user.created_at.strftime('%B %d, %Y') }}</p>
                </div>
                <button type="submit" class="btn btn-primary-custom"><i class="bi bi-check2 me-2"></i>Save Changes</button>
            </form>
        </div>
    </div>
    <div class="content-card mb-4">
        <div class="card-header-custom"><h5><i class="bi bi-lock me-2"></i>Change Password</h5></div>
        <div class="card-body-custom">
            <form method="POST">
                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                <input type="hidden" name="action" value="change_password">
                <div class="mb-3"><label class="form-label">Current Password</label><input type="password" class="form-control" name="current_password" required></div>
                <div class="mb-3"><label class="form-label">New Password</label><input type="password" class="form-control" name="new_password" required minlength="8"></div>
                <div class="mb-3"><label class="form-label">Confirm New Password</label><input type="password" class="form-control" name="confirm_password" required></div>
                <button type="submit" class="btn btn-primary-custom"><i class="bi bi-shield-lock me-2"></i>Update Password</button>
            </form>
        </div>
    </div>
    <div class="content-card">
        <div class="card-header-custom"><h5><i class="bi bi-bar-chart me-2"></i>Activity Summary</h5></div>
        <div class="card-body-custom">
            <div class="row g-3">
                <div class="col-4 text-center">
                    <div class="stat-value" style="font-size:1.5rem;">{{ total_reports }}</div>
                    <div class="stat-label">Total Reports</div>
                </div>
                <div class="col-4 text-center">
                    <div class="stat-value" style="font-size:1.5rem;">{{ resolved_reports }}</div>
                    <div class="stat-label">Resolved</div>
                </div>
                <div class="col-4 text-center">
                    <div class="stat-value" style="font-size:1.5rem;">{{ last_report.created_at.strftime('%b %d') if last_report else '—' }}</div>
                    <div class="stat-label">Last Activity</div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
