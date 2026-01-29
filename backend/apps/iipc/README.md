# IIPC (Industry Institute Partnership Cell) - Backend Module

## Overview
The IIPC module manages LinkedIn verification for students, including post engagement and professional connections verification.

## Features

### 1. LinkedIn Post Verification
- **Post URL tracking** with engagement metrics
- **Engagement scoring** (likes, comments, shares)
- **Character and hashtag counting**
- **Sentiment analysis** (Positive/Negative/Neutral)
- **Minimum engagement threshold**: 50 for submission

### 2. LinkedIn Connection Verification
- **Two verification methods**:
  - Screenshot upload (Google Drive links)
  - Profile link verification
- **Connection tracking** with verified connections list
- **Minimum connections**: 100 for submission
- **Verified connection details** (name, company, designation)

## Models

### LinkedInPostVerification
- User's LinkedIn post with engagement metrics
- Fields: post_url, post_date, character_count, hashtag_count, engagement_score
- Optional: likes_count, comments_count, shares_count, sentiment
- Status: draft → pending → approved/rejected

### LinkedInConnectionVerification
- User's LinkedIn connections verification
- Fields: verification_method, profile_url, total_connections
- Related: screenshots, verified_connections
- Status: draft → pending → approved/rejected

### ConnectionScreenshot
- Google Drive links to connection screenshots
- Related to LinkedInConnectionVerification

### VerifiedConnection
- Individual verified LinkedIn connections
- Fields: name, company, designation, profile_url, is_verified

## API Endpoints

### LinkedIn Post Verification

#### List Posts
```
GET /api/iipc/posts/
```
Returns all post verifications for the current user.

#### Create Post
```
POST /api/iipc/posts/
{
  "post_url": "https://linkedin.com/posts/...",
  "post_date": "2025-12-10",
  "character_count": 487,
  "hashtag_count": 5,
  "engagement_score": 145,
  "likes_count": 100,
  "comments_count": 30,
  "shares_count": 15,
  "sentiment": "Positive"
}
```

#### Get Post Details
```
GET /api/iipc/posts/{id}/
```

#### Update Post
```
PUT /api/iipc/posts/{id}/
PATCH /api/iipc/posts/{id}/
```

#### Submit for Review
```
POST /api/iipc/posts/{id}/submit/
```
Submits the post verification for mentor review. Requires:
- Post URL and date
- Minimum engagement score of 50

#### Get Post Statistics
```
GET /api/iipc/posts/stats/
```
Returns:
```json
{
  "total": 5,
  "draft": 1,
  "pending": 2,
  "approved": 2,
  "rejected": 0
}
```

### LinkedIn Connection Verification

#### List Connections
```
GET /api/iipc/connections/
```
Returns all connection verifications with screenshots and verified connections.

#### Create Connection Verification
```
POST /api/iipc/connections/
{
  "verification_method": "screenshot",
  "total_connections": 250,
  "screenshot_urls": [
    "https://drive.google.com/file/d/...",
    "https://drive.google.com/file/d/..."
  ],
  "verified_connections": [
    {
      "name": "John Smith",
      "company": "Google",
      "designation": "Software Engineer",
      "profile_url": "https://linkedin.com/in/john-smith",
      "is_verified": true
    }
  ]
}
```

Or with profile method:
```json
{
  "verification_method": "profile",
  "profile_url": "https://linkedin.com/in/your-profile",
  "total_connections": 250
}
```

#### Get Connection Details
```
GET /api/iipc/connections/{id}/
```

#### Update Connection
```
PUT /api/iipc/connections/{id}/
PATCH /api/iipc/connections/{id}/
```

#### Submit for Review
```
POST /api/iipc/connections/{id}/submit/
```
Submits connection verification for review. Requires:
- For screenshot method: At least one screenshot
- For profile method: Profile URL
- Minimum 100 connections

#### Connect LinkedIn Profile
```
POST /api/iipc/connections/connect_profile/
{
  "profile_url": "https://www.linkedin.com/in/john-doe",
  "total_connections": 250
}
```
Connects and verifies a LinkedIn profile. Creates or updates a connection verification with:
- Profile URL (required)
- Total connections count (required, minimum 100)
- Automatically sets verification_method to 'profile'

Response:
```json
{
  "message": "Profile connected successfully",
  "verification": {
    "id": 1,
    "verification_method": "profile",
    "profile_url": "https://www.linkedin.com/in/john-doe",
    "total_connections": 250,
    "status": "draft"
  },
  "created": true
}
```

#### Get Connection Statistics
```
GET /api/iipc/connections/stats/
```

#### Get All IIPC Statistics
```
GET /api/iipc/connections/all_stats/
```
Returns combined statistics:
```json
{
  "total_posts": 5,
  "total_connections": 3,
  "approved_posts": 2,
  "approved_connections": 1,
  "pending_posts": 2,
  "pending_connections": 1
}
```

## Permissions
- All endpoints require authentication (`IsAuthenticated`)
- Users can only view/edit their own submissions
- Mentors/Admins can review submissions via Django admin

## Validation Rules

### Post Verification
- Post URL is required (valid URL format)
- Post date is required
- Character count ≥ 0
- Hashtag count ≥ 0
- Engagement score ≥ 50 for submission
- Sentiment: Optional (Positive/Negative/Neutral)

### Connection Verification
- Verification method: screenshot or profile
- Total connections ≥ 100 for submission
- Screenshot method requires at least one screenshot URL
- Profile method requires valid LinkedIn profile URL
- Verified connections count is auto-calculated

## Status Flow
```
draft → pending → approved/rejected
```

1. **draft**: User is creating/editing the submission
2. **pending**: Submitted for mentor review
3. **approved**: Mentor approved the submission
4. **rejected**: Mentor rejected with comments

## Admin Interface
- Full CRUD operations for all models
- Inline editing for screenshots and verified connections
- Filtering by status, date, verification method
- Search by user, company, name
- Review workflow with comments

## Usage Example

```python
# Create a post verification
import requests

headers = {'Authorization': 'Bearer <token>'}
data = {
    "post_url": "https://linkedin.com/posts/example",
    "post_date": "2025-12-10",
    "character_count": 500,
    "hashtag_count": 6,
    "engagement_score": 200,
    "sentiment": "Positive"
}
response = requests.post(
    'http://localhost:8000/api/iipc/posts/',
    headers=headers,
    json=data
)

# Submit for review
post_id = response.json()['id']
requests.post(
    f'http://localhost:8000/api/iipc/posts/{post_id}/submit/',
    headers=headers
)
```

## Integration Notes
- Uses Google Drive links for screenshots (no file uploads)
- Engagement metrics can be manually entered or scraped
- Verified connections can be added incrementally
- Supports both screenshot and profile-based verification methods
