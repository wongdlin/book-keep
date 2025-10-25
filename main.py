# main.py
import os
import sys
from pathlib import Path
from src.pdf_unlocker import PdfUnlocker

def main():
    print("BookKeep - Transaction Processing System")
    print("=" * 40)
    
    # Initialize PDF unlocker with new folder structure
    unlocker = PdfUnlocker()
    
    # List available PDF files
    pdf_files = list(unlocker.input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("\nNo PDF files found in 'pdf_files/input' directory")
        print("Please add PDF files to the 'pdf_files/input' folder and run again")
        return
    
    print(f"\nFound {len(pdf_files)} PDF file(s):")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"  {i}. {pdf_file.name}")
    
    # For now, just show what we found
    print("\nNext steps:")
    print("1. Add password manager")
    print("2. Add PDF processing logic")
    print("3. Add transaction extraction")
    print("4. Add Excel/Google Sheets export")

if __name__ == "__main__":
    main()