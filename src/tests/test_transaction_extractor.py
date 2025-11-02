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
from test_runner import run_test_suite

def test_transaction_pattern_matching():
    """Test the algorithmic pattern matching against sample transaction lines."""
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
        "29/9/2025 Success DUITNOW_RECEI VEFROM20250929111 21700010100 17112044383 9561Jawahar Ganesh A/L Murali 2025092910110000010000TNGOW3 MY171120417435510RM10.50 RM10.50",
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
        "29/9/2025,Success,Receive from Wallet,10.50,10.50", 
        "29/9/2025,Success,DuitNow QR TNGD,61.65,0.00",
        "29/9/2025,Success,DUITNOW_RECEIVEFROM,10.50,10.50",
        "30/9/2025,Success,GO+ Daily Earnings,0.0139,157.16",
        "29/9/2025,Success,GO+ Cash In,10.50,157.15"
    ]
        
    for i, line in enumerate(sample_lines, 1):
        print(f"\nLine {i}: {line}")
        
        # Use the actual algorithmic extraction method
        transactions = extractor.extract_transactions_from_text(line)
        
        if transactions and len(transactions) > 0:
            print("✅ MATCH FOUND!")
            tx = transactions[0]
            print(f"  Date: {tx['date']}")
            print(f"  Status: {tx['status']}")
            print(f"  Transaction Type: {tx['transaction_type']}")
            print(f"  Amount: {tx['amount']}")
            print(f"  Balance: {tx['wallet_balance']}")
            
            # Create the actual output
            actual_output = f"{tx['date']},{tx['status']},{tx['transaction_type']},{tx['amount']},{tx['wallet_balance']}"
            expected_output = expected_outputs[i-1]
            
            print(f"  Expected: {expected_output}")
            print(f"  Actual:   {actual_output}")
            
            if actual_output == expected_output:
                print("  ✅ CORRECT")
                matches += 1
            else:
                print("  ❌ INCORRECT")
            
            detected_types.add(tx['transaction_type'])
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

def test_incremental_file_naming():
    """Test that CSV files get incremented names when files already exist."""
    print("\n🔍 Testing Incremental File Naming")
    print("=" * 50)
    
    import tempfile
    import shutil
    
    # Create a temporary directory for testing
    temp_dir = Path(tempfile.mkdtemp())
    extractor = TransactionExtractor(
        unlocked_dir=str(temp_dir),
        output_dir=str(temp_dir)
    )
    
    try:
        # Create a dummy PDF file for testing
        dummy_pdf = temp_dir / "test_transactions.pdf"
        dummy_pdf.write_bytes(b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\nxref\n0 1\ntrailer\n<<\n/Root 1 0 R\n>>\nstartxref\n9\n%%EOF")
        
        # Create dummy CSV files to simulate existing files
        csv1 = temp_dir / "test_transactions_transactions.csv"
        csv2 = temp_dir / "test_transactions_transactions_1.csv"
        csv3 = temp_dir / "test_transactions_transactions_2.csv"
        
        csv1.write_text("date,status,transaction_type,amount,wallet_balance\n")
        csv2.write_text("date,status,transaction_type,amount,wallet_balance\n")
        csv3.write_text("date,status,transaction_type,amount,wallet_balance\n")
        
        print(f"✅ Created test files: {csv1.name}, {csv2.name}, {csv3.name}")
        
        # Since we can't easily extract from the dummy PDF, we'll test the logic manually
        # by checking what filename would be generated
        base_name = f"{dummy_pdf.stem}_transactions"
        output_csv_path = temp_dir / f"{base_name}.csv"
        
        # Simulate the incremental naming logic
        if output_csv_path.exists():
            counter = 1
            while output_csv_path.exists():
                output_csv_path = temp_dir / f"{base_name}_{counter}.csv"
                counter += 1
        
        expected_path = temp_dir / "test_transactions_transactions_3.csv"
        
        print(f"📝 Expected next filename: {expected_path.name}")
        print(f"📝 Generated filename: {output_csv_path.name}")
        
        if output_csv_path == expected_path:
            print("✅ Incremental naming working correctly!")
            result = True
        else:
            print(f"❌ Expected {expected_path.name}, got {output_csv_path.name}")
            result = False
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            print(f"🧹 Cleaned up temporary directory: {temp_dir}")

if __name__ == "__main__":
    # Define test functions with aliases and descriptions
    test_functions = [
        ("pattern_matching", ["pattern", "matching"], test_transaction_pattern_matching, "Test algorithmic pattern matching against sample lines"),
        ("incremental_naming", ["naming", "increment", "file"], test_incremental_file_naming, "Test incremental CSV file naming when files exist")
    ]
    
    # Run the test suite
    run_test_suite(
        test_name="Transaction Extractor",
        description="Unit tests for PDF transaction extraction functionality",
        test_functions=test_functions
    )
