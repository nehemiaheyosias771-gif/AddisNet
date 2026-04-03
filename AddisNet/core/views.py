"""Django Views for AddisNet Smart City Platform"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.conf import settings
import json
from .models import CustomUser, Issue, IssueComment, Post, PostComment, Vote, IoTSensorData, EmergencyAlert

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(request.GET.get('next', 'dashboard'))
        messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        from .forms import UserSignupForm
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Welcome to AddisNet!')
            return redirect('dashboard')
        messages.error(request, 'Please correct the errors below')
    else:
        from .forms import UserSignupForm
        form = UserSignupForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('login')

def dashboard(request):
    total_issues = Issue.objects.count()
    active_issues = Issue.objects.filter(status__in=['reported', 'confirmed', 'in_progress']).count()
    resolved_issues = Issue.objects.filter(status='resolved').count()
    total_posts = Post.objects.count()
    active_users = CustomUser.objects.filter(is_active=True).count()
    emergency_alerts_count = EmergencyAlert.objects.filter(is_active=True).count()
    issues_by_category = Issue.objects.values('category').annotate(count=Count('id')).order_by('-count')[:5]
    recent_issues = Issue.objects.select_related('user').order_by('-created_at')[:5]
    recent_posts = Post.objects.select_related('user').order_by('-created_at')[:3]
    active_emergencies = EmergencyAlert.objects.filter(is_active=True).order_by('-priority', '-created_at')[:3]
    context = {
        'total_issues': total_issues, 'active_issues': active_issues,
        'resolved_issues': resolved_issues, 'total_posts': total_posts,
        'active_users': active_users, 'emergency_alerts': emergency_alerts_count,
        'issues_by_category': issues_by_category, 'recent_issues': recent_issues,
        'recent_posts': recent_posts, 'active_emergencies': active_emergencies,
        'page_title': 'Dashboard',
    }
    return render(request, 'dashboard.html', context)

@login_required
def issue_list(request):
    issues = Issue.objects.select_related('user').all()
    if request.GET.get('category'):
        issues = issues.filter(category=request.GET.get('category'))
    if request.GET.get('severity'):
        issues = issues.filter(severity=request.GET.get('severity'))
    if request.GET.get('status'):
        issues = issues.filter(status=request.GET.get('status'))
    if request.GET.get('search'):
        issues = issues.filter(Q(title__icontains=request.GET.get('search')) | Q(description__icontains=request.GET.get('search')))
    paginator = Paginator(issues.order_by('-created_at'), 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {
        'page_obj': page_obj, 'categories': Issue.CATEGORY_CHOICES,
        'severities': Issue.SEVERITY_CHOICES, 'statuses': Issue.STATUS_CHOICES,
        'page_title': 'Reported Issues',
    }
    return render(request, 'issue_list.html', context)

@login_required
def report_issue(request):
    if request.method == 'POST':
        from .forms import IssueForm
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.ai_tags = []
            issue.urgency_score = 0.3
            if any(w in issue.title.lower() for w in ['emergency', 'urgent', 'critical']):
                issue.urgency_score = 0.8
                issue.ai_tags.append('urgent')
            issue.save()
            messages.success(request, 'Issue reported successfully!')
            return redirect('issue_detail', issue_id=issue.id)
        messages.error(request, 'Please correct the errors below')
    else:
        from .forms import IssueForm
        form = IssueForm()
    return render(request, 'report_issue.html', {'form': form, 'page_title': 'Report Issue'})

def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue.objects.select_related('user', 'assigned_to'), id=issue_id)
    issue.views += 1
    issue.save(update_fields=['views'])
    comments = issue.comments.select_related('user').order_by('-created_at')
    can_edit = request.user.is_authenticated and (request.user == issue.user or request.user.is_staff)
    similar_issues = Issue.objects.filter(category=issue.category, status__in=['reported', 'confirmed', 'in_progress']).exclude(id=issue.id)[:3]
    return render(request, 'issue_detail.html', {'issue': issue, 'comments': comments, 'can_edit': can_edit, 'similar_issues': similar_issues, 'page_title': issue.title})

@login_required
def edit_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    if request.user != issue.user and not request.user.is_staff:
        messages.error(request, 'Permission denied')
        return redirect('issue_detail', issue_id=issue_id)
    if request.method == 'POST':
        from .forms import IssueForm
        form = IssueForm(request.POST, request.FILES, instance=issue)
        if form.is_valid():
            form.save()
            messages.success(request, 'Issue updated')
            return redirect('issue_detail', issue_id=issue.id)
    else:
        from .forms import IssueForm
        form = IssueForm(instance=issue)
    return render(request, 'report_issue.html', {'form': form, 'page_title': 'Edit Issue'})

@login_required
def delete_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    if request.user != issue.user and not request.user.is_staff:
        messages.error(request, 'Permission denied')
        return redirect('issue_detail', issue_id=issue_id)
    if request.method == 'POST':
        issue.delete()
        messages.success(request, 'Issue deleted')
        return redirect('issue_list')
    return render(request, 'issue_confirm_delete.html', {'issue': issue})

@login_required
@require_http_methods(["POST"])
def upvote_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    issue.upvotes += 1
    issue.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'upvotes': issue.upvotes})
    messages.success(request, 'Upvoted!')
    return redirect('issue_detail', issue_id=issue_id)

@login_required
@require_http_methods(["POST"])
def add_issue_comment(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    content = request.POST.get('content')
    if content:
        IssueComment.objects.create(issue=issue, user=request.user, content=content, is_official_response=request.user.role in ['government', 'admin'])
        messages.success(request, 'Comment added')
    return redirect('issue_detail', issue_id=issue_id)

def map_view(request):
    issues = Issue.objects.filter(status__in=['reported', 'confirmed', 'in_progress'])
    if request.GET.get('category'):
        issues = issues.filter(category=request.GET.get('category'))
    return render(request, 'map.html', {'issues_count': issues.count(), 'map_config': settings.MAP_CONFIG, 'page_title': 'Issue Map'})

@login_required
@require_http_methods(["GET"])
def issues_geojson(request):
    issues = Issue.objects.filter(status__in=['reported', 'confirmed', 'in_progress'])
    features = [{'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [float(i.longitude), float(i.latitude)]}, 'properties': {'id': str(i.id), 'title': i.title, 'category': i.category, 'severity': i.severity, 'upvotes': i.upvotes}} for i in issues]
    return JsonResponse({'type': 'FeatureCollection', 'features': features})

def community_board(request):
    posts = Post.objects.select_related('user').all()
    if request.GET.get('type'):
        posts = posts.filter(type=request.GET.get('type'))
    if request.GET.get('search'):
        posts = posts.filter(Q(title__icontains=request.GET.get('search')) | Q(description__icontains=request.GET.get('search')))
    paginator = Paginator(posts.order_by('-created_at'), 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'community.html', {'page_obj': page_obj, 'post_types': Post.TYPE_CHOICES, 'page_title': 'Community Board'})

@login_required
def create_post(request):
    if request.method == 'POST':
        from .forms import PostForm
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created!')
            return redirect('post_detail', post_id=post.id)
    else:
        from .forms import PostForm
        form = PostForm()
    return render(request, 'create_post.html', {'form': form, 'page_title': 'Create Post'})

def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related('user'), id=post_id)
    comments = post.comments.select_related('user').order_by('-created_at')
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'page_title': post.title})

@login_required
@require_http_methods(["POST"])
def upvote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.upvotes += 1
    post.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'upvotes': post.upvotes})
    return redirect('post_detail', post_id=post_id)

@login_required
@require_http_methods(["POST"])
def add_post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content')
    if content:
        PostComment.objects.create(post=post, user=request.user, content=content)
        post.comments_count += 1
        post.save()
    return redirect('post_detail', post_id=post_id)

@login_required
def analytics_dashboard(request):
    total_issues = Issue.objects.count()
    resolved_rate = Issue.objects.filter(status='resolved').count() / max(total_issues, 1) * 100
    return render(request, 'analytics.html', {'total_issues': total_issues, 'resolved_rate': round(resolved_rate, 1), 'page_title': 'Analytics Dashboard'})

@login_required
@require_http_methods(["GET"])
def analytics_trends_api(request):
    start_date = timezone.now() - timezone.timedelta(days=30)
    return JsonResponse({'issues_created': Issue.objects.filter(created_at__gte=start_date).count(), 'issues_resolved': Issue.objects.filter(status='resolved', resolved_at__gte=start_date).count(), 'new_users': CustomUser.objects.filter(created_at__gte=start_date).count()})

@login_required
def participatory_budgeting(request):
    votable_issues = Issue.objects.filter(status__in=['reported', 'confirmed', 'in_progress'], severity__in=['high', 'critical']).annotate(vote_count=Count('budget_votes')).order_by('-vote_count', '-upvotes')
    total_budget = settings.BUDGET_CONFIG.get('total_budget', 10000000)
    voted_ids = list(Vote.objects.filter(user=request.user, vote_type='issue').values_list('issue_id', flat=True))
    return render(request, 'participatory_budget.html', {'votable_issues': votable_issues, 'total_budget': total_budget, 'voted_issue_ids': voted_ids, 'page_title': 'Participatory Budgeting'})

@login_required
@require_http_methods(["POST"])
def cast_budget_vote(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    if Vote.objects.filter(user=request.user, vote_type='issue', issue=issue).exists():
        messages.warning(request, 'Already voted')
        return redirect('participatory_budgeting')
    Vote.objects.create(user=request.user, vote_type='issue', issue=issue, justification=request.POST.get('justification', ''))
    messages.success(request, 'Vote cast!')
    return redirect('participatory_budgeting')

def emergency_alerts(request):
    alerts = EmergencyAlert.objects.filter(is_active=True).order_by('-priority', '-created_at')
    return render(request, 'emergency_alerts.html', {'active_alerts': alerts, 'page_title': 'Emergency Alerts'})

@login_required
def create_emergency_alert(request):
    if request.user.role not in ['government', 'admin', 'volunteer']:
        messages.error(request, 'Unauthorized')
        return redirect('emergency_alerts')
    if request.method == 'POST':
        from .forms import EmergencyAlertForm
        form = EmergencyAlertForm(request.POST)
        if form.is_valid():
            alert = form.save()
            alert.sms_sent = alert.email_sent = alert.push_sent = True
            alert.save()
            messages.success(request, 'Alert created!')
            return redirect('emergency_alerts')
    else:
        from .forms import EmergencyAlertForm
        form = EmergencyAlertForm()
    return render(request, 'create_emergency_alert.html', {'form': form})

@login_required
@require_http_methods(["POST"])
def acknowledge_alert(request, alert_id):
    alert = get_object_or_404(EmergencyAlert, id=alert_id)
    alert.acknowledged_by.add(request.user)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('emergency_alerts')

@login_required
def iot_dashboard(request):
    sensors = IoTSensorData.objects.order_by('-timestamp')
    return render(request, 'iot_dashboard.html', {'traffic_sensors': sensors.filter(sensor_type='traffic')[:5], 'water_sensors': sensors.filter(sensor_type='water_quality')[:5], 'air_sensors': sensors.filter(sensor_type='air_quality')[:5], 'page_title': 'IoT Dashboard'})

@login_required
@require_http_methods(["GET"])
def iot_sensors_api(request):
    sensors = IoTSensorData.objects.all()
    if request.GET.get('type'):
        sensors = sensors.filter(sensor_type=request.GET.get('type'))
    data = [{'id': str(s.id), 'type': s.sensor_type, 'location': s.location_name, 'readings': s.readings, 'status': s.status} for s in sensors.order_by('-timestamp')[:50]]
    return JsonResponse({'sensors': data})

@login_required
def settings_view(request):
    if request.method == 'POST':
        if request.POST.get('language_preference'):
            request.user.language_preference = request.POST.get('language_preference')
            request.user.save()
        request.session['dark_mode'] = request.POST.get('dark_mode') == 'on'
        messages.success(request, 'Settings updated')
    return render(request, 'settings.html', {'page_title': 'Settings'})

def profile_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'profile.html', {'profile_user': user, 'user_issues': Issue.objects.filter(user=user).order_by('-created_at')[:10], 'user_posts': Post.objects.filter(user=user).order_by('-created_at')[:5], 'page_title': f'{user.username} Profile'})

@login_required
def set_language(request, language):
    if language in ['en', 'am']:
        request.user.language_preference = language
        request.user.save()
        request.session['language'] = language
    return redirect(request.GET.get('next', 'dashboard'))

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)
