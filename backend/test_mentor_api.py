import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.cfc.models import HackathonSubmission, GenAIProjectSubmission
from apps.clt.models import CLTSubmission
from apps.scd.models import LeetCodeProfile

# Test the status mapping logic from mentor_views.py
def normalize_status(status):
    """Map backend statuses to frontend statuses"""
    if status in ['submitted', 'under_review', 'draft']:
        return 'pending'
    elif status == 'approved':
        return 'approved'
    elif status == 'rejected':
        return 'rejected'
    return status

print("=== Testing Status Mapping ===")
print("\nCFC Submissions:")
cfc_submissions = list(HackathonSubmission.objects.all()) + list(GenAIProjectSubmission.objects.all())
for sub in cfc_submissions:
    print(f"  ID: {sub.id}, Backend Status: {sub.status} -> Frontend: {normalize_status(sub.status)}")

print("\nCLT Submissions (first 10):")
for sub in CLTSubmission.objects.all()[:10]:
    print(f"  ID: {sub.id}, Backend Status: {sub.status} -> Frontend: {normalize_status(sub.status)}")

print("\nSCD Submissions:")
for sub in LeetCodeProfile.objects.all():
    print(f"  ID: {sub.id}, Backend Status: {sub.status} -> Frontend: {normalize_status(sub.status)}")

# Count by status
print("\n=== Stats for 'all' pillar ===")
all_submissions = cfc_submissions + list(CLTSubmission.objects.all()) + list(LeetCodeProfile.objects.all())
total = len(all_submissions)
pending = sum(1 for s in all_submissions if normalize_status(s.status) == 'pending')
approved = sum(1 for s in all_submissions if s.status == 'approved')
rejected = sum(1 for s in all_submissions if s.status == 'rejected')

print(f"Total: {total}")
print(f"Pending: {pending}")
print(f"Approved: {approved}")
print(f"Rejected: {rejected}")
