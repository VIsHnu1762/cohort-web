import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile

# Configuration
EXCEL_FILE = os.path.join(os.path.dirname(__file__), '..', 'Book1.xlsx')
CAMPUS = 'TECH'
FLOOR = 2
DEFAULT_PASSWORD = 'pass123#'

# Accepted column name variants (case-insensitive)
COL_MAP = {
    'reg': ['reg', 'reg no', 'reg no.', 'reg number', 'regnumber', 'registration', 'registration no', 'registration number', 'registernumber', 'register number'],
    'name': ['name', 'student name', 'full name', 'username', 'user name'],
    'email': ['email', 'email id', 'email address', 'mail', 'mail id']
}

def normalize_columns(cols):
    norm = {}
    lower_cols = {c.lower().strip(): c for c in cols}
    def find_key(keys):
        for k in keys:
            if k in lower_cols:
                return lower_cols[k]
        return None
    norm['reg'] = find_key(COL_MAP['reg'])
    norm['name'] = find_key(COL_MAP['name'])
    norm['email'] = find_key(COL_MAP['email'])
    return norm

def get_floor2_mentors():
    return list(UserProfile.objects.filter(campus=CAMPUS, floor=FLOOR, role='MENTOR').select_related('user'))

def safe_str(x):
    if pd.isna(x):
        return ''
    return str(x).strip()

def username_from(reg, name, email):
    base = ''
    if reg:
        base = reg.replace(' ', '').replace('/', '_').lower()
    elif email:
        base = email.split('@')[0].lower()
    else:
        base = name.replace(' ', '_').lower() if name else 'student'
    base = f"student_tech_f2_{base}"
    u = base
    i = 1
    while User.objects.filter(username=u).exists():
        u = f"{base}_{i}"
        i += 1
    return u

def ensure_profile(user, mentor):
    profile, _ = UserProfile.objects.get_or_create(user=user, defaults={
        'role': 'STUDENT', 'campus': CAMPUS, 'floor': FLOOR,
    })
    # Normalize fields if existing
    changed = False
    if profile.role != 'STUDENT':
        profile.role = 'STUDENT'; changed = True
    if profile.campus != CAMPUS:
        profile.campus = CAMPUS; changed = True
    if profile.floor != FLOOR:
        profile.floor = FLOOR; changed = True
    if mentor and (not profile.assigned_mentor or profile.assigned_mentor_id != mentor.user_id):
        profile.assigned_mentor = mentor.user; changed = True
    if changed:
        profile.save()
    return profile

def main():
    print('=' * 80)
    print('IMPORTING STUDENTS FROM Book1.xlsx -> TECH campus, Floor 2')
    print('=' * 80)

    if not os.path.exists(EXCEL_FILE):
        print(f"❌ Excel file not found: {EXCEL_FILE}")
        return

    try:
        # Read Excel - actual headers are in row 2 but columns show as Unnamed
        # Read without header first
        df_raw = pd.read_excel(EXCEL_FILE, header=None)
        # Row 2 (index 2) has the headers (but they're NaN)
        # Data starts from row 3 onwards
        df = pd.read_excel(EXCEL_FILE, skiprows=3)
        print(f"✓ Loaded {len(df)} rows")
    except Exception as e:
        print(f"❌ Failed to read Excel: {e}")
        return

    # Drop completely empty rows
    df = df.dropna(how='all')
    cols = [str(c) for c in df.columns]
    
    # Direct mapping: columns are 'nan', 'nan.1', 'nan.2'
    # nan = reg number, nan.1 = name, nan.2 = email
    if len(cols) >= 3:
        # Use positional columns instead of name matching
        mapping = {
            'reg': cols[0],    # First column (Unnamed: 0 or nan)
            'name': cols[1],   # Second column (Unnamed: 1 or nan.1)
            'email': cols[2]   # Third column (Unnamed: 2 or nan.2)
        }
        print(f"✓ Using columns: Reg={cols[0]}, Name={cols[1]}, Email={cols[2]}")
    else:
        print(f"❌ Expected at least 3 columns, found: {cols}")
        return

    mentors = get_floor2_mentors()
    if not mentors:
        print('❌ No mentors found for TECH Floor 2. Please create/assign mentors first.')
        return

    print(f"✓ Found {len(mentors)} mentor(s) for Floor 2")
    created, updated, skipped = 0, 0, 0
    mentor_idx = 0

    for _, row in df.iterrows():
        reg = safe_str(row[mapping['reg']])
        name = safe_str(row[mapping['name']])
        email = safe_str(row[mapping['email']])

        if not name and not reg and not email:
            continue
        if not email:
            email = (reg or name.replace(' ', '').lower() or 'student') + '@student.sns.edu'

        # Split name
        first, last = '', ''
        if name:
            parts = name.split(' ', 1)
            first = parts[0]
            last = parts[1] if len(parts) > 1 else ''

        # Decide username
        uname = username_from(reg, name, email)
        mentor = mentors[mentor_idx % len(mentors)]

        # If email exists, reuse that account
        user = User.objects.filter(email=email).first()
        if user:
            user.first_name = first
            user.last_name = last
            user.set_password(DEFAULT_PASSWORD)
            user.save()
            ensure_profile(user, mentor)
            updated += 1
            mentor_idx += 1
            print(f"↻ Updated existing user: {user.username} ({email})")
            continue

        # If username exists, skip to avoid collision
        if User.objects.filter(username=uname).exists():
            print(f"⏭️  Skipping (username exists): {uname}")
            skipped += 1
            continue

        # Create new user
        user = User.objects.create_user(
            username=uname,
            email=email,
            password=DEFAULT_PASSWORD,
            first_name=first,
            last_name=last,
            is_staff=False,
            is_superuser=False,
        )
        ensure_profile(user, mentor)
        created += 1
        mentor_idx += 1
        print(f"✓ Created: {uname}  |  {name}  |  {email}")

    print('\n' + '=' * 80)
    print(f"Done. Created: {created}, Updated: {updated}, Skipped: {skipped}")
    print('=' * 80)

if __name__ == '__main__':
    main()
