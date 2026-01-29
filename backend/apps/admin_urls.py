from django.urls import path
from apps import admin_views

urlpatterns = [
    path('users/', admin_views.get_all_users, name='admin_get_users'),
    path('assign-mentor/', admin_views.assign_mentor_to_student, name='admin_assign_mentor'),
    path('bulk-assign-mentor/', admin_views.bulk_assign_mentor, name='admin_bulk_assign'),
    path('auto-assign-mentors/', admin_views.auto_assign_mentors, name='admin_auto_assign'),
]
