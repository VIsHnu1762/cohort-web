"""
Authentication and Authorization Tests
Tests login, logout, session persistence, and role-based access control
"""
import pytest
from tests.utils.auth_helper import AuthHelper


class TestAuthentication:
    """Test authentication for all user roles"""
    
    def test_student_valid_login(self, driver, test_student_credentials):
        """Test student can login with valid credentials"""
        auth = AuthHelper(driver)
        success = auth.login_as_student(
            test_student_credentials["email"],
            test_student_credentials["password"]
        )
        
        assert success, "Student login failed"
        assert auth.is_logged_in(), "Student not logged in after successful login"
        # Students are redirected to "/" (root path/dashboard)
        current_url = auth.get_current_url()
        assert current_url.endswith("/") or "/dashboard" in current_url or "/clt" in current_url, \
            f"Not redirected to student dashboard, current URL: {current_url}"
    
    def test_mentor_valid_login(self, driver, test_mentor_credentials):
        """Test mentor can login with valid credentials"""
        auth = AuthHelper(driver)
        success = auth.login_as_mentor(
            test_mentor_credentials["email"],
            test_mentor_credentials["password"]
        )
        
        assert success, "Mentor login failed"
        assert auth.is_logged_in(), "Mentor not logged in after successful login"
        assert "/mentor" in auth.get_current_url(), "Not redirected to mentor dashboard"
    
    def test_floorwing_valid_login(self, driver, test_floorwing_credentials):
        """Test floor wing can login with valid credentials"""
        auth = AuthHelper(driver)
        success = auth.login_as_floor_wing(
            test_floorwing_credentials["email"],
            test_floorwing_credentials["password"]
        )
        
        assert success, "Floor wing login failed"
        assert auth.is_logged_in(), "Floor wing not logged in after successful login"
        assert "/floor-wing" in auth.get_current_url() or "/floorwing" in auth.get_current_url(), \
            "Not redirected to floor wing dashboard"
    
    def test_admin_valid_login(self, driver, test_admin_credentials):
        """Test admin can login with valid credentials"""
        auth = AuthHelper(driver)
        success = auth.login_as_admin(
            test_admin_credentials["email"],
            test_admin_credentials["password"]
        )
        
        assert success, "Admin login failed"
        assert auth.is_logged_in(), "Admin not logged in after successful login"
        assert "/admin" in auth.get_current_url(), "Not redirected to admin dashboard"
    
    def test_invalid_credentials_show_error(self, driver, invalid_credentials):
        """Test invalid credentials show proper error message"""
        auth = AuthHelper(driver)
        
        auth.navigate_to("/login")
        auth.type_text(*auth.EMAIL_INPUT, invalid_credentials["username"])
        auth.type_text(*auth.PASSWORD_INPUT, invalid_credentials["password"])
        auth.click(*auth.LOGIN_BUTTON)
        
        # Should show error message
        assert auth.element_exists(*auth.ERROR_MESSAGE, timeout=5), \
            "No error message shown for invalid credentials"
        
        error_text = auth.get_error_message().lower()
        assert any(word in error_text for word in ["invalid", "incorrect", "wrong", "failed"]), \
            f"Error message doesn't indicate login failure: {error_text}"
    
    def test_empty_credentials_show_error(self, driver):
        """Test empty credentials show validation error"""
        auth = AuthHelper(driver)
        
        auth.navigate_to("/login")
        auth.click(*auth.LOGIN_BUTTON)
        
        # Should show validation error or stay on login page
        current_url = auth.get_current_url()
        assert "/login" in current_url, "Navigated away from login with empty credentials"


class TestSessionPersistence:
    """Test session persistence across page refreshes"""
    
    def test_student_session_persists_after_refresh(self, driver, test_student_credentials):
        """Test student session persists after page refresh"""
        auth = AuthHelper(driver)
        auth.login_as_student(
            test_student_credentials["email"],
            test_student_credentials["password"]
        )
        
        # Verify session persists
        auth.verify_session_persistence()
    
    def test_mentor_session_persists_after_refresh(self, driver, test_mentor_credentials):
        """Test mentor session persists after page refresh"""
        auth = AuthHelper(driver)
        auth.login_as_mentor(
            test_mentor_credentials["email"],
            test_mentor_credentials["password"]
        )
        
        # Verify session persists
        auth.verify_session_persistence()


class TestLogout:
    """Test logout functionality"""
    
    def test_student_logout(self, driver, test_student_credentials):
        """Test student can logout successfully"""
        auth = AuthHelper(driver)
        auth.login_as_student(
            test_student_credentials["email"],
            test_student_credentials["password"]
        )
        
        # Logout
        auth.logout()
        
        # Verify logged out
        assert not auth.is_logged_in(), "Student still logged in after logout"
        assert "/login" in auth.get_current_url(), "Not redirected to login after logout"
    
    def test_mentor_logout(self, driver, test_mentor_credentials):
        """Test mentor can logout successfully"""
        auth = AuthHelper(driver)
        auth.login_as_mentor(
            test_mentor_credentials["email"],
            test_mentor_credentials["password"]
        )
        
        # Logout
        auth.logout()
        
        # Verify logged out
        assert not auth.is_logged_in(), "Mentor still logged in after logout"
        assert "/login" in auth.get_current_url(), "Not redirected to login after logout"


class TestRoleBasedAccessControl:
    """Test role-based access control and permission boundaries"""
    
    def test_student_cannot_access_mentor_dashboard(self, driver, test_student_credentials):
        """Test student cannot access mentor dashboard"""
        auth = AuthHelper(driver)
        auth.login_as_student(
            test_student_credentials["username"],
            test_student_credentials["password"]
        )
        
        # Try to access mentor dashboard
        blocked = auth.attempt_unauthorized_access("/mentor/dashboard")
        assert blocked, "Student was able to access mentor dashboard"
    
    def test_student_cannot_access_admin_dashboard(self, driver, test_student_credentials):
        """Test student cannot access admin dashboard"""
        auth = AuthHelper(driver)
        auth.login_as_student(
            test_student_credentials["username"],
            test_student_credentials["password"]
        )
        
        # Try to access admin dashboard
        blocked = auth.attempt_unauthorized_access("/admin/dashboard")
        assert blocked, "Student was able to access admin dashboard"
    
    def test_mentor_cannot_access_student_dashboard(self, driver, test_mentor_credentials):
        """Test mentor cannot access student dashboard"""
        auth = AuthHelper(driver)
        auth.login_as_mentor(
            test_mentor_credentials["username"],
            test_mentor_credentials["password"]
        )
        
        # Try to access student dashboard
        blocked = auth.attempt_unauthorized_access("/student/home")
        assert blocked, "Mentor was able to access student dashboard"
    
    def test_mentor_cannot_access_admin_dashboard(self, driver, test_mentor_credentials):
        """Test mentor cannot access admin dashboard"""
        auth = AuthHelper(driver)
        auth.login_as_mentor(
            test_mentor_credentials["username"],
            test_mentor_credentials["password"]
        )
        
        # Try to access admin dashboard
        blocked = auth.attempt_unauthorized_access("/admin/dashboard")
        assert blocked, "Mentor was able to access admin dashboard"
    
    def test_floorwing_cannot_access_mentor_features(self, driver, test_floorwing_credentials):
        """Test floor wing cannot access mentor features"""
        auth = AuthHelper(driver)
        auth.login_as_floor_wing(
            test_floorwing_credentials["username"],
            test_floorwing_credentials["password"]
        )
        
        # Try to access mentor dashboard
        blocked = auth.attempt_unauthorized_access("/mentor/dashboard")
        assert blocked, "Floor wing was able to access mentor dashboard"


class TestAPIAuthorization:
    """Test API authorization and permission enforcement"""
    
    def test_unauthorized_api_access_returns_401(self, driver):
        """Test unauthorized API access returns 401"""
        auth = AuthHelper(driver)
        
        # Make API request without token
        response = auth.api_request("GET", "/api/gamification/profile/")
        
        assert response.status_code in [401, 403], \
            f"Expected 401/403 for unauthorized access, got {response.status_code}"
    
    def test_student_cannot_access_mentor_api(self, driver, test_student_credentials):
        """Test student cannot access mentor-only API endpoints"""
        auth = AuthHelper(driver)
        auth.login_as_student(
            test_student_credentials["username"],
            test_student_credentials["password"]
        )
        
        token = auth.get_auth_token_from_browser()
        
        # Try to access mentor-only endpoint
        response = auth.api_request("GET", "/api/mentor/submissions/", token=token)
        
        assert response.status_code in [403, 404], \
            f"Student should not access mentor API, got status {response.status_code}"
    
    def test_mentor_cannot_access_admin_api(self, driver, test_mentor_credentials):
        """Test mentor cannot access admin-only API endpoints"""
        auth = AuthHelper(driver)
        auth.login_as_mentor(
            test_mentor_credentials["username"],
            test_mentor_credentials["password"]
        )
        
        token = auth.get_auth_token_from_browser()
        
        # Try to access admin-only endpoint
        response = auth.api_request("GET", "/api/admin/system-stats/", token=token)
        
        assert response.status_code in [403, 404], \
            f"Mentor should not access admin API, got status {response.status_code}"
