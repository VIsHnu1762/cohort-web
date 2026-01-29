from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q, Count, Avg
from django.contrib.auth.models import User
from .models import FloorAnnouncement, UserProfile
from .notification_models import Notification
from .announcement_serializers import FloorAnnouncementSerializer, FloorAnnouncementListSerializer
from .permissions import IsFloorWing


class FloorAnnouncementViewSet(viewsets.ModelViewSet):
    """
    Floor Wing Announcements CRUD
    - Create, update, delete announcements
    - Scoped to floor wing's campus + floor
    """
    permission_classes = [IsAuthenticated, IsFloorWing]
    serializer_class = FloorAnnouncementSerializer
    
    def get_queryset(self):
        """Return announcements for floor wing's campus and floor only"""
        user = self.request.user
        return FloorAnnouncement.objects.filter(
            campus=user.profile.campus,
            floor=user.profile.floor,
            floor_wing=user
        ).select_related('floor_wing')
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view"""
        if self.action == 'list':
            return FloorAnnouncementListSerializer
        return FloorAnnouncementSerializer
    
    def perform_create(self, serializer):
        """Save announcement with auto-set campus/floor and create notifications"""
        announcement = serializer.save()
        
        # If announcement is published, create notifications for all students on the floor
        if announcement.status == 'published':
            self._create_notifications_for_floor(announcement)
    
    def perform_update(self, serializer):
        """Update announcement and create notifications if status changed to published"""
        old_status = self.get_object().status
        announcement = serializer.save()
        
        # If announcement was just published, create notifications
        if old_status != 'published' and announcement.status == 'published':
            self._create_notifications_for_floor(announcement)
    
    def _create_notifications_for_floor(self, announcement):
        """Create notifications for all students on the same campus and floor"""
        # Get all students on the same campus and floor
        students = UserProfile.objects.filter(
            campus=announcement.campus,
            floor=announcement.floor,
            role='STUDENT'
        ).select_related('user')
        
        # Create notifications for each student
        notifications = []
        for student_profile in students:
            notifications.append(Notification(
                recipient=student_profile.user,
                notification_type='floor_announcement',
                title=f"New Announcement: {announcement.title}",
                message=announcement.message[:200],  # Truncate if too long
                announcement_id=announcement.id
            ))
        
        # Bulk create all notifications at once
        if notifications:
            Notification.objects.bulk_create(notifications)
            print(f"Created {len(notifications)} notifications for announcement: {announcement.title}")
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get announcement statistics for floor wing"""
        user = request.user
        queryset = self.get_queryset()
        
        total = queryset.count()
        published = queryset.filter(status='published').count()
        drafts = queryset.filter(status='draft').count()
        
        # Get read statistics
        published_announcements = queryset.filter(status='published')
        total_reads = sum(a.read_count for a in published_announcements)
        
        # Get student count on floor
        student_count = UserProfile.objects.filter(
            campus=user.profile.campus,
            floor=user.profile.floor,
            role='STUDENT'
        ).count()
        
        return Response({
            'total_announcements': total,
            'published': published,
            'drafts': drafts,
            'total_reads': total_reads,
            'students_on_floor': student_count,
            'avg_read_rate': round((total_reads / (published * student_count)) * 100, 1) if published and student_count else 0
        })


class StudentAnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Student-facing announcements
    - Read-only
    - Scoped to student's campus + floor
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FloorAnnouncementSerializer
    
    def get_queryset(self):
        """Return published announcements for student's campus and floor"""
        user = self.request.user
        
        # Students see announcements for their floor
        if user.profile.role == 'STUDENT':
            return FloorAnnouncement.objects.filter(
                campus=user.profile.campus,
                floor=user.profile.floor,
                status='published'
            ).filter(
                Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())
            ).select_related('floor_wing').order_by('-created_at')
        
        return FloorAnnouncement.objects.none()
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark announcement as read by student"""
        announcement = self.get_object()
        announcement.mark_as_read(request.user)
        return Response({'status': 'marked as read'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread announcements"""
        queryset = self.get_queryset()
        unread = queryset.exclude(read_by=request.user).count()
        return Response({'unread_count': unread})
