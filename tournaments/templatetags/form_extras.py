from django import template

register = template.Library()

@register.filter(name="add_class")
def add_class(bound_field, css_classes):
    """Append CSS classes to a form field's existing widget classes.

    Usage: {{ form.field|add_class:"form-control" }}
    """
    if not hasattr(bound_field, "as_widget"):
        return bound_field
    existing = bound_field.field.widget.attrs.get("class", "")
    new_classes = f"{existing} {css_classes}".strip()
    attrs = {**bound_field.field.widget.attrs, "class": new_classes}
    return bound_field.as_widget(attrs=attrs)
