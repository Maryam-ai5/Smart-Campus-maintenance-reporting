<!DOCTYPE html>
<html lang="en" data-bs-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Smart Campus Maintenance Reporting System">
    <title>{% block title %}CampusFix{% endblock %}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    {% if current_user.is_authenticated %}
    <aside class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <div class="sidebar-logo"><i class="bi bi-buildings"></i><span>CampusFix</span></div>
            <button class="sidebar-toggle d-lg-none" onclick="toggleSidebar()"><i class="bi bi-x-lg"></i></button>
        </div>
        <nav class="sidebar-nav">
            {% if current_user.role == 'student' %}
            <a href="{{ url_for('student.dashboard') }}" class="sidebar-link {% if request.endpoint == 'student.dashboard' %}active{% endif %}"><i class="bi bi-grid-1x2-fill"></i><span>Dashboard</span></a>
            <a href="{{ url_for('student.submit_report') }}" class="sidebar-link {% if request.endpoint == 'student.submit_report' %}active{% endif %}"><i class="bi bi-plus-circle-fill"></i><span>Submit Report</span></a>
            <a href="{{ url_for('student.track_reports') }}" class="sidebar-link {% if request.endpoint == 'student.track_reports' %}active{% endif %}"><i class="bi bi-list-check"></i><span>My Reports</span></a>
            {% elif current_user.role == 'maintenance' %}
            <a href="{{ url_for('maintenance.panel') }}" class="sidebar-link {% if request.endpoint == 'maintenance.panel' %}active{% endif %}"><i class="bi bi-wrench-adjustable"></i><span>Work Panel</span></a>
            {% elif current_user.role == 'admin' %}
            <a href="{{ url_for('admin.dashboard') }}" class="sidebar-link {% if request.endpoint == 'admin.dashboard' %}active{% endif %}"><i class="bi bi-speedometer2"></i><span>Analytics</span></a>
            <a href="{{ url_for('admin.users') }}" class="sidebar-link {% if request.endpoint == 'admin.users' %}active{% endif %}"><i class="bi bi-people-fill"></i><span>Users</span></a>
            <a href="{{ url_for('admin.categories') }}" class="sidebar-link {% if request.endpoint == 'admin.categories' %}active{% endif %}"><i class="bi bi-tags-fill"></i><span>Categories</span></a>
            {% endif %}
            <div class="sidebar-divider"></div>
            <a href="{{ url_for('shared.search') }}" class="sidebar-link {% if request.endpoint == 'shared.search' %}active{% endif %}"><i class="bi bi-search"></i><span>Search</span></a>
            <a href="{{ url_for('shared.notifications') }}" class="sidebar-link {% if request.endpoint == 'shared.notifications' %}active{% endif %}"><i class="bi bi-bell-fill"></i><span>Notifications</span>{% if unread_notification_count > 0 %}<span class="sidebar-badge">{{ unread_notification_count }}</span>{% endif %}</a>
            <a href="{{ url_for('shared.profile') }}" class="sidebar-link {% if request.endpoint == 'shared.profile' %}active{% endif %}"><i class="bi bi-person-circle"></i><span>Profile</span></a>
        </nav>
        <div class="sidebar-footer">
            <div class="sidebar-user">
                <div class="sidebar-user-avatar">{{ current_user.name[0]|upper }}</div>
                <div class="sidebar-user-info"><span class="sidebar-user-name">{{ current_user.name }}</span><span class="sidebar-user-role">{{ current_user.role|capitalize }}</span></div>
            </div>
            <a href="{{ url_for('auth.logout') }}" class="sidebar-link logout-link"><i class="bi bi-box-arrow-left"></i><span>Logout</span></a>
        </div>
    </aside>
    <main class="main-content" id="mainContent">
        <header class="top-navbar">
            <button class="sidebar-toggle-btn d-lg-none" onclick="toggleSidebar()"><i class="bi bi-list"></i></button>
            <div class="top-navbar-title"><h1 class="h5 mb-0">{% block page_title %}Dashboard{% endblock %}</h1></div>
            <div class="top-navbar-actions">
                <a href="{{ url_for('shared.notifications') }}" class="top-nav-icon" id="notificationBell"><i class="bi bi-bell"></i>{% if unread_notification_count > 0 %}<span class="notification-badge">{{ unread_notification_count }}</span>{% endif %}</a>
                <div class="dropdown">
                    <button class="top-nav-user dropdown-toggle" data-bs-toggle="dropdown"><div class="user-avatar-sm">{{ current_user.name[0]|upper }}</div><span class="d-none d-md-inline">{{ current_user.name }}</span></button>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li><a class="dropdown-item" href="{{ url_for('shared.profile') }}"><i class="bi bi-person me-2"></i>Profile</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item text-danger" href="{{ url_for('auth.logout') }}"><i class="bi bi-box-arrow-left me-2"></i>Logout</a></li>
                    </ul>
                </div>
            </div>
        </header>
        <div class="content-wrapper">
            {% with messages = get_flashed_messages(with_categories=true) %}{% if messages %}<div class="flash-container">{% for category, message in messages %}<div class="alert alert-{{ category }} alert-dismissible fade show flash-alert" role="alert"><i class="bi bi-{% if category == 'success' %}check-circle-fill{% elif category == 'danger' %}exclamation-triangle-fill{% elif category == 'warning' %}exclamation-circle-fill{% else %}info-circle-fill{% endif %} me-2"></i>{{ message }}<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>{% endfor %}</div>{% endif %}{% endwith %}
            {% block content %}{% endblock %}
        </div>
    </main>
    {% else %}
    <div class="auth-wrapper">
        {% with messages = get_flashed_messages(with_categories=true) %}{% if messages %}<div class="flash-container auth-flash">{% for category, message in messages %}<div class="alert alert-{{ category }} alert-dismissible fade show flash-alert" role="alert">{{ message }}<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>{% endfor %}</div>{% endif %}{% endwith %}
        {% block auth_content %}{% endblock %}
    </div>
    {% endif %}
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
