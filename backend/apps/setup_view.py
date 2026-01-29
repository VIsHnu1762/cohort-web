"""
Simple setup endpoint to initialize database with users
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from apps.profiles.models import UserProfile
from apps.gamification.models import Season, Title
import csv
import os

@csrf_exempt
@require_http_methods(["POST"])
def setup_database(request):
    """
    One-time setup endpoint to create admin and import users
    Add a simple auth check for security
    """
    # Simple security check - only allow if no users exist or if secret key provided
    setup_key = request.POST.get('setup_key', '')
    
    if User.objects.count() > 0 and setup_key != 'cohort_setup_2024':
        return JsonResponse({'error': 'Database already initialized or invalid setup key'}, status=403)
    
    results = {
        'admin_created': False,
        'students_created': 0,
        'students_updated': 0,
        'errors': []
    }
    
    # Create admin user
    admin_email = "admin@test.com"
    try:
        if not User.objects.filter(email=admin_email).exists():
            admin = User.objects.create_superuser(
                username='admin',
                email=admin_email,
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            results['admin_created'] = True
        else:
            admin = User.objects.get(email=admin_email)
            admin.set_password('admin123')
            admin.is_superuser = True
            admin.is_staff = True
            admin.save()
            results['admin_updated'] = True
        
        # Create admin profile
        admin_profile, _ = UserProfile.objects.get_or_create(
            user=admin,
            defaults={
                'role': 'ADMIN',
                'campus': 'TECH',
                'floor': 1
            }
        )
        admin_profile.role = 'ADMIN'
        admin_profile.campus = 'TECH'
        admin_profile.save()
        
    except Exception as e:
        results['errors'].append(f'Admin creation error: {str(e)}')
    
    # Import CSV users
    # Try multiple possible paths
    possible_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'dummy users - Sheet1.csv'),
        os.path.join(os.path.dirname(__file__), '..', '..', 'dummy users - Sheet1.csv'),
        '/app/dummy users - Sheet1.csv',
        '/app/backend/dummy users - Sheet1.csv',
    ]
    
    csv_path = None
    for path in possible_paths:
        normalized = os.path.normpath(path)
        if os.path.exists(normalized):
            csv_path = normalized
            break
    
    if not csv_path:
        results['errors'].append(f'CSV not found. Tried: {[os.path.normpath(p) for p in possible_paths]}')
        results['cwd'] = os.getcwd()
        results['files_in_app'] = os.listdir('/app') if os.path.exists('/app') else 'N/A'
        return JsonResponse(results)
    
    campus = 'TECH'
    floor = 2
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    email = row['email'].strip()
                    username = row['username'].strip()
                    
                    user, is_new = User.objects.get_or_create(
                        email=email,
                        defaults={
                            'username': username,
                            'first_name': username.split()[0] if username else '',
                            'last_name': ' '.join(username.split()[1:]) if len(username.split()) > 1 else ''
                        }
                    )
                    
                    user.set_password('pass123#')
                    user.save()
                    
                    profile, _ = UserProfile.objects.get_or_create(
                        user=user,
                        defaults={'role': 'STUDENT', 'campus': campus, 'floor': floor}
                    )
                    profile.role = 'STUDENT'
                    profile.campus = campus
                    profile.floor = floor
                    profile.save()
                    
                    if is_new:
                        results['students_created'] += 1
                    else:
                        results['students_updated'] += 1
                        
                except Exception as e:
                    results['errors'].append(f'Error with {email}: {str(e)}')
                    
    except Exception as e:
        results['errors'].append(f'CSV reading error: {str(e)}')
    
    # Initialize gamification system
    try:
        results['gamification_setup'] = setup_gamification()
    except Exception as e:
        results['errors'].append(f'Gamification setup error: {str(e)}')
    
    # Create mentors and assign students
    try:
        results['mentor_setup'] = setup_mentors_and_assignments()
    except Exception as e:
        results['errors'].append(f'Mentor setup error: {str(e)}')
    
    results['success'] = True
    results['total_users'] = User.objects.count()
    
    return JsonResponse(results)

def setup_gamification():
    """Initialize gamification system with first season and titles"""
    gamif_results = {}
    
    # Create first season if doesn't exist
    if not Season.objects.exists():
        today = timezone.now().date()
        start_date = today.replace(day=1)
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        Season.objects.create(
            name=f"Season 1 - {start_date.strftime('%B %Y')}",
            season_number=1,
            start_date=start_date,
            end_date=end_date,
            is_active=True
        )
        gamif_results['season_created'] = True
    else:
        gamif_results['season_exists'] = True
    
    # Create titles
    titles_data = [
        {'name': 'The Consistent', 'description': 'Completed all episodes without breaking streak', 'vault_credit_cost': 50, 'icon': '🔥', 'rarity': 'rare'},
        {'name': 'The Ascender', 'description': 'Achieved Ascension Bonus in 3 consecutive seasons', 'vault_credit_cost': 100, 'icon': '📈', 'rarity': 'epic'},
        {'name': 'The Finisher', 'description': 'Completed first season with 100% episode completion', 'vault_credit_cost': 30, 'icon': '✅', 'rarity': 'common'},
        {'name': 'Code Warrior', 'description': 'Maintained perfect LeetCode streak for entire season', 'vault_credit_cost': 80, 'icon': '⚔️', 'rarity': 'epic'},
    ]
    
    created_count = 0
    for title_data in titles_data:
        _, created = Title.objects.get_or_create(
            name=title_data['name'],
            defaults=title_data
        )
        if created:
            created_count += 1
    
    gamif_results['titles_created'] = created_count
    gamif_results['total_titles'] = Title.objects.count()
    
    return gamif_results

def setup_mentors_and_assignments():
    """Create 2 mentors and assign 5 students to each"""
    mentor_results = {}
    
    # Create mentor 1
    mentor1, created1 = User.objects.get_or_create(
        email='mentor1@snsce.ac.in',
        defaults={
            'username': 'mentor1',
            'first_name': 'Mentor',
            'last_name': 'One'
        }
    )
    mentor1.set_password('mentor123')
    mentor1.save()
    
    profile1, _ = UserProfile.objects.get_or_create(
        user=mentor1,
        defaults={'role': 'MENTOR', 'campus': 'TECH', 'floor': 2}
    )
    profile1.role = 'MENTOR'
    profile1.campus = 'TECH'
    profile1.floor = 2
    profile1.save()
    
    # Create mentor 2
    mentor2, created2 = User.objects.get_or_create(
        email='mentor2@snsce.ac.in',
        defaults={
            'username': 'mentor2',
            'first_name': 'Mentor',
            'last_name': 'Two'
        }
    )
    mentor2.set_password('mentor123')
    mentor2.save()
    
    profile2, _ = UserProfile.objects.get_or_create(
        user=mentor2,
        defaults={'role': 'MENTOR', 'campus': 'TECH', 'floor': 2}
    )
    profile2.role = 'MENTOR'
    profile2.campus = 'TECH'
    profile2.floor = 2
    profile2.save()
    
    mentor_results['mentor1_created'] = created1
    mentor_results['mentor2_created'] = created2
    
    # Get students (excluding admin and mentors)
    students = UserProfile.objects.filter(role='STUDENT').select_related('user')[:10]
    
    assignments = []
    for i, student_profile in enumerate(students):
        # Assign first 5 to mentor1, next 5 to mentor2
        if i < 5:
            student_profile.mentor = mentor1
            assignments.append(f"{student_profile.user.email} → Mentor One")
        else:
            student_profile.mentor = mentor2
            assignments.append(f"{student_profile.user.email} → Mentor Two")
        student_profile.save()
    
    mentor_results['assignments'] = assignments
    mentor_results['total_assigned'] = len(assignments)
    
    return mentor_results
