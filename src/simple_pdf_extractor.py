#!/usr/bin/env python3
"""
Simple PDF to CSV Extractor
Just extracts raw text from PDF and puts it into CSV without processing
"""
import csv
from pathlib import Path
from typing import List, Dict
from .pdf_extractor import PdfExtractor

class SimplePdfExtractor:
    def __init__(self, 
                 unlocked_dir: str = "pdf_files/unlocked",
                 output_dir: str = "pdf_files/output"):
        self.unlocked_dir = Path(unlocked_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.extractor = PdfExtractor(str(unlocked_dir))
    
    def extract_pdf_to_csv(self, pdf_path: str) -> str:
        """Extract PDF text and save to CSV file"""
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            print(f"❌ PDF file not found: {pdf_path}")
            return ""
        
        print(f"📄 Extracting text from: {pdf_path.name}")
        
        # Extract text
        text = self.extractor.extract_text(str(pdf_path))
        if not text:
            print(f"❌ Failed to extract text from {pdf_path.name}")
            return ""
        
        # Create CSV filename
        csv_filename = f"{pdf_path.stem}_raw_text.csv"
        csv_path = self.output_dir / csv_filename
        
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['Line Number', 'Text Content'])
                
                # Split text into lines and write each line
                lines = text.split('\n')
                for i, line in enumerate(lines, 1):
                    if line.strip():  # Only write non-empty lines
                        writer.writerow([i, line.strip()])
            
            print(f"✅ Extracted {len(lines)} lines to: {csv_path}")
            return str(csv_path)
            
        except Exception as e:
            print(f"❌ Error creating CSV: {e}")
            return ""
    
    def extract_all_pdfs(self) -> List[str]:
        """Extract all unlocked PDFs to CSV"""
        pdf_files = self.extractor.list_unlocked_pdfs()
        
        if not pdf_files:
            print("❌ No unlocked PDF files found")
            return []
        
        print(f"📄 Found {len(pdf_files)} unlocked PDF file(s)")
        
        csv_files = []
        for pdf_path in pdf_files:
            csv_file = self.extract_pdf_to_csv(pdf_path)
            if csv_file:
                csv_files.append(csv_file)
        
        return csv_files

if __name__ == "__main__":
    # Test the simple extractor
    extractor = SimplePdfExtractor()
    
    print("📄 Simple PDF to CSV Extractor")
    print("=" * 40)
    
    csv_files = extractor.extract_all_pdfs()
    
    if csv_files:
        print(f"\n✅ Generated {len(csv_files)} CSV file(s):")
        for csv_file in csv_files:
            print(f"  - {Path(csv_file).name}")
    else:
        print("❌ No CSV files generated")
