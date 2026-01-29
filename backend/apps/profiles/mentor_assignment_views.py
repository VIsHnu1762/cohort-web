"""
API views for mentor assignment management

Features:
1. Mentors can reassign students to themselves (from their floor)
2. Admins can view and modify all assignments
3. Admins can reassign any student to any mentor
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from .models import UserProfile


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mentor_students(request):
    """
    Get all students assigned to the logged-in mentor
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        
        if profile.role != 'MENTOR':
            return Response(
                {'error': 'Only mentors can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get all students assigned to this mentor
        students = UserProfile.objects.filter(
            role='STUDENT',
            assigned_mentor=request.user
        ).select_related('user').values(
            'user__id',
            'user__email',
            'user__first_name',
            'user__last_name',
            'user__username',
            'campus',
            'floor',
            'wing'
        )
        
        return Response({
            'mentor': {
                'email': request.user.email,
                'name': request.user.get_full_name(),
                'campus': profile.campus,
                'floor': profile.floor
            },
            'students': list(students),
            'total_count': students.count()
        })
    
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'User profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_students(request):
    """
    Get unassigned students on the mentor's floor that can be assigned
    Mentors can only see students from their own floor
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        
        if profile.role != 'MENTOR':
            return Response(
                {'error': 'Only mentors can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get unassigned students on the same floor
        available_students = UserProfile.objects.filter(
            role='STUDENT',
            campus=profile.campus,
            floor=profile.floor,
            assigned_mentor__isnull=True
        ).select_related('user').values(
            'user__id',
            'user__email',
            'user__first_name',
            'user__last_name',
            'user__username',
            'campus',
            'floor',
            'wing'
        )
        
        return Response({
            'available_students': list(available_students),
            'count': available_students.count(),
            'filter': {
                'campus': profile.campus,
                'floor': profile.floor
            }
        })
    
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'User profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_student_to_self(request):
    """
    Allow mentor to assign an unassigned student to themselves
    Mentor can only assign students from their own floor
    
    Request body:
    {
        "student_id": 123
    }
    """
    try:
        mentor_profile = UserProfile.objects.get(user=request.user)
        
        if mentor_profile.role != 'MENTOR':
            return Response(
                {'error': 'Only mentors can assign students'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        student_id = request.data.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the student
        try:
            student_user = User.objects.get(id=student_id)
            student_profile = UserProfile.objects.get(user=student_user)
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            return Response(
                {'error': 'Student not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verify student is on the same floor
        if (student_profile.role != 'STUDENT' or 
            student_profile.campus != mentor_profile.campus or 
            student_profile.floor != mentor_profile.floor):
            return Response(
                {'error': 'Can only assign students from your own floor'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verify student is unassigned
        if student_profile.assigned_mentor is not None:
            return Response(
                {'error': f'Student is already assigned to {student_profile.assigned_mentor.email}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Assign student to mentor
        student_profile.assigned_mentor = request.user
        student_profile.save()
        
        return Response({
            'success': True,
            'message': f'Successfully assigned {student_user.email} to you',
            'student': {
                'id': student_user.id,
                'email': student_user.email,
                'name': student_user.get_full_name()
            }
        })
    
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'User profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reassign_student_to_mentor(request):
    """
    Allow mentor to reassign any student on their floor to another mentor on the same floor
    This enables mentors to transfer students between themselves
    
    Request body:
    {
        "student_id": 123,
        "new_mentor_id": 456  // Must be a mentor on the same floor
    }
    """
    try:
        current_mentor_profile = UserProfile.objects.get(user=request.user)
        
        if current_mentor_profile.role != 'MENTOR':
            return Response(
                {'error': 'Only mentors can reassign students'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        student_id = request.data.get('student_id')
        new_mentor_id = request.data.get('new_mentor_id')
        
        if not student_id or not new_mentor_id:
            return Response(
                {'error': 'student_id and new_mentor_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the student
        try:
            student_user = User.objects.get(id=student_id)
            student_profile = UserProfile.objects.get(user=student_user)
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            return Response(
                {'error': 'Student not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verify student is on the same floor as current mentor
        if (student_profile.role != 'STUDENT' or 
            student_profile.campus != current_mentor_profile.campus or 
            student_profile.floor != current_mentor_profile.floor):
            return Response(
                {'error': 'Can only reassign students from your own floor'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get the new mentor
        try:
            new_mentor_user = User.objects.get(id=new_mentor_id)
            new_mentor_profile = UserProfile.objects.get(user=new_mentor_user)
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            return Response(
                {'error': 'New mentor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verify new mentor is a mentor on the same floor
        if (new_mentor_profile.role != 'MENTOR' or
            new_mentor_profile.campus != current_mentor_profile.campus or
            new_mentor_profile.floor != current_mentor_profile.floor):
            return Response(
                {'error': 'Can only reassign to mentors on your own floor'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Store old mentor for response
        old_mentor = student_profile.assigned_mentor
        
        # Reassign student to new mentor
        student_profile.assigned_mentor = new_mentor_user
        student_profile.save()
        
        return Response({
            'success': True,
            'message': f'Successfully reassigned {student_user.email} to {new_mentor_user.email}',
            'student': {
                'id': student_user.id,
                'email': student_user.email,
                'name': student_user.get_full_name()
            },
            'old_mentor': {
                'id': old_mentor.id if old_mentor else None,
                'email': old_mentor.email if old_mentor else None,
                'name': old_mentor.get_full_name() if old_mentor else None
            },
            'new_mentor': {
                'id': new_mentor_user.id,
                'email': new_mentor_user.email,
                'name': new_mentor_user.get_full_name()
            }
        })
    
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'User profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_get_all_assignments(request):
    """
    Admin endpoint to view all mentor-student assignments
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        
        # Check if user is admin or superuser
        if profile.role != 'ADMIN' and not request.user.is_superuser:
            return Response(
                {'error': 'Only admins can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get all mentors with their student count
        mentors = UserProfile.objects.filter(role='MENTOR').select_related('user')
        
        assignments = []
        for mentor_profile in mentors:
            students = UserProfile.objects.filter(
                role='STUDENT',
                assigned_mentor=mentor_profile.user
            ).select_related('user')
            
            assignments.append({
                'mentor': {
                    'id': mentor_profile.user.id,
                    'email': mentor_profile.user.email,
                    'name': mentor_profile.user.get_full_name(),
                    'campus': mentor_profile.campus,
                    'floor': mentor_profile.floor
                },
                'students': [
                    {
                        'id': s.user.id,
                        'email': s.user.email,
                        'name': s.user.get_full_name(),
                        'username': s.user.username,
                        'campus': s.campus,
                        'floor': s.floor,
                        'wing': s.wing
                    }
                    for s in students
                ],
                'student_count': students.count()
            })
        
        # Get unassigned students
        unassigned_students = UserProfile.objects.filter(
            role='STUDENT',
            assigned_mentor__isnull=True
        ).select_related('user')
        
        return Response({
            'assignments': assignments,
            'unassigned_students': [
                {
                    'id': s.user.id,
                    'email': s.user.email,
                    'name': s.user.get_full_name(),
                    'username': s.user.username,
                    'campus': s.campus,
                    'floor': s.floor,
                    'wing': s.wing
                }
                for s in unassigned_students
            ],
            'total_mentors': mentors.count(),
            'total_unassigned': unassigned_students.count()
        })
    
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'User profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_reassign_student(request):
    """
    Admin endpoint to reassign any student to any mentor
    
    Request body:
    {
        "student_id": 123,
        "mentor_id": 456  // or null to unassign
    }
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        
        # Check if user is admin or superuser
        if profile.role != 'ADMIN' and not request.user.is_superuser:
            return Response(
                {'error': 'Only admins can reassign students'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        student_id = request.data.get('student_id')
        mentor_id = request.data.get('mentor_id')
        
        if not student_id:
            return Response(
                {'error': 'student_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the student
        try:
            student_user = User.objects.get(id=student_id)
            student_profile = UserProfile.objects.get(user=student_user)
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            return Response(
                {'error': 'Student not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if student_profile.role != 'STUDENT':
            return Response(
                {'error': 'User is not a student'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Handle unassignment
        if mentor_id is None:
            old_mentor = student_profile.assigned_mentor
            student_profile.assigned_mentor = None
            student_profile.save()
            
            return Response({
                'success': True,
                'message': f'Unassigned {student_user.email}',
                'old_mentor': old_mentor.email if old_mentor else None
            })
        
        # Get the mentor
        try:
            mentor_user = User.objects.get(id=mentor_id)
            mentor_profile = UserProfile.objects.get(user=mentor_user)
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            return Response(
                {'error': 'Mentor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if mentor_profile.role != 'MENTOR':
            return Response(
                {'error': 'User is not a mentor'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Assign student to mentor
        old_mentor = student_profile.assigned_mentor
        student_profile.assigned_mentor = mentor_user
        student_profile.save()
        
        return Response({
            'success': True,
            'message': f'Reassigned {student_user.email} to {mentor_user.email}',
            'student': {
                'id': student_user.id,
                'email': student_user.email,
                'name': student_user.get_full_name()
            },
            'mentor': {
                'id': mentor_user.id,
                'email': mentor_user.email,
                'name': mentor_user.get_full_name()
            },
            'old_mentor': old_mentor.email if old_mentor else None
        })
    
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'User profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_floor_mentors(request):
    """
    Get all mentors on a specific floor
    Query params: ?campus=TECH&floor=2
    """
    campus = request.query_params.get('campus')
    floor = request.query_params.get('floor')
    
    if not campus or not floor:
        return Response(
            {'error': 'campus and floor query parameters are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        floor = int(floor)
    except ValueError:
        return Response(
            {'error': 'floor must be a number'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    mentors = UserProfile.objects.filter(
        role='MENTOR',
        campus=campus,
        floor=floor
    ).select_related('user')
    
    mentor_list = []
    for mentor_profile in mentors:
        student_count = UserProfile.objects.filter(
            role='STUDENT',
            assigned_mentor=mentor_profile.user
        ).count()
        
        mentor_list.append({
            'id': mentor_profile.user.id,
            'email': mentor_profile.user.email,
            'name': mentor_profile.user.get_full_name(),
            'campus': mentor_profile.campus,
            'floor': mentor_profile.floor,
            'student_count': student_count
        })
    
    return Response({
        'mentors': mentor_list,
        'count': len(mentor_list),
        'max_mentors_per_floor': 3
    })
