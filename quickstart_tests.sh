#!/bin/bash
# Quick Start Script for E2E Test Suite
# Unix/Linux/Mac shell script to set up and run tests

echo "================================================"
echo "  Cohort Web App - E2E Test Suite Quick Start"
echo "================================================"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

echo "[1/5] Installing test dependencies..."
echo ""
pip install -r tests/requirements-test.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[2/5] Checking backend server..."
echo ""
if ! curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo "WARNING: Backend server is not running on port 8000"
    echo "Please start the Django backend:"
    echo "  cd backend"
    echo "  python manage.py runserver"
    echo ""
fi

echo "[3/5] Checking frontend server..."
echo ""
if ! curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo "WARNING: Frontend server is not running on port 5173"
    echo "Please start the React frontend:"
    echo "  npm run dev"
    echo ""
fi

echo "[4/5] Seeding test data..."
echo ""
python tests/fixtures/seed_test_data.py
if [ $? -ne 0 ]; then
    echo "WARNING: Test data seeding failed"
    echo "You may need to run migrations first:"
    echo "  cd backend"
    echo "  python manage.py migrate"
    echo ""
fi

echo ""
echo "[5/5] Ready to run tests!"
echo ""
echo "================================================"
echo "  Test Suite Ready"
echo "================================================"
echo ""
echo "Quick Commands:"
echo ""
echo "  Run all tests:"
echo "    python run_tests.py"
echo ""
echo "  Run in headless mode:"
echo "    python run_tests.py --headless"
echo ""
echo "  Run specific suite:"
echo "    python run_tests.py --auth"
echo "    python run_tests.py --student"
echo "    python run_tests.py --mentor"
echo ""
echo "  Generate HTML report:"
echo "    python run_tests.py --html-report"
echo ""
echo "  Run with parallel execution:"
echo "    python run_tests.py -n 4"
echo ""
echo "================================================"
echo ""

read -p "Do you want to run the tests now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running tests..."
    python run_tests.py
fi

echo ""
echo "For more information, see tests/README.md"
echo ""
