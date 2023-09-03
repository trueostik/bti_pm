from django.contrib import admin

from .models import Subject, Comment, Subtask


admin.site.register(Subject)
admin.site.register(Comment)
admin.site.register(Subtask)

