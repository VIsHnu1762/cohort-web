"""
Admin-only view to import dummy users
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from apps.profiles.models import UserProfile
import csv
import os

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_dummy_users(request):
    """
    Import dummy users from CSV file. Admin only.
    """
    # Check if user is admin
    if not request.user.is_staff and not request.user.is_superuser:
        return Response(
            {'error': 'Only administrators can import users'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    campus = 'TECH'  # SNS College of Technology
    floor = 2  # 2nd Year / Floor 2
    
    # Find CSV file
    csv_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'dummy users - Sheet1.csv')
    
    if not os.path.exists(csv_path):
        return Response(
            {'error': f'CSV file not found at: {csv_path}'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    created_count = 0
    updated_count = 0
    users_data = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                email = row['email'].strip()
                username = row['username'].strip()
                password = 'pass123#'
                
                # Create or update user
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'username': username,
                        'first_name': username.split()[0] if username else '',
                        'last_name': ' '.join(username.split()[1:]) if len(username.split()) > 1 else ''
                    }
                )
                
                user.set_password(password)
                user.save()
                
                if created:
                    created_count += 1
                else:
                    updated_count += 1
                
                # Create or update profile
                profile, profile_created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'role': 'STUDENT',
                        'campus': campus,
                        'floor': floor,
                    }
                )
                
                if not profile_created:
                    profile.role = 'STUDENT'
                    profile.campus = campus
                    profile.floor = floor
                    profile.save()
                
                users_data.append({
                    'username': username,
                    'email': email,
                    'status': 'created' if created else 'updated'
                })
        
        return Response({
            'success': True,
            'message': 'Users imported successfully',
            'created': created_count,
            'updated': updated_count,
            'total': created_count + updated_count,
            'campus': 'SNS College of Technology',
            'floor': 2,
            'users': users_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
