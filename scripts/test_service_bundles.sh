#!/bin/bash
# Script to run tests for service bundle functionality

echo "Running service bundle tests..."
pytest -xvs tests/test_service_bundles.py

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All service bundle tests passed!"
else
    echo "Some tests failed. Please check the output above for details."
    exit 1
fi

echo "Service bundle functionality is working correctly."