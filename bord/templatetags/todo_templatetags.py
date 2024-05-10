from django import template
from bord.models import Task, Subject

register = template.Library()


@register.filter
def unfinished_tasks_count(user):
    if user.is_authenticated:
        return Task.objects.filter(user=user, done=False).count()
    return 0


@register.filter
def my_subjects_count(user):
    if user.is_authenticated:
        return Subject.objects.filter(user=user, archived=False).count()
    return 0
