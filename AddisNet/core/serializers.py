"""
Django REST Framework Serializers for AddisNet

Provides serialization for all models with validation and nested relationships.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    CustomUser, Issue, IssueComment, Post, PostComment, 
    Vote, IoTSensorData, EmergencyAlert, AnalyticsSnapshot
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model"""
    reputation_score = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'role', 'phone', 'location',
            'profile_picture', 'bio', 'language_preference', 'is_verified',
            'reputation_score', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reputation_score', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance


class UserLiteSerializer(serializers.ModelSerializer):
    """Lightweight user serializer for nested relationships"""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'profile_picture', 'location']


class IssueCommentSerializer(serializers.ModelSerializer):
    """Serializer for IssueComment model"""
    user = UserLiteSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='user', write_only=True
    )
    
    class Meta:
        model = IssueComment
        fields = ['id', 'issue', 'user', 'user_id', 'content', 
                  'is_official_response', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class IssueSerializer(serializers.ModelSerializer):
    """Serializer for Issue model with nested relationships"""
    user = UserLiteSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='user', write_only=True
    )
    assigned_to = UserLiteSerializer(read_only=True)
    comments = IssueCommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'category', 'severity', 'status',
            'latitude', 'longitude', 'address', 'sub_city',
            'image', 'video', 'user', 'user_id', 'assigned_to',
            'upvotes', 'views', 'ai_tags', 'urgency_score',
            'comments', 'created_at', 'updated_at', 'resolved_at'
        ]
        read_only_fields = ['id', 'upvotes', 'views', 'ai_tags', 'urgency_score', 
                           'created_at', 'updated_at', 'resolved_at']
    
    def create(self, validated_data):
        # AI classification stub - in production, integrate NLP service
        title = validated_data.get('title', '')
        description = validated_data.get('description', '')
        
        # Simple keyword-based categorization (stub for AI)
        ai_tags = []
        urgency_keywords = ['emergency', 'urgent', 'critical', 'danger', 'immediate']
        if any(word in (title + description).lower() for word in urgency_keywords):
            validated_data['urgency_score'] = 0.8
            ai_tags.append('urgent')
        
        validated_data['ai_tags'] = ai_tags
        
        return super().create(validated_data)


class IssueLiteSerializer(serializers.ModelSerializer):
    """Lightweight issue serializer for map markers"""
    class Meta:
        model = Issue
        fields = ['id', 'title', 'category', 'severity', 'status', 
                  'latitude', 'longitude', 'upvotes', 'created_at']


class PostCommentSerializer(serializers.ModelSerializer):
    """Serializer for PostComment model"""
    user = UserLiteSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='user', write_only=True
    )
    
    class Meta:
        model = PostComment
        fields = ['id', 'post', 'user', 'user_id', 'content', 
                  'parent', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model"""
    user = UserLiteSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='user', write_only=True
    )
    comments = PostCommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'type', 'title', 'description', 'user', 'user_id',
            'upvotes', 'comments_count', 'tags', 'latitude', 'longitude',
            'comments', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'upvotes', 'comments_count', 'created_at', 'updated_at']


class VoteSerializer(serializers.ModelSerializer):
    """Serializer for Vote model (participatory budgeting)"""
    user = UserLiteSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='user', write_only=True
    )
    issue = IssueLiteSerializer(read_only=True)
    
    class Meta:
        model = Vote
        fields = ['id', 'user', 'user_id', 'vote_type', 'issue', 
                  'project_id', 'vote_value', 'justification', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate(self, data):
        # Ensure user hasn't already voted on this issue
        if data.get('issue'):
            existing_vote = Vote.objects.filter(
                user=data['user'],
                vote_type=data['vote_type'],
                issue=data['issue']
            ).first()
            if existing_vote:
                raise serializers.ValidationError("You have already voted on this issue")
        return data


class IoTSensorDataSerializer(serializers.ModelSerializer):
    """Serializer for IoT Sensor Data"""
    class Meta:
        model = IoTSensorData
        fields = ['id', 'sensor_type', 'location_name', 'latitude', 'longitude',
                  'readings', 'unit', 'status', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class EmergencyAlertSerializer(serializers.ModelSerializer):
    """Serializer for Emergency Alert model"""
    acknowledged_by = UserLiteSerializer(many=True, read_only=True)
    
    class Meta:
        model = EmergencyAlert
        fields = [
            'id', 'alert_type', 'priority', 'title', 'description',
            'latitude', 'longitude', 'affected_radius_km', 'is_active',
            'acknowledged_by', 'sms_sent', 'email_sent', 'push_sent',
            'created_at', 'expires_at', 'resolved_at'
        ]
        read_only_fields = ['id', 'created_at', 'resolved_at']


class AnalyticsSnapshotSerializer(serializers.ModelSerializer):
    """Serializer for Analytics Snapshot"""
    class Meta:
        model = AnalyticsSnapshot
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


# Additional API utility serializers

class GeoJSONFeatureSerializer(serializers.Serializer):
    """Serializer for GeoJSON feature format"""
    type = serializers.CharField(default='Feature')
    geometry = serializers.DictField()
    properties = serializers.DictField()


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    total_issues = serializers.IntegerField()
    active_issues = serializers.IntegerField()
    resolved_issues = serializers.IntegerField()
    total_posts = serializers.IntegerField()
    active_users = serializers.IntegerField()
    emergency_alerts = serializers.IntegerField()
    issues_by_category = serializers.DictField()
    recent_issues = IssueLiteSerializer(many=True)
    recent_posts = serializers.ListField()


class PredictiveInsightSerializer(serializers.Serializer):
    """Serializer for predictive analytics insights"""
    hotspot_areas = serializers.ListField()
    predicted_trends = serializers.DictField()
    recommendations = serializers.ListField()
    confidence_score = serializers.FloatField()
