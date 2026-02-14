from django.db import models
from django.contrib.auth.models import User
from tournaments.models import Tournament, Comment, MatchComment

class Report(models.Model):
    """Refined Report model for Content Moderation"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]

    reporter = models.ForeignKey(User, related_name='filed_reports', on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Polymorphic-like targets (keep it simple with nullable FKs)
    target_user = models.ForeignKey(
        User, 
        related_name='reports_received', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Report a specific user for behavior"
    )
    target_match_comment = models.ForeignKey(
        MatchComment, 
        related_name='reports', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Report a live match chat message"
    )
    target_tournament_comment = models.ForeignKey(
        Comment, 
        related_name='reports', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Report a tournament discussion comment"
    )
    target_tournament = models.ForeignKey(
        Tournament, 
        related_name='reports', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Report a tournament for inappropriate content"
    )

    admin_note = models.TextField(blank=True, help_text="Internal notes by admin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report {self.pk} by {self.reporter}"


class AuditLog(models.Model):
    """Simplified Audit Log for tracking Admin actions"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text="Who performed the action")
    action = models.CharField(max_length=50, help_text="e.g., DELETE, UPDATE, BAN")
    target_model = models.CharField(max_length=50, help_text="e.g., Tournament, User")
    details = models.TextField(help_text="JSON-like details of what changed")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} {self.action} {self.target_model}"

