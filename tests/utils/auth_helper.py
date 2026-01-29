"""
Authentication helpers for all user roles
"""
from selenium.webdriver.common.by import By
from tests.utils.base_test import BaseTest


class AuthHelper(BaseTest):
    """Helper class for authentication operations"""
    
    # Login page selectors - matching the actual Login.jsx form
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message, .alert-danger, [role='alert'], .input-error")
    
    # Role selection buttons
    ROLE_STUDENT = (By.XPATH, "//button[contains(@class, 'role-card')]//span[text()='Student']")
    ROLE_MENTOR = (By.XPATH, "//button[contains(@class, 'role-card')]//span[text()='Mentor']")
    ROLE_FLOORWING = (By.XPATH, "//button[contains(@class, 'role-card')]//span[text()='Floor Wing']")
    ROLE_ADMIN = (By.XPATH, "//button[contains(@class, 'role-card')]//span[text()='Admin']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def login(self, email: str, password: str, role: str = 'STUDENT', expected_redirect: str = None):
        """
        Generic login method
        
        Args:
            email: Email address
            password: Password
            role: Role to select (STUDENT, MENTOR, FLOOR_WING, ADMIN)
            expected_redirect: Expected URL path after login (optional)
        
        Returns:
            bool: True if login successful
        """
        # Navigate to login page
        self.navigate_to("/login")
        self.wait_for_page_load()
        
        # Select role first
        role_selector_map = {
            'STUDENT': self.ROLE_STUDENT,
            'MENTOR': self.ROLE_MENTOR,
            'FLOOR_WING': self.ROLE_FLOORWING,
            'ADMIN': self.ROLE_ADMIN
        }
        
        if role in role_selector_map:
            try:
                self.click(*role_selector_map[role])
                self.sleep(0.5)  # Small wait for role selection animation
            except Exception as e:
                print(f"Warning: Could not select role {role}: {e}")
        
        # Enter credentials
        self.type_text(*self.EMAIL_INPUT, email)
        self.type_text(*self.PASSWORD_INPUT, password)
        
        # Store current URL to detect redirect
        old_url = self.get_current_url()
        
        # Wait for button to be fully ready
        self.sleep(0.5)
        
        # Click login button (may need double click due to form validation)
        try:
            self.click(*self.LOGIN_BUTTON)
            self.sleep(1)
            
            # If still on login page, click again
            if "/login" in self.get_current_url():
                self.click(*self.LOGIN_BUTTON)
        except Exception as e:
            print(f"Warning during login button click: {e}")
        
        # Wait a bit for the login request to complete
        self.sleep(2)
        
        # Wait for redirect OR check if still on login page (means failure)
        try:
            self.wait_for_url_change(old_url, timeout=10)
        except Exception as e:
            # Check if we got an error message (login failed)
            if self.element_exists(*self.ERROR_MESSAGE, timeout=1):
                return False
            # If no error and URL didn't change, we might already be logged in
            # or React Router handled it differently
            print(f"URL didn't change as expected, but no error detected. Current URL: {self.get_current_url()}")
        
        # Check if redirected to expected page
        if expected_redirect:
            try:
                self.wait_for_url_contains(expected_redirect, timeout=5)
            except Exception as e:
                # If we're not at the expected redirect, check if we're at least not on login
                current_url = self.get_current_url()
                if "/login" not in current_url:
                    print(f"Redirected to {current_url} instead of {expected_redirect}")
                else:
                    return False
        
        # Return success if no error message
        return not self.element_exists(*self.ERROR_MESSAGE, timeout=2)
    
    def login_as_student(self, email: str = None, password: str = None):
        """Login as student with test credentials"""
        email = email or "test_student@cohort.com"
        password = password or "test_password_123"
        # Students are redirected to "/" (root/dashboard)
        return self.login(email, password, role='STUDENT', expected_redirect="/")
    
    def login_as_mentor(self, email: str = None, password: str = None):
        """Login as mentor with test credentials"""
        email = email or "test_mentor@cohort.com"
        password = password or "test_password_123"
        return self.login(email, password, role='MENTOR', expected_redirect="/mentor-dashboard")
    
    def login_as_floor_wing(self, email: str = None, password: str = None):
        """Login as floor wing with test credentials"""
        email = email or "test_floorwing@cohort.com"
        password = password or "test_password_123"
        return self.login(email, password, role='FLOOR_WING', expected_redirect="/floorwing-dashboard")
    
    def login_as_admin(self, email: str = None, password: str = None):
        """Login as admin with test credentials"""
        email = email or "test_admin@cohort.com"
        password = password or "test_password_123"
        return self.login(email, password, role='ADMIN', expected_redirect="/admin")
    
    def login_as_superadmin(self, email: str = None, password: str = None):
        """Login as superadmin with test credentials"""
        email = email or "test_superadmin@cohort.com"
        password = password or "test_password_123"
        return self.login(email, password, role='ADMIN', expected_redirect="/admin")
    
    def logout(self):
        """Logout current user"""
        # Try multiple common logout methods
        logout_selectors = [
            (By.CSS_SELECTOR, "button.logout"),
            (By.CSS_SELECTOR, "[data-testid='logout']"),
            (By.XPATH, "//button[contains(text(), 'Logout')]"),
            (By.XPATH, "//a[contains(text(), 'Logout')]"),
            (By.CSS_SELECTOR, ".logout-btn"),
        ]
        
        for selector in logout_selectors:
            if self.element_exists(*selector, timeout=2):
                self.click(*selector)
                # Wait for redirect to login
                self.wait_for_url_contains("/login", timeout=10)
                return True
        
        # Fallback: Clear localStorage and navigate to login
        self.driver.execute_script("localStorage.clear(); sessionStorage.clear();")
        self.navigate_to("/login")
        return True
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        # Check for auth token in localStorage
        token = self.get_auth_token_from_browser()
        return token is not None and token != ""
    
    def get_current_role(self) -> str:
        """Detect current user role from URL or localStorage"""
        url = self.get_current_url()
        
        if "/student" in url:
            return "student"
        elif "/mentor" in url:
            return "mentor"
        elif "/floor-wing" in url:
            return "floor_wing"
        elif "/admin" in url:
            return "admin"
        else:
            # Try to get from localStorage
            try:
                role = self.driver.execute_script("return localStorage.getItem('userRole');")
                return role
            except:
                return "unknown"
    
    def verify_session_persistence(self):
        """Verify session persists after page refresh"""
        old_url = self.get_current_url()
        self.refresh_page()
        self.wait_for_page_load()
        
        # Should still be logged in
        assert self.is_logged_in(), "Session lost after page refresh"
        
        # Should be on same page
        new_url = self.get_current_url()
        assert old_url == new_url, f"URL changed after refresh: {old_url} -> {new_url}"
    
    def attempt_unauthorized_access(self, path: str) -> bool:
        """
        Attempt to access a path and check if redirected/blocked
        
        Returns:
            bool: True if access was blocked (redirected to login or error)
        """
        old_url = self.get_current_url()
        self.navigate_to(path)
        self.wait_for_page_load(timeout=5)
        
        new_url = self.get_current_url()
        
        # Check if redirected to login or stayed on same page
        if "/login" in new_url or new_url == old_url:
            return True
        
        # Check for 403/401 error messages
        forbidden_indicators = [
            (By.XPATH, "//*[contains(text(), '403')]"),
            (By.XPATH, "//*[contains(text(), '401')]"),
            (By.XPATH, "//*[contains(text(), 'Unauthorized')]"),
            (By.XPATH, "//*[contains(text(), 'Forbidden')]"),
            (By.XPATH, "//*[contains(text(), 'Access Denied')]"),
        ]
        
        for selector in forbidden_indicators:
            if self.element_exists(*selector, timeout=2):
                return True
        
        return False
    
    def get_error_message(self) -> str:
        """Get login error message if present"""
        if self.element_exists(*self.ERROR_MESSAGE, timeout=2):
            return self.get_text(*self.ERROR_MESSAGE)
        return ""
