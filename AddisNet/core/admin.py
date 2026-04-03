"""
Django Admin Configuration for AddisNet

Provides comprehensive admin interface for managing:
- Users with role filtering
- Issues with status management
- Community posts
- Emergency alerts
- IoT sensor data
- Analytics
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    CustomUser, Issue, IssueComment, Post, PostComment, 
    Vote, IoTSensorData, EmergencyAlert, AnalyticsSnapshot
)


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    """Custom user admin with Ethiopian civic engagement features"""
    
    list_display = ['username', 'email', 'role', 'location', 'is_verified', 
                    'reputation_score_display', 'created_at']
    list_filter = ['role', 'is_verified', 'is_staff', 'is_active', 'language_preference']
    search_fields = ['username', 'email', 'location', 'phone']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Ethiopian Civic Profile', {
            'fields': ('role', 'phone', 'location', 'profile_picture', 'bio', 
                      'language_preference', 'is_verified')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Ethiopian Civic Profile', {
            'fields': ('role', 'email', 'phone', 'location', 'language_preference')
        }),
    )
    
    def reputation_score_display(self, obj):
        return obj.reputation_score
    reputation_score_display.short_description = 'Reputation Score'
    
    actions = ['verify_users', 'mark_as_government_official']
    
    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)
    verify_users.short_description = "Verify selected users"
    
    def mark_as_government_official(self, request, queryset):
        queryset.update(role='government', is_verified=True)
    mark_as_government_official.short_description = "Mark as government official"


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    """Admin for city issues with comprehensive filtering"""
    
    list_display = ['title_preview', 'category', 'severity', 'status', 'user_link', 
                    'location_preview', 'upvotes', 'created_at', 'quick_actions']
    list_filter = ['category', 'severity', 'status', 'sub_city', 'created_at']
    search_fields = ['title', 'description', 'user__username', 'address']
    readonly_fields = ['id', 'created_at', 'updated_at', 'resolved_at', 'views']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Issue Details', {
            'fields': ('id', 'title', 'description', 'category', 'severity', 'status')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude', 'address', 'sub_city')
        }),
        ('Media Evidence', {
            'fields': ('image', 'video'),
            'classes': ('collapse',)
        }),
        ('Assignment & Tracking', {
            'fields': ('user', 'assigned_to', 'upvotes', 'views')
        }),
        ('AI Analysis', {
            'fields': ('ai_tags', 'urgency_score'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_resolved', 'mark_as_in_progress', 'escalate_to_critical', 
               'export_selected_issues']
    
    def title_preview(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_preview.short_description = 'Title'
    
    def user_link(self, obj):
        url = reverse('admin:core_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'Reporter'
    
    def location_preview(self, obj):
        return f"{obj.sub_city or 'Unknown'}"
    location_preview.short_description = 'Location'
    
    def quick_actions(self, obj):
        return format_html(
            '<a href="/issues/{}/" target="_blank">View</a> | '
            '<a href="/map/?issue={}" target="_blank">Map</a>',
            obj.id, obj.id
        )
    quick_actions.short_description = 'Actions'
    
    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(status='resolved')
        self.message_user(request, f'{updated} issues marked as resolved')
    mark_as_resolved.short_description = "Mark as resolved"
    
    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} issues marked as in progress')
    mark_as_in_progress.short_description = "Mark as in progress"
    
    def escalate_to_critical(self, request, queryset):
        updated = queryset.update(severity='critical')
        self.message_user(request, f'{updated} issues escalated to critical')
    escalate_to_critical.short_description = "Escalate to critical"


@admin.register(IssueComment)
class IssueCommentAdmin(admin.ModelAdmin):
    list_display = ['content_preview', 'issue_link', 'user_link', 
                    'is_official_response', 'created_at']
    list_filter = ['is_official_response', 'created_at']
    search_fields = ['content', 'user__username', 'issue__title']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def content_preview(self, obj):
        return obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
    
    def issue_link(self, obj):
        url = reverse('admin:core_issue_change', args=[obj.issue.id])
        return format_html('<a href="{}">{}</a>', url, obj.issue.title[:30])
    
    def user_link(self, obj):
        url = reverse('admin:core_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin for community posts"""
    
    list_display = ['title_preview', 'type', 'user_link', 'upvotes', 
                    'comments_count', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['title', 'description', 'user__username', 'tags']
    readonly_fields = ['created_at', 'updated_at', 'comments_count']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Post Details', {
            'fields': ('type', 'title', 'description', 'user', 'tags')
        }),
        ('Engagement', {
            'fields': ('upvotes', 'comments_count')
        }),
        ('Location (Optional)', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
    )
    
    def title_preview(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    
    def user_link(self, obj):
        url = reverse('admin:core_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['content_preview', 'post_link', 'user_link', 'created_at']
    search_fields = ['content', 'user__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def content_preview(self, obj):
        return obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
    
    def post_link(self, obj):
        url = reverse('admin:core_post_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title[:30])
    
    def user_link(self, obj):
        url = reverse('admin:core_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """Admin for participatory budgeting votes"""
    
    list_display = ['user_link', 'vote_type', 'issue_link', 'vote_value', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['user__username', 'issue__title']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def user_link(self, obj):
        url = reverse('admin:core_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    
    def issue_link(self, obj):
        if obj.issue:
            url = reverse('admin:core_issue_change', args=[obj.issue.id])
            return format_html('<a href="{}">{}</a>', url, obj.issue.title[:30])
        return '-'


@admin.register(IoTSensorData)
class IoTSensorDataAdmin(admin.ModelAdmin):
    """Admin for IoT sensor readings"""
    
    list_display = ['sensor_type', 'location_name', 'status', 'timestamp', 'readings_preview']
    list_filter = ['sensor_type', 'status', 'timestamp']
    search_fields = ['location_name', 'sensor_type']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    date_hierarchy = 'timestamp'
    
    def readings_preview(self, obj):
        if isinstance(obj.readings, dict):
            items = list(obj.readings.items())[:3]
            return ', '.join([f"{k}: {v}" for k, v in items])
        return str(obj.readings)[:50]
    
    actions = ['export_sensor_data']


@admin.register(EmergencyAlert)
class EmergencyAlertAdmin(admin.ModelAdmin):
    """Admin for emergency alerts with priority management"""
    
    list_display = ['priority_badge', 'title_preview', 'alert_type', 'location_preview', 
                    'is_active', 'notifications_status', 'created_at']
    list_filter = ['priority', 'alert_type', 'is_active', 'sms_sent', 'email_sent']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'expires_at', 'resolved_at']
    ordering = ['-priority', '-created_at']
    
    fieldsets = (
        ('Alert Details', {
            'fields': ('alert_type', 'priority', 'title', 'description')
        }),
        ('Location & Impact', {
            'fields': ('latitude', 'longitude', 'affected_radius_km')
        }),
        ('Status', {
            'fields': ('is_active', 'acknowledged_by')
        }),
        ('Notifications', {
            'fields': ('sms_sent', 'email_sent', 'push_sent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'expires_at', 'resolved_at')
        }),
    )
    
    actions = ['deactivate_alert', 'send_notifications', 'mark_as_resolved']
    
    def priority_badge(self, obj):
        colors = {'low': 'green', 'medium': 'blue', 'high': 'orange', 'critical': 'red'}
        color = colors.get(obj.priority, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'
    
    def title_preview(self, obj):
        return obj.title[:40] + '...' if len(obj.title) > 40 else obj.title
    
    def location_preview(self, obj):
        return f"({obj.latitude}, {obj.longitude})"
    
    def notifications_status(self, obj):
        statuses = []
        if obj.sms_sent: statuses.append('SMS ✓')
        if obj.email_sent: statuses.append('Email ✓')
        if obj.push_sent: statuses.append('Push ✓')
        return ', '.join(statuses) if statuses else 'Not sent'
    
    def deactivate_alert(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_alert.short_description = "Deactivate selected alerts"
    
    def send_notifications(self, request, queryset):
        # In production, integrate with SMS/email providers
        queryset.update(sms_sent=True, email_sent=True, push_sent=True)
        self.message_user(request, 'Notifications marked as sent')
    send_notifications.short_description = "Send all notifications"
    
    def mark_as_resolved(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_active=False, resolved_at=timezone.now())
    mark_as_resolved.short_description = "Mark as resolved"


@admin.register(AnalyticsSnapshot)
class AnalyticsSnapshotAdmin(admin.ModelAdmin):
    """Admin for analytics snapshots"""
    
    list_display = ['date', 'total_issues', 'issues_resolved', 'active_users', 'new_users']
    readonly_fields = ['date', 'created_at']
    ordering = ['-date']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Date', {
            'fields': ('date',)
        }),
        ('Issue Metrics', {
            'fields': ('total_issues', 'issues_resolved', 'avg_resolution_time_hours', 
                      'issues_by_category')
        }),
        ('User Metrics', {
            'fields': ('active_users', 'new_users')
        }),
        ('Community Metrics', {
            'fields': ('total_posts', 'total_votes')
        }),
        ('Predictive Insights', {
            'fields': ('hotspot_areas', 'trend_analysis'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['export_analytics']


# Admin site customization
admin.site.site_header = "AddisNet Administration"
admin.site.site_title = "AddisNet Admin"
admin.site.index_title = "Smart City Management Dashboard"
