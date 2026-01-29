"""
Mentor-specific views for reviewing student submissions across all pillars
This file consolidates mentor review APIs for: CFC, CLT, SRI, IIPC, SCD
"""

from django.contrib.auth.models import User
from django.db.models import Q, Count, Case, When, Value, IntegerField
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.cfc.models import HackathonSubmission, BMCVideoSubmission, InternshipSubmission, GenAIProjectSubmission
from apps.cfc.serializers import (
    HackathonSubmissionSerializer, 
    BMCVideoSubmissionSerializer,
    InternshipSubmissionSerializer,
    GenAIProjectSubmissionSerializer
)
from apps.clt.models import CLTSubmission
from apps.clt.serializers import CLTSubmissionSerializer
from apps.iipc.models import LinkedInPostVerification
from apps.iipc.serializers import LinkedInPostVerificationSerializer
from apps.scd.models import LeetCodeProfile
from apps.scd.serializers import LeetCodeProfileSerializer
from apps.dashboard.models import Notification, Message, MessageThread
from apps.dashboard.notifications_serializers import (
    NotificationSerializer, MessageSerializer, MessageThreadSerializer, MessageCreateSerializer
)


# Helper function to check if user is a mentor
def is_mentor(user):
    """Check if user has mentor privileges"""
    if user.is_staff or user.is_superuser:
        return True
    if hasattr(user, 'profile'):
        return user.profile.role in ['MENTOR', 'FLOOR_WING', 'ADMIN']
    return False


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mentor_dashboard(request):
    """
    Get mentor dashboard overview with recent submissions and stats
    Shows recent submissions from all assigned students across all pillars
    """
    if not is_mentor(request.user):
        return Response(
            {"error": "You don't have permission to access this resource"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get mentor's assigned students
    assigned_students = request.user.mentored_students.all().values_list('user_id', flat=True)
    
    if not assigned_students:
        return Response({
            'recent_submissions': [],
            'stats': {
                'total_students': 0,
                'pending_reviews': 0,
                'approved_today': 0,
                'total_submissions': 0
            }
        })
    
    # Get recent submissions (last 20) from all pillars
    recent_submissions = []
    
    # Helper to add submission with common format
    def add_submission(sub, pillar_type, model_type, title_getter):
        return {
            'id': f"{pillar_type}_{model_type}_{sub.id}",
            'dbId': sub.id,
            'modelType': model_type,
            'pillar': pillar_type,
            'title': title_getter(sub),
            'student': {
                'id': sub.user.id,
                'name': sub.user.get_full_name() or sub.user.username,
                'email': sub.user.email,
            },
            'status': sub.status,
            'submitted_at': sub.submitted_at or sub.created_at,
            'created_at': sub.created_at,
        }
    
    # Get submissions from each pillar (only assigned students)
    hackathons = HackathonSubmission.objects.filter(user_id__in=assigned_students).select_related('user')
    for sub in hackathons:
        recent_submissions.append(add_submission(sub, 'cfc', 'hackathon', lambda s: s.hackathon_name))
    
    bmc_videos = BMCVideoSubmission.objects.filter(user_id__in=assigned_students).select_related('user')
    for sub in bmc_videos:
        recent_submissions.append(add_submission(sub, 'cfc', 'bmc', lambda s: "BMC Video Submission"))
    
    internships = InternshipSubmission.objects.filter(user_id__in=assigned_students).select_related('user')
    for sub in internships:
        recent_submissions.append(add_submission(sub, 'cfc', 'internship', lambda s: f"Internship at {s.company}"))
    
    genai = GenAIProjectSubmission.objects.filter(user_id__in=assigned_students).select_related('user')
    for sub in genai:
        recent_submissions.append(add_submission(sub, 'cfc', 'genai', lambda s: "GenAI Project"))
    
    clt = CLTSubmission.objects.filter(user_id__in=assigned_students).select_related('user')
    for sub in clt:
        recent_submissions.append(add_submission(sub, 'clt', 'clt', lambda s: s.title))
    
    linkedin = LinkedInPostVerification.objects.filter(user_id__in=assigned_students).select_related('user')
    for sub in linkedin:
        recent_submissions.append(add_submission(sub, 'iipc', 'linkedin', lambda s: "LinkedIn Post"))
    
    # Sort by submission date (most recent first) and limit to 20
    recent_submissions.sort(key=lambda x: x['submitted_at'], reverse=True)
    recent_submissions = recent_submissions[:20]
    
    # Calculate stats
    today = timezone.now().date()
    pending_statuses = ['draft', 'submitted', 'under_review', 'pending']
    
    total_submissions = (
        hackathons.count() + bmc_videos.count() + internships.count() + 
        genai.count() + clt.count() + linkedin.count()
    )
    
    pending_reviews = (
        hackathons.filter(status__in=pending_statuses).count() +
        bmc_videos.filter(status__in=pending_statuses).count() +
        internships.filter(status__in=pending_statuses).count() +
        genai.filter(status__in=pending_statuses).count() +
        clt.filter(status__in=pending_statuses).count() +
        linkedin.filter(status__in=pending_statuses).count()
    )
    
    approved_today = (
        hackathons.filter(status='approved', reviewed_at__date=today).count() +
        bmc_videos.filter(status='approved', reviewed_at__date=today).count() +
        internships.filter(status='approved', reviewed_at__date=today).count() +
        genai.filter(status='approved', reviewed_at__date=today).count() +
        clt.filter(status='approved', reviewed_at__date=today).count() +
        linkedin.filter(status='verified', verified_at__date=today).count()
    )
    
    return Response({
        'recent_submissions': recent_submissions,
        'stats': {
            'total_students': len(assigned_students),
            'pending_reviews': pending_reviews,
            'approved_today': approved_today,
            'total_submissions': total_submissions
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pillar_submissions(request, pillar):
    """
    Get all submissions for a specific pillar for mentor review
    
    Pillars: cfc, clt, iipc, scd, all (sri not implemented yet)
    Query params:
        - status: filter by status (pending, approved, rejected, all)
        - search: search by student name or title
        - year: filter by student year
        - sort: latest or oldest
    """
    # Check if user is mentor
    if not is_mentor(request.user):
        return Response(
            {"error": "You don't have permission to access this resource"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get query parameters
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')
    year_filter = request.GET.get('year', 'all')
    sort_order = request.GET.get('sort', 'latest')
    student_id = request.GET.get('student_id', None)  # NEW: Filter by specific student
    
    submissions = []
    
    # Map status filters
    status_map = {
        'pending': ['draft', 'submitted', 'under_review', 'pending'],
        'approved': ['approved'],
        'rejected': ['rejected'],
        'all': None
    }
    
    status_values = status_map.get(status_filter, None)
    
    print(f"\n=== BACKEND: Fetching submissions for pillar='{pillar}', status='{status_filter}', student_id='{student_id}' ===")
    
    # Get mentor's assigned students
    assigned_students = request.user.mentored_students.all().values_list('user_id', flat=True)
    if not assigned_students:
        print(f"⚠️ Mentor {request.user.username} has no assigned students")
        return Response({'submissions': [], 'total': 0})
    
    # If student_id is provided, only show that student's submissions
    if student_id:
        try:
            student_id = int(student_id)
            if student_id not in assigned_students:
                print(f"⚠️ Student {student_id} is not assigned to mentor {request.user.username}")
                return Response({'submissions': [], 'total': 0})
            assigned_students = [student_id]
            print(f"🎯 Filtering for specific student: {student_id}")
        except (ValueError, TypeError):
            pass
    
    print(f"👥 Showing submissions for {len(assigned_students)} student(s)")
    
    # Helper function to format submission data
    def format_submission(sub, pillar_type, model_type):
        # Get user profile info
        user_profile = {
            'name': sub.user.get_full_name() or sub.user.username,
            'avatar': sub.user.first_name[0].upper() if sub.user.first_name else sub.user.username[0].upper(),
            'email': sub.user.email,
            'username': sub.user.username,
        }
        
        # Map status to frontend format - ensure we're checking the ACTUAL database status
        actual_status = sub.status  # Get the actual status from DB
        if actual_status in ['draft', 'submitted', 'under_review', 'pending']:
            frontend_status = 'pending'
        elif actual_status == 'approved':
            frontend_status = 'approved'
        elif actual_status == 'rejected':
            frontend_status = 'rejected'
        else:
            frontend_status = 'pending'
        
        print(f"   📊 {model_type} #{sub.id}: DB status='{actual_status}' → frontend='{frontend_status}'")
        
        # Get title based on model type
        title = ''
        description = ''
        if model_type == 'hackathon':
            title = sub.hackathon_name
            description = f"{sub.mode.title()} hackathon participation"
        elif model_type == 'bmc':
            title = "Business Model Canvas Video"
            description = sub.description or "BMC video submission"
        elif model_type == 'internship':
            title = f"Internship at {sub.company}"
            description = sub.role
        elif model_type == 'genai':
            title = "GenAI Project"
            description = sub.problem_statement[:100] if len(sub.problem_statement) > 100 else sub.problem_statement
        elif model_type == 'clt':
            title = sub.title
            description = sub.description
        elif model_type == 'linkedin':
            title = "LinkedIn Post Verification"
            description = f"Post from {sub.post_date}"
        elif model_type == 'leetcode':
            title = f"LeetCode Profile - {sub.leetcode_username}"
            description = f"Total solved: {sub.total_solved}"
        
        # Count evidence and get primary evidence URL
        evidence_count = {'images': 0, 'links': 0}
        evidence_url = None
        
        # Determine primary evidence URL based on submission type
        if hasattr(sub, 'certificate_link') and sub.certificate_link:
            evidence_count['links'] += 1
            if not evidence_url:
                evidence_url = sub.certificate_link
        if hasattr(sub, 'drive_link') and sub.drive_link:
            evidence_count['links'] += 1
            if not evidence_url:
                evidence_url = sub.drive_link
        if hasattr(sub, 'github_repo') and sub.github_repo:
            evidence_count['links'] += 1
            if not evidence_url:
                evidence_url = sub.github_repo
        if hasattr(sub, 'video_url') and sub.video_url:
            evidence_count['links'] += 1
            if not evidence_url:
                evidence_url = sub.video_url
        if hasattr(sub, 'post_url') and sub.post_url:
            evidence_count['links'] += 1
            if not evidence_url:
                evidence_url = sub.post_url
        if hasattr(sub, 'screenshot_url') and sub.screenshot_url:
            evidence_count['links'] += 1
            if not evidence_url:
                evidence_url = sub.screenshot_url
        if hasattr(sub, 'profile_url') and sub.profile_url:
            evidence_count['links'] += 1
            if not evidence_url:
                evidence_url = sub.profile_url
        
        return {
            'id': f"{pillar_type}_{model_type}_{sub.id}",  # Unique composite key
            'dbId': sub.id,  # Original DB ID for updates
            'modelType': model_type,  # For backend operations
            'student': user_profile,
            'title': title,
            'description': description,
            'submittedDate': sub.submitted_at.date() if sub.submitted_at else sub.created_at.date(),
            'status': frontend_status,
            'pillar': pillar_type,
            'evidenceLinks': evidence_count,
            'evidence': evidence_url,  # Add the actual evidence URL
            'reviewerComments': getattr(sub, 'reviewer_comments', None) or getattr(sub, 'review_comments', '') or '',
            'reviewedAt': getattr(sub, 'reviewed_at', None),
        }
    
    # Get submissions based on pillar - FIXED: Use if-elif-else for proper isolation
    # FILTER BY ASSIGNED STUDENTS ONLY
    if pillar == 'all':
        # Get ALL submissions from all pillars (only from assigned students)
        cfc_qs = HackathonSubmission.objects.select_related('user').filter(user_id__in=assigned_students)
        bmc_qs = BMCVideoSubmission.objects.select_related('user').filter(user_id__in=assigned_students)
        internship_qs = InternshipSubmission.objects.select_related('user').filter(user_id__in=assigned_students)
        genai_qs = GenAIProjectSubmission.objects.select_related('user').filter(user_id__in=assigned_students)
        
        if status_values:
            cfc_qs = cfc_qs.filter(status__in=status_values)
            bmc_qs = bmc_qs.filter(status__in=status_values)
            internship_qs = internship_qs.filter(status__in=status_values)
            genai_qs = genai_qs.filter(status__in=status_values)
        
        submissions.extend([format_submission(s, 'cfc', 'hackathon') for s in cfc_qs])
        submissions.extend([format_submission(s, 'cfc', 'bmc') for s in bmc_qs])
        submissions.extend([format_submission(s, 'cfc', 'internship') for s in internship_qs])
        submissions.extend([format_submission(s, 'cfc', 'genai') for s in genai_qs])
        
        clt_qs = CLTSubmission.objects.select_related('user').filter(user_id__in=assigned_students)
        if status_values:
            clt_qs = clt_qs.filter(status__in=status_values)
        submissions.extend([format_submission(s, 'clt', 'clt') for s in clt_qs])
        
        iipc_qs = LinkedInPostVerification.objects.select_related('user').filter(user_id__in=assigned_students)
        if status_values:
            iipc_qs = iipc_qs.filter(status__in=status_values)
        submissions.extend([format_submission(s, 'iipc', 'linkedin') for s in iipc_qs])
        
        scd_qs = LeetCodeProfile.objects.select_related('user').filter(user_id__in=assigned_students)
        if status_values:
            scd_qs = scd_qs.filter(status__in=status_values)
        submissions.extend([format_submission(s, 'scd', 'leetcode') for s in scd_qs])
    
    elif pillar == 'cfc':
        # Get ONLY CFC submissions (from assigned students)
        cfc_qs = HackathonSubmission.objects.select_related('user').filter(user_id__in=assigned_students)
        bmc_qs = BMCVideoSubmission.objects.select_related('user').filter(user_id__in=assigned_students)
        internship_qs = InternshipSubmission.objects.select_related('user').filter(user_id__in=assigned_students)
        genai_qs = GenAIProjectSubmission.objects.select_related('user').filter(user_id__in=assigned_students)
        
        if status_values:
            cfc_qs = cfc_qs.filter(status__in=status_values)
            bmc_qs = bmc_qs.filter(status__in=status_values)
            internship_qs = internship_qs.filter(status__in=status_values)
            genai_qs = genai_qs.filter(status__in=status_values)
        
        submissions.extend([format_submission(s, 'cfc', 'hackathon') for s in cfc_qs])
        submissions.extend([format_submission(s, 'cfc', 'bmc') for s in bmc_qs])
        submissions.extend([format_submission(s, 'cfc', 'internship') for s in internship_qs])
        submissions.extend([format_submission(s, 'cfc', 'genai') for s in genai_qs])
    
    elif pillar == 'clt':
        # Get ONLY CLT submissions (from assigned students)
        clt_qs = CLTSubmission.objects.select_related('user').filter(user_id__in=assigned_students)
        if status_values:
            clt_qs = clt_qs.filter(status__in=status_values)
        submissions.extend([format_submission(s, 'clt', 'clt') for s in clt_qs])
    
    elif pillar == 'iipc':
        # Get ONLY IIPC submissions (from assigned students)
        iipc_qs = LinkedInPostVerification.objects.select_related('user').filter(user_id__in=assigned_students)
        if status_values:
            iipc_qs = iipc_qs.filter(status__in=status_values)
        submissions.extend([format_submission(s, 'iipc', 'linkedin') for s in iipc_qs])
    
    elif pillar == 'scd':
        # Get ONLY SCD submissions (from assigned students)
        scd_qs = LeetCodeProfile.objects.select_related('user').filter(user_id__in=assigned_students)
        if status_values:
            scd_qs = scd_qs.filter(status__in=status_values)
        submissions.extend([format_submission(s, 'scd', 'leetcode') for s in scd_qs])
    
    # SRI not implemented yet
    
    # Apply search filter
    if search_query:
        search_lower = search_query.lower()
        submissions = [
            s for s in submissions 
            if search_lower in s['student']['name'].lower() 
            or search_lower in s['title'].lower()
            or search_lower in s['description'].lower()
        ]
    
    # Sort submissions
    if sort_order == 'latest':
        submissions.sort(key=lambda x: x['submittedDate'], reverse=True)
    else:
        submissions.sort(key=lambda x: x['submittedDate'])
    
    # Debug logging
    print(f"\n=== BACKEND: Returning {len(submissions)} submissions for pillar '{pillar}' ===")
    if submissions:
        pillar_counts = {}
        for s in submissions:
            p = s['pillar']
            pillar_counts[p] = pillar_counts.get(p, 0) + 1
        print(f"Pillar breakdown: {pillar_counts}")
    
    return Response({
        'submissions': submissions,
        'total': len(submissions)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pillar_stats(request, pillar):
    """
    Get statistics for a specific pillar
    Returns: total, pending, approved, rejected counts
    """
    if not is_mentor(request.user):
        return Response(
            {"error": "You don't have permission to access this resource"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get mentor's assigned students
    assigned_students = request.user.mentored_students.all().values_list('user_id', flat=True)
    if not assigned_students:
        return Response({'total': 0, 'pending': 0, 'approved': 0, 'rejected': 0})
    
    stats = {'total': 0, 'pending': 0, 'approved': 0, 'rejected': 0}
    
    def count_submissions(queryset):
        return {
            'total': queryset.count(),
            'pending': queryset.filter(status__in=['draft', 'submitted', 'under_review', 'pending']).count(),
            'approved': queryset.filter(status='approved').count(),
            'rejected': queryset.filter(status='rejected').count(),
        }
    
    def add_stats(s1, s2):
        return {k: s1[k] + s2[k] for k in s1}
    
    # Use if-elif-else for proper pillar isolation and filter by assigned students
    if pillar == 'all':
        stats = add_stats(stats, count_submissions(HackathonSubmission.objects.filter(user_id__in=assigned_students)))
        stats = add_stats(stats, count_submissions(BMCVideoSubmission.objects.filter(user_id__in=assigned_students)))
        stats = add_stats(stats, count_submissions(InternshipSubmission.objects.filter(user_id__in=assigned_students)))
        stats = add_stats(stats, count_submissions(GenAIProjectSubmission.objects.filter(user_id__in=assigned_students)))
        stats = add_stats(stats, count_submissions(CLTSubmission.objects.filter(user_id__in=assigned_students)))
        stats = add_stats(stats, count_submissions(LinkedInPostVerification.objects.filter(user_id__in=assigned_students)))
        stats = add_stats(stats, count_submissions(LeetCodeProfile.objects.filter(user_id__in=assigned_students)))
    
    elif pillar == 'cfc':
        stats = add_stats(stats, count_submissions(HackathonSubmission.objects.filter(user_id__in=assigned_students)))
        stats = add_stats(stats, count_submissions(BMCVideoSubmission.objects.filter(user_id__in=assigned_students)))
        stats = add_stats(stats, count_submissions(InternshipSubmission.objects.filter(user_id__in=assigned_students)))
        stats = add_stats(stats, count_submissions(GenAIProjectSubmission.objects.filter(user_id__in=assigned_students)))
    
    elif pillar == 'clt':
        stats = add_stats(stats, count_submissions(CLTSubmission.objects.filter(user_id__in=assigned_students)))
    
    elif pillar == 'iipc':
        stats = add_stats(stats, count_submissions(LinkedInPostVerification.objects.filter(user_id__in=assigned_students)))
    
    elif pillar == 'scd':
        stats = add_stats(stats, count_submissions(LeetCodeProfile.objects.filter(user_id__in=assigned_students)))
    
    # SRI not implemented yet
    
    return Response(stats)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_submission(request):
    """
    Review a submission (approve/reject/resubmit)
    
    Body:
        - pillar: cfc, clt, iipc, scd
        - submission_id: ID of the submission
        - submission_type: hackathon, bmc, internship, genai, clt, linkedin, leetcode
        - action: approve, reject, or resubmit
        - comment: reviewer comment (required for reject/resubmit)
    """
    if not is_mentor(request.user):
        return Response(
            {"error": "You don't have permission to access this resource"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    pillar = request.data.get('pillar')
    submission_id = request.data.get('submission_id')
    submission_type = request.data.get('submission_type')
    action = request.data.get('action')  # 'approve', 'reject', or 'resubmit'
    comment = request.data.get('comment', '')
    
    if not all([pillar, submission_id, submission_type, action]):
        return Response(
            {"error": "Missing required fields"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if action in ['reject', 'resubmit'] and not comment:
        return Response(
            {"error": "Comment is required for rejection or resubmission request"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get the submission model based on type
    model_map = {
        'hackathon': HackathonSubmission,
        'bmc': BMCVideoSubmission,
        'internship': InternshipSubmission,
        'genai': GenAIProjectSubmission,
        'clt': CLTSubmission,
        'linkedin': LinkedInPostVerification,
        'leetcode': LeetCodeProfile,
    }
    
    model_class = model_map.get(submission_type)
    if not model_class:
        return Response(
            {"error": "Invalid submission type"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        submission = model_class.objects.get(id=submission_id)
    except model_class.DoesNotExist:
        return Response(
            {"error": "Submission not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Map action to status
    status_map = {
        'approve': 'approved',
        'reject': 'rejected',
        'resubmit': 'under_review'  # or 'resubmit' if model supports it
    }
    
    # Update submission
    new_status = status_map.get(action, 'under_review')
    print(f"\n🔄 REVIEW: Updating {submission_type} submission #{submission_id}")
    print(f"   Old status: {submission.status}")
    print(f"   New status: {new_status}")
    print(f"   Action: {action}")
    
    submission.status = new_status
    
    # Handle different field names for comments
    if hasattr(submission, 'reviewer_comments'):
        submission.reviewer_comments = comment
    elif hasattr(submission, 'review_comments'):
        submission.review_comments = comment
    
    # Handle different field names for reviewer
    if hasattr(submission, 'reviewed_by'):
        submission.reviewed_by = request.user
    elif hasattr(submission, 'reviewer'):
        submission.reviewer = request.user
    
    if hasattr(submission, 'reviewed_at'):
        submission.reviewed_at = timezone.now()
    
    submission.save()
    
    # Verify the save
    submission.refresh_from_db()
    print(f"   ✅ Status after save: {submission.status}")
    
    # Create notification for student
    notification_type_map = {
        'approve': 'submission_approved',
        'reject': 'submission_rejected',
        'resubmit': 'submission_resubmit'
    }
    
    title_map = {
        'approve': f'✅ Submission Approved - {pillar.upper()}',
        'reject': f'❌ Submission Rejected - {pillar.upper()}',
        'resubmit': f'🔄 Resubmission Requested - {pillar.upper()}'
    }
    
    message_map = {
        'approve': f'Your {submission_type} submission has been approved by your mentor!',
        'reject': f'Your {submission_type} submission needs revision. Please review the feedback.',
        'resubmit': f'Your mentor has requested a resubmission for your {submission_type}.'
    }
    
    notification = Notification.objects.create(
        recipient=submission.user,
        sender=request.user,
        notification_type=notification_type_map.get(action, 'general'),
        priority='high' if action == 'reject' else 'normal',
        title=title_map.get(action, 'Submission Updated'),
        message=f"{message_map.get(action, 'Your submission has been reviewed.')} {comment}",
        related_pillar=pillar,
        related_submission_type=submission_type,
        related_submission_id=submission_id,
        action_url=f"/{pillar}"
    )
    
    return Response({
        'message': f'Submission {action}ed successfully',
        'submission_id': submission_id,
        'status': submission.status,
        'notification_id': notification.id
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_submission_detail(request, pillar, submission_type, submission_id):
    """
    Get detailed information about a specific submission
    """
    if not is_mentor(request.user):
        return Response(
            {"error": "You don't have permission to access this resource"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    model_map = {
        'hackathon': HackathonSubmission,
        'bmc': BMCVideoSubmission,
        'internship': InternshipSubmission,
        'genai': GenAIProjectSubmission,
        'clt': CLTSubmission,
        'linkedin': LinkedInPostVerification,
        'leetcode': LeetCodeProfile,
    }
    
    serializer_map = {
        'hackathon': HackathonSubmissionSerializer,
        'bmc': BMCVideoSubmissionSerializer,
        'internship': InternshipSubmissionSerializer,
        'genai': GenAIProjectSubmissionSerializer,
        'clt': CLTSubmissionSerializer,
        'linkedin': LinkedInPostVerificationSerializer,
        'leetcode': LeetCodeProfileSerializer,
    }
    
    model_class = model_map.get(submission_type)
    serializer_class = serializer_map.get(submission_type)
    
    if not model_class or not serializer_class:
        return Response(
            {"error": "Invalid submission type"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        submission = model_class.objects.select_related('user').get(id=submission_id)
    except model_class.DoesNotExist:
        return Response(
            {"error": "Submission not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = serializer_class(submission)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mentor_students(request):
    """
    Get list of students assigned to the current mentor with their progress stats
    """
    if not is_mentor(request.user):
        return Response(
            {"error": "You don't have permission to access this resource"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get mentor's assigned students
    assigned_students = request.user.mentored_students.all().select_related('user')
    
    students_data = []
    for profile in assigned_students:
        student = profile.user
        
        # Get submission stats for each pillar
        clt_submissions = CLTSubmission.objects.filter(user=student)
        clt_stats = {
            'status': 'completed' if clt_submissions.filter(status='approved').exists() 
                     else 'pending' if clt_submissions.filter(status__in=['draft', 'submitted', 'under_review']).exists()
                     else 'not-started',
            'count': clt_submissions.count(),
            'lastSubmission': clt_submissions.order_by('-created_at').first().created_at if clt_submissions.exists() else None
        }
        
        # CFC stats (all types combined)
        hackathons = HackathonSubmission.objects.filter(user=student)
        bmc_videos = BMCVideoSubmission.objects.filter(user=student)
        internships = InternshipSubmission.objects.filter(user=student)
        genai_projects = GenAIProjectSubmission.objects.filter(user=student)
        
        cfc_total = hackathons.count() + bmc_videos.count() + internships.count() + genai_projects.count()
        cfc_approved = (hackathons.filter(status='approved').count() + 
                       bmc_videos.filter(status='approved').count() +
                       internships.filter(status='approved').count() +
                       genai_projects.filter(status='approved').count())
        cfc_pending = cfc_total - cfc_approved
        
        cfc_stats = {
            'status': 'completed' if cfc_approved > 0 
                     else 'pending' if cfc_pending > 0
                     else 'not-started',
            'count': cfc_total,
            'lastSubmission': max(
                [s.created_at for s in list(hackathons) + list(bmc_videos) + list(internships) + list(genai_projects)],
                default=None
            )
        }
        
        # IIPC stats
        iipc_posts = LinkedInPostVerification.objects.filter(user=student)
        iipc_stats = {
            'status': 'completed' if iipc_posts.filter(status='verified').exists()
                     else 'pending' if iipc_posts.filter(status='pending').exists()
                     else 'not-started',
            'count': iipc_posts.count(),
            'lastSubmission': iipc_posts.order_by('-created_at').first().created_at if iipc_posts.exists() else None
        }
        
        # SCD stats
        try:
            leetcode_profile = LeetCodeProfile.objects.get(user=student)
            scd_stats = {
                'status': 'completed' if leetcode_profile.monthly_problems_count >= 10 else 'pending',
                'count': leetcode_profile.total_solved,
                'lastSubmission': leetcode_profile.last_synced
            }
        except LeetCodeProfile.DoesNotExist:
            scd_stats = {
                'status': 'not-started',
                'count': 0,
                'lastSubmission': None
            }
        
        # SRI stats (placeholder - not implemented yet)
        sri_stats = {
            'status': 'not-started',
            'count': 0,
            'lastSubmission': None
        }
        
        students_data.append({
            'id': student.id,
            'name': student.get_full_name() or student.username,
            'email': student.email,
            'username': student.username,
            'rollNo': f'STU{student.id:03d}',  # Generate roll number from ID
            'submissions': {
                'clt': clt_stats,
                'sri': sri_stats,
                'cfc': cfc_stats,
                'iipc': iipc_stats,
                'scd': scd_stats,
            }
        })
    
    return Response({
        'students': students_data,
        'total': len(students_data)
    })


# ============= NOTIFICATION ENDPOINTS =============

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    """
    Get all notifications for the current user
    Query params:
        - unread_only: true/false (default: false)
        - limit: number of notifications to return
    """
    unread_only = request.GET.get('unread_only', 'false').lower() == 'true'
    limit = int(request.GET.get('limit', 50))
    
    notifications = Notification.objects.filter(recipient=request.user)
    
    if unread_only:
        notifications = notifications.filter(is_read=False)
    
    notifications = notifications[:limit]
    
    serializer = NotificationSerializer(notifications, many=True)
    
    return Response({
        'notifications': serializer.data,
        'unread_count': Notification.objects.filter(recipient=request.user, is_read=False).count(),
        'total': notifications.count()
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.mark_as_read()
        return Response({'message': 'Notification marked as read'})
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_notifications_read(request):
    """Mark all notifications as read for current user"""
    updated = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(
        is_read=True,
        read_at=timezone.now()
    )
    
    return Response({
        'message': f'{updated} notifications marked as read',
        'count': updated
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request, notification_id):
    """Delete a notification"""
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.delete()
        return Response({'message': 'Notification deleted'})
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'},
            status=status.HTTP_404_NOT_FOUND
        )


# ============= MESSAGING ENDPOINTS =============

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_message_threads(request):
    """Get all message threads for the current user"""
    threads = MessageThread.objects.filter(
        Q(participant1=request.user) | Q(participant2=request.user)
    ).select_related('participant1', 'participant2', 'last_message')
    
    serializer = MessageThreadSerializer(threads, many=True, context={'request': request})
    
    return Response({
        'threads': serializer.data,
        'total': threads.count()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_thread_messages(request, user_id):
    """
    Get all messages in a thread with a specific user
    Query params:
        - limit: number of messages to return (default: 50)
        - offset: offset for pagination (default: 0)
    """
    limit = int(request.GET.get('limit', 50))
    offset = int(request.GET.get('offset', 0))
    
    try:
        other_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get or create thread
    thread = MessageThread.objects.filter(
        (Q(participant1=request.user) & Q(participant2=other_user)) |
        (Q(participant1=other_user) & Q(participant2=request.user))
    ).first()
    
    if not thread:
        # Create new thread
        thread = MessageThread.objects.create(
            participant1=request.user,
            participant2=other_user
        )
    
    # Get messages
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user)) |
        (Q(sender=other_user) & Q(recipient=request.user))
    ).order_by('-created_at')[offset:offset+limit]
    
    # Mark messages as read
    Message.objects.filter(
        sender=other_user,
        recipient=request.user,
        is_read=False
    ).update(is_read=True, read_at=timezone.now(), status='read')
    
    # Reset unread count for current user
    thread.reset_unread(request.user)
    
    serializer = MessageSerializer(messages, many=True)
    
    return Response({
        'messages': serializer.data,
        'thread_id': thread.id,
        'total': messages.count()
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    """
    Send a message to another user
    Body:
        - recipient_id: ID of the recipient
        - subject: optional subject
        - message: message text
        - related_pillar: optional
        - related_submission_type: optional
        - related_submission_id: optional
        - parent_message_id: optional (for replies)
    """
    serializer = MessageCreateSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    data = serializer.validated_data
    recipient = User.objects.get(id=data['recipient_id'])
    
    # Create message
    message = Message.objects.create(
        sender=request.user,
        recipient=recipient,
        subject=data.get('subject', ''),
        message=data['message'],
        related_pillar=data.get('related_pillar'),
        related_submission_type=data.get('related_submission_type'),
        related_submission_id=data.get('related_submission_id'),
        parent_message=Message.objects.get(id=data['parent_message_id']) if data.get('parent_message_id') else None
    )
    
    # Get or create thread
    thread = MessageThread.objects.filter(
        (Q(participant1=request.user) & Q(participant2=recipient)) |
        (Q(participant1=recipient) & Q(participant2=request.user))
    ).first()
    
    if not thread:
        thread = MessageThread.objects.create(
            participant1=request.user,
            participant2=recipient
        )
    
    # Update thread
    thread.last_message = message
    thread.last_message_at = timezone.now()
    thread.increment_unread(recipient)  # Increment unread for recipient
    thread.save()
    
    # Create notification for recipient
    Notification.objects.create(
        recipient=recipient,
        sender=request.user,
        notification_type='message',
        title=f'💬 New Message from {request.user.get_full_name() or request.user.username}',
        message=data['message'][:100] + ('...' if len(data['message']) > 100 else ''),
        action_url='/messages'
    )
    
    return Response({
        'message': 'Message sent successfully',
        'message_id': message.id,
        'thread_id': thread.id
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unread_counts(request):
    """Get unread counts for notifications and messages"""
    notifications_count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    
    messages_count = Message.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    
    return Response({
        'notifications': notifications_count,
        'messages': messages_count,
        'total': notifications_count + messages_count
    })


# ============= ANNOUNCEMENT ENDPOINTS =============

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def announcements(request):
    """
    GET: List all announcements created by the current mentor
    POST: Create a new announcement
    """
    from apps.dashboard.models import Announcement
    from apps.dashboard.notifications_serializers import AnnouncementSerializer, AnnouncementCreateSerializer
    
    if not is_mentor(request.user):
        return Response(
            {"error": "You don't have permission to access this resource"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'GET':
        # Get all announcements by this mentor
        announcements_list = Announcement.objects.filter(mentor=request.user)
        serializer = AnnouncementSerializer(announcements_list, many=True)
        return Response({
            'announcements': serializer.data,
            'total': len(serializer.data)
        })
    
    elif request.method == 'POST':
        # Create new announcement
        print("\n=== ANNOUNCEMENT CREATE DEBUG ===")
        print(f"Request data: {request.data}")
        print(f"Content type: {request.content_type}")
        
        serializer = AnnouncementCreateSerializer(data=request.data)
        if serializer.is_valid():
            announcement = serializer.save(mentor=request.user)
            return Response(
                AnnouncementSerializer(announcement).data,
                status=status.HTTP_201_CREATED
            )
        
        print(f"Validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def announcement_detail(request, announcement_id):
    """
    GET: Get announcement details
    PUT: Update announcement
    DELETE: Delete announcement
    """
    from apps.dashboard.models import Announcement
    from apps.dashboard.notifications_serializers import AnnouncementSerializer, AnnouncementCreateSerializer
    
    if not is_mentor(request.user):
        return Response(
            {"error": "You don't have permission to access this resource"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        announcement = Announcement.objects.get(id=announcement_id, mentor=request.user)
    except Announcement.DoesNotExist:
        return Response(
            {"error": "Announcement not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = AnnouncementSerializer(announcement)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = AnnouncementCreateSerializer(announcement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(AnnouncementSerializer(announcement).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        announcement.delete()
        return Response(
            {"message": "Announcement deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_announcements(request):
    """Get all announcements for the current student from their mentor"""
    from apps.dashboard.models import Announcement
    from apps.profiles.models import UserProfile
    from apps.dashboard.notifications_serializers import AnnouncementSerializer
    
    try:
        student_profile = UserProfile.objects.get(user=request.user)
        if not student_profile.assigned_mentor:
            return Response({
                'announcements': [],
                'total': 0,
                'unread_count': 0
            })
        
        announcements_list = Announcement.objects.filter(mentor=student_profile.assigned_mentor).order_by('-created_at')
        serializer = AnnouncementSerializer(announcements_list, many=True, context={'request': request})
        
        # Count unread announcements
        unread_count = sum(1 for ann in serializer.data if not ann['is_read'])
        
        return Response({
            'announcements': serializer.data,
            'total': len(serializer.data),
            'unread_count': unread_count
        })
    except UserProfile.DoesNotExist:
        return Response({
            'announcements': [],
            'total': 0,
            'unread_count': 0
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_announcement_read(request, announcement_id):
    """Mark an announcement as read for the current student"""
    from apps.dashboard.models import Announcement, AnnouncementRead
    
    try:
        announcement = Announcement.objects.get(id=announcement_id)
        
        # Create or get the read record
        read_record, created = AnnouncementRead.objects.get_or_create(
            announcement=announcement,
            user=request.user
        )
        
        return Response({
            'success': True,
            'message': 'Announcement marked as read',
            'already_read': not created
        })
    except Announcement.DoesNotExist:
        return Response(
            {'error': 'Announcement not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except StudentProfile.DoesNotExist:
        return Response(
            {'error': 'Student profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_monthly_report(request, student_id):
    """Get monthly report for a specific student (Mentor view)"""
    from datetime import datetime
    from apps.clt.models import CLTSubmission
    from apps.cfc.models import HackathonSubmission, BMCVideoSubmission, InternshipSubmission, GenAIProjectSubmission
    from apps.iipc.models import LinkedInPostVerification, LinkedInConnectionVerification
    from apps.scd.models import LeetCodeProfile
    
    # Check if user is mentor
    if not is_mentor(request.user):
        return Response(
            {"error": "You don't have permission to access this resource"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    if not month or not year:
        return Response(
            {'error': 'Month and year are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        month = int(month)
        year = int(year)
        student = User.objects.get(id=student_id)
        
        # Create date range
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        # Monthly task requirements
        MONTHLY_REQUIREMENTS = {
            'clt': 1,
            'sri': 0,
            'cfc': 3,
            'iipc': 2,
            'scd': 1,
        }
        
        # Calculate CLT stats
        clt_submissions = CLTSubmission.objects.filter(
            user=student,
            created_at__gte=start_date,
            created_at__lt=end_date
        )
        clt_completed = clt_submissions.filter(status='approved').count()
        
        # Calculate CFC stats
        cfc_hackathons = HackathonSubmission.objects.filter(
            user=student, created_at__gte=start_date, created_at__lt=end_date, status='approved'
        ).count()
        cfc_bmc = BMCVideoSubmission.objects.filter(
            user=student, created_at__gte=start_date, created_at__lt=end_date, status='approved'
        ).count()
        cfc_genai = GenAIProjectSubmission.objects.filter(
            user=student, created_at__gte=start_date, created_at__lt=end_date, status='approved'
        ).count()
        cfc_completed = cfc_hackathons + cfc_bmc + cfc_genai
        
        # Calculate IIPC stats
        iipc_posts = LinkedInPostVerification.objects.filter(
            user=student, created_at__gte=start_date, created_at__lt=end_date, status='approved'
        ).count()
        iipc_connections = LinkedInConnectionVerification.objects.filter(
            user=student, created_at__gte=start_date, created_at__lt=end_date, status='approved'
        ).count()
        iipc_completed = iipc_posts + iipc_connections
        
        # Calculate SCD stats
        scd_profile = LeetCodeProfile.objects.filter(user=student).first()
        scd_completed = 1 if (scd_profile and scd_profile.problems_solved >= 10) else 0
        
        report_data = {
            'month': month,
            'year': year,
            'student': {
                'id': student.id,
                'name': f"{student.first_name} {student.last_name}",
                'email': student.email,
            },
            'overall_progress': round((clt_completed + cfc_completed + iipc_completed + scd_completed) / 7 * 100),
            'pillars': {
                'clt': {
                    'completed': clt_completed,
                    'target': MONTHLY_REQUIREMENTS['clt'],
                    'percentage': min(100, round((clt_completed / MONTHLY_REQUIREMENTS['clt']) * 100)) if MONTHLY_REQUIREMENTS['clt'] > 0 else 0,
                },
                'cfc': {
                    'completed': cfc_completed,
                    'target': MONTHLY_REQUIREMENTS['cfc'],
                    'percentage': min(100, round((cfc_completed / MONTHLY_REQUIREMENTS['cfc']) * 100)) if MONTHLY_REQUIREMENTS['cfc'] > 0 else 0,
                },
                'iipc': {
                    'completed': iipc_completed,
                    'target': MONTHLY_REQUIREMENTS['iipc'],
                    'percentage': min(100, round((iipc_completed / MONTHLY_REQUIREMENTS['iipc']) * 100)) if MONTHLY_REQUIREMENTS['iipc'] > 0 else 0,
                },
                'scd': {
                    'completed': scd_completed,
                    'target': MONTHLY_REQUIREMENTS['scd'],
                    'percentage': min(100, round((scd_completed / MONTHLY_REQUIREMENTS['scd']) * 100)) if MONTHLY_REQUIREMENTS['scd'] > 0 else 0,
                },
            }
        }
        
        return Response(report_data)
        
    except User.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_available_months(request, student_id):
    """Get available months for a student's monthly reports (Mentor view)"""
    from datetime import datetime
    from apps.clt.models import CLTSubmission
    
    # Check if user is mentor
    if not is_mentor(request.user):
        return Response(
            {"error": "You don't have permission to access this resource"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        student = User.objects.get(id=student_id)
        
        # Get all months where student has any submissions
        submissions = CLTSubmission.objects.filter(user=student).order_by('created_at')
        
        if not submissions.exists():
            # Default to current month if no submissions
            now = datetime.now()
            return Response({
                'months': [{
                    'month': now.month,
                    'year': now.year,
                    'label': now.strftime('%B %Y')
                }]
            })
        
        # Get unique year-month combinations
        months_set = set()
        for sub in submissions:
            months_set.add((sub.created_at.year, sub.created_at.month))
        
        # Sort and format
        months_sorted = sorted(months_set, reverse=True)
        available_months = [
            {
                'month': month,
                'year': year,
                'label': datetime(year, month, 1).strftime('%B %Y')
            }
            for year, month in months_sorted
        ]
        
        return Response({'months': available_months})
        
    except User.DoesNotExist:
        return Response(
            {'error': 'Student not found'},
            status=status.HTTP_404_NOT_FOUND
        )
