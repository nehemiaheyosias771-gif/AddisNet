"""
Django Models for AddisNet Smart City Platform

Models:
- CustomUser: Extended user model with roles and profile info
- Issue: City issues reported by citizens
- Post: Community posts for collaboration
- Vote: Votes for participatory budgeting
- IoT Sensor Data: Mock sensor readings
- EmergencyAlert: Emergency notifications
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class CustomUser(AbstractUser):
    """Extended user model with Ethiopian civic engagement features"""
    
    ROLE_CHOICES = [
        ('citizen', 'Citizen'),
        ('volunteer', 'Volunteer'),
        ('ngo', 'NGO Representative'),
        ('government', 'Government Official'),
        ('admin', 'Administrator'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True, 
                                help_text="Sub-city or neighborhood in Addis Ababa")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, max_length=500)
    language_preference = models.CharField(max_length=2, choices=[('en', 'English'), ('am', 'Amharic')], 
                                           default='en')
    is_verified = models.BooleanField(default=False, help_text="Verified citizen/government official")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def reputation_score(self):
        """Calculate user reputation based on activity"""
        issues_reported = self.issues_reported.count()
        upvotes_received = self.issues_reported.aggregate(
            total=models.Sum('upvotes'))['total'] or 0
        posts_created = self.posts.count()
        return (issues_reported * 10) + upvotes_received + (posts_created * 5)


class Issue(models.Model):
    """City issues reported by citizens (water, waste, transport, infrastructure)"""
    
    CATEGORY_CHOICES = [
        ('water', 'Water Supply'),
        ('waste', 'Waste Management'),
        ('transport', 'Transportation'),
        ('infrastructure', 'Infrastructure'),
        ('electricity', 'Electricity'),
        ('road', 'Road Conditions'),
        ('drainage', 'Drainage/Sewage'),
        ('public_safety', 'Public Safety'),
        ('environment', 'Environmental'),
        ('other', 'Other'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    
    # Location data
    latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Latitude coordinate")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Longitude coordinate")
    address = models.CharField(max_length=255, blank=True, null=True)
    sub_city = models.CharField(max_length=100, blank=True, null=True, 
                                help_text="Sub-city in Addis Ababa")
    
    # Media
    image = models.ImageField(upload_to='issues/images/', blank=True, null=True)
    video = models.FileField(upload_to='issues/videos/', blank=True, null=True)
    
    # User and tracking
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='issues_reported')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, 
                                    related_name='issues_assigned', 
                                    null=True, blank=True, limit_choices_to={'role__in': ['government', 'admin']})
    
    # Engagement metrics
    upvotes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    
    # AI/NLP classification
    ai_tags = models.JSONField(default=list, blank=True, help_text="AI-generated tags")
    urgency_score = models.FloatField(default=0.0, help_text="AI-calculated urgency (0-1)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Issue'
        verbose_name_plural = 'Issues'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'status']),
            models.Index(fields=['severity', 'status']),
            models.Index(fields=['latitude', 'longitude']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.get_category_display()} ({self.get_status_display()})"
    
    def save(self, *args, **kwargs):
        if self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)


class IssueComment(models.Model):
    """Comments on issues for discussion and updates"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    is_official_response = models.BooleanField(default=False, 
                                               help_text="Mark as official government response")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.issue.title}"


class Post(models.Model):
    """Community posts for tutoring, volunteering, skill exchange, collaboration"""
    
    TYPE_CHOICES = [
        ('tutoring', 'Tutoring/Education'),
        ('volunteering', 'Volunteering Opportunity'),
        ('skill_exchange', 'Skill Exchange'),
        ('collaboration', 'Collaboration Proposal'),
        ('announcement', 'Announcement'),
        ('discussion', 'Discussion'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    
    # Engagement
    upvotes = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    
    # Tags for categorization
    tags = models.JSONField(default=list, blank=True)
    
    # Location (optional for local initiatives)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Community Post'
        verbose_name_plural = 'Community Posts'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"


class PostComment(models.Model):
    """Comments on community posts"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                               related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment on {self.post.title} by {self.user.username}"


class Vote(models.Model):
    """Votes for participatory budgeting - citizens vote on funding priorities"""
    
    VOTE_TYPE_CHOICES = [
        ('issue', 'Issue Funding'),
        ('project', 'Project Proposal'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPE_CHOICES)
    
    # Related entity (Issue or Project)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='budget_votes')
    project_id = models.UUIDField(null=True, blank=True)  # For future project model
    
    vote_value = models.IntegerField(default=1, help_text="Weight of vote")
    justification = models.TextField(blank=True, max_length=500)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'vote_type', 'issue']
        ordering = ['-created_at']
    
    def __str__(self):
        target = self.issue.title if self.issue else f"Project {self.project_id}"
        return f"{self.user.username} voted on {target}"


class IoTSensorData(models.Model):
    """Mock IoT sensor data for traffic, water, pollution, noise monitoring"""
    
    SENSOR_TYPE_CHOICES = [
        ('traffic', 'Traffic Flow'),
        ('water_quality', 'Water Quality'),
        ('air_quality', 'Air Quality'),
        ('noise', 'Noise Level'),
        ('weather', 'Weather'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPE_CHOICES)
    location_name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Sensor readings (JSON for flexibility)
    readings = models.JSONField(help_text="Sensor data (e.g., {pm25: 45, temperature: 25})")
    
    # Metadata
    unit = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='normal', 
                              choices=[('normal', 'Normal'), ('warning', 'Warning'), 
                                     ('critical', 'Critical')])
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'IoT Sensor Data'
        verbose_name_plural = 'IoT Sensor Data'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['sensor_type', 'timestamp']),
            models.Index(fields=['latitude', 'longitude']),
        ]
    
    def __str__(self):
        return f"{self.get_sensor_type_display()} at {self.location_name}"


class EmergencyAlert(models.Model):
    """Emergency alerts for critical issues requiring immediate attention"""
    
    ALERT_TYPE_CHOICES = [
        ('infrastructure_failure', 'Infrastructure Failure'),
        ('public_safety', 'Public Safety Emergency'),
        ('environmental_hazard', 'Environmental Hazard'),
        ('utility_outage', 'Utility Outage'),
        ('natural_disaster', 'Natural Disaster'),
        ('other', 'Other Emergency'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'CRITICAL'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPE_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    affected_radius_km = models.FloatField(default=1.0, help_text="Radius in kilometers")
    
    # Status
    is_active = models.BooleanField(default=True)
    acknowledged_by = models.ManyToManyField(CustomUser, related_name='acknowledged_alerts', 
                                             blank=True)
    
    # Notifications sent
    sms_sent = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    push_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Emergency Alert'
        verbose_name_plural = 'Emergency Alerts'
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"[{self.get_priority_display()}] {self.title}"


class AnalyticsSnapshot(models.Model):
    """Daily analytics snapshots for trends and reporting"""
    
    date = models.DateField(unique=True)
    
    # Issue metrics
    total_issues = models.IntegerField(default=0)
    issues_resolved = models.IntegerField(default=0)
    avg_resolution_time_hours = models.FloatField(default=0)
    
    # By category
    issues_by_category = models.JSONField(default=dict, 
                                          help_text="Count per category")
    
    # User metrics
    active_users = models.IntegerField(default=0)
    new_users = models.IntegerField(default=0)
    
    # Community metrics
    total_posts = models.IntegerField(default=0)
    total_votes = models.IntegerField(default=0)
    
    # Predictive insights
    hotspot_areas = models.JSONField(default=list, 
                                     help_text="Predicted problem areas")
    trend_analysis = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"Analytics for {self.date}"
