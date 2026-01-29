from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q
from apps.dashboard.models import Notification as DashboardNotification
from .notification_models import Notification as ProfileNotification
from apps.dashboard.serializers import NotificationSerializer
from .notification_serializers import NotificationSerializer as ProfileNotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    User notifications API - combines both dashboard and profile notifications
    - Get all notifications
    - Get unread count
    - Mark as read
    - Mark all as read
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        """Return notifications for current user from both sources"""
        # Get dashboard notifications
        dashboard_notifs = list(DashboardNotification.objects.filter(
            recipient=self.request.user
        )[:25])
        
        # Get profile notifications (announcements, etc.)
        profile_notifs = list(ProfileNotification.objects.filter(
            recipient=self.request.user
        )[:25])
        
        # Combine and sort by created_at
        all_notifs = dashboard_notifs + profile_notifs
        all_notifs.sort(key=lambda x: x.created_at, reverse=True)
        
        return all_notifs[:50]  # Return top 50
    
    def list(self, request, *args, **kwargs):
        """Custom list to handle mixed notification types"""
        queryset = self.get_queryset()
        
        # Serialize each notification with appropriate serializer
        serialized = []
        for notif in queryset:
            if isinstance(notif, ProfileNotification):
                serializer = ProfileNotificationSerializer(notif)
            else:
                serializer = NotificationSerializer(notif)
            serialized.append(serializer.data)
        
        return Response({'results': serialized})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications from both sources"""
        dashboard_count = DashboardNotification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        
        profile_count = ProfileNotification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        
        total_count = dashboard_count + profile_count
        
        return Response({'unread_count': total_count})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a single notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        
        return Response({
            'status': 'success',
            'message': 'Notification marked as read'
        })
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all user's notifications as read"""
        dashboard_updated = DashboardNotification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)
        
        profile_updated = ProfileNotification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)
        
        total_updated = dashboard_updated + profile_updated
        
        return Response({
            'status': 'success',
            'message': f'{total_updated} notifications marked as read',
            'updated_count': total_updated
        })
    
    @action(detail=False, methods=['delete'])
    def clear_all(self, request):
        """Delete all read notifications"""
        dashboard_deleted, _ = DashboardNotification.objects.filter(
            recipient=request.user,
            is_read=True
        ).delete()
        
        profile_deleted, _ = ProfileNotification.objects.filter(
            recipient=request.user,
            is_read=True
        ).delete()
        
        total_deleted = dashboard_deleted + profile_deleted
        
        return Response({
            'status': 'success',
            'message': f'{total_deleted} notifications deleted',
            'deleted_count': total_deleted
        })
