"""
Django REST Framework API Views for AddisNet
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import CustomUser, Issue, IssueComment, Post, PostComment, Vote, IoTSensorData, EmergencyAlert, AnalyticsSnapshot
from .serializers import (
    UserSerializer, IssueSerializer, IssueCommentSerializer, PostSerializer, 
    PostCommentSerializer, VoteSerializer, IoTSensorDataSerializer, 
    EmergencyAlertSerializer, AnalyticsSnapshotSerializer, IssueLiteSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all().order_by('-created_at')
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IssueCommentViewSet(viewsets.ModelViewSet):
    queryset = IssueComment.objects.all().order_by('-created_at')
    serializer_class = IssueCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all().order_by('-created_at')
    serializer_class = PostCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all().order_by('-created_at')
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IoTSensorDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IoTSensorData.objects.all().order_by('-timestamp')
    serializer_class = IoTSensorDataSerializer
    permission_classes = [permissions.AllowAny]


class EmergencyAlertViewSet(viewsets.ModelViewSet):
    queryset = EmergencyAlert.objects.filter(is_active=True).order_by('-priority', '-created_at')
    serializer_class = EmergencyAlertSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AnalyticsSnapshotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AnalyticsSnapshot.objects.all().order_by('-date')
    serializer_class = AnalyticsSnapshotSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upvote_issue_api(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    issue.upvotes += 1
    issue.save()
    return Response({'success': True, 'upvotes': issue.upvotes})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upvote_post_api(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.upvotes += 1
    post.save()
    return Response({'success': True, 'upvotes': post.upvotes})


@api_view(['GET'])
def issues_geojson_api(request):
    issues = Issue.objects.filter(status__in=['reported', 'confirmed', 'in_progress'])
    features = []
    for issue in issues:
        features.append({
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': [float(issue.longitude), float(issue.latitude)]},
            'properties': {
                'id': str(issue.id), 'title': issue.title, 'category': issue.category,
                'severity': issue.severity, 'status': issue.status, 'upvotes': issue.upvotes,
            }
        })
    return Response({'type': 'FeatureCollection', 'features': features})


@api_view(['GET'])
def analytics_dashboard_api(request):
    from django.db.models import Count
    total_issues = Issue.objects.count()
    resolved_rate = Issue.objects.filter(status='resolved').count() / max(total_issues, 1) * 100
    
    issues_by_category = list(Issue.objects.values('category').annotate(count=Count('id')).order_by('-count'))
    
    return Response({
        'total_issues': total_issues,
        'resolved_rate': round(resolved_rate, 1),
        'issues_by_category': issues_by_category,
    })


@api_view(['GET'])
def predictive_analytics_api(request):
    """Predictive analytics stub - in production integrate ML models"""
    hotspots = [
        {'area': 'Bole', 'risk': 0.75, 'category': 'traffic'},
        {'area': 'Piazza', 'risk': 0.65, 'category': 'infrastructure'},
        {'area': 'Merkato', 'risk': 0.80, 'category': 'waste'},
    ]
    
    trends = {
        'water': 'increasing',
        'transport': 'stable',
        'infrastructure': 'decreasing',
    }
    
    recommendations = [
        'Increase waste collection in Merkato area',
        'Schedule road maintenance in Piazza',
        'Monitor water quality in Bole sub-city',
    ]
    
    return Response({
        'hotspot_areas': hotspots,
        'predicted_trends': trends,
        'recommendations': recommendations,
        'confidence_score': 0.82,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cast_budget_vote_api(request):
    issue_id = request.data.get('issue_id')
    justification = request.data.get('justification', '')
    
    issue = get_object_or_404(Issue, id=issue_id)
    
    existing_vote = Vote.objects.filter(user=request.user, vote_type='issue', issue=issue).first()
    if existing_vote:
        return Response({'error': 'Already voted'}, status=status.HTTP_400_BAD_REQUEST)
    
    Vote.objects.create(user=request.user, vote_type='issue', issue=issue, justification=justification)
    return Response({'success': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_emergency_alert_api(request):
    if request.user.role not in ['government', 'admin', 'volunteer']:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = EmergencyAlertSerializer(data=request.data)
    if serializer.is_valid():
        alert = serializer.save()
        alert.sms_sent = True
        alert.email_sent = True
        alert.push_sent = True
        alert.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
