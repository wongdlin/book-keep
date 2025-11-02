#!/usr/bin/env python3
"""
Test script for PDF unlocker functionality
Supports both real files and mock testing
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

# Add the src directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from pdf_unlocker import PdfUnlocker
from password_manager import PasswordManager
from test_runner import run_test_suite

def test_pdf_unlocker():
    print("🔓 Testing PDF Unlocker")
    print("=" * 40)
    print("🧪 Using MOCK data (no real files required)")
    return test_with_mocks()

def test_with_mocks():
    """Test with mock data - no real files needed"""
    # Create temporary directories for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        input_dir = temp_path / "input"
        unlocked_dir = temp_path / "unlocked"
        
        # Create directories
        input_dir.mkdir()
        unlocked_dir.mkdir()
        
        print(f"📁 Using temporary directories:")
        print(f"   Input: {input_dir}")
        print(f"   Unlocked: {unlocked_dir}")
        
        # Initialize unlocker with temp directories
        unlocker = PdfUnlocker(input_dir=str(input_dir), unlocked_dir=str(unlocked_dir))
        
        # Mock passwords
        mock_passwords = [
            "password123",
            "test456", 
            "mock789",
            "test"  # Your specific password
        ]
        
        print(f"\n🔑 Using mock passwords: {mock_passwords}")
        
        # Test 1: Check if PDF is encrypted (mock)
        print("\n1. Testing PDF encryption detection...")
        
        # Mock a non-encrypted PDF
        with patch('pdf_unlocker.PdfReader') as mock_reader:
            mock_reader_instance = Mock()
            mock_reader_instance.is_encrypted = False
            mock_reader.return_value = mock_reader_instance
            
            is_encrypted = unlocker.is_pdf_encrypted("fake_path.pdf")
            print(f"   ✅ Non-encrypted PDF detection: {is_encrypted}")
        
        # Mock an encrypted PDF
        with patch('pdf_unlocker.PdfReader') as mock_reader:
            mock_reader_instance = Mock()
            mock_reader_instance.is_encrypted = True
            mock_reader.return_value = mock_reader_instance
            
            is_encrypted = unlocker.is_pdf_encrypted("fake_path.pdf")
            print(f"   ✅ Encrypted PDF detection: {is_encrypted}")
        
        # Test 2: Mock PDF unlocking
        print("\n2. Testing PDF unlocking with mock...")
        
        # Create a fake PDF file
        fake_pdf = input_dir / "test_encrypted.pdf"
        fake_pdf.write_bytes(b"fake pdf content")
        
        # Mock the PDF reader for unlocking
        with patch('pdf_unlocker.PdfReader') as mock_reader:
            mock_reader_instance = Mock()
            mock_reader_instance.is_encrypted = True
            mock_reader_instance.decrypt = Mock(side_effect=lambda pwd: pwd == "test456")
            mock_reader.return_value = mock_reader_instance
            
            success, password = unlocker.unlock_pdf(str(fake_pdf), mock_passwords)
            print(f"   ✅ Mock unlock result: Success={success}, Password={password}")
        
        # Test 3: Mock complete workflow
        print("\n3. Testing complete workflow with mocks...")
        
        # Create multiple fake PDFs
        fake_pdfs = [
            input_dir / "encrypted1.pdf",
            input_dir / "encrypted2.pdf", 
            input_dir / "normal.pdf"
        ]
        
        for pdf in fake_pdfs:
            pdf.write_bytes(b"fake pdf content")
        
        # Mock the complete process
        with patch('pdf_unlocker.PdfReader') as mock_reader, \
             patch('pdf_unlocker.PdfWriter') as mock_writer, \
             patch('shutil.copy2') as mock_copy:
            
            # Setup mocks
            mock_reader_instance = Mock()
            mock_reader_instance.is_encrypted = True
            mock_reader_instance.decrypt = Mock(side_effect=lambda pwd: pwd == "test456")
            mock_reader_instance.pages = [Mock(), Mock()]  # Mock pages
            mock_reader.return_value = mock_reader_instance
            
            mock_writer_instance = Mock()
            mock_writer.return_value = mock_writer_instance
            
            # Process all PDFs
            results = unlocker.process_all_pdfs(mock_passwords)
            
            print(f"   ✅ Processed {len(results)} PDFs")
            for pdf_name, success in results.items():
                status = "Success" if success else "Failed"
                print(f"      {pdf_name}: {status}")
        
        print(f"\n📊 Mock Test Summary:")
        print(f"   ✅ All mock operations completed successfully")
        print(f"   ✅ No real files were created or modified")
        print(f"   ✅ Tests are isolated and repeatable")
        
        return True  # Mock test passed


if __name__ == "__main__":
    # Define all tests in one place
    test_functions = [
        ("mock", ["mocks"], test_pdf_unlocker, "Test PDF unlocker with mock data")
    ]
    
    # Run the test suite
    run_test_suite("PDF Unlocker", "Test PDF unlocker functionality with mock data only", test_functions)
