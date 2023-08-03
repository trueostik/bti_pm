from django.urls import path

from . import views


app_name = 'bord'
urlpatterns = [
    path('', views.index, name='index'),
    path('subject/<int:subject_id>/', views.subject_view, name='subject'),
    path('new_subject/', views.new_subject, name='new_subject'),
    path('new_comment/<int:subject_id>/', views.new_comment, name='new_comment'),
    path('edit_comment/<int:comment_id>', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('edit_subject/<int:subject_id>', views.edit_subject, name='edit_subject'),
    path('delete_subject/<int:subject_id>', views.delete_subject, name='delete_subject'),
    path('change_status/<int:subject_id>/<str:field>', views.change_status, name='change_status'),
]
