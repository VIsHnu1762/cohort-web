"""
Pytest configuration and shared fixtures
"""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# Import fixtures from test_fixtures
from tests.fixtures.test_fixtures import (
    test_student_credentials,
    test_mentor_credentials,
    test_floorwing_credentials,
    test_admin_credentials,
    invalid_credentials
)


def pytest_addoption(parser):
    """Add custom command-line options"""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="http://localhost:5173",
        help="Base URL for the application"
    )
    parser.addoption(
        "--api-url",
        action="store",
        default="http://localhost:8000",
        help="API base URL"
    )


@pytest.fixture(scope="session")
def test_config(request):
    """Test configuration fixture"""
    return {
        "headless": request.config.getoption("--headless"),
        "base_url": request.config.getoption("--base-url"),
        "api_url": request.config.getoption("--api-url"),
        "screenshot_dir": os.path.join(os.path.dirname(__file__), "screenshots"),
        "implicit_wait": 10,
        "page_load_timeout": 30,
    }


@pytest.fixture(scope="function")
def driver(request, test_config):
    """
    WebDriver fixture with automatic setup and teardown
    Creates a new browser instance for each test
    """
    # Configure Chrome options
    chrome_options = Options()
    
    if test_config["headless"]:
        chrome_options.add_argument("--headless=new")
    
    # Additional Chrome options for stability
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-notifications")
    
    # Enable browser logging
    chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    
    # Initialize WebDriver with manually downloaded 64-bit ChromeDriver
    import os as os_module
    chromedriver_path = os_module.path.join(
        os_module.path.expanduser("~"),
        ".wdm", "drivers", "chromedriver", "win64", "143.0.7499.169",
        "chromedriver-win64", "chromedriver.exe"
    )
    
    # Fallback to webdriver-manager if manual path doesn't exist
    if not os_module.path.exists(chromedriver_path):
        service = Service(ChromeDriverManager(driver_version="143.0.7499.169").install())
    else:
        service = Service(chromedriver_path)
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Set timeouts
    driver.implicitly_wait(test_config["implicit_wait"])
    driver.set_page_load_timeout(test_config["page_load_timeout"])
    
    # Make driver and config available to tests
    driver.test_config = test_config
    
    yield driver
    
    # Teardown: Take screenshot on failure
    if request.node.rep_call.failed:
        take_screenshot(driver, request.node.nodeid, test_config["screenshot_dir"])
        save_console_logs(driver, request.node.nodeid, test_config["screenshot_dir"])
    
    # Close browser
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results for screenshot on failure
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def take_screenshot(driver, test_name, screenshot_dir):
    """Take screenshot on test failure"""
    try:
        os.makedirs(screenshot_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Sanitize test name for filename
        safe_name = test_name.replace("::", "_").replace("/", "_").replace("\\", "_")
        filename = f"{safe_name}_{timestamp}.png"
        filepath = os.path.join(screenshot_dir, filename)
        driver.save_screenshot(filepath)
        print(f"\n📸 Screenshot saved: {filepath}")
    except Exception as e:
        print(f"\n❌ Failed to take screenshot: {e}")


def save_console_logs(driver, test_name, screenshot_dir):
    """Save browser console logs on test failure"""
    try:
        os.makedirs(screenshot_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = test_name.replace("::", "_").replace("/", "_").replace("\\", "_")
        filename = f"{safe_name}_{timestamp}_console.log"
        filepath = os.path.join(screenshot_dir, filename)
        
        logs = driver.get_log("browser")
        with open(filepath, "w", encoding="utf-8") as f:
            for log in logs:
                f.write(f"{log['level']}: {log['message']}\n")
        print(f"📝 Console logs saved: {filepath}")
    except Exception as e:
        print(f"❌ Failed to save console logs: {e}")
