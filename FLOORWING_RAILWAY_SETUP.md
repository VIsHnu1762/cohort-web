# Adding Floor Wing Users to Railway PostgreSQL

## Quick Setup

The easiest way to add floor wing users is to call the API endpoint from your local machine.

### Steps:

1. **Make sure your backend is deployed on Railway** with the latest code including the setup endpoint

2. **Run the setup script from your local machine**:
   ```bash
   cd C:\Python310\cohort_webapp\cohort
   python backend/call_setup_floorwings.py
   ```

This will:
- Login as admin
- Call the setup endpoint on Railway
- Create 7 floor wing users directly in the PostgreSQL database
- Display a complete summary

### What Gets Created:
### What Gets Created:

7 floor wing users will be created:

7 floor wing users will be created:

- **TECH Campus**: floorwing_tech_1 to floorwing_tech_4 (4 floors)
- **ARTS Campus**: floorwing_arts_1 to floorwing_arts_3 (3 floors)
- **Password for all**: `floorwing123`

---

## Floor Wing User Details

---

## Testing the Floor Wing Users

1. **Login Test**:
   - Go to your frontend: `https://your-frontend.up.railway.app`
   - Login with: `floorwing_tech_1` / `floorwing123`

2. **Access Dashboard**:
   - After login, floor wings should see their dashboard
   - They can view students assigned to their floor
   - They can see mentor assignments

---

## Troubleshooting

### Issue: "Login failed: 401"
**Solution**: Update the admin credentials in [call_setup_floorwings.py](backend/call_setup_floorwings.py):
```python
ADMIN_EMAIL = "your_admin@test.com"
ADMIN_PASSWORD = "your_admin_password"
```

### Issue: "Connection refused" or "Unable to connect"
**Solution**: 
1. Check your Railway backend URL in [call_setup_floorwings.py](backend/call_setup_floorwings.py)
2. Make sure your backend is running on Railway
3. Verify the URL is correct (should be something like `https://your-app.up.railway.app`)

### Issue: "404 Not Found"
**Solution**: Make sure you've deployed the latest code with the new endpoint to Railway

### Issue: "403 Forbidden"
**Solution**: The admin user doesn't have permission. Make sure the admin user is a superuser or staff member

---

## Customization

To modify floor wing details, edit the `FLOORWINGS` list in [views_floorwings.py](backend/apps/profiles/views_floorwings.py):

```python
FLOORWINGS = [
    {"username": "floorwing_tech_1", "email": "fw_tech_1@sns.edu", "campus": "TECH", "floor": 1, "name": "Floor Wing TECH Floor 1"},
    # Add more floor wings here
]
```

To change the default password, modify in the same file:
```python
DEFAULT_PASSWORD = 'your_new_password_here'
```

After making changes, commit and push to Railway, then run the setup script again.

---

## API Endpoint

The setup endpoint is available at:
```
POST /api/profiles/admin/setup-floorwings/
```

Requires admin authentication (Bearer token).

You can also call it manually using curl:
```bash
# Get token
TOKEN=$(curl -X POST https://your-app.up.railway.app/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@test.com","password":"admin123"}' | jq -r .access)

# Setup floor wings
curl -X POST https://your-app.up.railway.app/api/profiles/admin/setup-floorwings/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

---

## Security Note

⚠️ **Important**: After deployment, you should:
1. Change the default password for all floor wing users
2. Or ask floor wings to change their passwords on first login
3. Consider implementing password reset functionality
