"""
Mentor-only views for gamification control
Mentors approve tasks, control episode progression, finalize seasons
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Season, Episode, EpisodeProgress
from .services import EpisodeService, SeasonScoringService
from .serializers import EpisodeProgressSerializer, SeasonScoreSerializer

User = get_user_model()


def is_mentor(user):
    """Check if user is a mentor"""
    try:
        return user.profile.role == 'MENTOR'
    except:
        return False


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_task(request):
    """
    Mentor approves a task submission
    This marks the task as complete in the gamification system
    
    Expected payload:
    {
        "student_id": 123,
        "episode_id": 1,
        "task_type": "clt" | "cfc_task1" | "cfc_task2" | "cfc_task3" | 
                     "iipc_task1" | "iipc_task2" | "sri" | "scd_streak"
    }
    """
    if not is_mentor(request.user):
        return Response(
            {'error': 'Only mentors can approve tasks'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    student_id = request.data.get('student_id')
    episode_id = request.data.get('episode_id')
    task_type = request.data.get('task_type')
    
    if not all([student_id, episode_id, task_type]):
        return Response(
            {'error': 'student_id, episode_id, and task_type are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    student = get_object_or_404(User, id=student_id)
    episode = get_object_or_404(Episode, id=episode_id)
    
    # Mark task completed
    episode_completed, message = EpisodeService.mark_task_completed(
        student, episode, task_type
    )
    
    # Get updated progress
    progress = EpisodeProgress.objects.get(student=student, episode=episode)
    serializer = EpisodeProgressSerializer(progress)
    
    return Response({
        'message': message,
        'episode_completed': episode_completed,
        'progress': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_progress_detail(request, student_id):
    """
    Get detailed gamification progress for a student
    Mentor can view assigned student's complete progress
    """
    if not is_mentor(request.user):
        return Response(
            {'error': 'Only mentors can view student progress'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    student = get_object_or_404(User, id=student_id)
    current_season = Season.objects.filter(is_active=True).first()
    
    if not current_season:
        return Response({'error': 'No active season'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get all episode progress for current season
    episode_progress = EpisodeProgress.objects.filter(
        student=student,
        episode__season=current_season
    ).order_by('episode__episode_number')
    
    progress_serializer = EpisodeProgressSerializer(episode_progress, many=True)
    
    # Get season score
    season_score = SeasonScore.objects.filter(
        student=student,
        season=current_season
    ).first()
    
    score_serializer = SeasonScoreSerializer(season_score) if season_score else None
    
    return Response({
        'student': {
            'id': student.id,
            'username': student.username,
            'email': student.email
        },
        'season': {
            'id': current_season.id,
            'name': current_season.name
        },
        'episode_progress': progress_serializer.data,
        'season_score': score_serializer.data if score_serializer else None
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finalize_student_season(request, student_id):
    """
    Mentor can trigger season finalization for a student
    (Normally auto-triggered when Episode 4 completes)
    
    This calculates Season Score, updates Legacy Score, allocates Vault Credits
    """
    if not is_mentor(request.user):
        return Response(
            {'error': 'Only mentors can finalize seasons'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    student = get_object_or_404(User, id=student_id)
    current_season = Season.objects.filter(is_active=True).first()
    
    if not current_season:
        return Response({'error': 'No active season'}, status=status.HTTP_404_NOT_FOUND)
    
    # Finalize season
    season_score, message = SeasonScoringService.finalize_season(student, current_season)
    
    if season_score:
        serializer = SeasonScoreSerializer(season_score)
        return Response({
            'message': message,
            'season_score': serializer.data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': message
        }, status=status.HTTP_400_BAD_REQUEST)
