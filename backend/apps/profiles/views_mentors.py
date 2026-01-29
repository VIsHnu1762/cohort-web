"""
Admin-only view to setup mentors and assign students
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setup_mentors(request):
    """
    Setup mentors and assign students. Admin only.
    Creates 2 mentors and assigns 5 students to each.
    """
    # Check if user is admin
    if not request.user.is_staff and not request.user.is_superuser:
        return Response(
            {'error': 'Only administrators can setup mentors'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    result = {
        'mentors_created': [],
        'students_assigned': []
    }
    
    try:
        # Create Mentor 1
        mentor1_email = 'mentor1@sns.edu'
        mentor1, created1 = User.objects.get_or_create(
            email=mentor1_email,
            defaults={
                'username': 'mentor1_tech',
                'first_name': 'Rajesh',
                'last_name': 'Kumar'
            }
        )
        mentor1.set_password('mentor123')
        mentor1.save()
        
        # Set Mentor 1 profile
        profile1, _ = UserProfile.objects.get_or_create(user=mentor1)
        profile1.role = 'MENTOR'
        profile1.campus = 'TECH'
        profile1.floor = 2  # Changed to Floor 2 where students are
        profile1.save()
        
        result['mentors_created'].append({
            'id': mentor1.id,
            'email': mentor1_email,
            'name': f'{mentor1.first_name} {mentor1.last_name}',
            'status': 'created' if created1 else 'updated',
            'campus': 'TECH',
            'floor': 1
        })
        
        # Create Mentor 2
        mentor2_email = 'mentor2@sns.edu'
        mentor2, created2 = User.objects.get_or_create(
            email=mentor2_email,
            defaults={
                'username': 'mentor2_tech',
                'first_name': 'Priya',
                'last_name': 'Sharma'
            }
        )
        mentor2.set_password('mentor123')
        mentor2.save()
        
        # Set Mentor 2 profile
        profile2, _ = UserProfile.objects.get_or_create(user=mentor2)
        profile2.role = 'MENTOR'
        profile2.campus = 'TECH'
        profile2.floor = 2
        profile2.save()
        
        result['mentors_created'].append({
            'id': mentor2.id,
            'email': mentor2_email,
            'name': f'{mentor2.first_name} {mentor2.last_name}',
            'status': 'created' if created2 else 'updated',
            'campus': 'TECH',
            'floor': 2
        })
        
        # Get students without mentors (first 10)
        students = UserProfile.objects.filter(
            role='STUDENT'
        ).select_related('user')[:10]
        
        if students.count() < 10:
            return Response({
                'warning': f'Only {students.count()} students found. Need at least 10 students.',
                'mentors_created': result['mentors_created'],
                'message': 'Mentors created but not enough students to assign'
            }, status=status.HTTP_200_OK)
        
        # Assign first 5 students to Mentor 1
        for i, student_profile in enumerate(list(students)[:5]):
            student_profile.assigned_mentor = mentor1
            student_profile.save()
            result['students_assigned'].append({
                'student_id': student_profile.user.id,
                'student_email': student_profile.user.email,
                'student_name': f'{student_profile.user.first_name} {student_profile.user.last_name}',
                'mentor_id': mentor1.id,
                'mentor_email': mentor1_email,
                'mentor_name': f'{mentor1.first_name} {mentor1.last_name}'
            })
        
        # Assign next 5 students to Mentor 2
        for i, student_profile in enumerate(list(students)[5:10]):
            student_profile.assigned_mentor = mentor2
            student_profile.save()
            result['students_assigned'].append({
                'student_id': student_profile.user.id,
                'student_email': student_profile.user.email,
                'student_name': f'{student_profile.user.first_name} {student_profile.user.last_name}',
                'mentor_id': mentor2.id,
                'mentor_email': mentor2_email,
                'mentor_name': f'{mentor2.first_name} {mentor2.last_name}'
            })
        
        return Response({
            'success': True,
            'message': 'Mentors setup completed successfully',
            'mentors_created': result['mentors_created'],
            'students_assigned': result['students_assigned'],
            'summary': {
                'total_mentors': 2,
                'total_students_assigned': len(result['students_assigned']),
                'mentor1_students': 5,
                'mentor2_students': 5
            },
            'credentials': {
                'mentor1': f'{mentor1_email} / mentor123',
                'mentor2': f'{mentor2_email} / mentor123'
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
