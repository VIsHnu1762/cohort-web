from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q, Count
import re
import requests
from datetime import date

from .models import (
    HackathonRegistration,
    HackathonSubmission,
    BMCVideoSubmission,
    InternshipSubmission,
    GenAIProjectSubmission
)
from .serializers import (
    HackathonRegistrationSerializer,
    HackathonRegistrationCreateSerializer,
    HackathonSubmissionSerializer,
    HackathonSubmissionCreateSerializer,
    BMCVideoSubmissionSerializer,
    BMCVideoSubmissionCreateSerializer,
    InternshipSubmissionSerializer,
    InternshipSubmissionCreateSerializer,
    GenAIProjectSubmissionSerializer,
    GenAIProjectSubmissionCreateSerializer,
    CFCStatsSerializer
)


class HackathonRegistrationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Hackathon registrations (before participation)
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return HackathonRegistration.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return HackathonRegistrationCreateSerializer
        return HackathonRegistrationSerializer
    
    def perform_create(self, serializer):
        """Save the registration and notify mentor"""
        registration = serializer.save(user=self.request.user)
        
        # Notify mentor about the hackathon registration
        if hasattr(self.request.user, 'profile') and self.request.user.profile.assigned_mentor:
            from apps.dashboard.models import Notification
            
            mentor = self.request.user.profile.assigned_mentor
            student_name = self.request.user.get_full_name() or self.request.user.username
            
            Notification.objects.create(
                user=mentor,
                message=f"{student_name} has registered for {registration.hackathon_name} hackathon ({registration.get_mode_display()}) scheduled on {registration.participation_date.strftime('%B %d, %Y')}",
                notification_type='info'
            )
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming registered hackathons"""
        upcoming = self.get_queryset().filter(
            is_completed=False,
            participation_date__gte=date.today()
        ).order_by('participation_date')
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark a registration as completed"""
        registration = self.get_object()
        registration.is_completed = True
        registration.save()
        return Response({'status': 'marked as completed'})
    
    @action(detail=True, methods=['post'])
    def create_submission(self, request, pk=None):
        """Create a hackathon submission from a registration"""
        registration = self.get_object()
        
        # Check if submission already exists
        if registration.submission:
            return Response(
                {'error': 'Submission already exists for this registration'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create submission with registration data
        submission = HackathonSubmission.objects.create(
            user=request.user,
            hackathon_name=registration.hackathon_name,
            mode=registration.mode,
            registration_date=registration.registration_date,
            participation_date=registration.participation_date,
            status='draft',
            current_step=1
        )
        
        # Link submission to registration
        registration.submission = submission
        registration.is_completed = True
        registration.save()
        
        serializer = HackathonSubmissionSerializer(submission)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HackathonSubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Hackathon submissions
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return HackathonSubmission.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return HackathonSubmissionCreateSerializer
        return HackathonSubmissionSerializer
    
    def extract_github_repo_info(self, github_url):
        """Extract owner and repo name from GitHub URL"""
        github_regex = r'(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/\.]+)'
        match = re.search(github_regex, github_url)
        if match:
            return match.group(1), match.group(2)
        return None, None
    
    def validate_github_repo(self, github_url):
        """Validate and fetch GitHub repository information"""
        owner, repo = self.extract_github_repo_info(github_url)
        
        if not owner or not repo:
            return {
                'valid': False,
                'error': 'Invalid GitHub URL format. Use: https://github.com/owner/repo'
            }
        
        try:
            # Fetch repository info from GitHub API
            api_url = f'https://api.github.com/repos/{owner}/{repo}'
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 404:
                return {
                    'valid': False,
                    'error': 'Repository not found. Make sure the repository is public.'
                }
            elif response.status_code == 403:
                return {
                    'valid': False,
                    'error': 'GitHub API rate limit exceeded. Please try again later.'
                }
            elif response.status_code != 200:
                return {
                    'valid': False,
                    'error': f'Unable to access repository. Status: {response.status_code}'
                }
            
            repo_data = response.json()
            
            # Check if repository has README
            readme_url = f'https://api.github.com/repos/{owner}/{repo}/readme'
            readme_response = requests.get(readme_url, timeout=10)
            has_readme = readme_response.status_code == 200
            
            # Get commit count
            commits_url = f'https://api.github.com/repos/{owner}/{repo}/commits'
            commits_response = requests.get(commits_url, params={'per_page': 1}, timeout=10)
            commit_count = 0
            if commits_response.status_code == 200:
                # Get commit count from Link header if available
                link_header = commits_response.headers.get('Link', '')
                if 'last' in link_header:
                    last_page_match = re.search(r'page=(\d+)>; rel="last"', link_header)
                    if last_page_match:
                        commit_count = int(last_page_match.group(1))
                else:
                    commit_count = len(commits_response.json()) if commits_response.json() else 0
            
            return {
                'valid': True,
                'owner': owner,
                'repo': repo,
                'full_name': repo_data.get('full_name'),
                'description': repo_data.get('description', ''),
                'stars': repo_data.get('stargazers_count', 0),
                'forks': repo_data.get('forks_count', 0),
                'language': repo_data.get('language', 'Unknown'),
                'is_private': repo_data.get('private', False),
                'has_readme': has_readme,
                'commit_count': commit_count,
                'created_at': repo_data.get('created_at'),
                'updated_at': repo_data.get('updated_at'),
                'html_url': repo_data.get('html_url'),
                'warnings': []
            }
            
        except requests.exceptions.Timeout:
            return {
                'valid': False,
                'error': 'Request timeout. Please try again.'
            }
        except Exception as e:
            return {
                'valid': False,
                'error': f'Error validating repository: {str(e)}'
            }
    
    @action(detail=False, methods=['post'])
    def validate_repo(self, request):
        """Validate GitHub repository URL"""
        github_url = request.data.get('github_url', '')
        
        if not github_url:
            return Response(
                {'error': 'GitHub URL is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validation_result = self.validate_github_repo(github_url)
        
        if not validation_result['valid']:
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(validation_result)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit a hackathon submission for review"""
        submission = self.get_object()
        
        # Validate required fields
        if not submission.certificate_link:
            return Response(
                {'error': 'Please provide a certificate link before submitting.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        submission.status = 'submitted'
        submission.submitted_at = timezone.now()
        submission.save()
        
        serializer = self.get_serializer(submission)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get hackathon submission statistics for the current user"""
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'draft': queryset.filter(status='draft').count(),
            'submitted': queryset.filter(status='submitted').count(),
            'approved': queryset.filter(status='approved').count(),
            'rejected': queryset.filter(status='rejected').count(),
        }
        return Response(stats)


class BMCVideoSubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing BMC Video submissions
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BMCVideoSubmission.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BMCVideoSubmissionCreateSerializer
        return BMCVideoSubmissionSerializer
    
    def extract_youtube_video_id(self, url):
        """Extract YouTube video ID from URL"""
        youtube_regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
        match = re.search(youtube_regex, url)
        return match.group(1) if match else None
    
    def get_youtube_video_duration(self, video_id):
        """Get YouTube video duration using oEmbed API and page scraping"""
        try:
            # Try to get duration from YouTube page
            response = requests.get(f'https://www.youtube.com/watch?v={video_id}', timeout=10)
            if response.status_code == 200:
                # Extract lengthSeconds from YouTube page
                duration_match = re.search(r'"lengthSeconds":"(\d+)"', response.text)
                if duration_match:
                    duration_seconds = int(duration_match.group(1))
                    duration_minutes = duration_seconds / 60
                    return duration_minutes
        except Exception as e:
            print(f"Error fetching YouTube video duration: {str(e)}")
        return None
    
    def create(self, request, *args, **kwargs):
        """Override create to validate video duration"""
        video_url = request.data.get('video_url', '')
        
        if video_url:
            video_id = self.extract_youtube_video_id(video_url)
            
            if video_id:
                duration_minutes = self.get_youtube_video_duration(video_id)
                
                if duration_minutes is not None:
                    if duration_minutes < 5:
                        return Response(
                            {
                                'error': f'Video must be at least 5 minutes long. Current video is {duration_minutes:.1f} minutes.',
                                'duration': duration_minutes
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
        
        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'])
    def check_duration(self, request):
        """Check YouTube video duration"""
        video_url = request.data.get('video_url', '')
        
        if not video_url:
            return Response(
                {'error': 'Video URL is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        video_id = self.extract_youtube_video_id(video_url)
        
        if not video_id:
            return Response(
                {'error': 'Invalid YouTube URL'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        duration_minutes = self.get_youtube_video_duration(video_id)
        
        if duration_minutes is None:
            return Response(
                {'error': 'Unable to determine video duration'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'duration_minutes': round(duration_minutes, 1),
            'duration_seconds': int(duration_minutes * 60),
            'is_valid': duration_minutes >= 5,
            'video_id': video_id
        })
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit a BMC video for review"""
        submission = self.get_object()
        
        # Validate required fields
        if not submission.video_url:
            return Response(
                {'error': 'Please provide a video URL before submitting.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        submission.status = 'submitted'
        submission.submitted_at = timezone.now()
        submission.save()
        
        serializer = self.get_serializer(submission)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get BMC video submission statistics for the current user"""
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'draft': queryset.filter(status='draft').count(),
            'submitted': queryset.filter(status='submitted').count(),
            'approved': queryset.filter(status='approved').count(),
            'rejected': queryset.filter(status='rejected').count(),
        }
        return Response(stats)


class InternshipSubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Internship submissions
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return InternshipSubmission.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return InternshipSubmissionCreateSerializer
        return InternshipSubmissionSerializer
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit an internship for review"""
        submission = self.get_object()
        
        # Validate that internship is completed (status 4)
        if submission.internship_status != 4:
            return Response(
                {'error': 'Internship must be completed before submitting for review.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate required documents for completed internships
        if not submission.completion_certificate_link:
            return Response(
                {'error': 'Please provide a completion certificate link before submitting.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        submission.status = 'submitted'
        submission.submitted_at = timezone.now()
        submission.save()
        
        serializer = self.get_serializer(submission)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update internship progress status"""
        submission = self.get_object()
        new_status = request.data.get('internship_status')
        
        if new_status is None:
            return Response(
                {'error': 'internship_status is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            new_status = int(new_status)
            if new_status not in [1, 2, 3, 4]:
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                {'error': 'internship_status must be 1, 2, 3, or 4'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        submission.internship_status = new_status
        submission.save()
        
        serializer = self.get_serializer(submission)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get internship submission statistics for the current user"""
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'application': queryset.filter(internship_status=1).count(),
            'interview': queryset.filter(internship_status=2).count(),
            'offer': queryset.filter(internship_status=3).count(),
            'completed': queryset.filter(internship_status=4).count(),
            'approved': queryset.filter(status='approved').count(),
        }
        return Response(stats)


class GenAIProjectSubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing GenAI Project submissions
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return GenAIProjectSubmission.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return GenAIProjectSubmissionCreateSerializer
        return GenAIProjectSubmissionSerializer
    
    def extract_github_repo_info(self, github_url):
        """Extract owner and repo name from GitHub URL"""
        # Match patterns like:
        # https://github.com/owner/repo
        # https://github.com/owner/repo.git
        # github.com/owner/repo
        github_regex = r'(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/\.]+)'
        match = re.search(github_regex, github_url)
        if match:
            return match.group(1), match.group(2)
        return None, None
    
    def validate_github_repo(self, github_url):
        """Validate and fetch GitHub repository information"""
        owner, repo = self.extract_github_repo_info(github_url)
        
        if not owner or not repo:
            return {
                'valid': False,
                'error': 'Invalid GitHub URL format. Use: https://github.com/owner/repo'
            }
        
        try:
            # Fetch repository info from GitHub API
            api_url = f'https://api.github.com/repos/{owner}/{repo}'
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 404:
                return {
                    'valid': False,
                    'error': 'Repository not found. Make sure the repository is public.'
                }
            elif response.status_code == 403:
                return {
                    'valid': False,
                    'error': 'GitHub API rate limit exceeded. Please try again later.'
                }
            elif response.status_code != 200:
                return {
                    'valid': False,
                    'error': f'Unable to access repository. Status: {response.status_code}'
                }
            
            repo_data = response.json()
            
            # Check if repository has README
            readme_url = f'https://api.github.com/repos/{owner}/{repo}/readme'
            readme_response = requests.get(readme_url, timeout=10)
            has_readme = readme_response.status_code == 200
            
            # Get commit count
            commits_url = f'https://api.github.com/repos/{owner}/{repo}/commits'
            commits_response = requests.get(commits_url, params={'per_page': 1}, timeout=10)
            commit_count = 0
            if commits_response.status_code == 200:
                # Get commit count from Link header if available
                link_header = commits_response.headers.get('Link', '')
                if 'last' in link_header:
                    last_page_match = re.search(r'page=(\d+)>; rel="last"', link_header)
                    if last_page_match:
                        commit_count = int(last_page_match.group(1))
                else:
                    commit_count = len(commits_response.json()) if commits_response.json() else 0
            
            return {
                'valid': True,
                'owner': owner,
                'repo': repo,
                'full_name': repo_data.get('full_name'),
                'description': repo_data.get('description', ''),
                'stars': repo_data.get('stargazers_count', 0),
                'forks': repo_data.get('forks_count', 0),
                'language': repo_data.get('language', 'Unknown'),
                'is_private': repo_data.get('private', False),
                'has_readme': has_readme,
                'commit_count': commit_count,
                'created_at': repo_data.get('created_at'),
                'updated_at': repo_data.get('updated_at'),
                'html_url': repo_data.get('html_url'),
                'warnings': []
            }
            
        except requests.exceptions.Timeout:
            return {
                'valid': False,
                'error': 'Request timeout. Please try again.'
            }
        except Exception as e:
            return {
                'valid': False,
                'error': f'Error validating repository: {str(e)}'
            }
    
    @action(detail=False, methods=['post'])
    def validate_repo(self, request):
        """Validate GitHub repository URL"""
        github_url = request.data.get('github_url', '')
        
        if not github_url:
            return Response(
                {'error': 'GitHub URL is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validation_result = self.validate_github_repo(github_url)
        
        if not validation_result['valid']:
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(validation_result)
    
    def create(self, request, *args, **kwargs):
        """Override create to add detailed error logging"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
            print(f"Request data: {request.data}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit a GenAI project for review"""
        submission = self.get_object()
        
        # Validate required fields
        if not submission.github_repo:
            return Response(
                {'error': 'Please provide a GitHub repository link before submitting.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not submission.problem_statement or not submission.innovation_technology:
            return Response(
                {'error': 'Please complete all required fields before submitting.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        submission.status = 'submitted'
        submission.submitted_at = timezone.now()
        submission.save()
        
        serializer = self.get_serializer(submission)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get GenAI project submission statistics for the current user"""
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'draft': queryset.filter(status='draft').count(),
            'submitted': queryset.filter(status='submitted').count(),
            'approved': queryset.filter(status='approved').count(),
            'rejected': queryset.filter(status='rejected').count(),
        }
        return Response(stats)
