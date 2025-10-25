#!/usr/bin/env python3
"""
Integration test for Password Manager + PDF Unlocker
"""
import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from password_manager import PasswordManager
from pdf_unlocker import PdfUnlocker
from test_runner import run_test_suite

def test_integration():
    print("🔗 Testing Password Manager + PDF Unlocker Integration")
    print("=" * 60)
    
    # Initialize both components
    password_manager = PasswordManager()
    unlocker = PdfUnlocker()
    
    # Test 1: Password Manager functionality
    print("\n1. Testing Password Manager...")
    passwords = password_manager.get_passwords()
    categories = password_manager.list_categories()
    print(f"   ✅ Loaded {len(passwords)} passwords from {len(categories)} categories")
    
    # Test 2: Check PDF files
    print("\n2. Checking PDF files...")
    pdf_files = list(unlocker.input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("   ❌ No PDF files found in input directory")
        print("   Please add PDF files to 'pdf_files/input/' folder")
        return
    
    print(f"   ✅ Found {len(pdf_files)} PDF file(s):")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"      {i}. {pdf_file.name}")
    
    # Test 3: Test individual PDF processing
    print("\n3. Testing individual PDF processing...")
    for pdf_file in pdf_files:
        print(f"\n   Processing: {pdf_file.name}")
        
        # Check if PDF is encrypted
        is_encrypted = unlocker.is_pdf_encrypted(str(pdf_file))
        print(f"      Encrypted: {'Yes' if is_encrypted else 'No'}")
        
        if is_encrypted:
            # Try to unlock with passwords
            success, password = unlocker.unlock_pdf(str(pdf_file), passwords)
            if success:
                print(f"      ✅ Successfully unlocked with password: {password}")
            else:
                print(f"      ❌ Failed to unlock - no matching password found")
        else:
            print(f"      ℹ️  PDF is not encrypted - will be copied to unlocked folder")
    
    # Test 4: Process all PDFs
    print("\n4. Processing all PDFs...")
    results = unlocker.process_all_pdfs(passwords)
    
    # Test 5: Show results
    print("\n5. Results summary:")
    successful = 0
    failed = 0
    
    for pdf_name, success in results.items():
        status = "✅ Success" if success else "❌ Failed"
        print(f"   {pdf_name}: {status}")
        if success:
            successful += 1
        else:
            failed += 1
    
    # Test 6: Check unlocked folder
    print("\n6. Checking unlocked folder...")
    unlocked_files = list(unlocker.unlocked_dir.glob("*.pdf"))
    print(f"   📁 Unlocked folder contains {len(unlocked_files)} file(s):")
    for file in unlocked_files:
        print(f"      - {file.name}")
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 INTEGRATION TEST SUMMARY")
    print(f"   PDFs processed: {len(pdf_files)}")
    print(f"   Successful: {successful}")
    print(f"   Failed: {failed}")
    print(f"   Passwords tried: {len(passwords)}")
    print(f"   Files in unlocked folder: {len(unlocked_files)}")
    
    if successful > 0:
        print("   ✅ Integration test PASSED!")
        return True  # Integration test passed
    else:
        print("   ⚠️  No PDFs were successfully processed")
        return False  # Integration test failed

if __name__ == "__main__":
    # Define all tests in one place
    test_functions = [
        ("integration", ["full"], test_integration, "Test complete integration workflow")
    ]
    
    # Run the test suite
    run_test_suite("Integration", "Test complete integration workflow", test_functions)
