#!/usr/bin/env python3
"""
Unit tests for TransactionParser
"""
import sys
import os
import re
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from transaction_parser import TransactionParser
from PyPDF2 import PdfReader
from test_runner import run_test_suite

def test_debug_transaction_extraction():
    """Debug test to dump detailed transaction extraction output to file."""
    print("\n🔍 Debug: Detailed Transaction Extraction Analysis")
    print("=" * 60)
    
    pdf_path = Path("pdf_files/unlocked/tng_ewallet_transactions.pdf")
    
    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    try:
        # Extract text from PDF
        reader = PdfReader(pdf_path)
        all_text = ""
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            all_text += text + "\n"
            print(f"📄 Page {page_num + 1}: {len(text)} characters")
        
        print(f"\n📄 Total text extracted: {len(all_text)} characters")
        
        # Now test our transaction extractor (the actual one being used in main.py)
        print(f"\n🔍 Testing Transaction Extractor (same as main.py):")
        from transaction_extractor import TransactionExtractor
        extractor = TransactionExtractor()
        transactions = extractor.extract_transactions_from_text(all_text)
        
        print(f"📊 Extracted {len(transactions)} transactions")
        
        if transactions:
            print(f"\n📋 Transaction details:")
            for i, tx in enumerate(transactions[:10]):  # Show first 10
                print(f"  {i+1}. {tx['date']} | {tx['status']} | {tx['transaction_type']} | RM{tx['amount']} | RM{tx['wallet_balance']}")
            
            if len(transactions) > 10:
                print(f"  ... and {len(transactions) - 10} more")
            
            # Count transaction types
            type_counts = {}
            for tx in transactions:
                tx_type = tx['transaction_type']
                type_counts[tx_type] = type_counts.get(tx_type, 0) + 1
            
            print(f"\n📊 Transaction type counts:")
            for tx_type, count in sorted(type_counts.items()):
                print(f"  {tx_type}: {count}")
        
        return len(transactions) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_transaction_parser_basic():
    """Test basic transaction parser functionality."""
    print("\n🔍 Testing Basic Transaction Parser")
    print("=" * 50)
    
    parser = TransactionParser()
    
    # Sample text for testing
    sample_text = """
    Date: 2024-01-15
    Description: Salary Deposit
    Amount: $3000.00
    
    Date: 2024-01-16  
    Description: Grocery Store Purchase
    Amount: -$85.50
    
    Date: 2024-01-17
    Description: Gas Station
    Amount: -$45.00
    """
    
    transactions = parser.parse_transactions(sample_text)
    
    print(f"📊 Parsed {len(transactions)} transactions from sample text")
    
    if transactions:
        print("\nTransaction details:")
        for i, tx in enumerate(transactions, 1):
            print(f"  {i}. {tx.date} | {tx.description} | ${tx.amount:.2f} | {tx.type}")
    
    return len(transactions) > 0

if __name__ == "__main__":
    # Define test functions with aliases and descriptions
    test_functions = [
        ("basic", ["basic", "simple"], test_transaction_parser_basic, "Test basic transaction parser functionality"),
        ("debug", ["debug", "dump"], test_debug_transaction_extraction, "Debug detailed transaction extraction analysis")
    ]
    
    # Run the test suite
    run_test_suite(
        test_name="Transaction Parser",
        description="Unit tests for transaction parsing functionality",
        test_functions=test_functions
    )
