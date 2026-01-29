#!/usr/bin/env python3
"""Direct user insertion to Railway PostgreSQL"""
import psycopg
import csv
import os
from hashlib import pbkdf2_hmac
import base64

# Railway PostgreSQL connection
DATABASE_URL = 'postgresql://postgres:wUOcgZIVskopAQbBSwtzaxrqqySwHhwe@nozomi.proxy.rlwy.net:46837/railway'

def make_password(password):
    """Create Django-compatible PBKDF2 password hash"""
    salt = base64.b64encode(os.urandom(12)).decode('utf-8')
    hash_value = pbkdf2_hmac('sha256', password.encode(), salt.encode(), 260000)
    hash_b64 = base64.b64encode(hash_value).decode('utf-8').strip()
    return f'pbkdf2_sha256$260000${salt}${hash_b64}'

def main():
    print("="*60)
    print("PUSHING USERS TO RAILWAY POSTGRESQL")
    print("="*60)
    
    conn = psycopg.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Read CSV
    csv_path = 'dummy users - Sheet1.csv'
    created = 0
    updated = 0
    
    print(f"\nImporting students from {csv_path}...")
    print("-"*60)
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row['email'].strip()
            username = row['username'].strip()
            password_hash = make_password('pass123#')
            
            # Check if user exists
            cur.execute("SELECT id FROM auth_user WHERE email = %s", (email,))
            user = cur.fetchone()
            
            if user:
                # Update user
                cur.execute("""
                    UPDATE auth_user 
                    SET username = %s, password = %s, first_name = %s, last_name = %s
                    WHERE email = %s
                """, (username, password_hash, username.split()[0] if username else '', 
                      ' '.join(username.split()[1:]) if len(username.split()) > 1 else '', email))
                user_id = user[0]
                updated += 1
                status = '🔄 Updated'
            else:
                # Create user
                cur.execute("""
                    INSERT INTO auth_user (username, email, password, first_name, last_name, 
                                          is_active, is_staff, is_superuser, date_joined)
                    VALUES (%s, %s, %s, %s, %s, true, false, false, NOW())
                    RETURNING id
                """, (username, email, password_hash, username.split()[0] if username else '',
                      ' '.join(username.split()[1:]) if len(username.split()) > 1 else ''))
                user_id = cur.fetchone()[0]
                created += 1
                status = '✅ Created'
            
            # Create or update profile
            cur.execute("SELECT id FROM profiles_userprofile WHERE user_id = %s", (user_id,))
            profile = cur.fetchone()
            
            if profile:
                cur.execute("""
                    UPDATE profiles_userprofile 
                    SET role = 'STUDENT', campus = 'TECH', floor = 2
                    WHERE user_id = %s
                """, (user_id,))
            else:
                cur.execute("""
                    INSERT INTO profiles_userprofile (user_id, role, campus, floor)
                    VALUES (%s, 'STUDENT', 'TECH', 2)
                """, (user_id,))
            
            print(f"{status}: {username[:30]:<30} | {email}")
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("-"*60)
    print(f"\n✅ IMPORT COMPLETE!")
    print(f"   Students created: {created}")
    print(f"   Students updated: {updated}")
    print(f"   Total students: {created + updated}")
    print("\n📋 LOGIN CREDENTIALS:")
    print(f"   Students: <email> / pass123#")
    print("="*60)

if __name__ == '__main__':
    main()
