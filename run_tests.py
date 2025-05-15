#!/usr/bin/env python3
"""
Test Runner Script for Township Connect WhatsApp Assistant.

This script runs the test suite and displays the results.
"""

import os
import sys
import subprocess
import argparse

def main():
    """Run the test suite."""
    parser = argparse.ArgumentParser(description="Run Township Connect tests")
    parser.add_argument("--smoke", action="store_true", help="Run only smoke tests")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration", action="store_true", help="Run only integration tests")
    parser.add_argument("--language", action="store_true", help="Run only language tests")
    parser.add_argument("--payment", action="store_true", help="Run only payment tests")
    parser.add_argument("--database", action="store_true", help="Run only database tests")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()
    
    # Build the pytest command
    cmd = ["pytest"]
    
    # Add markers if specified
    markers = []
    if args.smoke:
        markers.append("smoke")
    if args.unit:
        markers.append("unit")
    if args.integration:
        markers.append("integration")
    if args.language:
        markers.append("language")
    if args.payment:
        markers.append("payment")
    if args.database:
        markers.append("database")
    
    if markers:
        cmd.append("-m")
        cmd.append(" or ".join(markers))
    
    # Add coverage if specified
    if args.coverage:
        cmd.append("--cov=src")
        cmd.append("--cov-report=term")
        cmd.append("--cov-report=html")
    
    # Add verbose flag if specified
    if args.verbose:
        cmd.append("-v")
    
    # Add the tests directory
    cmd.append("tests/")
    
    # Print the command
    print(f"Running: {' '.join(cmd)}")
    
    # Run the tests
    result = subprocess.run(cmd)
    
    # Return the exit code
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())