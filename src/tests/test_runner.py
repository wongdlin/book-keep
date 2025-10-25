#!/usr/bin/env python3
"""
Reusable test runner framework for all test files
Provides --filter functionality and common test utilities
"""
import sys
import argparse
from typing import Dict, Callable, List, Tuple

class TestRunner:
    def __init__(self, test_name: str, description: str = ""):
        self.test_name = test_name
        self.description = description
        self.tests: Dict[str, Callable] = {}
        self.parser = argparse.ArgumentParser(description=f'{test_name} Test Suite')
        self._setup_arguments()
    
    def _setup_arguments(self):
        """Setup command line arguments"""
        self.parser.add_argument('--filter', '-f', 
                               help='Filter tests to run (use --list to see available filters)')
        self.parser.add_argument('--list', '-l', action='store_true', 
                               help='List available test filters')
        self.parser.add_argument('--verbose', '-v', action='store_true', 
                               help='Verbose output')
        self.parser.add_argument('--help-tests', action='store_true',
                               help='Show detailed help for available tests')
    
    def add_test(self, name: str, aliases: List[str], test_func: Callable, description: str = ""):
        """Add a test to the runner"""
        test_key = name.lower()
        self.tests[test_key] = test_func
        
        # Add aliases
        for alias in aliases:
            self.tests[alias.lower()] = test_func
        
        # Store description for help
        if not hasattr(self, 'test_descriptions'):
            self.test_descriptions = {}
        self.test_descriptions[test_key] = description
    
    def list_tests(self):
        """List available tests"""
        print(f"Available test filters for {self.test_name}:")
        print("=" * 50)
        
        # Group tests by their main name
        main_tests = {}
        for key, func in self.tests.items():
            # Find the main test name (first one added)
            main_name = None
            for main_key, main_func in self.tests.items():
                if main_func == func and main_key in self.test_descriptions:
                    main_name = main_key
                    break
            
            if main_name and main_name not in main_tests:
                main_tests[main_name] = {
                    'func': func,
                    'description': self.test_descriptions.get(main_name, ''),
                    'aliases': []
                }
        
        for main_name, info in main_tests.items():
            # Find all aliases for this test
            aliases = [key for key, func in self.tests.items() 
                      if func == info['func'] and key != main_name]
            
            alias_str = f" (aliases: {', '.join(aliases)})" if aliases else ""
            print(f"  {main_name}{alias_str:<20} - {info['description']}")
        
        print(f"\nExamples:")
        print(f"  python src/tests/test_{self.test_name.lower()}.py --filter init")
        print(f"  python src/tests/test_{self.test_name.lower()}.py -f encrypt")
        print(f"  python src/tests/test_{self.test_name.lower()}.py --filter category")
    
    def run_test(self, test_name: str) -> bool:
        """Run a specific test"""
        test_key = test_name.lower()
        
        if test_key not in self.tests:
            print(f"❌ Unknown test filter: {test_name}")
            print("Use --list to see available filters")
            return False
        
        print(f"🔑 Running {test_name.title()} Test Only")
        print("=" * 40)
        
        try:
            result = self.tests[test_key]()
            print(f"\nResult: {'✅ PASSED' if result else '❌ FAILED'}")
            return result
        except Exception as e:
            print(f"\nResult: ❌ FAILED - {e}")
            return False
    
    def run_all_tests(self, test_functions: List[Tuple[str, Callable]]) -> bool:
        """Run all tests with summary"""
        print(f"🔑 Testing {self.test_name} - Comprehensive Unit Tests")
        print("=" * 60)
        
        test_results = []
        
        for test_name, test_func in test_functions:
            print(f"\n{test_name}...")
            try:
                result = test_func()
                test_results.append((test_name, result))
                status = "✅ PASSED" if result else "❌ FAILED"
                print(f"   {status}")
            except Exception as e:
                test_results.append((test_name, False))
                print(f"   ❌ FAILED - {e}")
        
        # Print results summary
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = 0
        failed = 0
        
        for test_name, result in test_results:
            if result:
                print(f"✅ PASSED - {test_name}")
                passed += 1
            else:
                print(f"❌ FAILED - {test_name}")
                failed += 1
        
        print(f"\n📈 Total: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("🎉 All tests passed!")
        else:
            print(f"⚠️  {failed} test(s) failed!")
        
        return failed == 0
    
    def run(self, test_functions: List[Tuple[str, Callable]]):
        """Main entry point for running tests"""
        args = self.parser.parse_args()
        
        # List available tests
        if args.list or args.help_tests:
            self.list_tests()
            sys.exit(0)
        
        # Run specific test if filter is provided
        if args.filter:
            success = self.run_test(args.filter)
            sys.exit(0 if success else 1)
        else:
            # Run all tests
            success = self.run_all_tests(test_functions)
            sys.exit(0 if success else 1)

# Convenience function for quick setup
def create_test_runner(test_name: str, description: str = "") -> TestRunner:
    """Create a new test runner instance"""
    return TestRunner(test_name, description)

def setup_test_suite(test_name: str, description: str, test_functions: List[Tuple[str, List[str], Callable, str]]):
    """
    Setup a complete test suite with minimal boilerplate
    
    Args:
        test_name: Name of the test suite
        description: Description of the test suite
        test_functions: List of (name, aliases, function, description) tuples
    """
    runner = create_test_runner(test_name, description)
    
    # Add all tests
    for name, aliases, func, desc in test_functions:
        runner.add_test(name, aliases, func, desc)
    
    # Create all_tests list for running all at once
    all_tests = [(name.title(), func) for name, _, func, _ in test_functions]
    
    return runner, all_tests

def run_test_suite(test_name: str, description: str, test_functions: List[Tuple[str, List[str], Callable, str]]):
    """
    Complete test suite setup and execution in one call
    
    Args:
        test_name: Name of the test suite
        description: Description of the test suite  
        test_functions: List of (name, aliases, function, description) tuples
    """
    runner, all_tests = setup_test_suite(test_name, description, test_functions)
    runner.run(all_tests)
