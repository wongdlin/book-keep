#!/usr/bin/env python3
"""
Unit tests for TransactionExtractor
"""
import sys
import os
import re
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from transaction_extractor import TransactionExtractor
from PyPDF2 import PdfReader
from test_runner import run_test_suite

def test_pdf_text_extraction():
    """Test extracting raw text from PDF to see what we're working with."""
    print("🔍 Testing PDF Text Extraction")
    print("=" * 50)
    
    # Path to the unlocked PDF
    pdf_path = Path("pdf_files/unlocked/tng_ewallet_transactions.pdf")
    
    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    try:
        reader = PdfReader(pdf_path)
        print(f"📄 PDF has {len(reader.pages)} pages")
        
        # Extract text from first few pages to see the format
        all_text = ""
        for i, page in enumerate(reader.pages[:3]):  # First 3 pages
            text = page.extract_text()
            all_text += text + "\n"
            print(f"\n📄 Page {i+1} text (first 500 chars):")
            print("-" * 30)
            print(text[:500])
            print("-" * 30)
        
        # Look for transaction-like lines
        lines = all_text.split('\n')
        print(f"\n🔍 Looking for transaction patterns in {len(lines)} lines...")
        
        transaction_like_lines = []
        for i, line in enumerate(lines):
            line = line.strip()
            if 'Success' in line and 'RM' in line and '/' in line:
                transaction_like_lines.append((i+1, line))
                if len(transaction_like_lines) <= 10:  # Show first 10 matches
                    print(f"Line {i+1}: {line}")
        
        print(f"\n📊 Found {len(transaction_like_lines)} potential transaction lines")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return False

def test_transaction_pattern_matching():
    """Test the regex pattern against sample transaction lines."""
    print("\n🔍 Testing Transaction Pattern Matching")
    print("=" * 50)
    
    extractor = TransactionExtractor()
    
    # Real transaction lines from the actual PDF (from debug_pdf_text.txt)
    sample_lines = [
        # Line 15 from debug file - DuitNow QR
        "30/9/2025 Success DuitNow QR 20250930101 10000010000 TNGOW3MY1 71120417717 025Day By Day NanYang 202509302112128001001711213020 74677RM15.00 RM0.00",
        # Line 21 from debug file - Reload  
        "30/9/2025 Success Reload 20250930101 10000010000 TNGOW3MY1 71120417717 023Quick Reload Payment (via GO+ Balance)202509301310030580397517900120 RM15.00 RM15.00",
        # Line 27 from debug file - Payment
        "30/9/2025 Success Payment 20250930101 10000010000 TNGOW3MY1 71120417681 793Parking 202509302112128001001711207020 21216RM2.00 RM0.00",
        # Line 39 from debug file - eWallet Cash Out
        "29/9/2025 Success eWallet Cash Out 20250929131 00305798298 31400120Via eWallet to GO+ 202509291310040571721858600120 RM10.50 RM0.00",
        # Multi-line Receive from Wallet transaction (lines 44-48 from debug file)
        "29/9/2025 Success Receive from Wallet 20250929111 21700010300 17151748357 2000WONG ZING ONN 2025092910110000010000TNGOW3 MY171517416347008RM10.50 RM10.50",
        # Line 65 from debug file - DuitNow QR TNGD
        "29/9/2025 Success DuitNow QR TNGD 20250929101 10000010000 TNGOW3MY1 71120417442 629SEDAPNYA RESOURCES (PUCHONG) SDN. BHD.202509292112128001001711245019 02091RM61.65 RM0.00",
        # Line 81 from debug file - DUITNOW_RECEIVEFROM
        "29/9/2025 Success DUITNOW_RECEIVEFROM20250929111 21700010100 17112044383 9561Jawahar Ganesh A/L Murali 2025092910110000010000TNGOW3 MY171120417435510RM10.50 RM10.50",
        # Line 1072 from debug file - GO+ Daily Earnings
        "30/9/2025 Success GO+ Daily Earnings MMF2025093 01310030580 03235340012 0Daily Interest 202509301310040572155300200120 RM0.0139 RM157.16",
        # Line 1077 from debug file - GO+ Cash In
        "29/9/2025 Success GO+ Cash In MMF2025092 91310030579 82983140012 0Via eWallet to GO+ 202509291310040571721858600120 RM10.50 RM157.15"
    ]
    
    print("Testing pattern against sample lines:")
    matches = 0
    detected_types = set()
    expected_outputs = [
        "30/9/2025,Success,DuitNow QR,15.00,0.00",
        "30/9/2025,Success,Reload,15.00,15.00", 
        "30/9/2025,Success,Payment,2.00,0.00",
        "29/9/2025,Success,eWallet Cash Out,10.50,0.00",
        "29/9/2025,Success,Receive from Wallet,10.50,10.50",  # This is the key test case
        "29/9/2025,Success,DuitNow QR TNGD,61.65,0.00",
        "29/9/2025,Success,DUITNOW_RECEIVEFROM,10.50,10.50",
        "30/9/2025,Success,GO+ Daily Earnings,0.0139,157.16",
        "29/9/2025,Success,GO+ Cash In,10.50,157.15"
    ]
        
    for i, line in enumerate(sample_lines, 1):
        print(f"\nLine {i}: {line}")
        match = extractor.transaction_pattern.match(line)
        if not match:
            match = extractor.transaction_pattern_alt.match(line)
        
        if match:
            print("✅ MATCH FOUND!")
            print(f"  Date: {match.group(1)}")
            print(f"  Status: {match.group(2)}")
            print(f"  Middle Part: {match.group(3)}")
            
            if len(match.groups()) == 5:
                amount = match.group(4)
                balance = match.group(5)
                middle_part = match.group(3)
            else:
                # Alternative pattern
                amount_with_rm = match.group(4)
                balance = match.group(5)
                middle_part = match.group(3)
                amount = amount_with_rm
            
            print(f"DEBUG: Original amount: '{amount}'")
            
            # Apply the same cleaning logic as in the extractor
            if 'RM' in amount:
                # Find the last occurrence of RM and take everything after it
                last_rm_index = amount.rfind('RM')
                if last_rm_index != -1:
                    amount = amount[last_rm_index + 2:]  # Take everything after 'RM'
                    print(f"DEBUG: Cleaned amount: '{amount}'")
            
            print(f"  Amount: {amount}")
            print(f"  Balance: {balance}")
            
            # Test transaction type detection
            transaction_type = ""
            
            # Look for all transaction types (order matters - more specific first)
            if "Payment Cancelled" in middle_part:
                transaction_type = "Payment Cancelled"
            elif "GO+ Daily Earnings" in middle_part:
                transaction_type = "GO+ Daily Earnings"
            elif "GO+ Cash In" in middle_part:
                transaction_type = "GO+ Cash In"
            elif "DuitNow QR TNGD" in middle_part:
                transaction_type = "DuitNow QR TNGD"
            elif "DUITNOW_RECEIVEFROM" in middle_part:
                transaction_type = "DUITNOW_RECEIVEFROM"
            elif "Transfer to Wallet" in middle_part:
                transaction_type = "Transfer to Wallet"
            elif "Receive from Wallet" in middle_part:
                transaction_type = "Receive from Wallet"
            elif "eWallet Cash Out" in middle_part:
                transaction_type = "eWallet Cash Out"
            elif "DuitNow QR" in middle_part:
                transaction_type = "DuitNow QR"
            elif "Reload" in middle_part:
                transaction_type = "Reload"
            elif middle_part.strip().startswith("Payment") and "Reload" not in middle_part:
                transaction_type = "Payment"
            else:
                parts = middle_part.split()
                transaction_type = " ".join(parts[:3]) if len(parts) >= 3 else " ".join(parts)
            
            print(f"  Detected Type: {transaction_type}")
            
            # Create the actual output
            actual_output = f"{match.group(1)},{match.group(2)},{transaction_type},{amount},{balance}"
            expected_output = expected_outputs[i-1]
            
            print(f"  Expected: {expected_output}")
            print(f"  Actual:   {actual_output}")
            
            if actual_output == expected_output:
                print("  ✅ CORRECT")
                matches += 1
            else:
                print("  ❌ INCORRECT")
            
            detected_types.add(transaction_type)
        else:
            print("❌ NO MATCH")
            # Let's see what parts we can identify
            parts = line.split()
            print(f"  Parts: {len(parts)}")
            for j, part in enumerate(parts):
                print(f"    {j}: '{part}'")
    
    print(f"\n📊 Pattern matching results: {matches}/{len(sample_lines)} lines matched correctly")
    print(f"📊 Detected transaction types: {sorted(detected_types)}")
    return matches == len(sample_lines)

def test_reconstruct_transaction_lines():
    """Test reconstructing transaction lines from PDF text."""
    print("\n🔍 Testing Transaction Line Reconstruction")
    print("=" * 50)
    
    extractor = TransactionExtractor()
    pdf_path = Path("pdf_files/unlocked/tng_ewallet_transactions.pdf")
    
    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        all_text = ""
        for page in reader.pages:
            all_text += page.extract_text() + "\n"
        
        lines = all_text.split('\n')
        print(f"📄 Processing {len(lines)} lines from PDF")
        
        # Show how we reconstruct transaction lines
        i = 0
        reconstructed_count = 0
        while i < len(lines) and reconstructed_count < 5:  # Show first 5
            line = lines[i].strip()
            
            if re.match(r'^\d{1,2}/\d{1,2}/\d{4}', line):
                transaction_lines = [line]
                j = i + 1
                
                # Collect subsequent lines until we find the amount and balance
                while j < len(lines) and not re.search(r'RM[\d,]+\.?\d*\s+RM[\d,]+\.?\d*$', lines[j]):
                    next_line = lines[j].strip()
                    if next_line:
                        transaction_lines.append(next_line)
                    j += 1
                
                if j < len(lines):
                    transaction_lines.append(lines[j].strip())
                
                full_transaction = ' '.join(transaction_lines)
                print(f"\nReconstructed transaction {reconstructed_count + 1}:")
                print(f"  Original lines: {len(transaction_lines)}")
                print(f"  Full text: {full_transaction}")
                
                # Test if it matches our pattern
                match = extractor.transaction_pattern.match(full_transaction)
                if match:
                    print("  ✅ MATCHES PATTERN!")
                else:
                    print("  ❌ Does not match pattern")
                
                reconstructed_count += 1
                i = j + 1
            else:
                i += 1
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_extract_transactions_from_pdf():
    """Test extracting transactions from the actual PDF."""
    print("\n🔍 Testing Transaction Extraction from PDF")
    print("=" * 50)
    
    extractor = TransactionExtractor()
    pdf_path = Path("pdf_files/unlocked/tng_ewallet_transactions.pdf")
    
    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    try:
        # Extract text from PDF
        reader = PdfReader(pdf_path)
        all_text = ""
        for page in reader.pages:
            all_text += page.extract_text() + "\n"
        
        print(f"📄 Extracted {len(all_text)} characters of text")
        
        # Extract transactions
        transactions = extractor.extract_transactions_from_text(all_text)
        
        print(f"📊 Found {len(transactions)} transactions")
        
        if transactions:
            print("\nFirst 5 transactions:")
            for i, tx in enumerate(transactions[:5]):
                print(f"\nTransaction {i+1}:")
                for key, value in tx.items():
                    print(f"  {key}: {value}")
        
        return len(transactions) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Define test functions with aliases and descriptions
    test_functions = [
        ("pdf_extraction", ["pdf", "text"], test_pdf_text_extraction, "Extract raw text from PDF to see format"),
        ("pattern_matching", ["pattern", "regex"], test_transaction_pattern_matching, "Test regex pattern against sample lines"),
        ("reconstruction", ["reconstruct", "lines"], test_reconstruct_transaction_lines, "Test reconstructing transaction lines from PDF text"),
        ("extraction", ["extract", "transactions"], test_extract_transactions_from_pdf, "Test extracting transactions from actual PDF")
    ]
    
    # Run the test suite
    run_test_suite(
        test_name="Transaction Extractor",
        description="Unit tests for PDF transaction extraction functionality",
        test_functions=test_functions
    )
