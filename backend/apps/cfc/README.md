# CFC (Career, Future & Competency) Backend

## Overview
The CFC module tracks students' career development activities across 4 main areas:
1. **Hackathons** - Participation and achievements
2. **BMC Videos** - Business Model Canvas presentations
3. **Internships** - Multi-stage internship tracking
4. **GenAI Projects** - Generative AI project submissions

## Models

### 1. HackathonSubmission
Tracks hackathon participation with certificates.

**Fields:**
- `hackathon_name` - Name of the hackathon
- `mode` - online/offline/hybrid
- `registration_date` - Registration date
- `participation_date` - Participation date
- `certificate_link` - Google Drive link to certificate
- `status` - draft/submitted/under_review/approved/rejected
- `current_step` - Current step in submission process

### 2. BMCVideoSubmission
Tracks Business Model Canvas video submissions.

**Fields:**
- `video_url` - YouTube or Drive link
- `description` - Optional description
- `status` - draft/submitted/under_review/approved/rejected

### 3. InternshipSubmission
Tracks internship progress through multiple stages.

**Fields:**
- `company` - Company name
- `role` - Internship position
- `mode` - remote/onsite/hybrid
- `duration` - Duration string
- `internship_status` - 1:Application, 2:Interview, 3:Offer, 4:Completion
- `completion_certificate_link` - Google Drive link
- `lor_link` - Letter of Recommendation link
- `status` - draft/submitted/under_review/approved/rejected

### 4. GenAIProjectSubmission
Tracks Generative AI projects.

**Fields:**
- `problem_statement` - Problem description
- `solution_type` - web_app/mobile_app/api/ml_model/chatbot/other
- `innovation_technology` - Technologies used
- `innovation_industry` - Target industry
- `github_repo` - GitHub repository link
- `demo_link` - Optional demo link
- `status` - draft/submitted/under_review/approved/rejected

## API Endpoints

### Hackathons
```
GET    /api/cfc/hackathons/                  - List all hackathons
POST   /api/cfc/hackathons/                  - Create hackathon
GET    /api/cfc/hackathons/{id}/             - Get hackathon details
PUT    /api/cfc/hackathons/{id}/             - Update hackathon
PATCH  /api/cfc/hackathons/{id}/             - Partial update
DELETE /api/cfc/hackathons/{id}/             - Delete hackathon
POST   /api/cfc/hackathons/{id}/submit/      - Submit for review
GET    /api/cfc/hackathons/stats/            - Get statistics
```

### BMC Videos
```
GET    /api/cfc/bmc-videos/                  - List all videos
POST   /api/cfc/bmc-videos/                  - Create video
GET    /api/cfc/bmc-videos/{id}/             - Get video details
PUT    /api/cfc/bmc-videos/{id}/             - Update video
PATCH  /api/cfc/bmc-videos/{id}/             - Partial update
DELETE /api/cfc/bmc-videos/{id}/             - Delete video
POST   /api/cfc/bmc-videos/{id}/submit/      - Submit for review
GET    /api/cfc/bmc-videos/stats/            - Get statistics
```

### Internships
```
GET    /api/cfc/internships/                 - List all internships
POST   /api/cfc/internships/                 - Create internship
GET    /api/cfc/internships/{id}/            - Get internship details
PUT    /api/cfc/internships/{id}/            - Update internship
PATCH  /api/cfc/internships/{id}/            - Partial update
DELETE /api/cfc/internships/{id}/            - Delete internship
POST   /api/cfc/internships/{id}/submit/     - Submit for review
PATCH  /api/cfc/internships/{id}/update_status/ - Update internship stage
GET    /api/cfc/internships/stats/           - Get statistics
```

### GenAI Projects
```
GET    /api/cfc/genai-projects/              - List all projects
POST   /api/cfc/genai-projects/              - Create project
GET    /api/cfc/genai-projects/{id}/         - Get project details
PUT    /api/cfc/genai-projects/{id}/         - Update project
PATCH  /api/cfc/genai-projects/{id}/         - Partial update
DELETE /api/cfc/genai-projects/{id}/         - Delete project
POST   /api/cfc/genai-projects/{id}/submit/  - Submit for review
GET    /api/cfc/genai-projects/stats/        - Get statistics
```

## Example API Calls

### Create Hackathon Submission
```bash
curl -X POST http://localhost:8000/api/cfc/hackathons/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "hackathon_name": "Smart India Hackathon 2025",
    "mode": "hybrid",
    "registration_date": "2025-01-15",
    "participation_date": "2025-02-20",
    "certificate_link": "https://drive.google.com/...",
    "current_step": 1
  }'
```

### Create Internship
```bash
curl -X POST http://localhost:8000/api/cfc/internships/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Google",
    "role": "Software Engineering Intern",
    "mode": "remote",
    "duration": "3 months (Summer 2025)",
    "internship_status": 1
  }'
```

### Update Internship Status
```bash
curl -X PATCH http://localhost:8000/api/cfc/internships/1/update_status/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"internship_status": 2}'
```

### Submit GenAI Project
```bash
curl -X POST http://localhost:8000/api/cfc/genai-projects/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "problem_statement": "Healthcare appointment scheduling",
    "solution_type": "chatbot",
    "innovation_technology": "GPT-4, LangChain, FastAPI",
    "innovation_industry": "healthcare",
    "github_repo": "https://github.com/user/health-bot",
    "demo_link": "https://healthbot.demo.com",
    "current_step": 1
  }'
```

## Features

### Hackathons
- Track multiple hackathon participations
- Upload certificate as Google Drive link
- Multi-step submission process
- Status tracking (draft → submitted → approved/rejected)

### BMC Videos
- Store YouTube or Google Drive video links
- Optional description field
- Simple submission and review workflow

### Internships
- 4-stage progress tracking (Application → Interview → Offer → Completion)
- Separate status for submission review
- Completion certificate and LOR links
- Can only submit for review when completed (stage 4)

### GenAI Projects
- Comprehensive project information capture
- GitHub repository requirement
- Optional demo link
- Industry and technology categorization
- Multi-step submission process

## Validation Rules

### Hackathons
- Certificate link required before submission
- All dates and basic info must be complete

### BMC Videos
- Video URL required before submission

### Internships
- Must be in Completion stage (4) before submitting for review
- Completion certificate link required for submission
- LOR link is optional

### GenAI Projects
- GitHub repo link required
- Problem statement and innovation technology required
- All fields validated before submission

## Admin Interface

All models are registered in Django admin with:
- List views with filtering and search
- Detailed fieldsets for easy review
- Readonly timestamp fields
- Review fields for mentors/admins

Access admin at: `http://localhost:8000/admin/cfc/`

## Statistics Endpoints

Each module provides a `/stats/` endpoint that returns:
- Total count
- Status breakdown (draft, submitted, approved, rejected)
- Module-specific metrics (e.g., internship stages)

## Authentication

All endpoints require JWT authentication:
```
Authorization: Bearer <access_token>
```

Users can only access their own submissions.
