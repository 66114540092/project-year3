from django import template
from accounts.models import Profile

register = template.Library()

@register.filter
def has_profile(user):
    """Check if user has a profile, create if missing (lazy creation)"""
    if not user.is_authenticated:
        return False
    
    try:
        return user.profile is not None
    except Profile.DoesNotExist:
        # Auto-create profile for legacy users
        Profile.objects.create(user=user)
        return True

@register.filter
def avatar_url(user):
    """Safely get avatar URL, create profile if missing"""
    if not user.is_authenticated:
        return None
        
    try:
        if user.profile.avatar:
            return user.profile.avatar.url
    except Profile.DoesNotExist:
        Profile.objects.create(user=user)
    
    return None
