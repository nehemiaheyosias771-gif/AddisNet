"""
Core App URL Configuration for AddisNet

Maps URLs to views for:
- Dashboard
- Issue reporting and management
- Map visualization
- Community board
- Analytics
- Participatory budgeting
- Emergency alerts
- User authentication
"""

from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Issue management
    path('issues/', views.issue_list, name='issue_list'),
    path('issues/create/', views.report_issue, name='report_issue'),
    path('issues/<uuid:issue_id>/', views.issue_detail, name='issue_detail'),
    path('issues/<uuid:issue_id>/edit/', views.edit_issue, name='edit_issue'),
    path('issues/<uuid:issue_id>/delete/', views.delete_issue, name='delete_issue'),
    path('issues/<uuid:issue_id>/upvote/', views.upvote_issue, name='upvote_issue'),
    path('issues/<uuid:issue_id>/comment/', views.add_issue_comment, name='add_issue_comment'),
    
    # Map
    path('map/', views.map_view, name='map'),
    path('api/issues/geojson/', views.issues_geojson, name='issues_geojson'),
    
    # Community
    path('community/', views.community_board, name='community'),
    path('community/create/', views.create_post, name='create_post'),
    path('community/<uuid:post_id>/', views.post_detail, name='post_detail'),
    path('community/<uuid:post_id>/upvote/', views.upvote_post, name='upvote_post'),
    path('community/<uuid:post_id>/comment/', views.add_post_comment, name='add_post_comment'),
    
    # Analytics
    path('analytics/', views.analytics_dashboard, name='analytics'),
    path('api/analytics/trends/', views.analytics_trends_api, name='analytics_trends'),
    
    # Participatory Budgeting
    path('budget/', views.participatory_budgeting, name='participatory_budgeting'),
    path('budget/vote/<uuid:issue_id>/', views.cast_budget_vote, name='cast_budget_vote'),
    
    # Emergency Alerts
    path('emergency/', views.emergency_alerts, name='emergency_alerts'),
    path('emergency/create/', views.create_emergency_alert, name='create_emergency_alert'),
    path('emergency/<uuid:alert_id>/acknowledge/', views.acknowledge_alert, name='acknowledge_alert'),
    
    # IoT Sensor Data (Mock)
    path('iot/', views.iot_dashboard, name='iot_dashboard'),
    path('api/iot/sensors/', views.iot_sensors_api, name='iot_sensors_api'),
    
    # Settings & Profile
    path('settings/', views.settings_view, name='settings'),
    path('profile/<uuid:user_id>/', views.profile_view, name='profile'),
    
    # Language switcher
    path('set-language/<str:language>/', views.set_language, name='set_language'),
]
