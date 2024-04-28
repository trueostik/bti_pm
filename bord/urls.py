from django.urls import path

from . import views


app_name = 'bord'
urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search_view, name='search'),
    path('archive', views.archive, name='archive'),
    path('todo', views.todo, name='todo'),
    path('add_to_archive/<int:subject_id>', views.add_to_archive, name='add_to_archive'),
    path('subject/<int:subject_id>/', views.subject_view, name='subject'),
    path('new_subject/', views.new_subject, name='new_subject'),
    path('new_comment/<int:subject_id>/', views.new_comment, name='new_comment'),
    path('edit_comment/<int:comment_id>', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('edit_subject/<int:subject_id>', views.edit_subject, name='edit_subject'),
    path('delete_subject/<int:subject_id>', views.delete_subject, name='delete_subject'),
    path('change_status/<int:subject_id>/<str:field>', views.change_status, name='change_status'),
    path('change_priority/<int:subject_id>/<str:priority>', views.change_priority, name='change_priority'),
    path('new_subtask/<int:subject_id>/', views.new_subtask, name='new_subtask'),
    path('check_subtask/<int:subtask_id>/', views.check_subtask, name='check_subtask'),
    path('edit_subtask/<int:subtask_id>', views.edit_subtask, name='edit_subtask'),
    path('delete_subtask/<int:subtask_id>', views.delete_subtask, name='delete_subtask'),
    path('delete_subtask_modal/<int:subtask_id>', views.delete_subtask_modal, name='delete_subtask_modal'),
    path('new_task/', views.new_task, name='new_task'),
    path('check_task/<int:task_id>/', views.check_task, name='check_task'),
    path('edit_task/<int:task_id>', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>', views.delete_task, name='delete_task'),
    path('contacts/<int:subject_id>/', views.contacts, name='contacts'),
    path('contact/<int:contact_id>/', views.contact, name='contact'),
    path('new_contact/<int:subject_id>/', views.new_contact, name='new_contact'),
    path('edit_contact/<int:contact_id>/', views.edit_contact, name='edit_contact'),
    path('delete_contact/<int:contact_id>', views.delete_contact, name='delete_contact'),
    path('delete_contact_modal/<int:contact_id>', views.delete_contact_modal, name='delete_contact_modal'),

]
