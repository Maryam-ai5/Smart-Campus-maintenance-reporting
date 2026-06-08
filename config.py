{% extends 'base.html' %}
{% block title %}Dashboard — CampusFix{% endblock %}
{% block page_title %}Dashboard{% endblock %}
{% block content %}
<div class="animate-in">
    <div class="d-flex flex-wrap align-items-center justify-content-between mb-4">
        <div>
            <h2 class="fw-bold mb-1">Welcome back, {{ current_user.name }}! 👋</h2>
            <p class="text-secondary mb-0">Here's an overview of your maintenance reports.</p>
        </div>
        <a href="{{ url_for('student.submit_report') }}" class="btn btn-primary-custom mt-2 mt-md-0">
            <i class="bi bi-plus-lg me-2"></i>Submit Report
        </a>
    </div>
    <div class="row g-3 mb-4">
        <div class="col-6 col-lg-3">
            <div class="stat-card blue">
                <div class="stat-icon blue"><i class="bi bi-file-earmark-text"></i></div>
                <div class="stat-value">{{ total }}</div>
                <div class="stat-label">Total Reports</div>
            </div>
        </div>
        <div class="col-6 col-lg-3">
            <div class="stat-card yellow">
                <div class="stat-icon yellow"><i class="bi bi-clock-history"></i></div>
                <div class="stat-value">{{ pending }}</div>
                <div class="stat-label">Pending</div>
            </div>
        </div>
        <div class="col-6 col-lg-3">
            <div class="stat-card blue">
                <div class="stat-icon cyan"><i class="bi bi-gear-wide-connected"></i></div>
                <div class="stat-value">{{ in_progress }}</div>
                <div class="stat-label">In Progress</div>
            </div>
        </div>
        <div class="col-6 col-lg-3">
            <div class="stat-card green">
                <div class="stat-icon green"><i class="bi bi-check-circle"></i></div>
                <div class="stat-value">{{ resolved }}</div>
                <div class="stat-label">Resolved</div>
            </div>
        </div>
    </div>
    <div class="content-card">
        <div class="card-header-custom">
            <h5><i class="bi bi-clock me-2"></i>Recent Reports</h5>
            <a href="{{ url_for('student.track_reports') }}" class="btn btn-sm btn-outline-custom">View All →</a>
        </div>
        <div class="card-body-custom p-0">
            {% if reports %}
            <div class="table-responsive">
                <table class="table table-modern">
                    <thead><tr><th>#</th><th>Category</th><th>Location</th><th>Urgency</th><th>Status</th><th>Date</th><th></th></tr></thead>
                    <tbody>
                    {% for r in reports %}
                    <tr>
                        <td class="fw-semibold">#{{ r.id }}</td>
                        <td>{{ r.category_ref.icon }} {{ r.category_ref.name }}</td>
                        <td>{{ r.location|truncate(30) }}</td>
                        <td><span class="badge-status badge-urgency-{{ r.urgency }}">{{ r.urgency_label }}</span></td>
                        <td><span class="badge-status badge-{{ r.status }}">{{ r.status_label }}</span></td>
                        <td style="font-size:0.8rem;color:var(--text-secondary);">{{ r.created_at.strftime('%b %d, %Y') }}</td>
                        <td><a href="{{ url_for('student.report_detail', report_id=r.id) }}" class="btn btn-sm btn-outline-custom">View</a></td>
                    </tr>
                    {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="empty-state"><i class="bi bi-inbox"></i><p>No reports yet. Submit your first report!</p></div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
