from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime
import traceback

from apps.clt.models import CLTSubmission
try:
    from apps.sri.models import SocialActivitySubmission
    HAS_SRI_MODELS = True
except ImportError:
    HAS_SRI_MODELS = False
from apps.cfc.models import HackathonSubmission, BMCVideoSubmission, InternshipSubmission, GenAIProjectSubmission
from apps.iipc.models import LinkedInPostVerification, LinkedInConnectionVerification
from apps.scd.models import LeetCodeProfile


# Monthly task requirements
MONTHLY_REQUIREMENTS = {
    'clt': 1,      # 1 certificate upload per month
    'sri': 0,      # Not specified
    'cfc': 3,      # 3 tasks: hackathon, BMC, GenAI project (internship is optional)
    'iipc': 2,     # 2 tasks: LinkedIn post and connection
    'scd': 1,      # 1 profile with minimum 10 problems
}


class MonthlyReportView(APIView):
    """
    Get monthly report for a specific month and year
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            
            # Get month and year from query params, default to current month
            month = request.query_params.get('month')
            year = request.query_params.get('year')
            
            if month and year:
                try:
                    month = int(month)
                    year = int(year)
                    if not (1 <= month <= 12):
                        return Response(
                            {'error': 'Month must be between 1 and 12'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except ValueError:
                    return Response(
                        {'error': 'Invalid month or year format'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                # Default to current month
                now = datetime.now()
                month = now.month
                year = now.year
            
            # Create start and end dates for the month
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
            
            # CLT Stats for the month
            clt_submissions = CLTSubmission.objects.filter(
                user=user,
                created_at__gte=start_date,
                created_at__lt=end_date
            )
            clt_completed = clt_submissions.filter(status='approved').count()
            clt_stats = {
                'total': clt_submissions.count(),
                'completed': clt_completed,
                'pending': clt_submissions.filter(status__in=['draft', 'submitted', 'under_review']).count(),
                'monthly_target': MONTHLY_REQUIREMENTS['clt'],
                'percentage': min(100, round((clt_completed / MONTHLY_REQUIREMENTS['clt']) * 100)) if MONTHLY_REQUIREMENTS['clt'] > 0 else 0,
                'status': 'completed' if clt_completed >= MONTHLY_REQUIREMENTS['clt'] else 'in-progress' if clt_completed > 0 else 'not-started',
            }
            
            # SRI Stats for the month
            if HAS_SRI_MODELS:
                sri_submissions = SocialActivitySubmission.objects.filter(
                    user=user,
                    created_at__gte=start_date,
                    created_at__lt=end_date
                )
                sri_completed = sri_submissions.filter(status='approved').count()
                sri_stats = {
                    'total': sri_submissions.count(),
                    'completed': sri_completed,
                    'pending': sri_submissions.filter(status__in=['draft', 'submitted', 'under_review']).count(),
                    'monthly_target': MONTHLY_REQUIREMENTS['sri'],
                    'percentage': 0,
                    'status': 'not-applicable',
                }
            else:
                sri_stats = {
                    'total': 0,
                    'completed': 0,
                    'pending': 0,
                    'monthly_target': MONTHLY_REQUIREMENTS['sri'],
                    'percentage': 0,
                    'status': 'not-applicable',
                }
            
            # CFC Stats for the month
            hackathons = HackathonSubmission.objects.filter(
                user=user,
                created_at__gte=start_date,
                created_at__lt=end_date
            )
            bmc_videos = BMCVideoSubmission.objects.filter(
                user=user,
                created_at__gte=start_date,
                created_at__lt=end_date
            )
            internships = InternshipSubmission.objects.filter(
                user=user,
                created_at__gte=start_date,
                created_at__lt=end_date
            )
            genai_projects = GenAIProjectSubmission.objects.filter(
                user=user,
                created_at__gte=start_date,
                created_at__lt=end_date
            )
            
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
                'status': 'completed' if cfc_completed >= MONTHLY_REQUIREMENTS['cfc'] else 'in-progress' if cfc_completed > 0 else 'not-started',
                'breakdown': {
                    'hackathons': {
                        'total': hackathons.count(),
                        'completed': hackathons.filter(status='approved').count(),
                    },
                    'bmc_videos': {
                        'total': bmc_videos.count(),
                        'completed': bmc_videos.filter(status='approved').count(),
                    },
                    'internships': {
                        'total': internships.count(),
                        'completed': internships.filter(status='approved').count(),
                    },
                    'genai_projects': {
                        'total': genai_projects.count(),
                        'completed': genai_projects.filter(status='approved').count(),
                    },
                }
            }
            
            # IIPC Stats for the month
            linkedin_posts = LinkedInPostVerification.objects.filter(
                user=user,
                created_at__gte=start_date,
                created_at__lt=end_date
            )
            linkedin_connections = LinkedInConnectionVerification.objects.filter(
                user=user,
                created_at__gte=start_date,
                created_at__lt=end_date
            )
            
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
                'status': 'completed' if iipc_completed >= MONTHLY_REQUIREMENTS['iipc'] else 'in-progress' if iipc_completed > 0 else 'not-started',
                'breakdown': {
                    'posts': {
                        'total': linkedin_posts.count(),
                        'completed': linkedin_posts.filter(status='approved').count(),
                    },
                    'connections': {
                        'total': linkedin_connections.count(),
                        'completed': linkedin_connections.filter(status='approved').count(),
                    },
                }
            }
            
            # SCD Stats for the month
            leetcode_profiles = LeetCodeProfile.objects.filter(
                user=user,
                created_at__gte=start_date,
                created_at__lt=end_date
            )
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
                'status': 'completed' if scd_completed >= MONTHLY_REQUIREMENTS['scd'] else 'in-progress' if scd_completed > 0 else 'not-started',
                'total_problems_solved': sum(p.total_solved or 0 for p in leetcode_profiles),
            }
            
            # Calculate overall progress
            total_monthly_target = sum(MONTHLY_REQUIREMENTS.values())
            total_completed_towards_target = sum([
                min(clt_stats['completed'], MONTHLY_REQUIREMENTS['clt']),
                min(sri_stats['completed'], MONTHLY_REQUIREMENTS['sri']),
                min(cfc_stats['completed'], MONTHLY_REQUIREMENTS['cfc']),
                min(iipc_stats['completed'], MONTHLY_REQUIREMENTS['iipc']),
                min(scd_stats['completed'], MONTHLY_REQUIREMENTS['scd'])
            ])
            overall_percentage = round((total_completed_towards_target / total_monthly_target * 100)) if total_monthly_target > 0 else 0
            
            data = {
                'month': month,
                'year': year,
                'month_name': datetime(year, month, 1).strftime('%B'),
                'overall': {
                    'completed': total_completed_towards_target,
                    'monthly_target': total_monthly_target,
                    'percentage': overall_percentage,
                    'status': 'completed' if total_completed_towards_target >= total_monthly_target else 'in-progress' if total_completed_towards_target > 0 else 'not-started',
                },
                'pillars': {
                    'clt': clt_stats,
                    'sri': sri_stats,
                    'cfc': cfc_stats,
                    'iipc': iipc_stats,
                    'scd': scd_stats,
                }
            }
            
            return Response(data)
            
        except Exception as e:
            print(f"Monthly Report API Error: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return Response(
                {'error': 'Failed to generate monthly report', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AvailableMonthsView(APIView):
    """
    Get list of months where user has activity
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            
            # Get all months where user has any activity
            months_set = set()
            
            # Check CLT submissions
            clt_dates = CLTSubmission.objects.filter(user=user).values_list('created_at', flat=True)
            for date in clt_dates:
                months_set.add((date.year, date.month))
            
            # Check CFC submissions
            for model in [HackathonSubmission, BMCVideoSubmission, InternshipSubmission, GenAIProjectSubmission]:
                dates = model.objects.filter(user=user).values_list('created_at', flat=True)
                for date in dates:
                    months_set.add((date.year, date.month))
            
            # Check IIPC submissions
            for model in [LinkedInPostVerification, LinkedInConnectionVerification]:
                dates = model.objects.filter(user=user).values_list('created_at', flat=True)
                for date in dates:
                    months_set.add((date.year, date.month))
            
            # Check SCD submissions
            scd_dates = LeetCodeProfile.objects.filter(user=user).values_list('created_at', flat=True)
            for date in scd_dates:
                months_set.add((date.year, date.month))
            
            # Always include current month
            now = datetime.now()
            months_set.add((now.year, now.month))
            
            # Convert to list of dicts and sort by date (most recent first)
            months_list = []
            for year, month in months_set:
                months_list.append({
                    'year': year,
                    'month': month,
                    'month_name': datetime(year, month, 1).strftime('%B'),
                    'display': datetime(year, month, 1).strftime('%B %Y'),
                })
            
            months_list.sort(key=lambda x: (x['year'], x['month']), reverse=True)
            
            return Response({'months': months_list})
            
        except Exception as e:
            print(f"Available Months API Error: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return Response(
                {'error': 'Failed to fetch available months', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
