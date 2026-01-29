# Mentor-Student Chat System

## Overview
A messaging system that enables mentors to communicate with their assigned students. Messages appear as notifications in the student's home page.

## Features

### For Mentors
- **Send Messages**: Mentors can send messages to students from the Student List page
- **Message Types**:
  - **General**: Regular messages for communication
  - **Completion**: Notify students when their tasks are completed
  - **Pending Review**: Remind students about pending items to review
- **Chat Interface**: Clean modal interface with message type selection

### For Students
- **Notifications**: Messages appear in the notifications section of the home page
- **Real-time Updates**: Notifications refresh every 30 seconds
- **Message Types**: Different icons and styling based on message type
- **Mark as Read**: Messages can be marked as read (future enhancement)

## Implementation

### Frontend

#### Files Modified
1. **src/pages/mentor/MentorDashboard.jsx**
   - Added chat button next to student name
   - Implemented chat modal with message type selection
   - Integrated with messageService API

2. **src/pages/mentor/MentorDashboard.css**
   - Styled chat button with golden gradient
   - Designed responsive chat modal
   - Added hover effects and transitions

3. **src/pages/student/Home.jsx**
   - Integrated message fetching from API
   - Display messages in notifications panel
   - Auto-refresh every 30 seconds
   - Fallback to mock data if API unavailable

4. **src/pages/student/Home.css**
   - Added notification icon styling
   - Different styles for read/unread messages

5. **src/services/messageService.js** (NEW)
   - API service for message operations
   - Methods:
     - `sendMessage(recipientId, content, messageType)`
     - `getMessages()`
     - `getUnreadMessages()`
     - `markAsRead(messageId)`
     - `markAllAsRead()`

### Backend

#### Files Modified
1. **backend_mentor/apps/communication/models.py**
   - `Message` model with fields:
     - sender (ForeignKey to User with role='mentor')
     - recipient (ForeignKey to User with role='student')
     - message_type (general/completion/pending)
     - content (TextField)
     - is_read (BooleanField)
     - created_at, read_at timestamps

2. **backend_mentor/apps/communication/views.py**
   - `MessageViewSet` with actions:
     - `list`: Get all messages (filtered by user role)
     - `create`: Send new message
     - `unread`: Get unread messages for students
     - `mark_read`: Mark single message as read
     - `mark_all_read`: Mark all messages as read

3. **backend_mentor/apps/communication/urls.py**
   - Registered MessageViewSet with router
   - Endpoint: `/api/communication/messages/`

4. **backend_mentor/apps/communication/admin.py**
   - Admin interface for Message model
   - Filters by message type, read status, date

#### Database Migrations
```bash
cd backend_mentor
python manage.py makemigrations communication
python manage.py migrate
```

## API Endpoints

### Base URL
```
http://127.0.0.1:8000/api/communication/
```

### Endpoints

#### 1. List Messages
```
GET /messages/
```
Returns messages based on user role:
- Mentors: Messages they sent
- Students: Messages they received

#### 2. Send Message
```
POST /messages/
```
**Body:**
```json
{
  "recipient": 1,
  "content": "Great work on your CLT submission!",
  "message_type": "completion"
}
```

#### 3. Get Unread Messages (Students only)
```
GET /messages/unread/
```

#### 4. Mark Message as Read
```
POST /messages/{id}/mark_read/
```

#### 5. Mark All Messages as Read
```
POST /messages/mark_all_read/
```

## Usage

### Mentor Flow
1. Navigate to `/mentor-dashboard/students`
2. Select a student from the list
3. Click the "Message" button next to student name
4. Select message type (General/Completion/Pending Review)
5. Type message and click "Send"
6. Message is sent to student and appears in their notifications

### Student Flow
1. Login and view home page
2. Check "Notifications" section in right column
3. See messages from mentor with icon indicators
4. Messages refresh automatically every 30 seconds
5. Unread messages are highlighted

## Message Types

### General
- Purpose: Regular communication
- Icon: MessageCircle
- Color: Standard theme colors
- Use Case: Questions, feedback, general updates

### Completion
- Purpose: Notify task completion
- Icon: CheckCircle (suggested)
- Color: Green accent
- Use Case: "Your assignment has been graded", "Project approved"

### Pending Review
- Purpose: Remind about pending items
- Icon: Clock (suggested)
- Color: Orange/Yellow accent
- Use Case: "Please review the feedback", "Update required"

## Database Setup

### Required Tables
- `communication_message` - Stores all messages

### Sample Data
```python
# Create test message (Django shell)
from django.contrib.auth import get_user_model
from apps.communication.models import Message

User = get_user_model()
mentor = User.objects.get(email='mentor@test.com')
student = User.objects.get(email='student@test.com')

Message.objects.create(
    sender=mentor,
    recipient=student,
    message_type='completion',
    content='Great work on your CLT submission!'
)
```

## Future Enhancements

1. **Real-time Notifications**
   - Implement WebSocket for instant message delivery
   - Push notifications

2. **Message History**
   - View all past messages
   - Search and filter messages

3. **Rich Text Support**
   - Markdown formatting
   - Attachments and links

4. **Two-way Communication**
   - Allow students to reply to mentors
   - Chat threads

5. **Read Receipts**
   - Show when message was read
   - Delivery confirmation

6. **Bulk Messaging**
   - Send messages to multiple students
   - Broadcast announcements

## Troubleshooting

### Messages not appearing
1. Check if backend server is running on `http://127.0.0.1:8000`
2. Verify migrations are applied: `python manage.py migrate`
3. Check browser console for API errors
4. Verify auth token is valid in localStorage

### API Errors
1. Ensure communication app is in INSTALLED_APPS
2. Check CORS settings allow frontend origin
3. Verify database connection in backend
4. Check authentication middleware

### Frontend Issues
1. Clear browser cache
2. Check messageService.js has correct API_BASE_URL
3. Verify axios is installed: `npm list axios`
4. Check React components are imported correctly

## Testing

### Manual Testing
1. Login as mentor (mentor@test.com/mentor123)
2. Go to Student List
3. Select a student
4. Send a test message
5. Logout and login as student (student@test.com/student123)
6. Check home page notifications

### API Testing (curl)
```bash
# Get token
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"mentor@test.com","password":"mentor123"}'

# Send message
curl -X POST http://127.0.0.1:8000/api/communication/messages/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"recipient":1,"content":"Test message","message_type":"general"}'
```

## Security Considerations

1. **Authorization**: Only mentors can send messages
2. **Access Control**: Users can only see their own messages
3. **Input Validation**: Message content is sanitized
4. **Authentication**: JWT tokens required for all endpoints
5. **Rate Limiting**: Consider implementing to prevent spam

## Performance

- **Database Indexing**: Created indexes on recipient+created_at and sender+created_at
- **Polling Interval**: 30 seconds (configurable)
- **Query Optimization**: Only fetch unread messages for students
- **Pagination**: Can be added for message lists (future)

## Notes

- Backend database migrations created but may need to be applied depending on your database setup
- Frontend gracefully falls back to mock data if API is unavailable
- Message polling can be adjusted in Home.jsx (currently 30 seconds)
- Consider implementing WebSocket for production use instead of polling
