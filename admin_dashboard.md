{% extends 'base.html' %}
{% block title %}Submit Report — CampusFix{% endblock %}
{% block page_title %}Submit Maintenance Report{% endblock %}
{% block content %}
<div class="animate-in" style="max-width:720px;">
    <div class="content-card">
        <div class="card-header-custom">
            <h5><i class="bi bi-plus-circle me-2"></i>New Report</h5>
        </div>
        <div class="card-body-custom">
            <form method="POST" enctype="multipart/form-data" novalidate>
                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                <div class="mb-3">
                    <label for="category_id" class="form-label">Category <span class="text-danger">*</span></label>
                    <select class="form-select" id="category_id" name="category_id" onchange="toggleCustomCategory(this)">
                        <option value="">Select a category</option>
                        {% for cat in categories %}
                        <option value="{{ cat.id }}">{{ cat.icon }} {{ cat.name }}</option>
                        {% endfor %}
                        <option value="other">✏️ Other (type your own)</option>
                    </select>
                    <div id="custom_category_wrapper" class="mt-2" style="display:none;">
                        <input type="text" class="form-control" id="custom_category" name="custom_category" placeholder="Enter custom category name" maxlength="100">
                        <div class="form-text">Type a new category name that isn't listed above.</div>
                    </div>
                </div>
                <script>
                function toggleCustomCategory(sel) {
                    var wrapper = document.getElementById('custom_category_wrapper');
                    var input = document.getElementById('custom_category');
                    if (sel.value === 'other') {
                        wrapper.style.display = 'block';
                        input.required = true;
                        input.focus();
                    } else {
                        wrapper.style.display = 'none';
                        input.required = false;
                        input.value = '';
                    }
                }
                </script>
                <div class="mb-3">
                    <label for="location" class="form-label">Location <span class="text-danger">*</span></label>
                    <input type="text" class="form-control" id="location" name="location" placeholder="e.g. Block A, Room 201" required minlength="3" maxlength="200">
                </div>
                <div class="mb-3">
                    <label for="description" class="form-label">Description <span class="text-danger">*</span></label>
                    <textarea class="form-control" id="description" name="description" rows="5" placeholder="Describe the issue in detail (min 20 characters)..." required minlength="20" maxlength="1000"></textarea>
                    <div class="form-text">Min 20, max 1000 characters.</div>
                </div>
                <div class="mb-3">
                    <label for="urgency" class="form-label">Urgency <span class="text-danger">*</span></label>
                    <select class="form-select" id="urgency" name="urgency" required>
                        <option value="low">🟢 Low</option>
                        <option value="medium" selected>🟡 Medium</option>
                        <option value="high">🔴 High</option>
                    </select>
                </div>
                <div class="mb-4">
                    <label for="photo" class="form-label">Photo (optional)</label>
                    <input type="file" class="form-control" id="photo" name="photo" accept="image/*" onchange="previewImage(this, 'photoPreview')">
                    <div class="form-text">JPG, PNG, GIF or WebP. Max 5MB.</div>
                    <img id="photoPreview" class="image-preview mt-2" style="display:none;" alt="Preview">
                </div>
                <div class="d-flex gap-2">
                    <button type="submit" class="btn btn-primary-custom"><i class="bi bi-send me-2"></i>Submit Report</button>
                    <a href="{{ url_for('student.dashboard') }}" class="btn btn-outline-custom">Cancel</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
