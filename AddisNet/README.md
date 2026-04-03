# AddisNet - Smart City Platform for Addis Ababa

🇪🇹 **A Competition-Ready Civic Engagement Platform**

AddisNet is a comprehensive smart city platform designed to solve real civic problems in Addis Ababa through technology, community engagement, and data-driven insights.

## 🌟 Features

### Core Functionality
- **Issue Reporting**: Citizens can report city issues (water, waste, transport, infrastructure) with photos, videos, and GPS location
- **Live Interactive Map**: Real-time visualization of all reported issues with filtering by category/severity
- **Community Board**: Platform for tutoring, volunteering, skill exchange, and collaboration
- **Analytics Dashboard**: Charts, trends, predictive insights, and environmental metrics
- **Participatory Budgeting**: Citizens vote on funding priorities for city improvements
- **Emergency Alerts**: Critical issue notifications to nearby users

### Smart City Features
- IoT sensor integration (mock) for traffic, water quality, air quality monitoring
- AI-powered issue classification and urgency detection
- Predictive analytics for problem hotspot identification
- Open data export for government transparency

### Ethiopian Context
- Multi-language support (English + Amharic)
- Addis Ababa sub-city divisions
- Localized categories and terminology
- Cultural branding and design

## 🛠 Technology Stack

- **Backend**: Django 5.x with Python 3.11+
- **Frontend**: HTML5, CSS3 (Glassmorphism), Bootstrap 5, JavaScript
- **Database**: SQLite (MVP), PostgreSQL ready
- **Maps**: OpenStreetMap / Leaflet
- **Charts**: Chart.js
- **API**: Django REST Framework
- **Real-time**: Django Channels (optional)

## 📁 Project Structure

```
AddisNet/
├── addisnet/                 # Django project settings
│   ├── settings.py           # Configuration
│   ├── urls.py               # Main URL routing
│   └── wsgi.py/asgi.py
├── core/                     # Main application
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── views_api.py          # REST API endpoints
│   ├── serializers.py        # DRF serializers
│   ├── forms.py              # Django forms
│   ├── admin.py              # Admin configuration
│   ├── urls.py               # App URLs
│   └── urls_api.py           # API URLs
├── templates/                # HTML templates
├── static/                   # CSS, JS, images
├── media/                    # User uploads
├── manage.py
└── requirements.txt
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation

1. **Clone/Navigate to project**
```bash
cd AddisNet
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
# Follow prompts to set username, email, password
```

6. **Start development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Main site: http://localhost:8000
- Admin panel: http://localhost:8000/admin

## 📋 Demo Instructions

For competition judges:

1. **Sign Up** - Create a citizen account at `/signup/`
2. **Report Issue** - Navigate to `/issues/create/` and submit an issue with photo
3. **View Map** - See your issue on the live map at `/map/`
4. **Dashboard** - View statistics at `/`
5. **Community** - Browse/create posts at `/community/`
6. **Analytics** - Explore charts at `/analytics/`
7. **Budget Voting** - Vote on priorities at `/budget/`
8. **Admin Panel** - Login as admin at `/admin/` to manage content

## 🔐 Default Credentials (Development)

After running `createsuperuser`:
- Username: admin
- Password: [your chosen password]

## 🌐 API Endpoints

REST API available at `/api/`:
- `/api/issues/` - CRUD operations for issues
- `/api/posts/` - Community posts
- `/api/users/` - User management
- `/api/iot-sensors/` - Sensor data
- `/api/emergency-alerts/` - Emergency alerts
- `/api/analytics/` - Analytics data

## 📊 Models Overview

- **CustomUser**: Extended user with roles (citizen, volunteer, government, admin)
- **Issue**: City issues with location, media, severity, status
- **Post**: Community posts for collaboration
- **Vote**: Participatory budgeting votes
- **IoTSensorData**: Mock sensor readings
- **EmergencyAlert**: Critical notifications
- **AnalyticsSnapshot**: Daily metrics

## 🎨 Design Features

- Modern glassmorphism UI
- Responsive mobile-first design
- Ethiopian cultural branding
- Dark mode support
- Accessibility features
- Smooth animations

## 🔒 Security

- CSRF protection
- XSS prevention
- SQL injection protection
- Role-based access control
- Input validation
- Secure authentication

## 📈 Future Enhancements

- Firebase integration for real-time updates
- SMS/Email notifications
- Machine learning for issue classification
- Mobile app (React Native/Flutter)
- Integration with city government systems
- Payment gateway for donations

## 👥 Team & Credits

Built for the Smart City Challenge - Addis Ababa 2024

## 📄 License

MIT License - Open for educational and civic use

---

**🇪🇹 Built with pride for Addis Ababa**
