"""
Base test class with common utilities and helpers
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
import time
from typing import Optional, Tuple


class BaseTest:
    """Base test class with common test utilities"""
    
    def __init__(self, driver):
        self.driver = driver
        self.config = driver.test_config
        self.base_url = self.config["base_url"]
        self.api_url = self.config["api_url"]
        self.wait_helper = WebDriverWait(driver, 10)
        self.long_wait = WebDriverWait(driver, 30)
    
    # ==================== NAVIGATION ====================
    
    def navigate_to(self, path: str = ""):
        """Navigate to a specific path"""
        url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
        self.driver.get(url)
    
    def get_current_url(self) -> str:
        """Get current URL"""
        return self.driver.current_url
    
    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
    
    def sleep(self, seconds: float):
        """Simple sleep/wait for specified seconds"""
        time.sleep(seconds)
    
    # ==================== ELEMENT FINDERS ====================
    
    def find_element(self, by: By, value: str, timeout: int = 10):
        """Find element with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))
    
    def find_elements(self, by: By, value: str, timeout: int = 10):
        """Find multiple elements with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.presence_of_element_located((by, value)))
        return self.driver.find_elements(by, value)
    
    def find_clickable_element(self, by: By, value: str, timeout: int = 10):
        """Find clickable element with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))
    
    def element_exists(self, by: By, value: str, timeout: int = 5) -> bool:
        """Check if element exists"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
    
    def element_visible(self, by: By, value: str, timeout: int = 5) -> bool:
        """Check if element is visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
    
    def element_not_present(self, by: By, value: str, timeout: int = 5) -> bool:
        """Check if element is not present"""
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_to_disappear(self, by: By, value: str, timeout: int = 10):
        """Wait for element to disappear"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.invisibility_of_element_located((by, value)))
    
    # ==================== INTERACTIONS ====================
    
    def click(self, by: By, value: str, timeout: int = 10):
        """Click element with wait"""
        element = self.find_clickable_element(by, value, timeout)
        element.click()
    
    def type_text(self, by: By, value: str, text: str, timeout: int = 10):
        """Type text into input field"""
        element = self.find_element(by, value, timeout)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, by: By, value: str, timeout: int = 10) -> str:
        """Get text from element"""
        element = self.find_element(by, value, timeout)
        return element.text
    
    def get_attribute(self, by: By, value: str, attribute: str, timeout: int = 10) -> str:
        """Get attribute from element"""
        element = self.find_element(by, value, timeout)
        return element.get_attribute(attribute)
    
    # ==================== WAITS ====================
    
    def wait_for_url_change(self, old_url: str, timeout: int = 10):
        """Wait for URL to change from old_url"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda driver: driver.current_url != old_url)
    
    def wait_for_url_contains(self, text: str, timeout: int = 10):
        """Wait for URL to contain text"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.url_contains(text))
    
    def wait_for_text_in_element(self, by: By, value: str, text: str, timeout: int = 10):
        """Wait for specific text to appear in element"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.text_to_be_present_in_element((by, value), text))
    
    def wait_for_page_load(self, timeout: int = 30):
        """Wait for page to fully load"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    # ==================== API HELPERS ====================
    
    def api_request(self, method: str, endpoint: str, token: Optional[str] = None, 
                    data: Optional[dict] = None, files: Optional[dict] = None) -> requests.Response:
        """Make API request with optional authentication"""
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        headers = {}
        
        if token:
            headers["Authorization"] = f"Token {token}"
        
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            if files:
                response = requests.post(url, headers=headers, data=data, files=files)
            else:
                headers["Content-Type"] = "application/json"
                response = requests.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            headers["Content-Type"] = "application/json"
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == "PATCH":
            headers["Content-Type"] = "application/json"
            response = requests.patch(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        return response
    
    def get_auth_token_from_browser(self) -> Optional[str]:
        """Extract auth token from browser localStorage or cookies"""
        try:
            # Check for accessToken (used by the app)
            token = self.driver.execute_script("return localStorage.getItem('accessToken');")
            if token:
                return token
            # Fallback to 'token' key
            token = self.driver.execute_script("return localStorage.getItem('token');")
            return token
        except Exception:
            return None
    
    def set_auth_token_in_browser(self, token: str):
        """Set auth token in browser localStorage"""
        self.driver.execute_script(f"localStorage.setItem('token', '{token}');")
    
    # ==================== VALIDATION ====================
    
    def assert_url_contains(self, text: str, message: str = ""):
        """Assert URL contains text"""
        current_url = self.get_current_url()
        assert text in current_url, message or f"Expected URL to contain '{text}', got '{current_url}'"
    
    def assert_element_exists(self, by: By, value: str, message: str = ""):
        """Assert element exists"""
        assert self.element_exists(by, value), message or f"Element not found: {value}"
    
    def assert_element_not_exists(self, by: By, value: str, message: str = ""):
        """Assert element does not exist"""
        assert not self.element_exists(by, value, timeout=3), message or f"Element found but should not exist: {value}"
    
    def assert_text_in_element(self, by: By, value: str, expected_text: str, message: str = ""):
        """Assert element contains text"""
        actual_text = self.get_text(by, value)
        assert expected_text in actual_text, message or f"Expected '{expected_text}' in '{actual_text}'"
    
    # ==================== SCREENSHOT ====================
    
    def take_screenshot(self, name: str):
        """Take screenshot with custom name"""
        import os
        from datetime import datetime
        
        screenshot_dir = self.config["screenshot_dir"]
        os.makedirs(screenshot_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(screenshot_dir, filename)
        
        self.driver.save_screenshot(filepath)
        print(f"\n📸 Screenshot saved: {filepath}")
