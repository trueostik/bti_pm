from django import template
from bord.models import Task

register = template.Library()


@register.filter
def unfinished_tasks_count(user):
    if user.is_authenticated:
        return Task.objects.filter(user=user, done=False).count()
    return 0
