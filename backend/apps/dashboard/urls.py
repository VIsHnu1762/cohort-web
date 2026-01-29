from django.urls import path
from .views import DashboardStatsView, NotificationListView, NotificationMarkReadView
from .monthly_report import MonthlyReportView, AvailableMonthsView
from apps import mentor_views

urlpatterns = [
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('monthly-report/', MonthlyReportView.as_view(), name='monthly-report'),
    path('available-months/', AvailableMonthsView.as_view(), name='available-months'),
    path('notifications/', NotificationListView.as_view(), name='notifications-list'),
    path('notifications/<int:pk>/mark-read/', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    path('announcements/', mentor_views.student_announcements, name='student-announcements'),
    path('announcements/<int:announcement_id>/mark-read/', mentor_views.mark_announcement_read, name='mark-announcement-read'),
]
