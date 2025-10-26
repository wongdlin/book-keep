#!/usr/bin/env python3
"""
PDF Processor - Main orchestrator
Combines PDF extraction, transaction parsing, and CSV export
"""
from pathlib import Path
from typing import List, Dict, Optional
from .pdf_extractor import PdfExtractor
from .transaction_parser import TransactionParser, Transaction
from .csv_exporter import CsvExporter

class PdfProcessor:
    def __init__(self, 
                 unlocked_dir: str = "pdf_files/unlocked",
                 output_dir: str = "pdf_files/output"):
        self.extractor = PdfExtractor(unlocked_dir)
        self.parser = TransactionParser()
        self.exporter = CsvExporter(output_dir)
    
    def process_single_pdf(self, pdf_path: str) -> Dict:
        """Process a single PDF file"""
        print(f"\n🔄 Processing: {Path(pdf_path).name}")
        print("-" * 50)
        
        try:
            # Extract text from PDF
            text = self.extractor.extract_text(pdf_path)
            if not text:
                return {"success": False, "error": "Failed to extract text"}
            
            # Extract tables (optional)
            tables = self.extractor.extract_tables(pdf_path)
            
            # Parse transactions
            transactions = self.parser.parse_transactions(text, tables)
            if not transactions:
                return {"success": False, "error": "No transactions found"}
            
            # Export to CSV
            base_filename = Path(pdf_path).stem  # Remove .pdf extension
            result = self.exporter.export_with_summary(transactions, base_filename)
            
            return {
                "success": True,
                "pdf_path": pdf_path,
                "transactions_count": len(transactions),
                "transactions_file": result["transactions_file"],
                "summary_file": result["summary_file"],
                "summary": result["summary"]
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_all_pdfs(self) -> Dict[str, Dict]:
        """Process all unlocked PDF files"""
        print("🚀 PDF Processor - Processing All Unlocked PDFs")
        print("=" * 60)
        
        # Get list of unlocked PDFs
        pdf_files = self.extractor.list_unlocked_pdfs()
        
        if not pdf_files:
            print("❌ No unlocked PDF files found")
            print("Please add unlocked PDF files to pdf_files/unlocked/")
            return {}
        
        print(f"📄 Found {len(pdf_files)} unlocked PDF file(s)")
        
        results = {}
        successful = 0
        failed = 0
        
        for pdf_path in pdf_files:
            result = self.process_single_pdf(pdf_path)
            results[pdf_path] = result
            
            if result["success"]:
                successful += 1
                print(f"✅ Success: {result['transactions_count']} transactions extracted")
            else:
                failed += 1
                print(f"❌ Failed: {result['error']}")
        
        # Summary
        print(f"\n📊 Processing Summary:")
        print(f"  ✅ Successful: {successful}")
        print(f"  ❌ Failed: {failed}")
        print(f"  📁 Total: {len(pdf_files)}")
        
        return results
    
    def get_processing_stats(self, results: Dict[str, Dict]) -> Dict:
        """Get overall processing statistics"""
        if not results:
            return {}
        
        total_transactions = 0
        total_income = 0
        total_expenses = 0
        successful_files = 0
        
        for result in results.values():
            if result["success"]:
                successful_files += 1
                summary = result.get("summary", {})
                total_transactions += summary.get("transaction_count", 0)
                total_income += summary.get("total_income", 0)
                total_expenses += summary.get("total_expenses", 0)
        
        return {
            "files_processed": len(results),
            "successful_files": successful_files,
            "failed_files": len(results) - successful_files,
            "total_transactions": total_transactions,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_balance": total_income - total_expenses
        }
    
    def list_output_files(self) -> List[str]:
        """List all generated CSV files"""
        return self.exporter.list_exported_files()

if __name__ == "__main__":
    # Test the PDF processor
    processor = PdfProcessor()
    
    print("🔄 PDF Processor Test")
    print("=" * 40)
    
    # Process all unlocked PDFs
    results = processor.process_all_pdfs()
    
    if results:
        # Show statistics
        stats = processor.get_processing_stats(results)
        print(f"\n📈 Overall Statistics:")
        print(f"  Files Processed: {stats['files_processed']}")
        print(f"  Successful: {stats['successful_files']}")
        print(f"  Failed: {stats['failed_files']}")
        print(f"  Total Transactions: {stats['total_transactions']}")
        print(f"  Total Income: ${stats['total_income']:.2f}")
        print(f"  Total Expenses: ${stats['total_expenses']:.2f}")
        print(f"  Net Balance: ${stats['net_balance']:.2f}")
        
        # List output files
        output_files = processor.list_output_files()
        if output_files:
            print(f"\n📁 Generated Files:")
            for file in output_files:
                print(f"  - {Path(file).name}")
    else:
        print("❌ No PDFs processed")
