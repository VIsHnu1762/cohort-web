#!/usr/bin/env python
"""
Create mentor users in Render database with proper Django password hashing
Run this locally to generate proper hashes and insert into Render DB
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.hashers import make_password
import psycopg
from datetime import datetime

# Generate proper Django password hash
mentor_password_hash = make_password('mentor123')
print(f"Generated password hash for 'mentor123':\n{mentor_password_hash}\n")

# Connect to Render PostgreSQL
conn = psycopg.connect(
    "postgresql://cohort_user:kUANfskqMQ0Wzrp8M7kXmxp6aFKSbDrZ@dpg-d5tepckoud1c7393ca70-a.virginia-postgres.render.com/cohort_db_lbjf"
)
cur = conn.cursor()

print("=== Creating Mentor Users ===\n")

mentors = [
    ('reshma', 'Reshma', '', 'reshma@cohort.com'),
    ('gopikannan', 'Gopi', 'Kannan', 'gopikannan@cohort.com'),
    ('thulasi', 'Thulasi', '', 'thulasi@cohort.com'),
]

for username, fname, lname, email in mentors:
    try:
        # Check if user exists
        cur.execute("SELECT id FROM auth_user WHERE email = %s", (email,))
        existing = cur.fetchone()
        
        if existing:
            # Update password
            cur.execute("UPDATE auth_user SET password = %s WHERE email = %s", (mentor_password_hash, email))
            print(f"✅ Updated password for: {email}")
        else:
            # Create new user
            cur.execute("""
                INSERT INTO auth_user (
                    password, last_login, is_superuser, username, first_name, last_name,
                    email, is_staff, is_active, date_joined
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (mentor_password_hash, None, False, username, fname, lname, 
                  email, True, True, datetime.now()))
            
            user_id = cur.fetchone()[0]
            
            # Create profile
            cur.execute("""
                INSERT INTO profiles_userprofile (
                    user_id, role, campus, floor, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, 'MENTOR', 'TECH', 2, datetime.now(), datetime.now()))
            
            print(f"✅ Created: {email} / mentor123")
        
        conn.commit()
    except Exception as e:
        print(f"❌ Error with {email}: {e}")
        conn.rollback()

conn.close()
print("\n✅ Done! All mentors can now login with: mentor123")
