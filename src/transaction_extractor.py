#!/usr/bin/env python3
"""
Transaction Extractor
Extracts only transaction data from TNG eWallet PDFs and saves to CSV.
"""
import csv
import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

class TransactionExtractor:
    def __init__(self, 
                 unlocked_dir: str = "pdf_files/unlocked",
                 output_dir: str = "pdf_files/output"):
        self.unlocked_dir = Path(unlocked_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Pattern to match transaction lines - simplified approach
        # Look for: Date Status ... RM amount RM balance
        # Handle cases where amounts are concatenated without spaces
        self.transaction_pattern = re.compile(
            r'^(\d{1,2}/\d{1,2}/\d{4})\s+(Success|Failed|Cancelled|Reversed)\s+(.+?)\s+RM([\d,]+\.?\d*)\s+RM([\d,]+\.?\d*)$'
        )
        
        # Alternative pattern for concatenated amounts (no space before RM)
        # This pattern captures the middle part and the final RM balance separately
        self.transaction_pattern_alt = re.compile(
            r'^(\d{1,2}/\d{1,2}/\d{4})\s+(Success|Failed|Cancelled|Reversed)\s+(.+?)(\d+RM[\d,]+\.?\d*)\s+RM([\d,]+\.?\d*)$'
        )
        
        # Better pattern that handles the concatenated amounts properly
        self.transaction_pattern_concatenated = re.compile(
            r'^(\d{1,2}/\d{1,2}/\d{4})\s+(Success|Failed|Cancelled|Reversed)\s+(.+?)(\d+RM[\d,]+\.?\d*)\s+RM([\d,]+\.?\d*)$'
        )
        
        # Pattern to extract amounts from concatenated format like "123RM45.67"
        self.amount_extract_pattern = re.compile(r'(\d+)RM([\d,]+\.?\d*)')

    def extract_transactions_from_text(self, text: str) -> List[Dict]:
        """Extract transaction data from raw text using algorithmic approach."""
        transactions = []
        lines = text.split('\n')
        
        # Look for lines that start with date pattern and contain transaction data
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if this line starts with a date pattern
            if re.match(r'^\d{1,2}/\d{1,2}/\d{4}', line):
                # This might be the start of a transaction, collect the full transaction
                transaction_lines = [line]
                j = i + 1
                
                # Collect subsequent lines until we find the amount and balance
                while j < len(lines) and not re.search(r'RM[\d,]+\.?\d*\s+RM[\d,]+\.?\d*$', lines[j]):
                    next_line = lines[j].strip()
                    if next_line:
                        transaction_lines.append(next_line)
                    j += 1
                
                # If we found the amount/balance line, add it
                if j < len(lines):
                    transaction_lines.append(lines[j].strip())
                
                # Join all lines to form the complete transaction
                full_transaction = ' '.join(transaction_lines)
                
                # Use algorithmic approach to extract transaction data
                transaction_data = self._extract_transaction_data_algorithmic(full_transaction)
                
                if transaction_data:
                    transactions.append(transaction_data)
                
                # Skip the lines we've already processed
                i = j + 1
            else:
                i += 1
        
        return transactions

    def _extract_transaction_data_algorithmic(self, line: str) -> Optional[Dict]:
        """Extract transaction data using algorithmic approach."""
        
        # Step 1: Split by spaces
        words = line.strip().split()
        
        if len(words) < 4:  # Need at least date, status, transaction, amount
            return None
        
        # Step 2: Find and extract date
        date = None
        date_index = None
        for i, word in enumerate(words):
            if re.match(r'\d{1,2}/\d{1,2}/\d{4}', word):
                date = word
                date_index = i
                break
        
        if date_index is None:
            return None
        
        # Remove date from words list
        words.pop(date_index)
        
        # Step 3: Find and extract status
        status = None
        status_index = None
        for i, word in enumerate(words):
            if word in ['Success', 'Failed', 'Cancelled', 'Reversed']:
                status = word
                status_index = i
                break
        
        if status_index is None:
            return None
        
        # Remove status from words list
        words.pop(status_index)
        
        # Step 4: Find transaction type by progressive matching
        transaction_type = self._find_transaction_type(words)
        
        # Step 5: Extract amount and balance (find RM and take what's after)
        amount, balance = self._extract_amounts_from_remaining(words)
        
        if amount is None or balance is None:
            return None
        
        return {
            'date': date,
            'status': status,
            'transaction_type': transaction_type,
            'amount': amount.replace(',', ''),
            'wallet_balance': balance.replace(',', '')
        }

    def _find_transaction_type(self, words: List[str]) -> str:
        """Find transaction type by progressive word matching."""
        transaction_types = [
            "Payment Cancelled",
            "GO+ Daily Earnings", 
            "GO+ Cash In",
            "DuitNow QR TNGD",
            "DUITNOW_RECEIVEFROM",
            "Transfer to Wallet",
            "Receive from Wallet",
            "eWallet Cash Out",
            "DuitNow QR",
            "Reload",
            "Payment"
        ]
        
        # Try single word matches first
        for word in words:
            if word in transaction_types:
                return word
        
        # Try progressive combinations (2-4 words)
        for i in range(len(words)):
            for j in range(i + 2, min(i + 5, len(words) + 1)):  # 2-4 words
                phrase = " ".join(words[i:j])
                if phrase in transaction_types:
                    return phrase
        
        # Fallback: use first few words as transaction type
        return " ".join(words[:3]) if len(words) >= 3 else " ".join(words)

    def _extract_amounts_from_remaining(self, words: List[str]) -> tuple:
        """Extract amount and balance from remaining words."""
        amount = None
        balance = None
        
        # Look for RM patterns in the words
        for i, word in enumerate(words):
            if 'RM' in word:
                # Extract number after RM
                amount_match = re.search(r'RM([\d,]+\.?\d*)', word)
                if amount_match:
                    amount = amount_match.group(1)
                    
                    # Look for the next RM pattern for balance
                    for j in range(i + 1, len(words)):
                        if 'RM' in words[j]:
                            balance_match = re.search(r'RM([\d,]+\.?\d*)', words[j])
                            if balance_match:
                                balance = balance_match.group(1)
                                break
                    break
        
        return amount, balance

    def extract_transactions_to_csv(self, pdf_path: Path) -> Optional[Path]:
        """Extract transactions from PDF and save to CSV."""
        try:
            from PyPDF2 import PdfReader
            
            reader = PdfReader(pdf_path)
            all_text = ""
            
            # Extract text from all pages
            for page in reader.pages:
                all_text += page.extract_text() + "\n"
            
            # Extract transactions
            transactions = self.extract_transactions_from_text(all_text)
            
            if not transactions:
                print(f"⚠️ No transactions found in {pdf_path.name}")
                return None
            
            # Create output CSV
            output_csv_path = self.output_dir / f"{pdf_path.stem}_transactions.csv"
            
            with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
                fieldnames = ['date', 'status', 'transaction_type', 'amount', 'wallet_balance']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for transaction in transactions:
                    writer.writerow(transaction)
            
            print(f"✅ Extracted {len(transactions)} transactions from '{pdf_path.name}' to '{output_csv_path.name}'")
            return output_csv_path
            
        except Exception as e:
            print(f"❌ Error extracting transactions from {pdf_path.name}: {e}")
            return None

    def extract_all_pdfs(self) -> List[Path]:
        """Process all PDF files in the unlocked directory and extract transactions."""
        unlocked_pdfs = list(self.unlocked_dir.glob("*.pdf"))

        if not unlocked_pdfs:
            print(f"No unlocked PDF files found in {self.unlocked_dir}")
            return []

        print(f"Found {len(unlocked_pdfs)} unlocked PDF file(s) to extract transactions from.")
        
        generated_csv_files = []
        for pdf_file in unlocked_pdfs:
            csv_path = self.extract_transactions_to_csv(pdf_file)
            if csv_path:
                generated_csv_files.append(csv_path)
                
        return generated_csv_files

if __name__ == "__main__":
    # Test the extractor
    extractor = TransactionExtractor()
    csv_files = extractor.extract_all_pdfs()
    
    if csv_files:
        print(f"\nSuccessfully extracted transactions to {len(csv_files)} CSV file(s):")
        for csv_file in csv_files:
            print(f"- {csv_file}")
    else:
        print("No transaction CSV files were generated.")
