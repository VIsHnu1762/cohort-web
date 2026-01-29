"""
URL configuration for mentor-specific views
"""

from django.urls import path
from apps import mentor_views

app_name = 'mentor'

urlpatterns = [
    # Mentor dashboard overview
    path('dashboard/', mentor_views.get_mentor_dashboard, name='mentor-dashboard'),
    
    # Mentor students list
    path('students/', mentor_views.get_mentor_students, name='mentor-students'),
    
    # Pillar review endpoints
    path('pillar/<str:pillar>/submissions/', mentor_views.get_pillar_submissions, name='pillar-submissions'),
    path('pillar/<str:pillar>/stats/', mentor_views.get_pillar_stats, name='pillar-stats'),
    
    # Submission review
    path('review/', mentor_views.review_submission, name='review-submission'),
    
    # Submission detail
    path('submission/<str:pillar>/<str:submission_type>/<int:submission_id>/', 
         mentor_views.get_submission_detail, 
         name='submission-detail'),
    
    # Notifications
    path('notifications/', mentor_views.get_notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', mentor_views.mark_notification_read, name='mark-notification-read'),
    path('notifications/read-all/', mentor_views.mark_all_notifications_read, name='mark-all-notifications-read'),
    path('notifications/<int:notification_id>/', mentor_views.delete_notification, name='delete-notification'),
    
    # Messaging
    path('messages/threads/', mentor_views.get_message_threads, name='message-threads'),
    path('messages/thread/<int:user_id>/', mentor_views.get_thread_messages, name='thread-messages'),
    path('messages/send/', mentor_views.send_message, name='send-message'),
    path('messages/unread-counts/', mentor_views.get_unread_counts, name='unread-counts'),
    
    # Announcements
    path('announcements/', mentor_views.announcements, name='announcements'),
    path('announcements/<int:announcement_id>/', mentor_views.announcement_detail, name='announcement-detail'),
    
    # Student Monthly Reports (Mentor View)
    path('student/<int:student_id>/monthly-report/', mentor_views.get_student_monthly_report, name='student-monthly-report'),
    path('student/<int:student_id>/available-months/', mentor_views.get_student_available_months, name='student-available-months'),
]
