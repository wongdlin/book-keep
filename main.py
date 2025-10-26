# main.py
import os
import sys
from pathlib import Path
from src.pdf_unlocker import PdfUnlocker
from src.password_manager import PasswordManager
from src.transaction_extractor import TransactionExtractor

def main():
    print("🚀 BookKeep - Complete PDF Processing System")
    print("=" * 50)
    
    # Initialize components
    unlocker = PdfUnlocker()
    password_manager = PasswordManager()
    extractor = TransactionExtractor()
    
    # Step 1: Check for password-protected PDFs
    print("\n📄 Step 1: Checking for PDF files...")
    pdf_files = list(unlocker.input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found in 'pdf_files/input' directory")
        print("Please add PDF files to the 'pdf_files/input' folder and run again")
        return
    
    print(f"✅ Found {len(pdf_files)} PDF file(s):")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"  {i}. {pdf_file.name}")
    
    # Step 2: Get passwords
    print("\n🔑 Step 2: Loading passwords...")
    passwords = password_manager.get_passwords()
    
    if not passwords:
        print("❌ No passwords found!")
        print("Please run: python scripts/password_cli.py")
        print("Add your PDF passwords and try again")
        return
    
    print(f"✅ Loaded {len(passwords)} passwords from {len(password_manager.list_categories())} categories")
    
    # Step 3: Unlock PDFs
    print("\n🔓 Step 3: Unlocking PDFs...")
    unlock_results = unlocker.process_all_pdfs(passwords)
    
    if not unlock_results:
        print("❌ No PDFs were unlocked")
        return
    
    successful_unlocks = sum(1 for success in unlock_results.values() if success)
    print(f"✅ Successfully unlocked {successful_unlocks}/{len(pdf_files)} PDFs")
    
    # Step 4: Extract transactions to CSV
    print("\n📊 Step 4: Extracting transactions to CSV...")
    csv_files = extractor.extract_all_pdfs()
    
    if not csv_files:
        print("❌ No transactions were extracted")
        return
    
    # Step 5: Show results
    print("\n📈 Step 5: Transaction Extraction Results")
    print("-" * 30)
    print(f"CSV Files Generated: {len(csv_files)}")
    
    # List generated files
    if csv_files:
        print(f"\n📁 Generated Files:")
        for file in csv_files:
            print(f"  - {Path(file).name}")
    
    print(f"\n🎉 Transaction extraction complete! Check 'pdf_files/output/' for CSV files")

if __name__ == "__main__":
    main()