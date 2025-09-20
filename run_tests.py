#!/usr/bin/env python3
"""
Test runner for the AI Compliance Co-Pilot application.
Runs all automated tests and provides comprehensive reporting.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def run_tests(test_type="all", verbose=False, coverage=False):
    """
    Run automated tests for the application.
    
    Args:
        test_type (str): Type of tests to run ('all', 'unit', 'integration', 'e2e')
        verbose (bool): Enable verbose output
        coverage (bool): Generate coverage report
    """
    
    # Add src to Python path
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # Test directory
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    
    # Base pytest command
    cmd = ['python', '-m', 'pytest']
    
    if verbose:
        cmd.append('-v')
    
    if coverage:
        cmd.extend(['--cov=src', '--cov-report=html', '--cov-report=term'])
    
    # Add test directory
    cmd.append(test_dir)
    
    # Run specific test types
    if test_type == "unit":
        cmd.extend(['-k', 'not integration and not e2e'])
    elif test_type == "integration":
        cmd.extend(['-k', 'integration'])
    elif test_type == "e2e":
        cmd.extend(['-k', 'e2e'])
    
    print(f"Running {test_type} tests...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("\n" + "=" * 50)
        print("✅ All tests passed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 50)
        print("❌ Some tests failed!")
        print(f"Exit code: {e.returncode}")
        return False
    except FileNotFoundError:
        print("❌ pytest not found. Please install it with: pip install pytest")
        return False

def run_linting():
    """Run code linting checks."""
    print("Running code linting...")
    print("-" * 30)
    
    try:
        # Run flake8 if available
        result = subprocess.run(['python', '-m', 'flake8', 'src/', '--max-line-length=100'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Linting passed!")
            return True
        else:
            print("❌ Linting issues found:")
            print(result.stdout)
            return False
    except FileNotFoundError:
        print("⚠️  flake8 not found. Install with: pip install flake8")
        return True

def run_type_checking():
    """Run type checking with mypy."""
    print("Running type checking...")
    print("-" * 30)
    
    try:
        result = subprocess.run(['python', '-m', 'mypy', 'src/'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Type checking passed!")
            return True
        else:
            print("❌ Type checking issues found:")
            print(result.stdout)
            return False
    except FileNotFoundError:
        print("⚠️  mypy not found. Install with: pip install mypy")
        return True

def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run tests for AI Compliance Co-Pilot")
    parser.add_argument('--type', choices=['all', 'unit', 'integration', 'e2e'], 
                       default='all', help='Type of tests to run')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose output')
    parser.add_argument('--coverage', '-c', action='store_true', 
                       help='Generate coverage report')
    parser.add_argument('--lint', action='store_true', 
                       help='Run linting checks')
    parser.add_argument('--type-check', action='store_true', 
                       help='Run type checking')
    parser.add_argument('--all', action='store_true', 
                       help='Run all checks (tests, linting, type checking)')
    
    args = parser.parse_args()
    
    print("🧪 AI Compliance Co-Pilot Test Suite")
    print("=" * 50)
    
    success = True
    
    # Run tests
    if args.all or not any([args.lint, args.type_check]):
        test_success = run_tests(args.type, args.verbose, args.coverage)
        success = success and test_success
    
    # Run linting
    if args.all or args.lint:
        lint_success = run_linting()
        success = success and lint_success
    
    # Run type checking
    if args.all or args.type_check:
        type_success = run_type_checking()
        success = success and type_success
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All checks passed! The application is ready for deployment.")
        sys.exit(0)
    else:
        print("💥 Some checks failed. Please fix the issues before deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main()
