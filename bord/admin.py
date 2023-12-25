from django.contrib import admin

from .models import Subject, Comment, Subtask, Task


admin.site.register(Subject)
admin.site.register(Comment)
admin.site.register(Subtask)
admin.site.register(Task)

