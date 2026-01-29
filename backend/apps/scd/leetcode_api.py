"""
LeetCode API Integration Utility

This module handles fetching data from LeetCode's GraphQL API.
"""

import requests
import time
from datetime import datetime
from typing import Dict, List, Optional


class LeetCodeAPI:
    """Handler for LeetCode GraphQL API requests"""
    
    GRAPHQL_URL = "https://leetcode.com/graphql"
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    
    HEADERS = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://leetcode.com',
        'Origin': 'https://leetcode.com',
    }
    
    # GraphQL query for user profile stats
    USER_PROFILE_QUERY = """
    query getUserProfile($username: String!) {
        matchedUser(username: $username) {
            username
            profile {
                ranking
                userAvatar
                realName
                aboutMe
                reputation
            }
            submitStats {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
        }
    }
    """
    
    # GraphQL query for recent submissions
    RECENT_SUBMISSIONS_QUERY = """
    query getRecentSubmissions($username: String!, $limit: Int!) {
        recentAcSubmissionList(username: $username, limit: $limit) {
            title
            titleSlug
            timestamp
            statusDisplay
            lang
        }
    }
    """
    
    # GraphQL query for contest info
    CONTEST_INFO_QUERY = """
    query getUserContestInfo($username: String!) {
        userContestRanking(username: $username) {
            attendedContestsCount
            rating
            globalRanking
            totalParticipants
            topPercentage
        }
    }
    """
    
    # GraphQL query for user calendar/streak data
    USER_CALENDAR_QUERY = """
    query getUserCalendar($username: String!, $year: Int!) {
        matchedUser(username: $username) {
            userCalendar(year: $year) {
                streak
                totalActiveDays
                submissionCalendar
            }
        }
    }
    """
    
    @staticmethod
    def fetch_user_profile(username: str) -> Optional[Dict]:
        """
        Fetch user profile data from LeetCode
        
        Args:
            username: LeetCode username
            
        Returns:
            Dictionary with user profile data or None if failed
        """
        for attempt in range(LeetCodeAPI.MAX_RETRIES):
            try:
                response = requests.post(
                    LeetCodeAPI.GRAPHQL_URL,
                    json={
                        'query': LeetCodeAPI.USER_PROFILE_QUERY,
                        'variables': {'username': username}
                    },
                    headers=LeetCodeAPI.HEADERS,
                    timeout=45
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('data') and data['data'].get('matchedUser'):
                        return LeetCodeAPI._parse_profile_data(data['data']['matchedUser'])
                else:
                    print(f"LeetCode API returned status {response.status_code}: {response.text[:200]}")
                
                return None
                
            except requests.exceptions.Timeout:
                if attempt < LeetCodeAPI.MAX_RETRIES - 1:
                    print(f"Timeout fetching profile for {username}, retrying in {LeetCodeAPI.RETRY_DELAY}s... (attempt {attempt + 1}/{LeetCodeAPI.MAX_RETRIES})")
                    time.sleep(LeetCodeAPI.RETRY_DELAY)
                    continue
                else:
                    print(f"Error fetching LeetCode profile for {username}: Max retries exceeded")
                    return None
            except Exception as e:
                print(f"Error fetching LeetCode profile for {username}: {str(e)}")
                return None
    
    @staticmethod
    def _parse_profile_data(matched_user: Dict) -> Dict:
        """Parse the matched user data into a clean format"""
        
        # Parse submission stats
        submit_stats = matched_user.get('submitStats', {})
        ac_submissions = submit_stats.get('acSubmissionNum', [])
        
        stats = {
            'total_solved': 0,
            'easy_solved': 0,
            'medium_solved': 0,
            'hard_solved': 0
        }
        
        for submission in ac_submissions:
            difficulty = submission.get('difficulty', '').lower()
            count = submission.get('count', 0)
            
            if difficulty == 'all':
                stats['total_solved'] = count
            elif difficulty == 'easy':
                stats['easy_solved'] = count
            elif difficulty == 'medium':
                stats['medium_solved'] = count
            elif difficulty == 'hard':
                stats['hard_solved'] = count
        
        # Parse profile info
        profile = matched_user.get('profile', {})
        
        return {
            'username': matched_user.get('username'),
            'ranking': profile.get('ranking'),
            'total_solved': stats['total_solved'],
            'easy_solved': stats['easy_solved'],
            'medium_solved': stats['medium_solved'],
            'hard_solved': stats['hard_solved'],
            'real_name': profile.get('realName'),
            'avatar': profile.get('userAvatar'),
            'reputation': profile.get('reputation')
        }
    
    @staticmethod
    def fetch_recent_submissions(username: str, limit: int = 10) -> List[Dict]:
        """
        Fetch recent accepted submissions
        
        Args:
            username: LeetCode username
            limit: Number of submissions to fetch
            
        Returns:
            List of submission dictionaries
        """
        for attempt in range(LeetCodeAPI.MAX_RETRIES):
            try:
                response = requests.post(
                    LeetCodeAPI.GRAPHQL_URL,
                    json={
                        'query': LeetCodeAPI.RECENT_SUBMISSIONS_QUERY,
                        'variables': {'username': username, 'limit': limit}
                    },
                    headers=LeetCodeAPI.HEADERS,
                    timeout=45
                )
                
                if response.status_code == 200:
                    data = response.json()
                    submissions = data.get('data', {}).get('recentAcSubmissionList', [])
                    
                    return [{
                        'problem_title': sub.get('title'),
                        'problem_slug': sub.get('titleSlug'),
                        'status': sub.get('statusDisplay'),
                        'language': sub.get('lang'),
                        'timestamp': datetime.fromtimestamp(int(sub.get('timestamp', 0)))
                    } for sub in submissions]
                
                return []
                
            except requests.exceptions.Timeout:
                if attempt < LeetCodeAPI.MAX_RETRIES - 1:
                    print(f"Timeout fetching submissions for {username}, retrying in {LeetCodeAPI.RETRY_DELAY}s... (attempt {attempt + 1}/{LeetCodeAPI.MAX_RETRIES})")
                    time.sleep(LeetCodeAPI.RETRY_DELAY)
                    continue
                else:
                    print(f"Error fetching recent submissions for {username}: Max retries exceeded")
                    return []
            except Exception as e:
                print(f"Error fetching recent submissions for {username}: {str(e)}")
                return []
    
    @staticmethod
    def fetch_contest_info(username: str) -> Optional[Dict]:
        """
        Fetch user contest information
        
        Args:
            username: LeetCode username
            
        Returns:
            Dictionary with contest info or None if failed
        """
        for attempt in range(LeetCodeAPI.MAX_RETRIES):
            try:
                response = requests.post(
                    LeetCodeAPI.GRAPHQL_URL,
                    json={
                        'query': LeetCodeAPI.CONTEST_INFO_QUERY,
                        'variables': {'username': username}
                    },
                    headers=LeetCodeAPI.HEADERS,
                    timeout=45
                )
                
                if response.status_code == 200:
                    data = response.json()
                    contest_data = data.get('data', {}).get('userContestRanking')
                    
                    if contest_data:
                        return {
                            'rating': int(contest_data.get('rating', 0)),
                            'global_ranking': contest_data.get('globalRanking'),
                            'contests_attended': contest_data.get('attendedContestsCount'),
                            'top_percentage': contest_data.get('topPercentage')
                        }
                
                return None
                
            except requests.exceptions.Timeout:
                if attempt < LeetCodeAPI.MAX_RETRIES - 1:
                    print(f"Timeout fetching contest info for {username}, retrying in {LeetCodeAPI.RETRY_DELAY}s... (attempt {attempt + 1}/{LeetCodeAPI.MAX_RETRIES})")
                    time.sleep(LeetCodeAPI.RETRY_DELAY)
                    continue
                else:
                    print(f"Error fetching contest info for {username}: Max retries exceeded")
                    return None
            except Exception as e:
                print(f"Error fetching contest info for {username}: {str(e)}")
                return None
    
    @staticmethod
    def fetch_calendar_data(username: str) -> Optional[Dict]:
        """
        Fetch user calendar data including streak and monthly submissions
        
        Args:
            username: LeetCode username
            
        Returns:
            Dictionary with streak and calendar data or None if failed
        """
        for attempt in range(LeetCodeAPI.MAX_RETRIES):
            try:
                from datetime import datetime
                current_year = datetime.now().year
                
                response = requests.post(
                    LeetCodeAPI.GRAPHQL_URL,
                    json={
                        'query': LeetCodeAPI.USER_CALENDAR_QUERY,
                        'variables': {'username': username, 'year': current_year}
                    },
                    headers=LeetCodeAPI.HEADERS,
                    timeout=45
                )
                
                if response.status_code == 200:
                    data = response.json()
                    matched_user = data.get('data', {}).get('matchedUser')
                    
                    if matched_user and matched_user.get('userCalendar'):
                        calendar_data = matched_user['userCalendar']
                        submission_calendar_str = calendar_data.get('submissionCalendar', '{}')
                        
                        # Parse submission calendar JSON string
                        import json
                        try:
                            submission_calendar = json.loads(submission_calendar_str) if isinstance(submission_calendar_str, str) else submission_calendar_str
                        except:
                            submission_calendar = {}
                        
                        # Convert to proper format and filter last 12 months
                        from datetime import datetime, timedelta
                        now = datetime.now()
                        twelve_months_ago = now - timedelta(days=365)
                        twelve_months_ago_timestamp = int(twelve_months_ago.timestamp())
                        
                        # Filter and convert calendar data
                        filtered_calendar = {}
                        for timestamp_str, count in submission_calendar.items():
                            try:
                                timestamp = int(timestamp_str)
                                if timestamp >= twelve_months_ago_timestamp:
                                    # Store as string key for JSON compatibility
                                    filtered_calendar[str(timestamp)] = int(count)
                            except (ValueError, TypeError):
                                continue
                        
                        # Calculate current month's problems
                        current_month_start = datetime(now.year, now.month, 1).timestamp()
                        next_month = now.month + 1 if now.month < 12 else 1
                        next_month_year = now.year if now.month < 12 else now.year + 1
                        current_month_end = datetime(next_month_year, next_month, 1).timestamp()
                        
                        monthly_problems = sum(
                            int(count) for timestamp_str, count in filtered_calendar.items()
                            if current_month_start <= int(timestamp_str) < current_month_end
                        )
                        
                        return {
                            'streak': calendar_data.get('streak', 0),
                            'total_active_days': calendar_data.get('totalActiveDays', 0),
                            'monthly_problems': monthly_problems,
                            'submission_calendar': filtered_calendar
                        }
                
                return None
                
            except requests.exceptions.Timeout:
                if attempt < LeetCodeAPI.MAX_RETRIES - 1:
                    print(f"Timeout fetching calendar for {username}, retrying in {LeetCodeAPI.RETRY_DELAY}s... (attempt {attempt + 1}/{LeetCodeAPI.MAX_RETRIES})")
                    time.sleep(LeetCodeAPI.RETRY_DELAY)
                    continue
                else:
                    print(f"Error fetching calendar data for {username}: Max retries exceeded")
                    return None
            except Exception as e:
                print(f"Error fetching calendar data for {username}: {str(e)}")
                return None
