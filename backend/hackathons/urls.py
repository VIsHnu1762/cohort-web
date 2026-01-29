from django.urls import path
from .views import HackathonListView

urlpatterns = [
    path('list/', HackathonListView.as_view(), name='hackathon_list'),
]
