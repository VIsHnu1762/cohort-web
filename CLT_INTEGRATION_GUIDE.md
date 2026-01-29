# CLT Backend-Frontend Integration Guide

## ✅ What's Been Completed

### Backend (Port 8000)
- ✅ CLT models with optimized database indexes
- ✅ CLT API endpoints with JWT authentication
- ✅ File upload with validation (10MB max, 10 files max)
- ✅ Submission workflow (draft → submitted → under_review → approved/rejected)
- ✅ Statistics endpoint with caching
- ✅ CORS configured for localhost:5173
- ✅ Optimized for 1000-2000 concurrent users

### Frontend (Port 5173)
- ✅ Axios installed and configured
- ✅ API service layer (api.js, clt.js, auth.js)
- ✅ JWT token management with auto-refresh
- ✅ AuthContext updated with backend integration
- ✅ CLT.jsx connected to backend API
- ✅ File upload with client-side validation
- ✅ Error handling and progress tracking
- ✅ Vite proxy configured

## 🧪 Testing the Integration

### 1. Start Backend Server
```bash
cd C:\Python310\cohort_webapp\Cohort_Web_App\backend
python manage.py runserver 8000
```

### 2. Start Frontend Development Server
```bash
cd C:\Python310\cohort_webapp\Cohort_Web_App
npm run dev
```
Frontend will be available at: http://localhost:5173

### 3. Test Credentials
- **Username:** testuser
- **Password:** testpass123

### 4. Test Flow
1. Open http://localhost:5173
2. Login with test credentials
3. Navigate to CLT page
4. Fill in course details:
   - Title: "Advanced React Course"
   - Description: "Completed React hooks and performance optimization"
   - Platform: "Udemy"
   - Completion Date: Select a date
5. Upload certificate/evidence files (PDF or images, max 10MB each)
6. Review and submit
7. Check that submission appears with status "submitted"

## 🔍 API Endpoints Available

### Authentication
- `POST /api/auth/token/` - Get JWT tokens
- `POST /api/auth/token/refresh/` - Refresh access token

### CLT Submissions
- `GET /api/clt/submissions/` - List all submissions (paginated)
- `POST /api/clt/submissions/` - Create new submission
- `GET /api/clt/submissions/{id}/` - Get submission details
- `PATCH /api/clt/submissions/{id}/` - Update submission
- `DELETE /api/clt/submissions/{id}/` - Delete submission (draft/rejected only)
- `POST /api/clt/submissions/{id}/upload_files/` - Upload files
- `POST /api/clt/submissions/{id}/submit/` - Submit for review
- `DELETE /api/clt/submissions/{id}/delete_file/?file_id={id}` - Delete file
- `GET /api/clt/submissions/stats/` - Get statistics (cached 5 min)

## 🛠️ Troubleshooting

### CORS Errors
- Ensure backend is running on port 8000
- Check CORS_ALLOWED_ORIGINS in backend/config/settings.py includes http://localhost:5173

### Authentication Errors
- Check that JWT tokens are being stored in localStorage
- Verify token is being sent in Authorization header
- Test login at: http://localhost:8000/admin (admin panel should work)

### File Upload Errors
- Maximum file size: 10MB per file
- Maximum files per request: 10 files
- Allowed types: PDF, images (PNG, JPG, JPEG)

### Network Errors
- Verify both servers are running
- Check browser console for detailed error messages
- Test API directly: http://localhost:8000/api/docs/ (Swagger UI)

## 📊 Performance Optimizations

### Backend
- Database indexes on user, status, created_at, submitted_at
- Query optimization with select_related and prefetch_related
- Caching for statistics (5 min TTL)
- Atomic transactions for data integrity
- File size validation
- Pagination on list endpoints

### Frontend
- Axios interceptors for token refresh
- Client-side file validation
- Progress tracking for uploads
- Error boundaries and handling

## 🎯 Next Steps

1. **Test the full flow** with the frontend UI
2. **Build SRI backend** (Social Responsibility Initiative)
3. **Build CFC backend** (Career, Future & Competency)
4. **Build IIPC backend** (Industry Interaction)
5. **Build SCD backend** (Skill & Career Development)
6. **Connect all modules** to frontend after backends are complete

## 📝 Notes

- Backend uses SQLite for development (will use PostgreSQL in production)
- All endpoints require JWT authentication except login
- Files are stored in backend/media/clt_files/
- Submissions are user-specific (users can only see their own)
- All write operations use atomic transactions
