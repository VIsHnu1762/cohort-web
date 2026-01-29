# Hackathon Registration & Reminder Feature

## Overview
Added a two-step hackathon management system where students first register for hackathons they plan to participate in, then submit participation details later. Includes motivational reminders on the home page.

## Backend Changes

### 1. New Model: `HackathonRegistration`
**Location:** `backend/apps/cfc/models.py`

**Fields:**
- `hackathon_name` - Name of the hackathon
- `mode` - Online/Offline/Hybrid
- `registration_date` - When student registered
- `participation_date` - Scheduled date
- `hackathon_url` - Optional website link
- `notes` - Personal preparation notes
- `is_completed` - Tracks if participated
- `submission` - Links to actual submission later

**Properties:**
- `days_until_event` - Calculates countdown
- `is_upcoming` - Checks if still upcoming

### 2. API Endpoints
**Location:** `backend/apps/cfc/views.py`, `backend/apps/cfc/urls.py`

**Base URL:** `/api/cfc/hackathon-registrations/`

**Endpoints:**
- `GET /` - List all registered hackathons
- `POST /` - Register new hackathon
- `GET /upcoming/` - Get only upcoming hackathons
- `POST /{id}/mark_completed/` - Mark as participated
- `POST /{id}/create_submission/` - Create submission from registration
- `PUT /{id}/` - Update registration
- `DELETE /{id}/` - Delete registration

### 3. Serializers
**Location:** `backend/apps/cfc/serializers.py`

- `HackathonRegistrationSerializer` - Full data with computed fields
- `HackathonRegistrationCreateSerializer` - For creating/updating

### 4. Service Functions
**Location:** `src/services/cfc.js`

Added functions:
```javascript
getHackathonRegistrations()
getUpcomingHackathons()
createHackathonRegistration(data)
updateHackathonRegistration(id, data)
deleteHackathonRegistration(id)
markRegistrationCompleted(id)
createSubmissionFromRegistration(id)
```

## Frontend Components

### 1. Registration Modal
**Component:** `src/components/HackathonRegistrationModal.jsx`
**Styles:** `src/components/HackathonRegistrationModal.css`

**Features:**
- Clean modal interface
- Form with hackathon details
- Date pickers for registration & participation
- Optional URL and notes fields
- Mode selection (Online/Offline/Hybrid)

### 2. Upcoming Hackathons Widget
**Component:** `src/components/UpcomingHackathonsWidget.jsx`
**Styles:** `src/components/UpcomingHackathonsWidget.css`

**Features:**
- Shows top 3 upcoming hackathons
- Dynamic countdown timers
- Color-coded urgency levels:
  - 🔴 Red (Urgent): Today or tomorrow
  - 🟠 Orange (Soon): 2-3 days
  - 🔵 Blue (Upcoming): 4-7 days
  - 🟢 Green (Planned): 7+ days

**Motivational Messages:**
- "It's TODAY! Give it your best shot! 🚀"
- "Tomorrow's the day! Get ready! 🔥"
- "Just a few days left! Time to shine! ✨"
- "One week to go! Keep preparing! 💪"
- "Start preparing now! You got this! 🎯"

**UI Elements:**
- Hackathon name and mode badge
- Participation date
- Countdown with icon
- Motivational message
- Personal notes (if added)
- Link to hackathon website
- "View all" link if more than 3

## Integration Steps

### Step 1: Update CFC Page
Add registration button and modal to `src/pages/student/CFC.jsx`:

```jsx
import HackathonRegistrationModal from '../../components/HackathonRegistrationModal';

// Add state
const [showRegistrationModal, setShowRegistrationModal] = useState(false);

// Add handler
const handleRegisterHackathon = async (formData) => {
  try {
    await cfcService.createHackathonRegistration(formData);
    setSuccess('Hackathon registered successfully! Check your home page for reminders.');
    setShowRegistrationModal(false);
  } catch (error) {
    setError('Failed to register hackathon');
  }
};

// Add button in hackathon tab header
<Button variant="secondary" onClick={() => setShowRegistrationModal(true)}>
  Register Hackathon
</Button>

// Add modal before closing div
<HackathonRegistrationModal
  isOpen={showRegistrationModal}
  onClose={() => setShowRegistrationModal(false)}
  onRegister={handleRegisterHackathon}
/>
```

### Step 2: Update Home Page
Add widget to `src/pages/student/Home.jsx`:

```jsx
import UpcomingHackathonsWidget from '../../components/UpcomingHackathonsWidget';

// Add widget in the dashboard (after welcome section or stats cards)
<UpcomingHackathonsWidget />
```

## Database Migration

**Applied:** `backend/apps/cfc/migrations/0004_hackathonregistration.py`

```bash
cd backend
python manage.py makemigrations cfc
python manage.py migrate cfc
```

## User Flow

1. **Register:** Student clicks "Register Hackathon" button in CFC page
2. **Fill Details:** Modal opens with form for hackathon details
3. **Save:** Registration saved to database
4. **Home Reminder:** Widget appears on home page with countdown
5. **Motivation:** Daily motivational messages based on days left
6. **Participate:** After event, create actual submission with GitHub repo/certificate

## Benefits

✅ **Proactive Planning:** Students register hackathons in advance
✅ **Daily Reminders:** Automated countdown on home page
✅ **Motivation:** Encouraging messages keep students engaged
✅ **Progress Tracking:** Clear visibility of upcoming events
✅ **No Missed Deadlines:** Color-coded urgency system
✅ **Preparation Notes:** Students can track their goals
✅ **Seamless Transition:** Easy to create submission after participation

## Testing

1. Navigate to CFC page
2. Click "Register Hackathon"
3. Fill form with future participation date
4. Save registration
5. Go to Home page
6. See widget with countdown and motivational message
7. Wait for date to approach and see message change

## Branch
Current branch: `sriram_backend`
Ready to commit and push!
