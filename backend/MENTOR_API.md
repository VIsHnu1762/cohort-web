# Mentor API Documentation

## Overview
The Mentor APIs provide endpoints for mentors to review student submissions across all pillars (CFC, CLT, SRI, IIPC, SCD).

**Base URL:** `/api/mentor/`

**Authentication:** All endpoints require JWT authentication with mentor privileges.

---

## Endpoints

### 1. Get Pillar Submissions
Get all submissions for a specific pillar with filtering and search capabilities.

**Endpoint:** `GET /api/mentor/pillar/<pillar>/submissions/`

**Pillars:** `cfc`, `clt`, `sri`, `iipc`, `scd`, `all`

**Query Parameters:**
- `status` (optional): Filter by status
  - `all` - All submissions (default)
  - `pending` - Submitted but not reviewed
  - `approved` - Approved submissions
  - `rejected` - Rejected submissions
- `search` (optional): Search by student name, title, or description
- `year` (optional): Filter by student year (e.g., "2nd Year", "3rd Year")
- `sort` (optional): Sort order
  - `latest` - Latest first (default)
  - `oldest` - Oldest first

**Example Request:**
```javascript
fetch('/api/mentor/pillar/cfc/submissions/?status=pending&sort=latest', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
})
```

**Response:**
```json
{
  "submissions": [
    {
      "id": 1,
      "student": {
        "name": "John Doe",
        "avatar": "J",
        "email": "john@example.com",
        "username": "johndoe"
      },
      "title": "Hackathon ABC 2024",
      "description": "Online hackathon participation",
      "submittedDate": "2024-12-10",
      "status": "pending",
      "pillar": "cfc",
      "evidenceLinks": {
        "images": 0,
        "links": 2
      },
      "reviewerComments": "",
      "reviewedAt": null
    }
  ],
  "total": 1
}
```

---

### 2. Get Pillar Statistics
Get submission statistics for a specific pillar.

**Endpoint:** `GET /api/mentor/pillar/<pillar>/stats/`

**Pillars:** `cfc`, `clt`, `sri`, `iipc`, `scd`, `all`

**Example Request:**
```javascript
fetch('/api/mentor/pillar/all/stats/', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
})
```

**Response:**
```json
{
  "total": 156,
  "pending": 23,
  "approved": 118,
  "rejected": 15
}
```

---

### 3. Review Submission (Approve/Reject)
Approve or reject a student submission.

**Endpoint:** `POST /api/mentor/review/`

**Request Body:**
```json
{
  "pillar": "cfc",
  "submission_id": 1,
  "submission_type": "hackathon",
  "action": "approve",
  "comment": "Great work! Well documented."
}
```

**Submission Types:**
- CFC: `hackathon`, `bmc`, `internship`, `genai`
- CLT: `clt`
- SRI: `sri`
- IIPC: `iipc`
- SCD: `scd`

**Actions:**
- `approve` - Approve the submission
- `reject` - Reject the submission (requires comment)

**Example Request:**
```javascript
fetch('/api/mentor/review/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    pillar: 'cfc',
    submission_id: 1,
    submission_type: 'hackathon',
    action: 'approve',
    comment: 'Excellent work!'
  })
})
```

**Response:**
```json
{
  "message": "Submission approved successfully",
  "submission_id": 1,
  "status": "approved"
}
```

---

### 4. Get Submission Detail
Get detailed information about a specific submission.

**Endpoint:** `GET /api/mentor/submission/<pillar>/<submission_type>/<submission_id>/`

**Example Request:**
```javascript
fetch('/api/mentor/submission/cfc/hackathon/1/', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
})
```

**Response:**
Returns full submission details using the respective serializer for that submission type.

---

## Frontend Integration

### Example: Fetch submissions for Pillar Review page

```javascript
// In PillarReview.jsx

const fetchSubmissions = async (pillar, filters) => {
  const params = new URLSearchParams({
    status: filters.statusFilter || 'all',
    search: filters.searchQuery || '',
    year: filters.yearFilter || 'all',
    sort: filters.sortOrder || 'latest'
  });
  
  try {
    const response = await fetch(
      `http://localhost:8000/api/mentor/pillar/${pillar}/submissions/?${params}`,
      {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      }
    );
    
    const data = await response.json();
    setSubmissions(data.submissions);
  } catch (error) {
    console.error('Error fetching submissions:', error);
  }
};

const fetchStats = async (pillar) => {
  try {
    const response = await fetch(
      `http://localhost:8000/api/mentor/pillar/${pillar}/stats/`,
      {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      }
    );
    
    const data = await response.json();
    setStats(data);
  } catch (error) {
    console.error('Error fetching stats:', error);
  }
};

const handleReview = async (submissionId, submissionType, action, comment) => {
  try {
    const response = await fetch('http://localhost:8000/api/mentor/review/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        pillar: activePillar,
        submission_id: submissionId,
        submission_type: submissionType,
        action: action,
        comment: comment
      })
    });
    
    const data = await response.json();
    console.log('Review submitted:', data);
    
    // Refresh submissions
    fetchSubmissions(activePillar, filters);
  } catch (error) {
    console.error('Error submitting review:', error);
  }
};
```

---

## Permission Requirements

**Mentor Access:**
Users must have one of the following:
- `is_staff = True` (Django staff member)
- `is_superuser = True` (Django superuser)
- Custom `is_mentor` attribute (if implemented)

**Adding Mentor Role to User:**
```python
# In Django shell or admin
user = User.objects.get(username='mentor_username')
user.is_staff = True  # Grant mentor access
user.save()
```

---

## Error Responses

**403 Forbidden:**
```json
{
  "error": "You don't have permission to access this resource"
}
```

**404 Not Found:**
```json
{
  "error": "Submission not found"
}
```

**400 Bad Request:**
```json
{
  "error": "Missing required fields"
}
```

---

## Testing

You can test the APIs using the provided test scripts or curl commands:

```bash
# Get all submissions for CFC pillar
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/mentor/pillar/cfc/submissions/

# Get statistics for all pillars
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/mentor/pillar/all/stats/

# Approve a submission
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"pillar":"cfc","submission_id":1,"submission_type":"hackathon","action":"approve","comment":"Great!"}' \
  http://localhost:8000/api/mentor/review/
```

---

## Next Steps

1. **Delete `backend_mentor` and `backend_admin` folders** - They're not needed!
2. **Test the APIs** using the Django server you already have
3. **Update frontend** to call these endpoints
4. **(Optional) Add custom mentor role** to User model if you want finer control

All mentor functionality is now in your existing backend at `/api/mentor/` 🎉
