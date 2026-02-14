from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('users/', views.admin_user_list, name='user_list'),
    
    # Tournament Management
    path('tournaments/', views.admin_tournament_list, name='tournament_list'),
    path('tournaments/<int:pk>/delete/', views.admin_delete_tournament, name='delete_tournament'),
    path('tournaments/<int:pk>/force-finish/', views.admin_force_finish_tournament, name='force_finish_tournament'),
    
    # User Management
    path('users/<int:pk>/', views.admin_user_detail, name='user_detail'),
    path('users/<int:pk>/ban/', views.admin_ban_user, name='ban_user'),
    path('users/<int:pk>/unban/', views.admin_unban_user, name='unban_user'),
    path('users/<int:pk>/delete/', views.admin_delete_user, name='delete_user'),
    
    # Audit Logs
    path('audit-logs/', views.admin_audit_logs, name='audit_logs'),
    
    # Reports
    path('reports/', views.admin_reports, name='reports'),
    path('reports/<int:pk>/resolve/', views.admin_resolve_report, name='resolve_report'),
    path('reports/<int:pk>/dismiss/', views.admin_dismiss_report, name='dismiss_report'),
    
    # Moderation
    path('comments/<int:pk>/delete/', views.admin_delete_comment, name='delete_comment'),
    path('tournament-comments/<int:pk>/delete/', views.admin_delete_tournament_comment, name='delete_tournament_comment'),
]

