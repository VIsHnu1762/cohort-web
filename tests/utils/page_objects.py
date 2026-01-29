"""
Page Object Models for different dashboards
"""
from selenium.webdriver.common.by import By
from tests.utils.base_test import BaseTest


class StudentDashboard(BaseTest):
    """Student Dashboard Page Object"""
    
    # Dashboard elements
    SEASON_SCORE = (By.CSS_SELECTOR, "[data-testid='season-score'], .season-score")
    LEGACY_SCORE = (By.CSS_SELECTOR, "[data-testid='legacy-score'], .legacy-score")
    VAULT_CREDITS = (By.CSS_SELECTOR, "[data-testid='vault-credits'], .vault-credits")
    FIVE_PILLARS_STATUS = (By.CSS_SELECTOR, "[data-testid='five-pillars'], .five-pillars-status")
    
    # Podium elements
    PODIUM_CONTAINER = (By.CSS_SELECTOR, "[data-testid='podium'], .podium")
    PODIUM_LOCKED = (By.CSS_SELECTOR, "[data-testid='podium-locked'], .podium-locked")
    CHAMPION_POSITION = (By.CSS_SELECTOR, "[data-testid='champion'], .champion")
    
    # Pillar submission buttons
    CLT_SUBMIT = (By.CSS_SELECTOR, "[data-testid='clt-submit'], button[data-pillar='clt']")
    CFC_SUBMIT = (By.CSS_SELECTOR, "[data-testid='cfc-submit'], button[data-pillar='cfc']")
    IIPC_SUBMIT = (By.CSS_SELECTOR, "[data-testid='iipc-submit'], button[data-pillar='iipc']")
    SRI_SUBMIT = (By.CSS_SELECTOR, "[data-testid='sri-submit'], button[data-pillar='sri']")
    SCD_SECTION = (By.CSS_SELECTOR, "[data-testid='scd-section'], .scd-pillar")
    
    # Gamification elements
    STREAK_COUNT = (By.CSS_SELECTOR, "[data-testid='streak-count'], .streak-count")
    TITLE_DISPLAY = (By.CSS_SELECTOR, "[data-testid='user-title'], .user-title")
    REDEMPTION_BUTTON = (By.CSS_SELECTOR, "[data-testid='redeem-credits'], .redeem-button")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to_dashboard(self):
        """Navigate to student dashboard"""
        self.navigate_to("/student/home")
        self.wait_for_page_load()
    
    def get_season_score(self) -> str:
        """Get season score value"""
        return self.get_text(*self.SEASON_SCORE)
    
    def get_legacy_score(self) -> str:
        """Get legacy score value"""
        return self.get_text(*self.LEGACY_SCORE)
    
    def get_vault_credits(self) -> str:
        """Get vault credits value"""
        return self.get_text(*self.VAULT_CREDITS)
    
    def is_five_pillars_visible(self) -> bool:
        """Check if 5 Pillars Status card is visible"""
        return self.element_visible(*self.FIVE_PILLARS_STATUS, timeout=3)
    
    def is_podium_locked(self) -> bool:
        """Check if podium is locked"""
        return self.element_visible(*self.PODIUM_LOCKED, timeout=3)
    
    def is_podium_unlocked(self) -> bool:
        """Check if podium is unlocked and visible"""
        return self.element_visible(*self.PODIUM_CONTAINER, timeout=3) and \
               not self.element_visible(*self.PODIUM_LOCKED, timeout=1)
    
    def is_champion_visible(self) -> bool:
        """Check if champion position is emphasized"""
        return self.element_visible(*self.CHAMPION_POSITION, timeout=3)
    
    def submit_clt(self):
        """Click CLT submission button"""
        self.click(*self.CLT_SUBMIT)
    
    def submit_cfc(self):
        """Click CFC submission button"""
        self.click(*self.CFC_SUBMIT)
    
    def submit_iipc(self):
        """Click IIPC submission button"""
        self.click(*self.IIPC_SUBMIT)
    
    def submit_sri(self):
        """Click SRI submission button"""
        self.click(*self.SRI_SUBMIT)
    
    def get_streak_count(self) -> int:
        """Get current LeetCode streak count"""
        text = self.get_text(*self.STREAK_COUNT)
        # Extract number from text
        import re
        match = re.search(r'\d+', text)
        return int(match.group()) if match else 0
    
    def get_current_title(self) -> str:
        """Get current equipped title"""
        if self.element_exists(*self.TITLE_DISPLAY, timeout=3):
            return self.get_text(*self.TITLE_DISPLAY)
        return ""
    
    def click_redeem_credits(self):
        """Click redemption button"""
        self.click(*self.REDEMPTION_BUTTON)


class MentorDashboard(BaseTest):
    """Mentor Dashboard Page Object"""
    
    # Dashboard elements
    PENDING_SUBMISSIONS = (By.CSS_SELECTOR, "[data-testid='pending-submissions'], .pending-submissions")
    SUBMISSION_CARD = (By.CSS_SELECTOR, ".submission-card")
    APPROVE_BUTTON = (By.CSS_SELECTOR, "[data-testid='approve-btn'], button.approve")
    REJECT_BUTTON = (By.CSS_SELECTOR, "[data-testid='reject-btn'], button.reject")
    QUALITY_SCORE_INPUT = (By.CSS_SELECTOR, "[data-testid='quality-score'], input[name='quality_score']")
    SUBMIT_REVIEW_BUTTON = (By.CSS_SELECTOR, "[data-testid='submit-review'], button.submit-review")
    
    # Student list
    ASSIGNED_STUDENTS = (By.CSS_SELECTOR, "[data-testid='assigned-students'], .assigned-students")
    STUDENT_CARD = (By.CSS_SELECTOR, ".student-card")
    
    # Unlock requests
    OD_REQUEST = (By.CSS_SELECTOR, "[data-testid='od-request'], .od-request")
    WFH_REQUEST = (By.CSS_SELECTOR, "[data-testid='wfh-request'], .wfh-request")
    APPROVE_UNLOCK = (By.CSS_SELECTOR, "[data-testid='approve-unlock'], button.approve-unlock")
    DENY_UNLOCK = (By.CSS_SELECTOR, "[data-testid='deny-unlock'], button.deny-unlock")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to_dashboard(self):
        """Navigate to mentor dashboard"""
        self.navigate_to("/mentor/dashboard")
        self.wait_for_page_load()
    
    def get_pending_submissions_count(self) -> int:
        """Get count of pending submissions"""
        if self.element_exists(*self.PENDING_SUBMISSIONS, timeout=3):
            cards = self.find_elements(*self.SUBMISSION_CARD)
            return len(cards)
        return 0
    
    def approve_first_submission(self, quality_score: int = None):
        """Approve the first pending submission"""
        if quality_score:
            self.type_text(*self.QUALITY_SCORE_INPUT, str(quality_score))
        self.click(*self.APPROVE_BUTTON)
        self.wait_for_element_to_disappear(*self.APPROVE_BUTTON, timeout=10)
    
    def reject_first_submission(self):
        """Reject the first pending submission"""
        self.click(*self.REJECT_BUTTON)
        self.wait_for_element_to_disappear(*self.REJECT_BUTTON, timeout=10)
    
    def get_assigned_students_count(self) -> int:
        """Get count of assigned students"""
        if self.element_exists(*self.ASSIGNED_STUDENTS, timeout=3):
            cards = self.find_elements(*self.STUDENT_CARD)
            return len(cards)
        return 0
    
    def approve_od_request(self):
        """Approve OD unlock request"""
        self.click(*self.APPROVE_UNLOCK)
    
    def deny_wfh_request(self):
        """Deny WFH unlock request"""
        self.click(*self.DENY_UNLOCK)


class FloorWingDashboard(BaseTest):
    """Floor Wing Dashboard Page Object"""
    
    # Dashboard elements
    FLOOR_STUDENTS = (By.CSS_SELECTOR, "[data-testid='floor-students'], .floor-students")
    STUDENT_PROGRESS = (By.CSS_SELECTOR, ".student-progress")
    ANNOUNCEMENT_BUTTON = (By.CSS_SELECTOR, "[data-testid='create-announcement'], button.announcement")
    ANNOUNCEMENT_TEXTAREA = (By.CSS_SELECTOR, "textarea[name='announcement']")
    SEND_ANNOUNCEMENT = (By.CSS_SELECTOR, "[data-testid='send-announcement'], button.send")
    
    # Statistics
    FLOOR_STATS = (By.CSS_SELECTOR, "[data-testid='floor-stats'], .floor-statistics")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to_dashboard(self):
        """Navigate to floor wing dashboard"""
        self.navigate_to("/floor-wing/dashboard")
        self.wait_for_page_load()
    
    def get_floor_students_count(self) -> int:
        """Get count of floor students"""
        if self.element_exists(*self.FLOOR_STUDENTS, timeout=3):
            students = self.find_elements(*self.STUDENT_PROGRESS)
            return len(students)
        return 0
    
    def create_announcement(self, message: str):
        """Create and send announcement"""
        self.click(*self.ANNOUNCEMENT_BUTTON)
        self.type_text(*self.ANNOUNCEMENT_TEXTAREA, message)
        self.click(*self.SEND_ANNOUNCEMENT)
        self.wait_for_element_to_disappear(*self.SEND_ANNOUNCEMENT, timeout=10)


class AdminDashboard(BaseTest):
    """Admin Dashboard Page Object"""
    
    # Dashboard elements
    SYSTEM_STATS = (By.CSS_SELECTOR, "[data-testid='system-stats'], .system-stats")
    LEADERBOARD = (By.CSS_SELECTOR, "[data-testid='leaderboard'], .leaderboard")
    SEASON_CONFIG = (By.CSS_SELECTOR, "[data-testid='season-config'], .season-config")
    USER_MANAGEMENT = (By.CSS_SELECTOR, "[data-testid='user-management'], .user-management")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to_dashboard(self):
        """Navigate to admin dashboard"""
        self.navigate_to("/admin/dashboard")
        self.wait_for_page_load()
    
    def has_system_stats_access(self) -> bool:
        """Check if system stats are accessible"""
        return self.element_visible(*self.SYSTEM_STATS, timeout=5)
    
    def has_leaderboard_access(self) -> bool:
        """Check if leaderboard is accessible"""
        return self.element_visible(*self.LEADERBOARD, timeout=5)
    
    def has_season_config_access(self) -> bool:
        """Check if season config is accessible"""
        return self.element_visible(*self.SEASON_CONFIG, timeout=5)
