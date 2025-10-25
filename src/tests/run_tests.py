#!/usr/bin/env python3
"""
Test runner for all BookKeep tests
"""
import subprocess
import sys
from pathlib import Path

def run_test(test_file):
    """Run a single test file and return success status"""
    print(f"\n{'='*60}")
    print(f"🧪 Running: {test_file}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=False, 
                              text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return False

def main():
    print("🚀 BookKeep Test Suite")
    print("=" * 60)
    
    # Define test files in order
    test_files = [
        "src/tests/test_password_manager.py",
        "src/tests/test_pdf_unlocker.py", 
        "src/tests/test_integration.py"
    ]
    
    # Check if test files exist
    existing_tests = []
    for test_file in test_files:
        if Path(test_file).exists():
            existing_tests.append(test_file)
        else:
            print(f"⚠️  Test file not found: {test_file}")
    
    if not existing_tests:
        print("❌ No test files found!")
        return
    
    print(f"📋 Found {len(existing_tests)} test file(s) to run")
    
    # Run all tests
    results = []
    for test_file in existing_tests:
        success = run_test(test_file)
        results.append((test_file, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    failed = 0
    
    for test_file, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {test_file}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
