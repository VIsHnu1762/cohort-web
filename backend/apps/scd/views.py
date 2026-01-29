from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction

from .models import LeetCodeProfile, LeetCodeSubmission, ProgressSnapshot
from .serializers import (
    LeetCodeProfileSerializer,
    LeetCodeProfileCreateSerializer,
    LeetCodeSubmissionSerializer,
    ProgressSnapshotSerializer,
    LeetCodeSyncSerializer
)
from .leetcode_api import LeetCodeAPI


class LeetCodeProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing LeetCode profiles
    
    Endpoints:
    - GET /api/scd/profiles/ - List user's profiles
    - POST /api/scd/profiles/ - Create new profile
    - GET /api/scd/profiles/{id}/ - Get profile details
    - PUT/PATCH /api/scd/profiles/{id}/ - Update profile
    - DELETE /api/scd/profiles/{id}/ - Delete profile
    - POST /api/scd/profiles/sync/ - Sync data from LeetCode API
    - POST /api/scd/profiles/{id}/submit/ - Submit for review
    - GET /api/scd/profiles/stats/ - Get user stats
    """
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return profiles for the current user"""
        return LeetCodeProfile.objects.filter(user=self.request.user).prefetch_related(
            'submissions', 'snapshots'
        )
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ['create', 'update', 'partial_update']:
            return LeetCodeProfileCreateSerializer
        elif self.action == 'sync':
            return LeetCodeSyncSerializer
        return LeetCodeProfileSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new profile and return full serializer with ID"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        # Return full serializer with ID
        output_serializer = LeetCodeProfileSerializer(instance)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def sync(self, request):
        """
        Sync LeetCode profile data from the API
        
        POST /api/scd/profiles/sync/
        Body: {"leetcode_username": "username"}
        """
        serializer = LeetCodeSyncSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['leetcode_username']
        
        # Fetch data from LeetCode API
        profile_data = LeetCodeAPI.fetch_user_profile(username)
        
        if not profile_data:
            return Response(
                {'error': 'Failed to fetch LeetCode profile. Please check the username and try again.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Fetch additional data (non-critical, can timeout)
        warnings = []
        
        contest_info = LeetCodeAPI.fetch_contest_info(username)
        if not contest_info:
            warnings.append('Contest data unavailable - LeetCode API timeout or no contest history')
        
        calendar_data = LeetCodeAPI.fetch_calendar_data(username)
        if not calendar_data:
            warnings.append('Calendar data unavailable - LeetCode API timeout')
        
        try:
            with transaction.atomic():
                # Get or create profile
                profile, created = LeetCodeProfile.objects.get_or_create(
                    user=request.user,
                    leetcode_username=username,
                    defaults={
                        'total_solved': profile_data['total_solved'],
                        'easy_solved': profile_data['easy_solved'],
                        'medium_solved': profile_data['medium_solved'],
                        'hard_solved': profile_data['hard_solved'],
                        'ranking': profile_data['ranking'],
                        'contest_rating': contest_info['rating'] if contest_info else None,
                        'streak': calendar_data['streak'] if calendar_data else 0,
                        'monthly_problems_count': calendar_data['monthly_problems'] if calendar_data else 0,
                        'total_active_days': calendar_data['total_active_days'] if calendar_data else 0,
                        'submission_calendar': calendar_data['submission_calendar'] if calendar_data else {},
                    }
                )
                
                # Update existing profile
                if not created:
                    profile.total_solved = profile_data['total_solved']
                    profile.easy_solved = profile_data['easy_solved']
                    profile.medium_solved = profile_data['medium_solved']
                    profile.hard_solved = profile_data['hard_solved']
                    profile.ranking = profile_data['ranking']
                    if contest_info:
                        profile.contest_rating = contest_info['rating']
                    if calendar_data:
                        profile.streak = calendar_data['streak']
                        profile.monthly_problems_count = calendar_data['monthly_problems']
                        profile.total_active_days = calendar_data['total_active_days']
                        profile.submission_calendar = calendar_data['submission_calendar']
                    profile.save()
                
                # Check if monthly target is met (minimum 10 problems)
                monthly_target_met = (calendar_data and calendar_data['monthly_problems'] >= 10) if calendar_data else False
                
                # If target not met, create notification for mentor
                if not monthly_target_met and hasattr(request.user, 'profile') and request.user.profile.assigned_mentor:
                    from apps.dashboard.models import Notification
                    from datetime import datetime
                    
                    # Check if notification already exists for this month
                    current_month = datetime.now().strftime('%Y-%m')
                    existing_notif = Notification.objects.filter(
                        user=request.user.profile.assigned_mentor,
                        message__contains=f"monthly target ({current_month})",
                        created_at__month=datetime.now().month,
                        created_at__year=datetime.now().year
                    ).exists()
                    
                    if not existing_notif:
                        problems_count = calendar_data['monthly_problems'] if calendar_data else 0
                        student_name = request.user.get_full_name() or request.user.username
                        Notification.objects.create(
                            user=request.user.profile.assigned_mentor,
                            message=f"{student_name} has only solved {problems_count}/10 problems this month on LeetCode (monthly target ({current_month}))",
                            notification_type='warning'
                        )
                
                # Create progress snapshot
                ProgressSnapshot.objects.create(
                    profile=profile,
                    total_solved=profile_data['total_solved'],
                    easy_solved=profile_data['easy_solved'],
                    medium_solved=profile_data['medium_solved'],
                    hard_solved=profile_data['hard_solved'],
                    ranking=profile_data['ranking']
                )
                
                # Fetch and save recent submissions (non-critical)
                recent_submissions = LeetCodeAPI.fetch_recent_submissions(username, limit=20)
                if not recent_submissions:
                    warnings.append('Recent submissions unavailable - LeetCode API timeout')
                
                # Clear old submissions and add new ones
                if recent_submissions:
                    profile.submissions.all().delete()
                    for sub_data in recent_submissions:
                        LeetCodeSubmission.objects.create(
                            profile=profile,
                            **sub_data
                        )
                
                # Return updated profile with warnings
                output_serializer = LeetCodeProfileSerializer(profile)
                response_data = {
                    'message': 'Profile synced successfully' + (' with warnings' if warnings else ''),
                    'profile': output_serializer.data
                }
                
                if warnings:
                    response_data['warnings'] = warnings
                
                return Response(response_data, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response(
                {'error': f'Failed to sync profile: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        Submit profile for mentor review
        
        POST /api/scd/profiles/{id}/submit/
        Body: {"screenshot_url": "https://..."}
        """
        profile = self.get_object()
        
        # Validate that profile is in draft status
        if profile.status not in ['draft', None, '']:
            return Response(
                {'error': f'Cannot submit profile with status: {profile.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate required fields
        screenshot_url = request.data.get('screenshot_url', '').strip()
        
        if not screenshot_url:
            return Response(
                {'error': 'Screenshot URL is required for submission'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update profile
        profile.screenshot_url = screenshot_url
        profile.status = 'pending'
        profile.submitted_at = timezone.now()
        profile.save()
        
        # Return full serializer
        serializer = LeetCodeProfileSerializer(profile)
        return Response({
            'message': 'Profile submitted for review successfully',
            'profile': serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get statistics for user's LeetCode profiles
        
        GET /api/scd/profiles/stats/
        """
        user_profiles = self.get_queryset()
        
        stats = {
            'total_profiles': user_profiles.count(),
            'draft': user_profiles.filter(status='draft').count(),
            'pending': user_profiles.filter(status='pending').count(),
            'approved': user_profiles.filter(status='approved').count(),
            'rejected': user_profiles.filter(status='rejected').count(),
        }
        
        # Get latest profile
        latest_profile = user_profiles.first()
        if latest_profile:
            stats['latest_profile'] = {
                'username': latest_profile.leetcode_username,
                'total_solved': latest_profile.total_solved,
                'ranking': latest_profile.ranking,
                'status': latest_profile.status
            }
        
        return Response(stats, status=status.HTTP_200_OK)
