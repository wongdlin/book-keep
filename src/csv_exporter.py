#!/usr/bin/env python3
"""
CSV Export Module
Exports transaction data to CSV files
"""
import csv
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from .transaction_parser import Transaction

class CsvExporter:
    def __init__(self, output_dir: str = "pdf_files/output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_transactions(self, transactions: List[Transaction], filename: str = None) -> str:
        """Export transactions to CSV file"""
        if not transactions:
            print("❌ No transactions to export")
            return ""
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"transactions_{timestamp}.csv"
        
        # Ensure .csv extension
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        csv_path = self.output_dir / filename
        
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow([
                    'Date', 'Description', 'Amount', 'Type', 'Category', 'Raw Text'
                ])
                
                # Write transactions
                for transaction in transactions:
                    writer.writerow([
                        transaction.date,
                        transaction.description,
                        f"{transaction.amount:.2f}",
                        transaction.type,
                        transaction.category,
                        transaction.raw_text
                    ])
            
            print(f"✅ Exported {len(transactions)} transactions to: {csv_path}")
            return str(csv_path)
            
        except Exception as e:
            print(f"❌ Error exporting to CSV: {e}")
            return ""
    
    def create_summary(self, transactions: List[Transaction]) -> Dict:
        """Create summary statistics from transactions"""
        if not transactions:
            return {}
        
        # Calculate totals
        total_income = sum(t.amount for t in transactions if t.amount > 0)
        total_expenses = abs(sum(t.amount for t in transactions if t.amount < 0))
        net_balance = total_income - total_expenses
        
        # Count transactions
        income_count = len([t for t in transactions if t.amount > 0])
        expense_count = len([t for t in transactions if t.amount < 0])
        
        # Date range
        dates = [t.date for t in transactions if t.date]
        date_range = ""
        if dates:
            dates.sort()
            date_range = f"{dates[0]} to {dates[-1]}"
        
        summary = {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_balance": net_balance,
            "transaction_count": len(transactions),
            "income_count": income_count,
            "expense_count": expense_count,
            "date_range": date_range
        }
        
        return summary
    
    def export_summary(self, summary: Dict, filename: str = None) -> str:
        """Export summary to CSV file"""
        if not summary:
            print("❌ No summary data to export")
            return ""
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"summary_{timestamp}.csv"
        
        # Ensure .csv extension
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        csv_path = self.output_dir / filename
        
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write summary data
                writer.writerow(['Metric', 'Value'])
                writer.writerow(['Total Income', f"${summary['total_income']:.2f}"])
                writer.writerow(['Total Expenses', f"${summary['total_expenses']:.2f}"])
                writer.writerow(['Net Balance', f"${summary['net_balance']:.2f}"])
                writer.writerow(['Transaction Count', summary['transaction_count']])
                writer.writerow(['Income Count', summary['income_count']])
                writer.writerow(['Expense Count', summary['expense_count']])
                writer.writerow(['Date Range', summary['date_range']])
            
            print(f"✅ Exported summary to: {csv_path}")
            return str(csv_path)
            
        except Exception as e:
            print(f"❌ Error exporting summary: {e}")
            return ""
    
    def export_with_summary(self, transactions: List[Transaction], base_filename: str = None) -> Dict[str, str]:
        """Export both transactions and summary"""
        if not base_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"export_{timestamp}"
        
        # Export transactions
        transactions_file = self.export_transactions(transactions, f"{base_filename}_transactions.csv")
        
        # Create and export summary
        summary = self.create_summary(transactions)
        summary_file = self.export_summary(summary, f"{base_filename}_summary.csv")
        
        return {
            "transactions_file": transactions_file,
            "summary_file": summary_file,
            "summary": summary
        }
    
    def list_exported_files(self) -> List[str]:
        """List all exported CSV files"""
        csv_files = list(self.output_dir.glob("*.csv"))
        return [str(f) for f in csv_files]

if __name__ == "__main__":
    # Test the CSV exporter
    exporter = CsvExporter()
    
    print("📊 CSV Exporter Test")
    print("=" * 40)
    
    # Create sample transactions
    from .transaction_parser import Transaction
    
    sample_transactions = [
        Transaction("2024-01-15", "Salary Deposit", 3000.00, "Income", "Salary"),
        Transaction("2024-01-16", "Grocery Store", -85.50, "Expense", "Food"),
        Transaction("2024-01-17", "Gas Station", -45.00, "Expense", "Transportation"),
        Transaction("2024-01-18", "Freelance Work", 500.00, "Income", "Freelance"),
    ]
    
    # Export transactions
    result = exporter.export_with_summary(sample_transactions, "test_export")
    
    if result["transactions_file"]:
        print(f"\n✅ Transactions exported to: {result['transactions_file']}")
    
    if result["summary_file"]:
        print(f"✅ Summary exported to: {result['summary_file']}")
    
    # Show summary
    summary = result["summary"]
    print(f"\n📈 Summary:")
    print(f"  Total Income: ${summary['total_income']:.2f}")
    print(f"  Total Expenses: ${summary['total_expenses']:.2f}")
    print(f"  Net Balance: ${summary['net_balance']:.2f}")
    print(f"  Transactions: {summary['transaction_count']}")
