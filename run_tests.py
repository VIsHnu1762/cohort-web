#!/usr/bin/env python
"""
Test Runner Script
Execute E2E tests with various configurations
"""
import sys
import subprocess
import argparse
import os


def run_tests(args):
    """Run pytest with specified arguments"""
    
    # Base command
    cmd = ["pytest"]
    
    # Add test path
    if args.test_path:
        cmd.append(args.test_path)
    else:
        cmd.append("tests/e2e")
    
    # Add markers
    if args.marker:
        cmd.extend(["-m", args.marker])
    
    # Add headless mode
    if args.headless:
        cmd.append("--headless")
    
    # Add base URL
    if args.base_url:
        cmd.extend(["--base-url", args.base_url])
    
    # Add API URL
    if args.api_url:
        cmd.extend(["--api-url", args.api_url])
    
    # Add parallel execution
    if args.parallel:
        cmd.extend(["-n", str(args.parallel)])
    
    # Add HTML report
    if args.html_report:
        cmd.extend(["--html=test_report.html", "--self-contained-html"])
    
    # Add verbose mode
    if args.verbose:
        cmd.append("-vv")
    
    # Add specific test
    if args.test_name:
        cmd.extend(["-k", args.test_name])
    
    # Print command
    print("\n🚀 Running E2E Tests\n")
    print(f"Command: {' '.join(cmd)}\n")
    
    # Run pytest
    result = subprocess.run(cmd)
    
    return result.returncode


def seed_test_data():
    """Seed test data before running tests"""
    print("\n🌱 Seeding test data...\n")
    
    script_path = os.path.join("tests", "fixtures", "seed_test_data.py")
    
    result = subprocess.run([sys.executable, script_path])
    
    if result.returncode == 0:
        print("\n✅ Test data seeded successfully\n")
    else:
        print("\n❌ Failed to seed test data\n")
        return False
    
    return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Run E2E Selenium tests")
    
    # Test selection
    parser.add_argument(
        "test_path",
        nargs="?",
        help="Specific test file or directory to run"
    )
    parser.add_argument(
        "-k", "--test-name",
        help="Run tests matching the given substring expression"
    )
    parser.add_argument(
        "-m", "--marker",
        help="Run tests with specific marker (auth, student, mentor, etc.)"
    )
    
    # Browser configuration
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run tests in headless mode"
    )
    
    # URLs
    parser.add_argument(
        "--base-url",
        default="http://localhost:5173",
        help="Base URL for the application (default: http://localhost:5173)"
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:8000",
        help="API base URL (default: http://localhost:8000)"
    )
    
    # Execution options
    parser.add_argument(
        "-n", "--parallel",
        type=int,
        help="Run tests in parallel with N workers"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--html-report",
        action="store_true",
        help="Generate HTML report"
    )
    
    # Data seeding
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Seed test data before running tests"
    )
    
    # Quick test suites
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run smoke tests only"
    )
    parser.add_argument(
        "--auth",
        action="store_true",
        help="Run authentication tests only"
    )
    parser.add_argument(
        "--student",
        action="store_true",
        help="Run student flow tests only"
    )
    parser.add_argument(
        "--mentor",
        action="store_true",
        help="Run mentor flow tests only"
    )
    
    args = parser.parse_args()
    
    # Seed data if requested
    if args.seed:
        if not seed_test_data():
            return 1
    
    # Set marker for quick suites
    if args.smoke:
        args.marker = "smoke"
    elif args.auth:
        args.marker = "auth"
    elif args.student:
        args.marker = "student"
    elif args.mentor:
        args.marker = "mentor"
    
    # Run tests
    return run_tests(args)


if __name__ == "__main__":
    sys.exit(main())
