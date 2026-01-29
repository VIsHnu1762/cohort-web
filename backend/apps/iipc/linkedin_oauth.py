"""
LinkedIn OAuth Integration Service
Handles LinkedIn Sign In and profile data fetching
"""
import os
import requests
from urllib.parse import urlencode


class LinkedInOAuthService:
    """Service for LinkedIn OAuth 2.0 authentication"""
    
    # LinkedIn OAuth URLs
    AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
    ACCESS_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
    PROFILE_URL = "https://api.linkedin.com/v2/userinfo"
    
    # OAuth Scopes (what we're requesting access to)
    SCOPES = ['openid', 'profile', 'email']
    
    def __init__(self):
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')
    
    def get_authorization_url(self, state=None):
        """
        Generate LinkedIn OAuth authorization URL
        User will be redirected to this URL to authorize the app
        
        Args:
            state: Random string for CSRF protection
            
        Returns:
            str: Full authorization URL
        """
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.SCOPES),
        }
        
        if state:
            params['state'] = state
        
        return f"{self.AUTHORIZATION_URL}?{urlencode(params)}"
    
    def exchange_code_for_token(self, code):
        """
        Exchange authorization code for access token
        
        Args:
            code: Authorization code from LinkedIn callback
            
        Returns:
            dict: Token response with access_token
        """
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        
        response = requests.post(
            self.ACCESS_TOKEN_URL,
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        response.raise_for_status()
        return response.json()
    
    def get_user_profile(self, access_token):
        """
        Fetch LinkedIn user profile using access token
        
        Args:
            access_token: LinkedIn OAuth access token
            
        Returns:
            dict: User profile data (name, email, sub/profile_id)
        """
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        
        response = requests.get(self.PROFILE_URL, headers=headers)
        response.raise_for_status()
        
        profile_data = response.json()
        
        # Extract profile URL from 'sub' (LinkedIn member ID)
        linkedin_id = profile_data.get('sub')
        
        return {
            'linkedin_id': linkedin_id,
            'first_name': profile_data.get('given_name', ''),
            'last_name': profile_data.get('family_name', ''),
            'full_name': profile_data.get('name', ''),
            'email': profile_data.get('email', ''),
            'profile_picture': profile_data.get('picture', ''),
            'profile_url': f"https://www.linkedin.com/in/{linkedin_id}" if linkedin_id else '',
        }
    
    def verify_profile(self, code):
        """
        Complete OAuth flow: exchange code for token and fetch profile
        
        Args:
            code: Authorization code from LinkedIn
            
        Returns:
            dict: User profile data
        """
        # Step 1: Exchange code for access token
        token_response = self.exchange_code_for_token(code)
        access_token = token_response.get('access_token')
        
        if not access_token:
            raise ValueError('Failed to obtain access token from LinkedIn')
        
        # Step 2: Fetch user profile
        profile_data = self.get_user_profile(access_token)
        
        return profile_data
