from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileView
from .floor_wing_views import (
    FloorWingDashboardView,
    FloorWingStudentsView,
    FloorWingMentorsView,
    FloorWingAssignStudentView
)
from .admin_views import (
    AdminCampusOverviewView,
    AdminFloorDetailView,
    AdminAssignFloorWingView,
    AdminAssignMentorView,
    AdminStudentDetailView,
    AdminStatsView
)
from .announcement_views import FloorAnnouncementViewSet, StudentAnnouncementViewSet
from .notification_views import NotificationViewSet
from .views_import import import_dummy_users
from .views_mentors import setup_mentors
from .views_floorwings import setup_floorwings
from .mentor_assignment_views import (
    get_mentor_students,
    get_available_students,
    assign_student_to_self,
    reassign_student_to_mentor,
    admin_get_all_assignments,
    admin_reassign_student,
    get_floor_mentors
)

app_name = 'profiles'

# Router for announcements and notifications
router = DefaultRouter()
router.register(r'floor-wing/announcements', FloorAnnouncementViewSet, basename='floor-announcements')
router.register(r'student/announcements', StudentAnnouncementViewSet, basename='student-announcements')
router.register(r'notifications', NotificationViewSet, basename='notifications')

urlpatterns = [
    path('me/', UserProfileView.as_view(), name='user-profile'),
    
    # Floor Wing routes
    path('floor-wing/dashboard/', FloorWingDashboardView.as_view(), name='floor-wing-dashboard'),
    path('floor-wing/students/', FloorWingStudentsView.as_view(), name='floor-wing-students'),
    path('floor-wing/mentors/', FloorWingMentorsView.as_view(), name='floor-wing-mentors'),
    path('floor-wing/assign-student/', FloorWingAssignStudentView.as_view(), name='floor-wing-assign-student'),
    
    # Admin routes
    path('admin/stats/', AdminStatsView.as_view(), name='admin-stats'),
    path('admin/campus/<str:campus>/', AdminCampusOverviewView.as_view(), name='admin-campus-overview'),
    path('admin/campus/<str:campus>/floor/<int:floor>/', AdminFloorDetailView.as_view(), name='admin-floor-detail'),
    path('admin/assign-floor-wing/', AdminAssignFloorWingView.as_view(), name='admin-assign-floor-wing'),
    path('admin/assign-mentor/', AdminAssignMentorView.as_view(), name='admin-assign-mentor'),
    path('admin/student/<int:student_id>/', AdminStudentDetailView.as_view(), name='admin-student-detail'),
    
    # Import users endpoint (admin only)
    path('admin/import-users/', import_dummy_users, name='admin-import-users'),
    
    # Setup mentors endpoint (admin only)
    path('admin/setup-mentors/', setup_mentors, name='admin-setup-mentors'),
    
    # Setup floor wings endpoint (admin only)
    path('admin/setup-floorwings/', setup_floorwings, name='admin-setup-floorwings'),
    
    # Mentor assignment routes (mentors can assign students to themselves)
    path('mentor/my-students/', get_mentor_students, name='mentor-my-students'),
    path('mentor/available-students/', get_available_students, name='mentor-available-students'),
    path('mentor/assign-student/', assign_student_to_self, name='mentor-assign-student'),
    path('mentor/reassign-student/', reassign_student_to_mentor, name='mentor-reassign-student'),
    path('mentor/floor-mentors/', get_floor_mentors, name='get-floor-mentors'),
    
    # Admin mentor assignment routes (admins can modify all assignments)
    path('admin/assignments/', admin_get_all_assignments, name='admin-all-assignments'),
    path('admin/reassign-student/', admin_reassign_student, name='admin-reassign-student'),
    
    # Announcement routes (via router)
    path('', include(router.urls)),
]
