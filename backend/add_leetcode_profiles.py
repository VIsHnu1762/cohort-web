import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.profiles.models import UserProfile
import re

# LeetCode profile URLs
LEETCODE_URLS = """
https://leetcode.com/u/sai_sri2712/
https://leetcode.com/u/arunesh_kumarar_c-2007/
https://leetcode.com/u/leninkishir3103
https://leetcode.com/u/ganesh21906
https://leetcode.com/u/Nitharshini/
https://leetcode.com/u/Naren_R_S/
https://leetcode.com/u/gobinath__g/
https://leetcode.com/u/nidhinnatraj_4/
https://leetcode.com/u/sandhyarj/
https://leetcode.com/u/Phrisha_G_15/
https://leetcode.com/u/Remigious_19j/
https://leetcode.com/u/KaviyaVijayakumar/
https://leetcode.com/u/Anisha_Mg/
https://leetcode.com/u/javid-7/
https://leetcode.com/u/KIRUTHIKA-D3102006/
https://leetcode.com/u/Keerthana__17
https://leetcode.com/u/_kishore_3_11_6_/
https://leetcode.com/u/sriramrp08/
https://leetcode.com/u/Anushri_SG_03/
https://leetcode.com/u/Pooja_VR/
https://leetcode.com/u/Aravinth8926/
https://leetcode.com/u/SILVERAXE69/
https://leetcode.com/u/jevesh/
https://leetcode.com/u/Mirula__1710/
https://leetcode.com/u/PranethiR/
https://leetcode.com/u/Bavish_3728/
https://leetcode.com/u/madhushri_/
https://leetcode.com/u/Cibivishnu/
https://leetcode.com/u/MarleneSaranya_10/
https://leetcode.com/u/VISHAL1619/
https://leetcode.com/u/Ranjana_Gopi/
https://leetcode.com/u/PreenaMageshwaran/
https://leetcode.com/u/Sanjana_leet24/
https://leetcode.com/u/SathyFrancis_M/
https://leetcode.com/u/perarasu_/
https://leetcode.com/u/gnanasric54/
https://leetcode.com/u/deekshi_08/
https://leetcode.com/u/Bhavyasri07/
https://leetcode.com/u/kavinak6/
https://leetcode.com/u/prika_krish/
https://leetcode.com/u/samuktha01/
https://leetcode.com/u/umarahul/
https://leetcode.com/u/sowparnikals/
https://leetcode.com/u/iniyan_6/
https://leetcode.com/u/Balavignesh1585/
https://leetcode.com/u/Abina_j/
https://leetcode.com/u/Srinila_sant_2006/
https://leetcode.com/u/Arun_pandiayn_S/
https://leetcode.com/u/AmalAS/
https://leetcode.com/u/kishore888/
https://leetcode.com/Antonyraj26/
https://leetcode.com/u/__arathisuresh__/
https://leetcode.com/u/tharungurusamy/
https://leetcode.com/u/bhavatarini__02
https://leetcode.com/u/pooja006/
https://leetcode.com/u/yatjeeshwar_m/
https://leetcode.com/u/nehaaa1226/
https://leetcode.com/u/Tarunyasree/
https://leetcode.com/u/nisha176/
https://leetcode.com/u/santhoshkrishnan__M/
https://leetcode.com/u/B_Prarthana/
https://leetcode.com/u/hacksquare/
https://leetcode.com/u/praveen-sk/
https://leetcode.com/u/prxthosh/
https://leetcode.com/u/DAYANITHI_28/
https://leetcode.com/u/Amal_0318/
https://leetcode.com/u/lokesh_ms/
https://leetcode.com/u/Madeline-Prathana-V12/
https://leetcode.com/u/Gopi-01/
https://leetcode.com/u/bharani01207/
https://leetcode.com/u/MADHIYARASU08/
https://leetcode.com/u/iamdjtharsh/
https://leetcode.com/u/Logana_2006_/
https://leetcode.com/u/sudharasshana_22/
https://leetcode.com/u/navalakshmi/
https://leetcode.com/u/alanaseb/
https://leetcode.com/u/mpakilesh_03/
https://leetcode.com/u/krithika_varathakumaran/
https://leetcode.com/u/BsKyhnCM3E/
https://leetcode.com/u/Dharunyasri/
https://leetcode.com/u/Yogesh_2203/
https://leetcode.com/u/shakthisharaan/
https://leetcode.com/u/spark_sakthi/
https://leetcode.com/u/_Madhu_78cr_/
https://leetcode.com/u/Ramkumar_A/
https://leetcode.com/u/fouzul/
https://leetcode.com/u/Keerthu09/
https://leetcode.com/u/sivaprasath4173/
https://leetcode.com/u/Adhii_pro/
https://leetcode.com/u/Gopikasree0423/
https://leetcode.com/u/Pugal_06/
https://leetcode.com/u/Gokul_Anjaan/
https://leetcode.com/u/Prajith-VL/
https://leetcode.com/u/Giridharan_9807/
https://leetcode.com/u/__sanjai_07_/
https://leetcode.com/u/vishnudharshan/
https://leetcode.com/u/Paulina_27/
https://leetcode.com/u/prathiba2007/
https://leetcode.com/u/chakratharie/
https://leetcode.com/u/lokeshsundar220/
https://leetcode.com/u/nithishramesh/
https://leetcode.com/u/Swetha_2007/
https://leetcode.com/u/chandru2575/
https://leetcode.com/u/BhushanVenkatrajah/
https://leetcode.com/u/kavyasathiyamurthi_16/
https://leetcode.com/u/gokulkanna20/
https://leetcode.com/u/yaswanthika_18/
https://leetcode.com/u/mathi88/
https://leetcode.com/u/perumal04/
https://leetcode.com/u/9025306274/
https://leetcode.com/u/OviSri/
https://leetcode.com/u/kathu006/
https://leetcode.com/u/Sachinsv/
https://leetcode.com/u/Bhaarathinesan/
https://leetcode.com/u/MithunAiz/
https://leetcode.com/u/naveenp13/
https://leetcode.com/u/Harini_PJ/
https://leetcode.com/u/hmhqGk3DoL/
https://leetcode.com/u/Divagar_Jagan/
https://leetcode.com/u/poojasenthil/
https://leetcode.com/u/Priyanka__B/
https://leetcode.com/u/SakthiKandhavel_S/
https://leetcode.com/u/priya__11/
https://leetcode.com/u/Dhanushriloganathan/
https://leetcode.com/u/Dinesh__2006/
https://leetcode.com/u/haricoder07/
https://leetcode.com/u/__bala__07/
https://leetcode.com/u/Jabbastin/
https://leetcode.com/u/Roshieni_selvaraj_01/
https://leetcode.com/u/grace_joy/
https://leetcode.com/u/jriswan236/
https://leetcode.com/u/AFREENA9566/
https://leetcode.com/u/gowtham76/
https://leetcode.com/u/SKavinila/
https://leetcode.com/u/0gNmHT2xCw/
https://leetcode.com/u/RLochana/
https://leetcode.com/u/mohankumar/
https://leetcode.com/u/Nivethitha_R/
https://leetcode.com/u/Varshana_Sankar/
https://leetcode.com/u/kishorre____
https://leetcode.com/u/Mathiyazhagan_NTL/
https://leetcode.com/u/nithilaaS/
https://leetcode.com/u/sri_vishhh/
https://leetcode.com/u/7pFcI3xJJw/
https://leetcode.com/u/vetri1712/
https://leetcode.com/u/sasmitharaja/
"""

def extract_leetcode_username(url):
    """Extract username from LeetCode URL"""
    match = re.search(r'leetcode\.com/u?/?([^/]+)/?', url)
    if match:
        return match.group(1)
    return None

def normalize_name(name):
    """Normalize name for matching"""
    return re.sub(r'[^a-z0-9]', '', name.lower())

def find_student_by_leetcode(leetcode_username, students):
    """Try to match LeetCode username to student"""
    lc_norm = normalize_name(leetcode_username)
    
    # Try exact email prefix match
    for student in students:
        email_prefix = student.user.email.split('@')[0]
        email_norm = normalize_name(email_prefix)
        if lc_norm == email_norm or lc_norm in email_norm or email_norm in lc_norm:
            return student
    
    # Try name match
    for student in students:
        full_name = f"{student.user.first_name} {student.user.last_name}"
        name_norm = normalize_name(full_name)
        # Check if leetcode username contains significant part of name
        if len(lc_norm) > 3 and lc_norm in name_norm:
            return student
        if len(name_norm) > 3 and name_norm in lc_norm:
            return student
        
        # Try first name only
        first_norm = normalize_name(student.user.first_name)
        if len(first_norm) > 3 and first_norm in lc_norm:
            return student
    
    return None

def main():
    print("=" * 80)
    print("ADDING LEETCODE PROFILES TO TECH FLOOR 2 STUDENTS")
    print("=" * 80)
    
    # Get all TECH floor 2 students
    students = UserProfile.objects.filter(
        campus='TECH',
        floor=2,
        role='STUDENT'
    ).select_related('user')
    
    print(f"\nFound {students.count()} students in TECH Floor 2")
    
    # Parse LeetCode URLs
    urls = [line.strip() for line in LEETCODE_URLS.strip().split('\n') if line.strip() and 'leetcode.com' in line]
    leetcode_profiles = []
    
    for url in urls:
        username = extract_leetcode_username(url)
        if username:
            leetcode_profiles.append((username, url))
    
    print(f"Found {len(leetcode_profiles)} LeetCode profiles\n")
    
    # Match and update
    matched = 0
    unmatched = []
    
    for username, url in leetcode_profiles:
        student = find_student_by_leetcode(username, students)
        
        if student:
            student.leetcode_id = username
            student.save()
            print(f"✓ Matched: {username} → {student.user.first_name} {student.user.last_name} ({student.user.email})")
            matched += 1
        else:
            unmatched.append(username)
            print(f"✗ No match: {username}")
    
    print("\n" + "=" * 80)
    print(f"Results: {matched} matched, {len(unmatched)} unmatched")
    print("=" * 80)
    
    if unmatched:
        print(f"\nUnmatched LeetCode profiles ({len(unmatched)}):")
        for u in unmatched:
            print(f"  - {u}")

if __name__ == '__main__':
    main()
