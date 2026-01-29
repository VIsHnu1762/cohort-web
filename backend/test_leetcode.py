import sys
sys.path.insert(0, '.')

from apps.scd.leetcode_api import LeetCodeAPI

print("Testing LeetCode API...")
print("-" * 50)

result = LeetCodeAPI.fetch_user_profile('sriramrp08')
print(f"\nProfile fetch: {'SUCCESS' if result else 'FAILED'}")
if result:
    print(f"Username: {result['username']}")
    print(f"Total solved: {result['total_solved']}")
