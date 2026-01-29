from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Count, Q
from django.core.cache import cache
from datetime import datetime
import traceback
from .models import Notification
from .serializers import NotificationSerializer
from apps.clt.models import CLTSubmission
# SRI models not yet implemented, so we'll handle it gracefully
try:
    from apps.sri.models import SocialActivitySubmission
    HAS_SRI_MODELS = True
except ImportError:
    HAS_SRI_MODELS = False
from apps.cfc.models import HackathonSubmission, BMCVideoSubmission, InternshipSubmission, GenAIProjectSubmission
from apps.iipc.models import LinkedInPostVerification, LinkedInConnectionVerification
from apps.scd.models import LeetCodeProfile


class DashboardStatsView(APIView):
    """
    Aggregate statistics from all 5 pillars for the dashboard
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            cache_key = f'dashboard_stats_{user.id}'
            
            # Check cache first (5 minutes)
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
            
            # Monthly task requirements
            MONTHLY_REQUIREMENTS = {
                'clt': 1,      # 1 certificate upload per month
                'sri': 0,      # Not specified
                'cfc': 3,      # 3 tasks: hackathon, BMC, GenAI project (internship is optional)
                'iipc': 2,     # 2 tasks: LinkedIn post and connection
                'scd': 1,      # 1 profile with minimum 10 problems
            }
            
            # CLT Stats (1 submission per month required)
            clt_submissions = CLTSubmission.objects.filter(user=user)
            clt_completed = clt_submissions.filter(status='approved').count()
            clt_stats = {
                'total': clt_submissions.count(),
                'completed': clt_completed,
                'pending': clt_submissions.filter(status__in=['draft', 'submitted', 'under_review']).count(),
                'monthly_target': MONTHLY_REQUIREMENTS['clt'],
                'percentage': min(100, round((clt_completed / MONTHLY_REQUIREMENTS['clt']) * 100)) if MONTHLY_REQUIREMENTS['clt'] > 0 else 0,
                'recent_activity': self.get_clt_recent_activity(user),
            }
            
            # SRI Stats (handle if models not yet implemented)
            if HAS_SRI_MODELS:
                sri_submissions = SocialActivitySubmission.objects.filter(user=user)
                sri_completed = sri_submissions.filter(status='approved').count()
                sri_stats = {
                    'total': sri_submissions.count(),
                    'completed': sri_completed,
                    'pending': sri_submissions.filter(status__in=['draft', 'submitted', 'under_review']).count(),
                    'monthly_target': MONTHLY_REQUIREMENTS['sri'],
                    'percentage': 0,
                    'recent_activity': self.get_sri_recent_activity(user),
                }
            else:
                # SRI models not implemented yet - return empty stats
                sri_stats = {
                    'total': 0,
                    'completed': 0,
                    'pending': 0,
                    'monthly_target': MONTHLY_REQUIREMENTS['sri'],
                    'percentage': 0,
                    'recent_activity': [],
                }
            
            # CFC Stats (4 tasks per month: hackathon, BMC, internship, GenAI)
            hackathons = HackathonSubmission.objects.filter(user=user)
            bmc_videos = BMCVideoSubmission.objects.filter(user=user)
            internships = InternshipSubmission.objects.filter(user=user)
            genai_projects = GenAIProjectSubmission.objects.filter(user=user)
            
            cfc_total = hackathons.count() + bmc_videos.count() + internships.count() + genai_projects.count()
            cfc_completed = (
                hackathons.filter(status='approved').count() +
                bmc_videos.filter(status='approved').count() +
                internships.filter(status='approved').count() +
                genai_projects.filter(status='approved').count()
            )
            
            cfc_stats = {
                'total': cfc_total,
                'completed': cfc_completed,
                'pending': cfc_total - cfc_completed,
                'monthly_target': MONTHLY_REQUIREMENTS['cfc'],
                'percentage': min(100, round((cfc_completed / MONTHLY_REQUIREMENTS['cfc']) * 100)) if MONTHLY_REQUIREMENTS['cfc'] > 0 else 0,
                'hackathons': hackathons.count(),
                'bmc_videos': bmc_videos.count(),
                'internships': internships.count(),
                'genai_projects': genai_projects.count(),
                'recent_activity': self.get_cfc_recent_activity(user),
            }
            
            # IIPC Stats (2 tasks per month: LinkedIn post and connection)
            linkedin_posts = LinkedInPostVerification.objects.filter(user=user)
            linkedin_connections = LinkedInConnectionVerification.objects.filter(user=user)
            
            iipc_total = linkedin_posts.count() + linkedin_connections.count()
            iipc_completed = (
                linkedin_posts.filter(status='approved').count() +
                linkedin_connections.filter(status='approved').count()
            )
            
            iipc_stats = {
                'total': iipc_total,
                'completed': iipc_completed,
                'pending': iipc_total - iipc_completed,
                'monthly_target': MONTHLY_REQUIREMENTS['iipc'],
                'percentage': min(100, round((iipc_completed / MONTHLY_REQUIREMENTS['iipc']) * 100)) if MONTHLY_REQUIREMENTS['iipc'] > 0 else 0,
                'posts': linkedin_posts.count(),
                'connections': linkedin_connections.count(),
                'recent_activity': self.get_iipc_recent_activity(user),
            }
            
            # SCD Stats (1 profile with minimum 10 problems per month)
            leetcode_profiles = LeetCodeProfile.objects.filter(user=user)
            # Count profiles with at least 10 problems solved and approved
            scd_completed = leetcode_profiles.filter(
                status='approved',
                total_solved__gte=10
            ).count()
            
            scd_stats = {
                'total': leetcode_profiles.count(),
                'completed': scd_completed,
                'pending': leetcode_profiles.filter(status__in=['draft', 'pending']).count(),
                'monthly_target': MONTHLY_REQUIREMENTS['scd'],
                'percentage': min(100, round((scd_completed / MONTHLY_REQUIREMENTS['scd']) * 100)) if MONTHLY_REQUIREMENTS['scd'] > 0 else 0,
                'total_problems_solved': sum(p.total_solved or 0 for p in leetcode_profiles),
                'recent_activity': self.get_scd_recent_activity(user),
            }
            
            # Calculate overall progress based on monthly targets
            total_monthly_target = sum(MONTHLY_REQUIREMENTS.values())
            total_completed_towards_target = sum([
                min(clt_stats['completed'], MONTHLY_REQUIREMENTS['clt']),
                min(sri_stats['completed'], MONTHLY_REQUIREMENTS['sri']),
                min(cfc_stats['completed'], MONTHLY_REQUIREMENTS['cfc']),
                min(iipc_stats['completed'], MONTHLY_REQUIREMENTS['iipc']),
                min(scd_stats['completed'], MONTHLY_REQUIREMENTS['scd'])
            ])
            overall_percentage = round((total_completed_towards_target / total_monthly_target * 100)) if total_monthly_target > 0 else 0
            
            # Aggregate all recent activities
            all_activities = []
            all_activities.extend(clt_stats['recent_activity'])
            all_activities.extend(sri_stats['recent_activity'])
            all_activities.extend(cfc_stats['recent_activity'])
            all_activities.extend(iipc_stats['recent_activity'])
            all_activities.extend(scd_stats['recent_activity'])
            
            # Sort by date and get top 5
            all_activities.sort(key=lambda x: x['date'], reverse=True)
            recent_activities = all_activities[:5]
            
            # Get pending notifications
            notifications = self.get_notifications(user)
            
            # Get student info including mentor
            student_info = self.get_student_info(user)
            
            data = {
                'student_info': student_info,
                'overall': {
                    'percentage': overall_percentage,
                    'monthly_target': total_monthly_target,
                    'completed': total_completed_towards_target,
                },
                'pillars': {
                    'clt': clt_stats,
                    'sri': sri_stats,
                    'cfc': cfc_stats,
                    'iipc': iipc_stats,
                    'scd': scd_stats,
                },
                'recent_activities': recent_activities,
                'notifications': notifications,
            }
            
            # Cache for 5 minutes
            cache.set(cache_key, data, 300)
            
            return Response(data)
            
        except Exception as e:
            # Log the error for debugging
            print(f"Dashboard API Error: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            
            # Return error response
            return Response(
            {
                'error': 'Failed to fetch dashboard data',
                'detail': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    def get_clt_recent_activity(self, user):
        submissions = CLTSubmission.objects.filter(user=user).order_by('-updated_at')[:3]
        return [{
            'id': f'clt-{s.id}',
            'title': f'CLT: {s.title}',
            'status': s.status,
            'date': s.updated_at.isoformat(),
            'pillar': 'clt',
        } for s in submissions]
    
    def get_sri_recent_activity(self, user):
        if not HAS_SRI_MODELS:
            return []
        submissions = SocialActivitySubmission.objects.filter(user=user).order_by('-updated_at')[:3]
        return [{
            'id': f'sri-{s.id}',
            'title': f'SRI: {s.activity_title}',
            'status': s.status,
            'date': s.updated_at.isoformat(),
            'pillar': 'sri',
        } for s in submissions]
    
    def get_cfc_recent_activity(self, user):
        activities = []
        
        # Get recent from each CFC module
        hackathons = HackathonSubmission.objects.filter(user=user).order_by('-updated_at')[:2]
        for h in hackathons:
            activities.append({
                'id': f'cfc-hackathon-{h.id}',
                'title': f'CFC: Hackathon - {h.hackathon_name}',
                'status': h.status,
                'date': h.updated_at.isoformat(),
                'pillar': 'cfc',
            })
        
        internships = InternshipSubmission.objects.filter(user=user).order_by('-updated_at')[:2]
        for i in internships:
            activities.append({
                'id': f'cfc-internship-{i.id}',
                'title': f'CFC: Internship - {i.company}',
                'status': i.status,
                'date': i.updated_at.isoformat(),
                'pillar': 'cfc',
            })
        
        return sorted(activities, key=lambda x: x['date'], reverse=True)[:3]
    
    def get_iipc_recent_activity(self, user):
        activities = []
        
        posts = LinkedInPostVerification.objects.filter(user=user).order_by('-updated_at')[:2]
        for p in posts:
            activities.append({
                'id': f'iipc-post-{p.id}',
                'title': f'IIPC: LinkedIn Post',
                'status': p.status,
                'date': p.updated_at.isoformat(),
                'pillar': 'iipc',
            })
        
        connections = LinkedInConnectionVerification.objects.filter(user=user).order_by('-updated_at')[:2]
        for c in connections:
            activities.append({
                'id': f'iipc-connection-{c.id}',
                'title': f'IIPC: LinkedIn Connections - {c.total_connections} connections',
                'status': c.status,
                'date': c.updated_at.isoformat(),
                'pillar': 'iipc',
            })
        
        return sorted(activities, key=lambda x: x['date'], reverse=True)[:3]
    
    def get_scd_recent_activity(self, user):
        profiles = LeetCodeProfile.objects.filter(user=user).order_by('-updated_at')[:3]
        return [{
            'id': f'scd-{p.id}',
            'title': f'SCD: LeetCode - {p.leetcode_username}',
            'status': p.status,
            'date': p.updated_at.isoformat(),
            'pillar': 'scd',
        } for p in profiles]
    
    def get_student_info(self, user):
        """Get student profile information including mentor details"""
        try:
            profile = user.profile
            mentor_name = None
            
            if profile.assigned_mentor:
                # Get mentor's full name or username
                mentor = profile.assigned_mentor
                mentor_name = f"{mentor.first_name} {mentor.last_name}".strip() if mentor.first_name else mentor.username
            
            return {
                'name': f"{user.first_name} {user.last_name}".strip() if user.first_name else user.username,
                'email': user.email,
                'roll_number': user.username,  # Assuming username is roll number
                'phone': getattr(profile, 'phone', None),
                'mentor_name': mentor_name,
            }
        except Exception as e:
            print(f"Error getting student info: {str(e)}")
            return {
                'name': user.username,
                'email': user.email,
                'roll_number': user.username,
                'phone': None,
                'mentor_name': None,
            }
    
    def get_notifications(self, user):
        notifications = []
        
        # CLT notifications
        clt_under_review = CLTSubmission.objects.filter(user=user, status='under_review').count()
        if clt_under_review > 0:
            notifications.append({
                'id': 'notif-clt-review',
                'message': f'{clt_under_review} CLT submission(s) under review',
                'time': 'Recently',
                'read': False,
                'pillar': 'clt',
            })
        
        # SRI notifications (only if models exist)
        if HAS_SRI_MODELS:
            sri_under_review = SocialActivitySubmission.objects.filter(user=user, status='under_review').count()
            if sri_under_review > 0:
                notifications.append({
                    'id': 'notif-sri-review',
                    'message': f'{sri_under_review} SRI activity(ies) under review',
                    'time': 'Recently',
                    'read': False,
                    'pillar': 'sri',
                })
        
        # CFC notifications
        cfc_under_review = (
            HackathonSubmission.objects.filter(user=user, status='under_review').count() +
            InternshipSubmission.objects.filter(user=user, status='under_review').count()
        )
        if cfc_under_review > 0:
            notifications.append({
                'id': 'notif-cfc-review',
                'message': f'{cfc_under_review} CFC submission(s) under review',
                'time': 'Recently',
                'read': False,
                'pillar': 'cfc',
            })
        
        # IIPC notifications
        iipc_under_review = (
            LinkedInPostVerification.objects.filter(user=user, status='pending').count() +
            LinkedInConnectionVerification.objects.filter(user=user, status='pending').count()
        )
        if iipc_under_review > 0:
            notifications.append({
                'id': 'notif-iipc-review',
                'message': f'{iipc_under_review} IIPC verification(s) pending review',
                'time': 'Recently',
                'read': False,
                'pillar': 'iipc',
            })
        
        return notifications[:5]


class NotificationListView(APIView):
    """API endpoint to get user notifications"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get all notifications for the current user"""
        notifications = Notification.objects.filter(recipient=request.user)[:50]
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    
    def delete(self, request):
        """Delete all read notifications"""
        deleted_count = Notification.objects.filter(recipient=request.user, is_read=True).delete()[0]
        return Response({
            'message': f'Deleted {deleted_count} notification(s)',
            'count': deleted_count
        })


class NotificationMarkReadView(APIView):
    """Mark a notification as read"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """Mark a specific notification as read"""
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
            notification.is_read = True
            notification.save()
            return Response({'status': 'marked as read'})
        except Notification.DoesNotExist:
            return Response(
                {'error': 'Notification not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request, pk):
        """Delete a specific notification"""
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
            notification.delete()
            return Response({'status': 'notification deleted'})
        except Notification.DoesNotExist:
            return Response(
                {'error': 'Notification not found'},
                status=status.HTTP_404_NOT_FOUND
            )
