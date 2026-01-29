import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# Configuration
EXCEL_FILE = '../DTPB Cohort Session Name List of IInd Years to Circulate.xlsx'
CAMPUS = 'TECH'
FLOOR = 2
DEFAULT_PASSWORD = 'pass123#'

def get_existing_mentors():
    """Get existing mentors for TECH floor 2"""
    mentors = UserProfile.objects.filter(
        campus='TECH',
        floor=2,
        role='MENTOR'
    ).select_related('user')
    
    return list(mentors)

def create_student_from_data(row, mentor):
    """Create a student from Excel row data"""
    try:
        # Extract data from row
        name = str(row['Name']).strip()
        reg_no = str(row['Reg_No']).strip()
        email = str(row['Email']).strip().lower()
        
        if not name or name == 'nan':
            return None
        
        # Generate username from registration number
        username = f"student_tech_f2_{reg_no.replace(' ', '_')}"
        
        # Ensure username is unique
        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}_{counter}"
            counter += 1
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            print(f"❌ Email {email} already exists - skipping {name}")
            return None
        
        # Split name
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=student_email,
            password=DEFAULT_PASSWORD,
            first_name=first_name,
            last_name=last_name,
            is_staff=False,
            is_superuser=False
        )
        
        # Create profile with mentor assignment
        profile = UserProfile.objects.create(
            user=user,
            role='STUDENT',
            campus=CAMPUS,
            floor=FLOOR,
            assigned_mentor=mentor.user if mentor else None
        )
        
        return user, profile, name, student_email
        
    except Exception as e:
        print(f"❌ Error creating student: {e}")
        return None

def main():
    print("=" * 80)
    print("ADDING STUDENTS FROM EXCEL TO SNS COLLEGE OF TECHNOLOGY - FLOOR 2")
    print("=" * 80)
    
    # Check if Excel file exists
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ Excel file not found: {EXCEL_FILE}")
        return
    
    # Read Excel file (skip first 2 rows - title and header)
    try:
        df = pd.read_excel(EXCEL_FILE, skiprows=2)
        # Rename columns for easier access
        df.columns = ['Sl_No', 'College', 'Year', 'Department', 'Reg_No', 'Name', 'Contact', 'Email', 'Mentor_Name']
        # Remove any empty rows
        df = df.dropna(subset=['Name'])
        print(f"✓ Loaded Excel file with {len(df)} student records")
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return
    
    # Get existing mentors
    mentors = get_existing_mentors()
    if not mentors:
        print("❌ No mentors found for TECH floor 2")
        return
    
    print(f"\n✓ Found {len(mentors)} mentors for TECH floor 2:")
    for mentor in mentors:
        print(f"  - {mentor.user.first_name} {mentor.user.last_name} ({mentor.user.email})")
    
    print(f"\nCampus: SNS College of Technology (TECH)")
    print(f"Floor: 2")
    print(f"Password: {DEFAULT_PASSWORD}")
    print("=" * 80)
    
    # Confirm
    response = input(f"\nProceed with adding {len(df)} students? (yes/no): ").strip().lower()
    if response != 'yes':
        print("Operation cancelled.")
        return
    
    # Create students
    created_count = 0
    mentor_index = 0
    
    for idx, row in df.iterrows():
        # Round-robin mentor assignment
        mentor = mentors[mentor_index % len(mentors)]
        
        result = create_student_from_data(row, mentor)
        
        if result:
            user, profile, name, email = result
            print(f"\n✓ Created: {user.username}")
            print(f"  Name: {name}")
            print(f"  Email: {email}")
            print(f"  Password: {DEFAULT_PASSWORD}")
            print(f"  Mentor: {mentor.user.first_name} {mentor.user.last_name}")
            created_count += 1
            mentor_index += 1
    
    print("\n" + "=" * 80)
    print(f"✓ Successfully created {created_count} out of {len(df)} students")
    print(f"✓ Students distributed among {len(mentors)} mentors")
    print("=" * 80)
    print("\nStudents can now login with:")
    print(f"  Email: <their_email>")
    print(f"  Password: {DEFAULT_PASSWORD}")
    print("=" * 80)

if __name__ == '__main__':
    main()
