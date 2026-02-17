from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from django.core.paginator import Paginator

# Import Models
# Import Models
from tournaments.models import Tournament, MatchVote, MatchComment, Comment, Match
from accounts.models import Profile
from .models import Report, AuditLog
from django.views.decorators.http import require_POST
from django.http import JsonResponse


def is_admin(user):
    """Check if user is authenticated and is staff/superuser"""
    return user.is_authenticated and user.is_staff


def admin_required(view_func):
    """Decorator combining login_required and user_passes_test for admin"""
    decorated = login_required(login_url='/accounts/login/')(view_func)
    decorated = user_passes_test(is_admin, login_url='/')(decorated)
    return decorated


@admin_required
def admin_dashboard(request):
    """
    Main Admin Dashboard View
    Displays key metrics and recent activity.
    """
    # Stats
    total_users = User.objects.count()
    new_users_today = User.objects.filter(date_joined__gte=timezone.now().date()).count()
    total_tournaments = Tournament.objects.count()
    active_tournaments = Tournament.objects.filter(status='open').count()
    total_votes = MatchVote.objects.count()
    
    # Recent tournaments (5 newest)
    recent_tournaments = Tournament.objects.select_related('created_by').order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'new_users_today': new_users_today,
        'total_tournaments': total_tournaments,
        'active_tournaments': active_tournaments,
        'total_votes': total_votes,
        'pending_reports': Report.objects.filter(status='pending').count(),
        'recent_tournaments': recent_tournaments,
        'section': 'dashboard',
    }
    return render(request, 'custom_admin/dashboard.html', context)


@admin_required
def admin_tournament_list(request):
    """
    Tournament Management View
    Features: Search, Filter, Pagination
    """
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    
    tournaments = Tournament.objects.select_related('created_by').order_by('-created_at')
    
    # Search
    if query:
        tournaments = tournaments.filter(
            Q(name__icontains=query) | 
            Q(created_by__username__icontains=query)
        )
    
    # Filter
    if status_filter:
        tournaments = tournaments.filter(status=status_filter)
        
    # Pagination
    paginator = Paginator(tournaments, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Counts for header stats
    live_count = Tournament.objects.filter(status='open').count()
    waiting_count = Tournament.objects.filter(status='waiting').count()
    finished_count = Tournament.objects.filter(status='finished').count()

    context = {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'live_count': live_count,
        'waiting_count': waiting_count,
        'finished_count': finished_count,
        'section': 'tournaments',
    }
    return render(request, 'custom_admin/tournament_list.html', context)


@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_user_list(request):
    """
    User Management View
    Features: List, Search, Filter (Role), Ban/Unban Status
    """
    query = request.GET.get('q', '')
    role_filter = request.GET.get('role', '')
    
    users = User.objects.all().order_by('-date_joined')
    
    # Search
    if query:
        users = users.filter(
            Q(username__icontains=query) | 
            Q(email__icontains=query)
        )
    
    # Filter
    if role_filter == 'admin':
        users = users.filter(is_superuser=True)
    elif role_filter == 'staff':
        users = users.filter(is_staff=True, is_superuser=False)
    elif role_filter == 'user':
        users = users.filter(is_staff=False, is_superuser=False)
        
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Counts for header stats
    active_count = User.objects.filter(is_active=True).count()
    banned_count = User.objects.filter(is_active=False).count()

    context = {
        'page_obj': page_obj,
        'query': query,
        'role_filter': role_filter,
        'active_count': active_count,
        'banned_count': banned_count,
        'section': 'users',
    }
    return render(request, 'custom_admin/user_list.html', context)


@admin_required
def admin_delete_tournament(request, pk):
    """Delete a tournament"""
    if request.method == 'POST':
        tournament = get_object_or_404(Tournament, pk=pk)
        name = tournament.name
        
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='DELETE',
            target_model='Tournament',
            details=f'Deleted tournament: {name} (ID: {pk})',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        tournament.delete()
        messages.success(request, f'Tournament "{name}" has been deleted.')
    
    return redirect('custom_admin:tournament_list')


@admin_required
def admin_force_finish_tournament(request, pk):
    """Force finish a tournament"""
    if request.method == 'POST':
        tournament = get_object_or_404(Tournament, pk=pk)
        
        # Update status to finished
        tournament.status = 'finished'
        tournament.save()
        
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='FORCE_FINISH',
            target_model='Tournament',
            details=f'Force finished tournament: {tournament.name} (ID: {pk})',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, f'Tournament "{tournament.name}" has been marked as finished.')
    
    return redirect('custom_admin:tournament_list')


@admin_required
def admin_ban_user(request, pk):
    """Ban a user (set is_active to False)"""
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        
        # Don't allow banning superusers
        if user.is_superuser:
            messages.error(request, 'Cannot ban a superuser.')
            return redirect('custom_admin:user_list')
        
        user.is_active = False
        user.save()
        
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='BAN',
            target_model='User',
            details=f'Banned user: {user.username} (ID: {pk})',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, f'User "{user.username}" has been banned.')
    
    return redirect('custom_admin:user_list')


@admin_required
def admin_unban_user(request, pk):
    """Unban a user (set is_active to True)"""
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        
        user.is_active = True
        user.save()
        
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='UNBAN',
            target_model='User',
            details=f'Unbanned user: {user.username} (ID: {pk})',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, f'User "{user.username}" has been unbanned.')
    
    return redirect('custom_admin:user_list')


@admin_required
def admin_delete_user(request, pk):
    """Delete a user permanently"""
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        
        # Don't allow deleting superusers
        if user.is_superuser:
            messages.error(request, 'Cannot delete a superuser.')
            return redirect('custom_admin:user_list')
        
        username = user.username
        
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='DELETE',
            target_model='User',
            details=f'Deleted user: {username} (ID: {pk})',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        user.delete()
        messages.success(request, f'User "{username}" has been permanently deleted.')
    
    return redirect('custom_admin:user_list')


@admin_required
def admin_audit_logs(request):
    """View audit logs"""
    logs = AuditLog.objects.select_related('user').order_by('-created_at')
    
    paginator = Paginator(logs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'section': 'audit_logs',
    }
    return render(request, 'custom_admin/audit_logs.html', context)


@admin_required
def admin_reports(request):
    """View and manage reports"""
    status_filter = request.GET.get('status', '')
    
    reports = Report.objects.select_related(
        'reporter', 'target_user', 'target_tournament', 
        'target_match_comment', 'target_tournament_comment'
    ).order_by('-created_at')
    
    # Get counts for stats
    pending_count = Report.objects.filter(status='pending').count()
    resolved_count = Report.objects.filter(status='resolved').count()
    dismissed_count = Report.objects.filter(status='dismissed').count()
    
    if status_filter:
        reports = reports.filter(status=status_filter)
    
    paginator = Paginator(reports, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'section': 'reports',
        'pending_count': pending_count,
        'resolved_count': resolved_count,
        'dismissed_count': dismissed_count,
    }
    return render(request, 'custom_admin/reports.html', context)


@admin_required
def admin_resolve_report(request, pk):
    """Mark a report as resolved"""
    if request.method == 'POST':
        report = get_object_or_404(Report, pk=pk)
        report.status = 'resolved'
        report.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='RESOLVE_REPORT',
            target_model='Report',
            details=f'Resolved report #{pk}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, f'Report #{pk} has been resolved.')
    
    return redirect('custom_admin:reports')


@admin_required
def admin_dismiss_report(request, pk):
    """Dismiss a report"""
    if request.method == 'POST':
        report = get_object_or_404(Report, pk=pk)
        report.status = 'dismissed'
        report.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='DISMISS_REPORT',
            target_model='Report',
            details=f'Dismissed report #{pk}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, f'Report #{pk} has been dismissed.')
    
    return redirect('custom_admin:reports')


@admin_required
def admin_user_detail(request, pk):
    """
    User Detail View for Admin
    Shows profile info, stats, and created tournaments (read-only)
    """
    target_user = get_object_or_404(User, pk=pk)
    target_profile, created = Profile.objects.get_or_create(user=target_user)
    
    # Recent tournaments by this user
    user_tournaments = Tournament.objects.filter(created_by=target_user).order_by('-created_at')[:10]
    
    context = {
        'target_user': target_user,
        'target_profile': target_profile,
        'user_tournaments': user_tournaments,
        'section': 'users',
    }
    return render(request, 'custom_admin/user_detail.html', context)


@admin_required
@require_POST
def admin_delete_comment(request, pk):
    """Delete a comment (admin moderation)"""
    # We use MatchComment from tournaments
    comment = get_object_or_404(MatchComment, pk=pk)
    
    # Audit Log
    AuditLog.objects.create(
        user=request.user,
        action='DELETE_COMMENT',
        target_model='MatchComment',
        details=f'Deleted comment #{pk} by {comment.user.username}: "{comment.text}"',
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    comment.delete()
    
    return JsonResponse({'success': True})


@admin_required
@require_POST
def admin_delete_tournament_comment(request, pk):
    """Delete a tournament discussion comment (admin moderation)"""
    comment = get_object_or_404(Comment, pk=pk)
    
    # Audit Log
    AuditLog.objects.create(
        user=request.user,
        action='DELETE_COMMENT',
        target_model='Comment',
        details=f'Deleted tournament comment #{pk} by {comment.user.username}: "{comment.text}"',
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    comment.delete()
    
    return JsonResponse({'success': True})


@admin_required
@require_POST
def admin_force_start_tournament(request, pk):
    """Force start a tournament (admin action)"""
    tournament = get_object_or_404(Tournament, pk=pk)
    
    if tournament.status != "waiting":
        messages.error(request, "Tournament must be in 'Waiting' status to force start.")
        return redirect("custom_admin:tournament_list")
        
    competitors = list(tournament.competitors.all())
    # Check if we have enough competitors? Or just force it?
    # Better to check, otherwise it crashes.
    if len(competitors) < 2:
         messages.error(request, "Not enough competitors to start. Need at least 2.")
         return redirect("custom_admin:tournament_list")

    # Reuse publish logic (simplified)
    tournament.matches.all().delete()
    round_number = 1
    index = 1
    
    # Simple pairing
    # If odd number, one might be left out? 
    # Logic in publish_tournament uses range(0, len, 2)
    # We should follow that.
    
    for i in range(0, len(competitors) - 1, 2):
        c1 = competitors[i]
        c2 = competitors[i + 1]
        Match.objects.create(
            tournament=tournament,
            round_number=round_number,
            index_in_round=index,
            competitor1=c1,
            competitor2=c2,
            is_finished=False,
        )
        index += 1

    tournament.status = "open"
    tournament.current_round = 1
    tournament.save()
    
    # Audit Log
    AuditLog.objects.create(
        user=request.user,
        action='FORCE_START_TOURNAMENT',
        target_model='Tournament',
        details=f'Force started tournament #{pk}: {tournament.name}',
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    messages.success(request, f"Tournament '{tournament.name}' force started successfully.")
    return redirect("custom_admin:tournament_list")
