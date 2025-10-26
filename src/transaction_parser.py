#!/usr/bin/env python3
"""
Transaction Data Parser
Parses extracted PDF text to identify and structure transaction data
"""
import re
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Transaction:
    date: str
    description: str
    amount: float
    type: str  # "Income" or "Expense"
    category: str
    raw_text: str = ""

class TransactionParser:
    def __init__(self):
        # Common date patterns
        self.date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # DD/MM/YYYY
            r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
            r'\d{1,2}/\d{1,2}/\d{4}',  # D/M/YYYY
            r'\d{1,2}-\d{1,2}-\d{4}',  # D-M-YYYY
        ]
        
        # Amount patterns (with various currency symbols)
        self.amount_patterns = [
            r'[\$€£¥RM]\s*[\d,]+\.?\d*',  # Currency symbol + amount
            r'[\d,]+\.?\d*\s*[\$€£¥RM]',  # Amount + currency symbol
            r'[\d,]+\.?\d*',  # Just numbers with commas/decimals
        ]
        
        # Common transaction keywords
        self.income_keywords = [
            'salary', 'wage', 'income', 'deposit', 'credit', 'refund',
            'bonus', 'interest', 'dividend', 'payment received'
        ]
        
        self.expense_keywords = [
            'purchase', 'payment', 'debit', 'withdrawal', 'fee', 'charge',
            'bill', 'rent', 'utilities', 'groceries', 'gas', 'fuel'
        ]
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers
        text = re.sub(r'Page \d+', '', text)
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Remove common PDF artifacts
        text = re.sub(r'[^\w\s\.,\-\$€£¥RM:/]', '', text)
        
        return text.strip()
    
    def extract_dates(self, text: str) -> List[str]:
        """Extract all dates from text"""
        dates = []
        for pattern in self.date_patterns:
            matches = re.findall(pattern, text)
            dates.extend(matches)
        return list(set(dates))  # Remove duplicates
    
    def extract_amounts(self, text: str) -> List[float]:
        """Extract all monetary amounts from text"""
        amounts = []
        
        for pattern in self.amount_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    # Clean the amount string
                    amount_str = re.sub(r'[^\d.,\-]', '', match)
                    if amount_str:
                        # Handle negative amounts
                        is_negative = '-' in amount_str or 'debit' in match.lower()
                        amount_str = amount_str.replace('-', '')
                        
                        # Convert to float
                        amount = float(amount_str.replace(',', ''))
                        if is_negative:
                            amount = -amount
                        
                        amounts.append(amount)
                except ValueError:
                    continue
        
        return amounts
    
    def categorize_transaction(self, description: str, amount: float) -> str:
        """Categorize transaction based on description and amount"""
        desc_lower = description.lower()
        
        # Check for income keywords
        for keyword in self.income_keywords:
            if keyword in desc_lower:
                return "Income"
        
        # Check for expense keywords
        for keyword in self.expense_keywords:
            if keyword in desc_lower:
                return "Expense"
        
        # Use amount to determine type
        if amount > 0:
            return "Income"
        elif amount < 0:
            return "Expense"
        else:
            return "Unknown"
    
    def parse_transactions_from_text(self, text: str) -> List[Transaction]:
        """Parse transactions from extracted PDF text"""
        transactions = []
        
        # Clean the text
        clean_text = self.clean_text(text)
        
        # Split into lines for processing
        lines = clean_text.split('\n')
        
        # Look for transaction patterns
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Extract dates and amounts from this line
            dates = self.extract_dates(line)
            amounts = self.extract_amounts(line)
            
            # If we found both date and amount, it might be a transaction
            if dates and amounts:
                for date in dates:
                    for amount in amounts:
                        # Create transaction
                        transaction = Transaction(
                            date=date,
                            description=line,
                            amount=amount,
                            type=self.categorize_transaction(line, amount),
                            category="Uncategorized",
                            raw_text=line
                        )
                        transactions.append(transaction)
        
        # Remove duplicates
        unique_transactions = []
        seen = set()
        for t in transactions:
            key = (t.date, t.description, t.amount)
            if key not in seen:
                seen.add(key)
                unique_transactions.append(t)
        
        return unique_transactions
    
    def parse_transactions_from_tables(self, tables: List[List[str]]) -> List[Transaction]:
        """Parse transactions from extracted tables"""
        transactions = []
        
        for table in tables:
            if not table or len(table) < 2:
                continue
            
            # Assume first row is headers
            headers = [col.lower().strip() for col in table[0]]
            
            # Find relevant columns
            date_col = None
            desc_col = None
            amount_col = None
            
            for i, header in enumerate(headers):
                if any(word in header for word in ['date', 'time']):
                    date_col = i
                elif any(word in header for word in ['description', 'details', 'memo', 'narration']):
                    desc_col = i
                elif any(word in header for word in ['amount', 'value', 'balance', 'debit', 'credit']):
                    amount_col = i
            
            # Process data rows
            for row in table[1:]:
                if len(row) < max([date_col or 0, desc_col or 0, amount_col or 0]):
                    continue
                
                try:
                    date = row[date_col] if date_col is not None else ""
                    description = row[desc_col] if desc_col is not None else ""
                    amount_str = row[amount_col] if amount_col is not None else "0"
                    
                    # Parse amount
                    amount = 0.0
                    if amount_str:
                        amount_str = re.sub(r'[^\d.,\-]', '', str(amount_str))
                        if amount_str:
                            amount = float(amount_str.replace(',', ''))
                    
                    if date and description and amount != 0:
                        transaction = Transaction(
                            date=date,
                            description=description,
                            amount=amount,
                            type=self.categorize_transaction(description, amount),
                            category="Uncategorized",
                            raw_text=str(row)
                        )
                        transactions.append(transaction)
                
                except (ValueError, IndexError):
                    continue
        
        return transactions
    
    def parse_transactions(self, text: str, tables: List[List[str]] = None) -> List[Transaction]:
        """Main method to parse transactions from PDF data"""
        transactions = []
        
        # Try parsing from tables first (more structured)
        if tables:
            table_transactions = self.parse_transactions_from_tables(tables)
            transactions.extend(table_transactions)
            print(f"📊 Found {len(table_transactions)} transactions from tables")
        
        # Parse from text (fallback)
        text_transactions = self.parse_transactions_from_text(text)
        transactions.extend(text_transactions)
        print(f"📄 Found {len(text_transactions)} transactions from text")
        
        # Remove duplicates
        unique_transactions = []
        seen = set()
        for t in transactions:
            key = (t.date, t.description, t.amount)
            if key not in seen:
                seen.add(key)
                unique_transactions.append(t)
        
        print(f"✅ Total unique transactions: {len(unique_transactions)}")
        return unique_transactions

if __name__ == "__main__":
    # Test the parser
    parser = TransactionParser()
    
    print("🔍 Transaction Parser Test")
    print("=" * 40)
    
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
    
    if transactions:
        print(f"\n📊 Parsed {len(transactions)} transactions:")
        for i, t in enumerate(transactions, 1):
            print(f"{i}. {t.date} | {t.description} | ${t.amount:.2f} | {t.type}")
    else:
        print("❌ No transactions found in sample text")
