from django.urls import path
from .views import HackathonListView
from .jobs_views import JobInternshipListView

urlpatterns = [
    path('list/', HackathonListView.as_view(), name='hackathon_list'),
    path('jobs/', JobInternshipListView.as_view(), name='job_internship_list'),
]
