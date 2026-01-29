# LinkedIn OAuth Integration - Setup Guide

## Overview
This guide will help you set up LinkedIn OAuth authentication for the IIPC module.

## Prerequisites
- LinkedIn account
- Deployed application or localhost for testing

---

## Step 1: Create LinkedIn Developer App

### 1.1 Go to LinkedIn Developers
Visit: https://www.linkedin.com/developers/

### 1.2 Create a New App
1. Click "Create app"
2. Fill in the required information:
   - **App name**: Cohort Web App
   - **LinkedIn Page**: Your company/organization page (required)
   - **App logo**: Upload your app logo
   - **Legal agreement**: Check the box

### 1.3 Verify Your App
1. LinkedIn will send a verification URL to your company page
2. Visit the verification URL and complete the process

---

## Step 2: Configure OAuth Settings

### 2.1 Add Products
1. In your app dashboard, go to the "Products" tab
2. Request access to **"Sign In with LinkedIn using OpenID Connect"**
3. Wait for approval (usually instant for OpenID Connect)

### 2.2 Configure Redirect URLs
1. Go to the "Auth" tab
2. Under "OAuth 2.0 settings", click "Edit"
3. Add your redirect URLs:
   ```
   Development:
   http://localhost:5173/iipc/linkedin/callback
   
   Production:
   https://yourdomain.com/iipc/linkedin/callback
   ```
4. Click "Update"

### 2.3 Get Your Credentials
1. In the "Auth" tab, you'll find:
   - **Client ID**: Copy this
   - **Client Secret**: Click "Show" and copy this

---

## Step 3: Update Backend Configuration

### 3.1 Update .env File
Open `backend/.env` and update the LinkedIn credentials:

```env
# LinkedIn OAuth Settings
LINKEDIN_CLIENT_ID=your_actual_client_id_here
LINKEDIN_CLIENT_SECRET=your_actual_client_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:5173/iipc/linkedin/callback
```

**Important:** 
- For production, use your production domain in `LINKEDIN_REDIRECT_URI`
- Never commit real credentials to Git
- Add `.env` to `.gitignore`

---

## Step 4: Configure Frontend Routing

### 4.1 Add Route for Callback Page

Update your routing configuration (e.g., `src/App.jsx` or router file):

```javascript
import LinkedInCallback from './pages/student/LinkedInCallback';

// Add this route
<Route path="/iipc/linkedin/callback" element={<LinkedInCallback />} />
```

**Example in App.jsx:**
```javascript
<Routes>
  {/* Existing routes */}
  <Route path="/student/iipc" element={<IIPC />} />
  
  {/* Add LinkedIn callback route */}
  <Route path="/iipc/linkedin/callback" element={<LinkedInCallback />} />
</Routes>
```

---

## Step 5: Testing

### 5.1 Start Development Servers

**Backend:**
```bash
cd backend
python manage.py runserver
```

**Frontend:**
```bash
npm run dev
```

### 5.2 Test OAuth Flow

1. Navigate to: `http://localhost:5173/student/iipc`
2. Click on "Connections Verification" tab
3. Select "Link Profile" method
4. Click "Sign in with LinkedIn" button
5. You'll be redirected to LinkedIn
6. Authorize the app
7. You'll be redirected back to the callback page
8. Profile URL should be auto-filled

---

## Step 6: Verification

### 6.1 What Should Work:
✅ Clicking "Sign in with LinkedIn" redirects to LinkedIn
✅ LinkedIn shows authorization screen
✅ After authorization, redirects back to your app
✅ Profile URL is auto-filled
✅ User's name and email are displayed

### 6.2 Common Issues:

**Issue: "Redirect URI mismatch"**
- Solution: Ensure the redirect URI in LinkedIn app settings exactly matches the one in `.env`

**Issue: "Invalid client_id"**
- Solution: Double-check your `LINKEDIN_CLIENT_ID` in `.env`

**Issue: "Access denied"**
- Solution: Make sure "Sign In with LinkedIn using OpenID Connect" product is approved

**Issue: 404 on callback**
- Solution: Ensure the LinkedInCallback route is properly configured

---

## API Endpoints

### Get Authorization URL
```
GET /api/iipc/connections/linkedin_auth_url/
```
Response:
```json
{
  "authorization_url": "https://www.linkedin.com/oauth/v2/authorization?...",
  "state": "random_csrf_token"
}
```

### Handle Callback
```
POST /api/iipc/connections/linkedin_callback/
{
  "code": "authorization_code_from_linkedin",
  "state": "csrf_token"
}
```
Response:
```json
{
  "success": true,
  "profile": {
    "linkedin_id": "abc123",
    "full_name": "John Doe",
    "email": "john@example.com",
    "profile_url": "https://www.linkedin.com/in/abc123"
  },
  "message": "LinkedIn profile verified successfully"
}
```

---

## Production Deployment

### Additional Steps for Production:

1. **Update Redirect URI**:
   - In LinkedIn app settings, add production URL
   - Update `LINKEDIN_REDIRECT_URI` in production `.env`

2. **Use HTTPS**:
   - LinkedIn requires HTTPS for production apps

3. **Environment Variables**:
   - Set environment variables on your hosting platform:
     - `LINKEDIN_CLIENT_ID`
     - `LINKEDIN_CLIENT_SECRET`
     - `LINKEDIN_REDIRECT_URI`

4. **CORS Settings**:
   - Add production domain to `CORS_ALLOWED_ORIGINS`

---

## Security Considerations

1. **Never expose Client Secret**: Keep it server-side only
2. **Validate State Parameter**: Prevents CSRF attacks (already implemented)
3. **Use HTTPS in Production**: Required by LinkedIn
4. **Store Tokens Securely**: Access tokens are handled server-side
5. **Implement Token Refresh**: For long-lived sessions (optional)

---

## Data Privacy

**What We Collect:**
- Full name
- Email address
- LinkedIn profile URL
- Profile picture (optional)

**What We DON'T Collect:**
- Connection data (not available via free API)
- Posts data (not available via free API)
- Detailed work history

**Note:** Students still need to manually enter connection count and upload screenshots as proof.

---

## Support

If you encounter issues:

1. Check LinkedIn Developer Documentation: https://docs.microsoft.com/en-us/linkedin/
2. Verify all redirect URIs match exactly
3. Ensure app is verified on LinkedIn
4. Check browser console for errors
5. Review Django logs for backend errors

---

## Summary

You've successfully integrated LinkedIn OAuth! The flow:

1. User clicks "Sign in with LinkedIn"
2. Backend generates authorization URL
3. User redirects to LinkedIn
4. User authorizes app
5. LinkedIn redirects back with code
6. Backend exchanges code for token
7. Backend fetches profile data
8. Profile URL auto-fills in form
9. User enters connection count manually
10. User submits for verification

This provides identity verification while keeping the manual verification process for connection counts.
