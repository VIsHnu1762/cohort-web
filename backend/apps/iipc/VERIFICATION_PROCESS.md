# IIPC Verification Process - Complete Guide

## Overview
The IIPC (Industry Institute Partnership Cell) module allows students to verify their LinkedIn activity through two main processes:
1. **Post Verification** - Verify LinkedIn post engagement
2. **Connection Verification** - Verify LinkedIn professional connections

Both processes use **Google Drive links** for screenshot evidence and follow a **draft → pending → approved/rejected** workflow.

---

## 1. LinkedIn Post Verification

### Student Workflow:

#### Step 1: Fill Post Details
Students provide the following information:

**Required Fields:**
- LinkedIn Post URL (e.g., `https://www.linkedin.com/posts/username_activity-123456789`)
- Post Date (date picker)
- Engagement Score (minimum 50 required)

**Optional Fields:**
- Character Count
- Hashtag Count
- Likes Count
- Comments Count
- Shares Count
- Sentiment Analysis (Positive/Negative/Neutral)

#### Step 2: Create Verification
- Click "Create Verification" button
- System creates a draft verification in database
- Status: `draft`

#### Step 3: Submit for Review
- Click "Submit for Review" button
- System validates:
  - ✅ Post URL is provided
  - ✅ Post date is provided
  - ✅ Engagement score >= 50
- Status changes to: `pending`
- Notification sent to mentor/admin

### Backend API Calls:

```javascript
// Create post verification
POST /api/iipc/posts/
{
  "post_url": "https://www.linkedin.com/posts/...",
  "post_date": "2025-12-10",
  "character_count": 487,
  "hashtag_count": 5,
  "engagement_score": 150,
  "likes_count": 100,
  "comments_count": 35,
  "shares_count": 15,
  "sentiment": "Positive"
}

// Submit for review
POST /api/iipc/posts/{id}/submit/
```

---

## 2. LinkedIn Connection Verification

### Student Workflow:

#### Step 1: Choose Verification Method

**Option A: Screenshot Method (Recommended for now)**
- Upload Google Drive links to connection screenshots
- Multiple screenshots can be added

**Option B: LinkedIn OAuth (Coming Soon)**
- Sign in with LinkedIn
- Auto-verify profile
- Requires college management approval for API access

#### Step 2: Provide Screenshot Links

**Google Drive Link Format:**
```
https://drive.google.com/file/d/1234567890abcdef/view
```

**Steps to get Google Drive link:**
1. Take screenshots of LinkedIn connections page
2. Upload screenshots to Google Drive
3. Right-click file → Get link
4. Set sharing to "Anyone with the link can view"
5. Copy the link
6. Paste in the portal

**Multiple Screenshots:**
- Click "+ Add Another Link" to add more
- Minimum: 1 screenshot
- Recommended: 2-3 screenshots showing different connections

#### Step 3: Enter Connection Count
- Total LinkedIn Connections (minimum 100 required)
- Must match the count shown in screenshots

#### Step 4: Create Verification
- Click "Create Verification" button
- System creates verification with screenshot links
- Status: `draft`

#### Step 5: Submit for Review
- Click "Submit for Review" button
- System validates:
  - ✅ At least one screenshot link provided
  - ✅ Total connections >= 100
- Status changes to: `pending`

### Backend API Calls:

```javascript
// Create connection verification
POST /api/iipc/connections/
{
  "verification_method": "screenshot",
  "total_connections": 250,
  "screenshot_urls": [
    "https://drive.google.com/file/d/1234567890abcdef/view",
    "https://drive.google.com/file/d/abcdef1234567890/view"
  ],
  "verified_connections": []
}

// Submit for review
POST /api/iipc/connections/{id}/submit/
```

---

## 3. Mentor/Admin Review Process

### Admin Dashboard (Django Admin)

Mentors/admins can access the review interface at:
```
http://localhost:8000/admin/iipc/
```

#### Post Verification Review:
1. Navigate to "LinkedIn Post Verifications"
2. Filter by status: `pending`
3. Click on submission to review
4. Verify:
   - Post URL is valid
   - Engagement metrics are reasonable
   - Post date is recent
5. Actions:
   - **Approve**: Set status to `approved`
   - **Reject**: Set status to `rejected` with comments

#### Connection Verification Review:
1. Navigate to "LinkedIn Connection Verifications"
2. Filter by status: `pending`
3. Click on submission to review
4. Open Google Drive screenshot links
5. Verify:
   - Screenshots show actual LinkedIn connections page
   - Connection count matches student's claim
   - Screenshots are not edited/fake
6. Actions:
   - **Approve**: Set status to `approved`
   - **Reject**: Set status to `rejected` with comments

---

## 4. Status Workflow

```
┌──────┐     Create          ┌─────────┐
│      │  Verification       │         │
│ User ├───────────────────► │  DRAFT  │
│      │                     │         │
└──────┘                     └────┬────┘
                                  │
                                  │ Submit for Review
                                  │ (validates requirements)
                                  ▼
                            ┌─────────┐
                            │         │
                            │ PENDING │◄────┐
                            │         │     │
                            └────┬────┘     │
                                 │          │
                   ┌─────────────┴──────────┴──────┐
                   │                                │
                   │ Mentor Review                  │
                   │                                │
           ┌───────▼────────┐              ┌───────▼────────┐
           │                │              │                │
           │   APPROVED     │              │   REJECTED     │
           │                │              │  (with comments) │
           └────────────────┘              └────────────────┘
```

---

## 5. Frontend Components

### IIPC.jsx - Main Component
- Two tabs: Post Verification and Connection Verification
- Real-time validation and error handling
- Success/error message display
- Integration with backend APIs

### Key States:
```javascript
// Post Verification
const [postUrl, setPostUrl] = useState('');
const [postDate, setPostDate] = useState('');
const [engagementScore, setEngagementScore] = useState('');
const [postData, setPostData] = useState(null);
const [postError, setPostError] = useState('');
const [postSuccess, setPostSuccess] = useState('');

// Connection Verification
const [screenshotLinks, setScreenshotLinks] = useState(['']);
const [totalConnections, setTotalConnections] = useState('');
const [connectionsData, setConnectionsData] = useState(null);
const [profileError, setProfileError] = useState('');
const [profileSuccess, setProfileSuccess] = useState('');
```

---

## 6. Validation Rules

### Post Verification:
- ✅ Post URL required (must contain linkedin.com)
- ✅ Post date required
- ✅ Engagement score >= 50 (for submission)
- ✅ Character count >= 0 (if provided)
- ✅ Hashtag count >= 0 (if provided)

### Connection Verification:
- ✅ At least 1 Google Drive link required
- ✅ Total connections >= 100 (for submission)
- ✅ Valid URL format for Google Drive links
- ✅ Verification method must be 'screenshot' or 'profile'

---

## 7. Error Handling

### Frontend Errors:
- Empty required fields → Show error message
- Invalid engagement score → "Minimum 50 required"
- Invalid connection count → "Minimum 100 required"
- Missing screenshots → "Please provide at least one screenshot link"

### Backend Errors:
- 400 Bad Request → Validation error (show error message)
- 401 Unauthorized → User not logged in (redirect to login)
- 500 Internal Server Error → Show generic error message

---

## 8. Google Drive Setup Guide for Students

### How to Share Screenshots via Google Drive:

1. **Take Screenshots:**
   - Open LinkedIn connections page
   - Press `Print Screen` or use Snipping Tool
   - Capture multiple views if you have many connections

2. **Upload to Google Drive:**
   - Go to https://drive.google.com
   - Click "New" → "File upload"
   - Select your screenshot files
   - Wait for upload to complete

3. **Get Shareable Link:**
   - Right-click on uploaded file
   - Click "Get link"
   - Change permission to "Anyone with the link"
   - Set to "Viewer" (not Editor)
   - Click "Copy link"

4. **Paste in Portal:**
   - Paste the link in the screenshot link field
   - Link format: `https://drive.google.com/file/d/[FILE_ID]/view`

5. **Verify Link Works:**
   - Open link in incognito/private browser window
   - Ensure screenshot is visible
   - Link should work without requiring login

---

## 9. Testing the Flow

### Manual Testing Steps:

**Post Verification:**
1. Go to http://localhost:5173/student/iipc
2. Click "Post Verification" tab
3. Fill in post URL: `https://www.linkedin.com/posts/test_activity-123`
4. Select post date: Today's date
5. Enter engagement score: 100
6. Fill optional fields
7. Click "Create Verification" → Should see success message
8. Click "Submit for Review" → Status should change to pending

**Connection Verification:**
1. Click "Connections Verification" tab
2. Click "Screenshot Links" method
3. Add Google Drive link: `https://drive.google.com/file/d/test123/view`
4. Add another link (optional)
5. Enter total connections: 150
6. Click "Create Verification" → Should see success message
7. Click "Submit for Review" → Status should change to pending

---

## 10. Database Schema

### LinkedInPostVerification Table:
```
- id (PK)
- user (FK to User)
- post_url (URLField)
- post_date (DateField)
- character_count (Integer)
- hashtag_count (Integer)
- engagement_score (Integer)
- likes_count (Integer)
- comments_count (Integer)
- shares_count (Integer)
- sentiment (CharField: Positive/Negative/Neutral)
- status (CharField: draft/pending/approved/rejected)
- submitted_at (DateTimeField)
- reviewed_at (DateTimeField)
- reviewer (FK to User)
- reviewer_comments (TextField)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

### LinkedInConnectionVerification Table:
```
- id (PK)
- user (FK to User)
- verification_method (CharField: screenshot/profile)
- profile_url (URLField)
- total_connections (Integer)
- verified_connections_count (Integer)
- status (CharField: draft/pending/approved/rejected)
- submitted_at (DateTimeField)
- reviewed_at (DateTimeField)
- reviewer (FK to User)
- reviewer_comments (TextField)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

### ConnectionScreenshot Table:
```
- id (PK)
- verification (FK to LinkedInConnectionVerification)
- screenshot_url (URLField - Google Drive link)
- uploaded_at (DateTimeField)
```

---

## Summary

The IIPC verification system is now fully functional with:
- ✅ Complete post verification form
- ✅ Connection verification with Google Drive links
- ✅ Two-step process: Create → Submit
- ✅ Real-time validation
- ✅ Error/success feedback
- ✅ Backend API integration
- ✅ Admin review workflow
- ⏳ LinkedIn OAuth (pending college approval)

Students can now submit their LinkedIn activity for verification, and mentors can review and approve submissions through the admin interface.
