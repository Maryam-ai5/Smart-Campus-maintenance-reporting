{% extends 'base.html' %}
{% block title %}My Reports — CampusFix{% endblock %}
{% block page_title %}My Reports{% endblock %}
{% block content %}
<div class="animate-in">
    <div class="filter-bar">
        <form method="GET" class="row g-2 align-items-end">
            <div class="col-md-3">
                <label class="form-label">Status</label>
                <select name="status" class="form-select">
                    <option value="">All Statuses</option>
                    <option value="submitted" {% if status_filter=='submitted' %}selected{% endif %}>Submitted</option>
                    <option value="assigned" {% if status_filter=='assigned' %}selected{% endif %}>Assigned</option>
                    <option value="in_progress" {% if status_filter=='in_progress' %}selected{% endif %}>In Progress</option>
                    <option value="resolved" {% if status_filter=='resolved' %}selected{% endif %}>Resolved</option>
                </select>
            </div>
            <div class="col-md-3">
                <label class="form-label">Category</label>
                <select name="category" class="form-select">
                    <option value="">All Categories</option>
                    {% for cat in categories %}
                    <option value="{{ cat.id }}" {% if category_filter==cat.id|string %}selected{% endif %}>{{ cat.icon }} {{ cat.name }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="col-md-3">
                <label class="form-label">Urgency</label>
                <select name="urgency" class="form-select">
                    <option value="">All</option>
                    <option value="high" {% if urgency_filter=='high' %}selected{% endif %}>🔴 High</option>
                    <option value="medium" {% if urgency_filter=='medium' %}selected{% endif %}>🟡 Medium</option>
                    <option value="low" {% if urgency_filter=='low' %}selected{% endif %}>🟢 Low</option>
                </select>
            </div>
            <div class="col-md-3"><button type="submit" class="btn btn-primary-custom w-100"><i class="bi bi-funnel me-2"></i>Apply</button></div>
        </form>
    </div>
    <div class="content-card">
        <div class="card-body-custom p-0">
            {% if reports.items %}
            <div class="table-responsive">
                <table class="table table-modern">
                    <thead><tr><th>#</th><th>Category</th><th>Location</th><th>Urgency</th><th>Status</th><th>Progress</th><th>Submitted</th><th></th></tr></thead>
                    <tbody>
                    {% for r in reports.items %}
                    <tr>
                        <td class="fw-semibold">#{{ r.id }}</td>
                        <td>{{ r.category_ref.icon }} {{ r.category_ref.name }}</td>
                        <td>{{ r.location|truncate(25) }}</td>
                        <td><span class="badge-status badge-urgency-{{ r.urgency }}">{{ r.urgency_label }}</span></td>
                        <td><span class="badge-status badge-{{ r.status }}">{{ r.status_label }}</span></td>
                        <td><div class="progress-mini"><div class="bar step-{{ r.status_step }}"></div></div></td>
                        <td style="font-size:0.8rem;color:var(--text-secondary);">{{ r.created_at.strftime('%b %d, %Y') }}</td>
                        <td><a href="{{ url_for('student.report_detail', report_id=r.id) }}" class="btn btn-sm btn-outline-custom">View</a></td>
                    </tr>
                    {% endfor %}
                    </tbody>
                </table>
            </div>
            {% if reports.pages > 1 %}
            <nav class="d-flex justify-content-center py-3">
                <ul class="pagination mb-0">
                    {% if reports.has_prev %}<li class="page-item"><a class="page-link" href="?page={{ reports.prev_num }}&status={{ status_filter }}&category={{ category_filter }}&urgency={{ urgency_filter }}">‹</a></li>{% endif %}
                    {% for p in reports.iter_pages(left_edge=1, right_edge=1, left_current=2, right_current=2) %}
                        {% if p %}<li class="page-item {% if p == reports.page %}active{% endif %}"><a class="page-link" href="?page={{ p }}&status={{ status_filter }}&category={{ category_filter }}&urgency={{ urgency_filter }}">{{ p }}</a></li>
                        {% else %}<li class="page-item disabled"><span class="page-link">…</span></li>{% endif %}
                    {% endfor %}
                    {% if reports.has_next %}<li class="page-item"><a class="page-link" href="?page={{ reports.next_num }}&status={{ status_filter }}&category={{ category_filter }}&urgency={{ urgency_filter }}">›</a></li>{% endif %}
                </ul>
            </nav>
            {% endif %}
            {% else %}
            <div class="empty-state"><i class="bi bi-inbox"></i><p>No reports found matching your filters.</p></div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
