@echo off
REM Quick Start Script for E2E Test Suite
REM Windows batch file to set up and run tests

echo ================================================
echo   Cohort Web App - E2E Test Suite Quick Start
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher
    pause
    exit /b 1
)

echo [1/5] Installing test dependencies...
echo.
pip install -r tests\requirements-test.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/5] Checking backend server...
echo.
curl -s http://localhost:8000 >nul 2>&1
if errorlevel 1 (
    echo WARNING: Backend server is not running on port 8000
    echo Please start the Django backend:
    echo   cd backend
    echo   python manage.py runserver
    echo.
)

echo [3/5] Checking frontend server...
echo.
curl -s http://localhost:5173 >nul 2>&1
if errorlevel 1 (
    echo WARNING: Frontend server is not running on port 5173
    echo Please start the React frontend:
    echo   npm run dev
    echo.
)

echo [4/5] Seeding test data...
echo.
python tests\fixtures\seed_test_data.py
if errorlevel 1 (
    echo WARNING: Test data seeding failed
    echo You may need to run migrations first:
    echo   cd backend
    echo   python manage.py migrate
    echo.
)

echo.
echo [5/5] Ready to run tests!
echo.
echo ================================================
echo   Test Suite Ready
echo ================================================
echo.
echo Quick Commands:
echo.
echo   Run all tests:
echo     python run_tests.py
echo.
echo   Run in headless mode:
echo     python run_tests.py --headless
echo.
echo   Run specific suite:
echo     python run_tests.py --auth
echo     python run_tests.py --student
echo     python run_tests.py --mentor
echo.
echo   Generate HTML report:
echo     python run_tests.py --html-report
echo.
echo   Run with parallel execution:
echo     python run_tests.py -n 4
echo.
echo ================================================
echo.

choice /C YN /M "Do you want to run the tests now"
if errorlevel 2 goto end
if errorlevel 1 goto runtests

:runtests
echo.
echo Running tests...
python run_tests.py
goto end

:end
echo.
echo For more information, see tests\README.md
echo.
pause
