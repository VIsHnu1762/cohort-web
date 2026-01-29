import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.cfc.models import HackathonSubmission, GenAIProjectSubmission
from apps.clt.models import CLTSubmission
from apps.scd.models import LeetCodeProfile

print("=== CFC Hackathon Submissions ===")
for h in HackathonSubmission.objects.all():
    print(f"ID: {h.id}, User: {h.user.username}, Status: {h.status}, Title: {h.hackathon_name}")

print("\n=== CFC GenAI Submissions ===")
for g in GenAIProjectSubmission.objects.all():
    print(f"ID: {g.id}, User: {g.user.username}, Status: {g.status}, Problem: {g.problem_statement[:50]}...")

print("\n=== CLT Submissions (first 5) ===")
for c in CLTSubmission.objects.all()[:5]:
    print(f"ID: {c.id}, User: {c.user.username}, Status: {c.status}, Title: {c.title}")

print("\n=== SCD LeetCode Profiles ===")
for s in LeetCodeProfile.objects.all():
    print(f"ID: {s.id}, User: {s.user.username}, Status: {s.status}, Username: {s.leetcode_username}")
