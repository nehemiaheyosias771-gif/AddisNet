// AddisNet Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));

    // Initialize popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    popoverTriggerList.forEach(el => new bootstrap.Popover(el));

    // Auto-dismiss alerts after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Confirm delete actions
    document.querySelectorAll('.delete-confirm').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this?')) {
                e.preventDefault();
            }
        });
    });

    // Image preview for file uploads
    const imageInput = document.querySelector('input[type="file"][accept="image/*"]');
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let preview = document.getElementById('image-preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.id = 'image-preview';
                        preview.className = 'img-fluid mt-2 rounded';
                        preview.style.maxHeight = '200px';
                        imageInput.parentNode.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }
});

// Map initialization helper
function initMap(elementId, lat, lon, zoom) {
    const map = L.map(elementId).setView([lat, lon], zoom);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    return map;
}

// Load issues onto map
async function loadIssuesOnMap(map) {
    try {
        const response = await fetch('/api/issues/geojson/');
        const data = await response.json();
        
        data.features.forEach(feature => {
            const marker = L.marker([feature.geometry.coordinates[1], feature.geometry.coordinates[0]])
                .addTo(map);
            
            const popup = L.popup();
            popup.setContent(`
                <strong>${feature.properties.title}</strong><br>
                Category: ${feature.properties.category}<br>
                Severity: ${feature.properties.severity}<br>
                Upvotes: ${feature.properties.upvotes}
            `);
            marker.bindPopup(popup);
        });
    } catch (error) {
        console.error('Error loading issues:', error);
    }
}

// Upvote handler
async function upvote(url, element) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        const data = await response.json();
        if (data.success) {
            element.innerHTML = `<i class="fas fa-arrow-up"></i> ${data.upvotes}`;
        }
    } catch (error) {
        console.error('Error upvoting:', error);
    }
}

// CSRF token helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
