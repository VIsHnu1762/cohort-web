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

def preview_excel():
    """Preview the Excel file structure"""
    print("=" * 80)
    print("PREVIEWING EXCEL FILE")
    print("=" * 80)
    
    df = pd.read_excel(EXCEL_FILE)
    print(f"\nTotal rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst 5 rows:")
    print(df.head())
    print("\n" + "=" * 80)

def get_existing_mentors():
    """Get existing mentors for TECH floor 2"""
    mentors = UserProfile.objects.filter(
        campus='TECH',
        floor=2,
        role='MENTOR'
    ).select_related('user')
    return list(mentors)

def create_student(reg_no, name, email, mentor):
    """Create a student user"""
    try:
        # Clean data
        reg_no = str(reg_no).strip()
        name = str(name).strip()
        email = str(email).strip().lower()
        
        # Skip if essential data is missing
        if not name or name == 'nan' or not email or email == 'nan':
            return None
        
        # Generate username from registration number
        username = f"student_tech_f2_{reg_no.replace('/', '_').replace(' ', '_')}"
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            print(f"❌ Username {username} already exists")
            return None
        
        if User.objects.filter(email=email).exists():
            print(f"❌ Email {email} already exists")
            return None
        
        # Split name
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=DEFAULT_PASSWORD,
            first_name=first_name,
            last_name=last_name,
            is_staff=False,
            is_superuser=False
        )
        
        # Create profile
        profile = UserProfile.objects.create(
            user=user,
            role='STUDENT',
            campus=CAMPUS,
            floor=FLOOR,
            assigned_mentor=mentor.user if mentor else None
        )
        
        return user, profile
        
    except Exception as e:
        print(f"❌ Error creating student {name}: {e}")
        return None

def main():
    print("\n" + "=" * 80)
    print("IMPORTING STUDENTS FROM EXCEL")
    print("=" * 80)
    
    # Read Excel - skip first 2 rows (title rows), use row 2 as header
    df = pd.read_excel(EXCEL_FILE, header=2)
    
    # Clean up the dataframe - remove completely empty rows
    df = df.dropna(how='all')
    
    print(f"\nTotal rows after cleanup: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst 3 rows:")
    print(df.head(3))
    
    # Use specific column indices or names
    # Based on the structure: Sl no, College, Dept, Year, Register No, Name, Phone Number, Mail ID, Mentor
    reg_col = 'Register No'
    name_col = 'Name'
    email_col = 'Mail ID'
    
    print(f"\nUsing columns:")
    print(f"  Registration: {reg_col}")
    print(f"  Name: {name_col}")
    print(f"  Email: {email_col}")
    
    if reg_col not in df.columns or name_col not in df.columns or email_col not in df.columns:
        print("\n❌ Required columns not found!")
        print(f"Available columns: {list(df.columns)}")
        return
    
    # Get mentors
    mentors = get_existing_mentors()
    if not mentors:
        print("\n❌ No mentors found for TECH floor 2")
        return
    
    print(f"\n✓ Found {len(mentors)} mentors:")
    for mentor in mentors:
        print(f"  - {mentor.user.first_name} {mentor.user.last_name}")
    
    print(f"\nCampus: TECH (SNS College of Technology)")
    print(f"Floor: 2")
    print(f"Password: {DEFAULT_PASSWORD}")
    print(f"Total students to import: {len(df)}")
    print("=" * 80)
    
    response = input(f"\nProceed with importing students? (yes/no): ").strip().lower()
    if response != 'yes':
        print("Operation cancelled.")
        return
    
    # Import students
    created_count = 0
    mentor_index = 0
    
    for idx, row in df.iterrows():
        reg_no = row[reg_col]
        name = row[name_col]
        email = row[email_col]
        
        # Skip empty rows
        if pd.isna(name) or pd.isna(email):
            continue
        
        mentor = mentors[mentor_index % len(mentors)]
        result = create_student(reg_no, name, email, mentor)
        
        if result:
            user, profile = result
            print(f"✓ {created_count + 1}. {user.username} - {name} - {email} (Mentor: {mentor.user.first_name})")
            created_count += 1
            mentor_index += 1
    
    print("\n" + "=" * 80)
    print(f"✓ Successfully created {created_count} students")
    print(f"✓ Distributed among {len(mentors)} mentors")
    print("=" * 80)
    print("\nLogin credentials:")
    print(f"  Email: <student_email_from_excel>")
    print(f"  Password: {DEFAULT_PASSWORD}")
    print("=" * 80)

if __name__ == '__main__':
    main()
