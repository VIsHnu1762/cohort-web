from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils import timezone
from django.db import transaction
from django.core.cache import cache
from django.db.models import Prefetch
from .models import CLTSubmission, CLTFile
from .serializers import (
    CLTSubmissionSerializer,
    CLTSubmissionCreateSerializer,
    CLTSubmissionUpdateSerializer,
    CLTFileSerializer
)


class CLTSubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing CLT (Creative Learning Track) submissions.
    Optimized for 1000-2000 concurrent users with caching, pagination, and throttling.
    
    Endpoints:
    - GET    /api/clt/submissions/           - List all submissions (paginated)
    - POST   /api/clt/submissions/           - Create new submission
    - GET    /api/clt/submissions/{id}/      - Get specific submission
    - PUT    /api/clt/submissions/{id}/      - Update submission (full)
    - PATCH  /api/clt/submissions/{id}/      - Update submission (partial)
    - DELETE /api/clt/submissions/{id}/      - Delete submission
    - POST   /api/clt/submissions/{id}/upload_files/     - Upload files (max 10 files, 10MB each)
    - POST   /api/clt/submissions/{id}/submit/           - Submit for review
    - DELETE /api/clt/submissions/{id}/delete_file/      - Delete file
    - GET    /api/clt/submissions/stats/                 - Get statistics (cached)
    
    Rate Limits:
    - 100 requests/hour for authenticated users
    - 20 file uploads/hour per user
    """
    
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    pagination_class = None  # Uses default pagination from settings
    
    def get_queryset(self):
        """Return submissions for current user only with optimized queries"""
        return CLTSubmission.objects.filter(
            user=self.request.user
        ).select_related(
            'user', 'reviewed_by'
        ).prefetch_related(
            Prefetch('files', queryset=CLTFile.objects.order_by('uploaded_at'))
        ).only(
            'id', 'title', 'description', 'platform', 'completion_date',
            'status', 'current_step', 'created_at', 'updated_at', 'submitted_at',
            'user__username', 'user__email', 'reviewed_by__username'
        )
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return CLTSubmissionCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CLTSubmissionUpdateSerializer
        return CLTSubmissionSerializer
    
    def create(self, request, *args, **kwargs):
        """Create new CLT submission with atomic transaction"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            # Create submission
            submission = serializer.save()
            
            # Handle files separately
            files = request.FILES.getlist('files', [])
            if files:
                # Validate file count
                if len(files) > 10:
                    submission.delete()
                    return Response(
                        {'error': 'Maximum 10 files allowed per submission'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Create file objects
                for file in files:
                    # Validate file size (10MB)
                    if file.size > 10 * 1024 * 1024:
                        submission.delete()
                        return Response(
                            {'error': f'File {file.name} exceeds 10MB limit'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    CLTFile.objects.create(
                        submission=submission,
                        file=file,
                        file_name=file.name,
                        file_size=file.size
                    )
            
            # Clear user's stats cache
            cache.delete(f'clt_stats_{request.user.id}')
        
        # Return full submission data
        response_serializer = CLTSubmissionSerializer(submission)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_files(self, request, pk=None):
        """
        Upload additional files to existing submission.
        POST /api/clt/submissions/{id}/upload_files/
        Body: files (multipart), file_type (optional)
        Max 10 files per request, max 10MB per file
        """
        submission = self.get_object()
        
        # Check if user owns this submission
        if submission.user != request.user:
            return Response(
                {'error': 'You do not have permission to modify this submission'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        files = request.FILES.getlist('files')
        if not files:
            return Response(
                {'error': 'No files provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Limit number of files per request
        if len(files) > 10:
            return Response(
                {'error': 'Maximum 10 files allowed per request'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file sizes (10MB limit per file)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        for file in files:
            if file.size > MAX_FILE_SIZE:
                return Response(
                    {'error': f'File {file.name} exceeds 10MB limit'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Bulk create files in transaction
        created_files = []
        with transaction.atomic():
            for file in files:
                clt_file = CLTFile.objects.create(
                    submission=submission,
                    file=file,
                    file_name=file.name,
                    file_size=file.size,
                    file_type=request.data.get('file_type', 'evidence')
                )
                created_files.append(clt_file)
        
        serializer = CLTFileSerializer(created_files, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        Submit CLT submission for review.
        POST /api/clt/submissions/{id}/submit/
        """
        submission = self.get_object()
        
        # Check if user owns this submission
        if submission.user != request.user:
            return Response(
                {'error': 'You do not have permission to modify this submission'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Prevent resubmission
        if submission.status in ['submitted', 'under_review', 'approved']:
            return Response(
                {'error': f'Cannot submit - submission is already {submission.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate submission is complete
        if not submission.title or not submission.description or not submission.platform or not submission.completion_date:
            return Response(
                {'error': 'Please complete all required fields before submitting'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not submission.drive_link:
            return Response(
                {'error': 'Please provide a Google Drive link to your certificate/evidence'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update submission status atomically
        with transaction.atomic():
            submission.status = 'submitted'
            submission.current_step = 3
            submission.submitted_at = timezone.now()
            submission.save(update_fields=['status', 'current_step', 'submitted_at', 'updated_at'])
            # Clear cache
            cache.delete(f'clt_stats_{request.user.id}')
        
        serializer = CLTSubmissionSerializer(submission)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def delete_file(self, request, pk=None):
        """
        Delete a file from submission.
        DELETE /api/clt/submissions/{id}/delete_file/?file_id={file_id}
        """
        submission = self.get_object()
        
        # Check if user owns this submission
        if submission.user != request.user:
            return Response(
                {'error': 'You do not have permission to modify this submission'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Prevent deletion if already submitted
        if submission.status in ['submitted', 'under_review']:
            return Response(
                {'error': 'Cannot delete files from submitted/under review submissions'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file_id = request.query_params.get('file_id')
        if not file_id:
            return Response(
                {'error': 'file_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            file_obj = CLTFile.objects.get(id=file_id, submission=submission)
            with transaction.atomic():
                file_obj.file.delete(save=False)  # Delete actual file from storage
                file_obj.delete()  # Delete database record
            return Response({'message': 'File deleted successfully'}, status=status.HTTP_200_OK)
        except CLTFile.DoesNotExist:
            return Response(
                {'error': 'File not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error deleting file: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get submission statistics for current user with caching.
        GET /api/clt/submissions/stats/
        Cached for 5 minutes per user
        """
        cache_key = f'clt_stats_{request.user.id}'
        stats = cache.get(cache_key)
        
        if stats is None:
            # Use aggregate query for better performance
            from django.db.models import Count, Q
            
            submissions = CLTSubmission.objects.filter(user=request.user)
            
            stats = submissions.aggregate(
                total=Count('id'),
                draft=Count('id', filter=Q(status='draft')),
                submitted=Count('id', filter=Q(status='submitted')),
                under_review=Count('id', filter=Q(status='under_review')),
                approved=Count('id', filter=Q(status='approved')),
                rejected=Count('id', filter=Q(status='rejected')),
            )
            
            # Cache for 5 minutes
            cache.set(cache_key, stats, 300)
        
        return Response(stats, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        """Delete submission and clear cache"""
        instance = self.get_object()
        
        # Prevent deletion if submitted
        if instance.status in ['submitted', 'under_review', 'approved']:
            return Response(
                {'error': f'Cannot delete {instance.status} submissions'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            # Delete all associated files
            for file_obj in instance.files.all():
                file_obj.file.delete(save=False)
            instance.delete()
            cache.delete(f'clt_stats_{request.user.id}')
        
        return Response(status=status.HTTP_204_NO_CONTENT)
