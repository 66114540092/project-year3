from .models import Report


def admin_context(request):
    """Add pending_reports count to all admin templates"""
    context = {}
    
    if request.user.is_authenticated and request.user.is_staff:
        context['pending_reports'] = Report.objects.filter(status='pending').count()
    
    return context
