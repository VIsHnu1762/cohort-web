"""
Admin-only view to setup floor wing users
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setup_floorwings(request):
    """
    Setup floor wing users. Admin only.
    Creates floor wing users for TECH (4 floors) and ARTS (3 floors) campuses.
    """
    # Check if user is admin
    if not request.user.is_staff and not request.user.is_superuser:
        return Response(
            {'error': 'Only administrators can setup floor wings'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Floor Wing configuration
    FLOORWINGS = [
        # TECH campus - 4 floors
        {"username": "floorwing_tech_1", "email": "fw_tech_1@sns.edu", "campus": "TECH", "floor": 1, "name": "Floor Wing TECH Floor 1"},
        {"username": "floorwing_tech_2", "email": "fw_tech_2@sns.edu", "campus": "TECH", "floor": 2, "name": "Floor Wing TECH Floor 2"},
        {"username": "floorwing_tech_3", "email": "fw_tech_3@sns.edu", "campus": "TECH", "floor": 3, "name": "Floor Wing TECH Floor 3"},
        {"username": "floorwing_tech_4", "email": "fw_tech_4@sns.edu", "campus": "TECH", "floor": 4, "name": "Floor Wing TECH Floor 4"},
        
        # ARTS campus - 3 floors
        {"username": "floorwing_arts_1", "email": "fw_arts_1@sns.edu", "campus": "ARTS", "floor": 1, "name": "Floor Wing ARTS Floor 1"},
        {"username": "floorwing_arts_2", "email": "fw_arts_2@sns.edu", "campus": "ARTS", "floor": 2, "name": "Floor Wing ARTS Floor 2"},
        {"username": "floorwing_arts_3", "email": "fw_arts_3@sns.edu", "campus": "ARTS", "floor": 3, "name": "Floor Wing ARTS Floor 3"},
    ]
    
    # Default password for all floor wings
    DEFAULT_PASSWORD = 'floorwing123'
    
    result = {
        'floorwings_created': [],
        'floorwings_updated': [],
        'errors': []
    }
    
    for fw_data in FLOORWINGS:
        try:
            # Get or create user
            user, user_created = User.objects.get_or_create(
                username=fw_data['username'],
                defaults={
                    'email': fw_data['email'],
                    'first_name': fw_data['name'],
                    'last_name': '',
                }
            )
            
            # Set password
            user.set_password(DEFAULT_PASSWORD)
            
            # Update email if needed
            if user.email != fw_data['email']:
                user.email = fw_data['email']
            
            user.save()
            
            # Get or create profile
            profile, profile_created = UserProfile.objects.get_or_create(user=user)
            
            # Set floor wing details
            profile.role = 'FLOOR_WING'
            profile.campus = fw_data['campus']
            profile.floor = fw_data['floor']
            profile.save()
            
            fw_info = {
                'id': user.id,
                'username': fw_data['username'],
                'email': fw_data['email'],
                'campus': fw_data['campus'],
                'floor': fw_data['floor']
            }
            
            if user_created:
                result['floorwings_created'].append(fw_info)
            else:
                result['floorwings_updated'].append(fw_info)
                
        except Exception as e:
            result['errors'].append({
                'username': fw_data['username'],
                'error': str(e)
            })
    
    # Get all floor wings for verification
    all_floor_wings = UserProfile.objects.filter(role='FLOOR_WING').select_related('user').order_by('campus', 'floor')
    
    result['total_floor_wings'] = all_floor_wings.count()
    result['all_floor_wings'] = [
        {
            'id': fw.user.id,
            'username': fw.user.username,
            'email': fw.user.email,
            'campus': fw.campus,
            'campus_display': fw.get_campus_display(),
            'floor': fw.floor
        }
        for fw in all_floor_wings
    ]
    
    result['summary'] = {
        'created': len(result['floorwings_created']),
        'updated': len(result['floorwings_updated']),
        'errors': len(result['errors']),
        'total_in_db': result['total_floor_wings']
    }
    
    result['default_password'] = DEFAULT_PASSWORD
    result['message'] = f"Setup complete! Created {len(result['floorwings_created'])} and updated {len(result['floorwings_updated'])} floor wing users."
    
    return Response(result, status=status.HTTP_200_OK)
