"""
Core App API URL Configuration for AddisNet

REST API endpoints for:
- Issues CRUD
- Posts CRUD
- Users
- Analytics
- IoT Sensor Data
- Emergency Alerts
- Participatory Budgeting
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views_api

router = DefaultRouter()
router.register(r'issues', views_api.IssueViewSet, basename='issue')
router.register(r'posts', views_api.PostViewSet, basename='post')
router.register(r'users', views_api.UserViewSet, basename='user')
router.register(r'comments', views_api.IssueCommentViewSet, basename='comment')
router.register(r'post-comments', views_api.PostCommentViewSet, basename='post-comment')
router.register(r'votes', views_api.VoteViewSet, basename='vote')
router.register(r'iot-sensors', views_api.IoTSensorDataViewSet, basename='iot-sensor')
router.register(r'emergency-alerts', views_api.EmergencyAlertViewSet, basename='emergency-alert')
router.register(r'analytics', views_api.AnalyticsSnapshotViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
    
    # Additional API endpoints
    path('issues/<uuid:pk>/upvote/', views_api.upvote_issue_api, name='api-upvote-issue'),
    path('posts/<uuid:pk>/upvote/', views_api.upvote_post_api, name='api-upvote-post'),
    path('geojson/issues/', views_api.issues_geojson_api, name='api-issues-geojson'),
    path('analytics/dashboard/', views_api.analytics_dashboard_api, name='api-analytics-dashboard'),
    path('analytics/predictions/', views_api.predictive_analytics_api, name='api-predictive-analytics'),
    path('budget/vote/', views_api.cast_budget_vote_api, name='api-cast-vote'),
    path('emergency/activate/', views_api.create_emergency_alert_api, name='api-emergency-create'),
]
