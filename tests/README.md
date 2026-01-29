# Cohort Web App - E2E Test Suite

## 🎯 Overview

Comprehensive End-to-End Selenium test suite for the Cohort Web Application. This suite validates the entire system including authentication, all user roles, gamification logic, and API interactions.

## 🏗️ Architecture

```
tests/
├── conftest.py                 # Pytest configuration and fixtures
├── requirements-test.txt       # Test dependencies
├── e2e/                       # E2E test files
│   ├── test_authentication.py # Auth tests for all roles
│   ├── test_student_flow.py   # Student dashboard and features
│   ├── test_mentor_flow.py    # Mentor dashboard and reviews
│   ├── test_floorwing_flow.py # Floor wing dashboard
│   ├── test_admin_flow.py     # Admin dashboard and config
│   └── test_edge_cases.py     # API validation and edge cases
├── fixtures/                   # Test data and fixtures
│   ├── seed_test_data.py      # Database seeding script
│   └── test_fixtures.py       # Pytest fixtures
├── utils/                      # Test utilities
│   ├── base_test.py           # Base test class with helpers
│   ├── auth_helper.py         # Authentication helper
│   └── page_objects.py        # Page object models
└── screenshots/                # Screenshots on test failure
```

## 📋 Prerequisites

### 1. Install Test Dependencies

```bash
pip install -r tests/requirements-test.txt
```

### 2. Ensure Servers Are Running

**Backend (Django):**
```bash
cd backend
python manage.py runserver
```

**Frontend (React):**
```bash
npm run dev
# or
yarn dev
```

### 3. Seed Test Data

```bash
python tests/fixtures/seed_test_data.py
```

Or use the test runner:
```bash
python run_tests.py --seed
```

## 🚀 Running Tests

### Run All Tests

```bash
# Basic run
pytest tests/e2e

# With verbose output
pytest tests/e2e -v

# In headless mode
pytest tests/e2e --headless

# Using test runner
python run_tests.py
```

### Run Specific Test Suites

```bash
# Authentication tests only
pytest tests/e2e -m auth
python run_tests.py --auth

# Student flow tests
pytest tests/e2e -m student
python run_tests.py --student

# Mentor flow tests
pytest tests/e2e -m mentor
python run_tests.py --mentor

# API validation tests
pytest tests/e2e -m api
```

### Run Specific Test Files

```bash
pytest tests/e2e/test_authentication.py
pytest tests/e2e/test_student_flow.py
```

### Run Specific Tests

```bash
# By test name
pytest tests/e2e -k "test_student_login"

# Multiple tests
pytest tests/e2e -k "login or logout"
```

### Parallel Execution

```bash
# Run with 4 workers
pytest tests/e2e -n 4

# Using test runner
python run_tests.py -n 4
```

### Generate HTML Report

```bash
pytest tests/e2e --html=test_report.html --self-contained-html

# Using test runner
python run_tests.py --html-report
```

## 🎭 Test Roles

The test suite validates these user roles:

1. **Student** - Dashboard, submissions, gamification
2. **Mentor** - Review submissions, manage students
3. **Floor Wing** - Monitor students, create announcements
4. **Admin** - System stats, leaderboard, configuration
5. **Super Admin** - Full system access

## ✅ Test Coverage

### Authentication Tests
- ✅ Valid login for all roles
- ✅ Invalid credentials error handling
- ✅ Session persistence
- ✅ Logout functionality
- ✅ Role-based access control
- ✅ API authorization

### Student Flow Tests
- ✅ Dashboard loads correctly
- ✅ Season Score, Legacy Score, Vault Credits visible
- ✅ 5 Pillars Status card removed
- ✅ Podium lock/unlock logic
- ✅ Pillar submission buttons (CLT, CFC, IIPC, SRI, SCD)
- ✅ LeetCode streak tracking
- ✅ Gamification features
- ✅ Title redemption

### Mentor Flow Tests
- ✅ Mentor dashboard loads
- ✅ View pending submissions
- ✅ Approve/reject submissions
- ✅ Quality score assignment
- ✅ View assigned students
- ✅ Permission boundaries

### Floor Wing Flow Tests
- ✅ Floor wing dashboard loads
- ✅ View floor students
- ✅ Monitor progress and stats
- ✅ Create announcements
- ✅ Permission boundaries

### Admin Flow Tests
- ✅ Admin dashboard loads
- ✅ System-wide statistics
- ✅ Leaderboard access
- ✅ Season configuration
- ✅ User management
- ✅ Superadmin full access

### API & Edge Case Tests
- ✅ API status codes (200, 401, 403, 404)
- ✅ Database update validation
- ✅ Session expiry handling
- ✅ Network error handling
- ✅ Duplicate submission prevention
- ✅ Invalid payload handling
- ✅ Permission enforcement
- ✅ Rollback on failure

## 🔧 Configuration

### Custom URLs

```bash
pytest tests/e2e --base-url=http://localhost:3000 --api-url=http://localhost:8000
```

### Browser Mode

```bash
# Headless (no browser window)
pytest tests/e2e --headless

# Headed (visible browser)
pytest tests/e2e
```

### Test Timeouts

Default timeout: 300 seconds (5 minutes)

Modify in `pytest.ini`:
```ini
timeout = 600
```

## 📸 Screenshots

Screenshots are automatically captured on test failures and saved to:
```
tests/screenshots/
```

## 🐛 Debugging

### View Browser Console Logs

Console logs are saved with screenshots on failure:
```
tests/screenshots/test_name_timestamp_console.log
```

### Run Single Test in Debug Mode

```bash
pytest tests/e2e/test_authentication.py::TestAuthentication::test_student_valid_login -v --capture=no
```

### Disable Headless Mode

```bash
pytest tests/e2e  # Remove --headless flag
```

## 📊 Test Markers

Use markers to organize and filter tests:

- `@pytest.mark.auth` - Authentication tests
- `@pytest.mark.student` - Student flow tests
- `@pytest.mark.mentor` - Mentor flow tests
- `@pytest.mark.floorwing` - Floor wing tests
- `@pytest.mark.admin` - Admin tests
- `@pytest.mark.api` - API validation tests
- `@pytest.mark.edge_case` - Edge case tests
- `@pytest.mark.smoke` - Smoke tests
- `@pytest.mark.slow` - Slow-running tests

## 🔐 Test Credentials

Default test users (created by seeder):

| Role | Username | Password |
|------|----------|----------|
| Student | test_student | test_password_123 |
| Mentor | test_mentor | test_password_123 |
| Floor Wing | test_floorwing | test_password_123 |
| Admin | test_admin | test_password_123 |
| Super Admin | superadmin | admin_password_123 |

## 🏆 Best Practices

### DO:
✅ Use explicit waits (WebDriverWait)
✅ Use page object models
✅ Use descriptive test names
✅ Test one thing per test
✅ Clean up test data
✅ Use fixtures for common setup

### DON'T:
❌ Use time.sleep()
❌ Hardcode credentials in tests
❌ Write flaky tests
❌ Test multiple things in one test
❌ Ignore test failures

## 🚨 Common Issues

### ChromeDriver Issues
```bash
pip install --upgrade webdriver-manager
```

### Port Already in Use
Ensure backend (8000) and frontend (5173) ports are available.

### Test Data Missing
Run the seeder:
```bash
python tests/fixtures/seed_test_data.py
```

### Timeouts
Increase timeout in pytest.ini or use:
```bash
pytest tests/e2e --timeout=600
```

## 📈 CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r tests/requirements-test.txt
      - name: Start backend
        run: |
          cd backend
          python manage.py migrate
          python manage.py runserver &
      - name: Start frontend
        run: |
          npm install
          npm run dev &
      - name: Run tests
        run: python run_tests.py --headless --html-report
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: test-report
          path: test_report.html
```

## 📝 Writing New Tests

### Example Test Structure

```python
import pytest
from tests.utils.auth_helper import AuthHelper

class TestNewFeature:
    """Test new feature"""
    
    def test_feature_works(self, driver, test_student_credentials):
        """Test that new feature works correctly"""
        # Setup
        auth = AuthHelper(driver)
        auth.login_as_student(
            test_student_credentials["username"],
            test_student_credentials["password"]
        )
        
        # Action
        # ... perform actions ...
        
        # Assert
        assert True, "Feature works as expected"
```

## 🤝 Contributing

1. Write tests for new features
2. Ensure all tests pass before committing
3. Follow existing test patterns
4. Add appropriate test markers
5. Update documentation

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review test logs and screenshots
3. Consult the team documentation

---

**Happy Testing! 🎉**
