"""
Admin API views for user and mentor-student assignment management
"""
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.profiles.models import UserProfile


def is_admin(user):
    """Check if user has admin privileges (superuser only)"""
    return user.is_superuser


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    """Get all users with their profile information"""
    if not is_admin(request.user):
        return Response(
            {"error": "You don't have permission to access this resource"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    users = User.objects.all().select_related('profile').order_by('username')
    
    users_data = []
    for user in users:
        profile = getattr(user, 'profile', None)
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'assigned_mentor': {
                'id': profile.assigned_mentor.id,
                'username': profile.assigned_mentor.username,
                'email': profile.assigned_mentor.email
            } if profile and profile.assigned_mentor else None
        })
    
    return Response(users_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_mentor_to_student(request):
    """Assign a mentor to a student"""
    if not is_admin(request.user):
        return Response(
            {"error": "You don't have permission to access this resource"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    student_id = request.data.get('student_id')
    mentor_id = request.data.get('mentor_id')
    
    if not student_id or not mentor_id:
        return Response(
            {"error": "student_id and mentor_id are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        student = User.objects.get(id=student_id)
        mentor = User.objects.get(id=mentor_id)
        
        if not mentor.is_staff:
            return Response(
                {"error": "Selected user is not a mentor"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profile, created = UserProfile.objects.get_or_create(user=student)
        profile.assigned_mentor = mentor
        profile.save()
        
        return Response({
            'message': f'Successfully assigned {mentor.username} to {student.username}',
            'student': student.username,
            'mentor': mentor.username
        })
    
    except User.DoesNotExist:
        return Response(
            {"error": "Student or mentor not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_assign_mentor(request):
    """Assign a mentor to multiple students at once"""
    if not is_admin(request.user):
        return Response(
            {"error": "You don't have permission to access this resource"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    student_ids = request.data.get('student_ids', [])
    mentor_id = request.data.get('mentor_id')
    
    if not student_ids or not mentor_id:
        return Response(
            {"error": "student_ids and mentor_id are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        mentor = User.objects.get(id=mentor_id)
        
        if not mentor.is_staff:
            return Response(
                {"error": "Selected user is not a mentor"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        students = User.objects.filter(id__in=student_ids)
        count = 0
        
        for student in students:
            profile, created = UserProfile.objects.get_or_create(user=student)
            profile.assigned_mentor = mentor
            profile.save()
            count += 1
        
        return Response({
            'message': f'Successfully assigned {count} students to {mentor.username}',
            'count': count,
            'mentor': mentor.username
        })
    
    except User.DoesNotExist:
        return Response(
            {"error": "Mentor not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def auto_assign_mentors(request):
    """Automatically assign all students to mentors in round-robin fashion"""
    if not is_admin(request.user):
        return Response(
            {"error": "You don't have permission to access this resource"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get all mentors and students
    mentors = list(User.objects.filter(is_staff=True, is_superuser=False).order_by('id'))
    students = User.objects.filter(is_staff=False, is_superuser=False).order_by('id')
    
    if not mentors:
        return Response(
            {"error": "No mentors available for assignment"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not students.exists():
        return Response(
            {"error": "No students found to assign"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Round-robin assignment
    count = 0
    for idx, student in enumerate(students):
        mentor = mentors[idx % len(mentors)]
        profile, created = UserProfile.objects.get_or_create(user=student)
        profile.assigned_mentor = mentor
        profile.save()
        count += 1
    
    return Response({
        'message': f'Successfully assigned {count} students to {len(mentors)} mentors',
        'students_assigned': count,
        'mentors_count': len(mentors),
        'students_per_mentor': count // len(mentors)
    })
