from django import template

register = template.Library()

@register.filter
def equals(value, arg):
    """Check if value equals arg - use in template like: {% if value|equals:arg %}"""
    return str(value) == str(arg)
