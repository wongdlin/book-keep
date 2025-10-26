#!/usr/bin/env python3
"""
PDF Text Extraction Module
Extracts text and data from unlocked PDF files
"""
import os
from pathlib import Path
from typing import List, Dict, Optional
import PyPDF2
import pdfplumber
from pdfminer.high_level import extract_text as pdfminer_extract

class PdfExtractor:
    def __init__(self, unlocked_dir: str = "pdf_files/unlocked"):
        self.unlocked_dir = Path(unlocked_dir)
        self.unlocked_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_text_pypdf2(self, pdf_path: str) -> str:
        """Extract text using PyPDF2"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"PyPDF2 extraction failed: {e}")
            return ""
    
    def extract_text_pdfplumber(self, pdf_path: str) -> str:
        """Extract text using pdfplumber (better for tables)"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception as e:
            print(f"pdfplumber extraction failed: {e}")
            return ""
    
    def extract_text_pdfminer(self, pdf_path: str) -> str:
        """Extract text using pdfminer (most reliable)"""
        try:
            return pdfminer_extract(pdf_path)
        except Exception as e:
            print(f"pdfminer extraction failed: {e}")
            return ""
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text using the best available method"""
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            print(f"PDF file not found: {pdf_path}")
            return ""
        
        print(f"Extracting text from: {pdf_path.name}")
        
        # Try pdfplumber first (best for tables)
        text = self.extract_text_pdfplumber(str(pdf_path))
        if text and len(text.strip()) > 50:
            print(f"✅ Extracted {len(text)} characters using pdfplumber")
            return text
        
        # Try pdfminer as fallback
        text = self.extract_text_pdfminer(str(pdf_path))
        if text and len(text.strip()) > 50:
            print(f"✅ Extracted {len(text)} characters using pdfminer")
            return text
        
        # Try PyPDF2 as last resort
        text = self.extract_text_pypdf2(str(pdf_path))
        if text and len(text.strip()) > 50:
            print(f"✅ Extracted {len(text)} characters using PyPDF2")
            return text
        
        print("❌ Failed to extract text from PDF")
        return ""
    
    def extract_tables(self, pdf_path: str) -> List[List[str]]:
        """Extract tables from PDF using pdfplumber"""
        try:
            tables = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)
            return tables
        except Exception as e:
            print(f"Table extraction failed: {e}")
            return []
    
    def get_pdf_info(self, pdf_path: str) -> Dict:
        """Get PDF metadata and info"""
        try:
            info = {
                "file_name": Path(pdf_path).name,
                "file_size": Path(pdf_path).stat().st_size,
                "pages": 0,
                "text_length": 0
            }
            
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                info["pages"] = len(reader.pages)
                
                # Extract text to get length
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                info["text_length"] = len(text)
            
            return info
        except Exception as e:
            print(f"Error getting PDF info: {e}")
            return {"file_name": Path(pdf_path).name, "error": str(e)}
    
    def list_unlocked_pdfs(self) -> List[str]:
        """List all unlocked PDF files"""
        pdf_files = list(self.unlocked_dir.glob("*.pdf"))
        return [str(f) for f in pdf_files]
    
    def extract_all_pdfs(self) -> Dict[str, str]:
        """Extract text from all unlocked PDFs"""
        results = {}
        pdf_files = self.list_unlocked_pdfs()
        
        if not pdf_files:
            print("No unlocked PDF files found")
            return results
        
        print(f"Found {len(pdf_files)} unlocked PDF file(s)")
        
        for pdf_path in pdf_files:
            print(f"\nProcessing: {Path(pdf_path).name}")
            text = self.extract_text(pdf_path)
            if text:
                results[pdf_path] = text
                print(f"✅ Successfully extracted text")
            else:
                print(f"❌ Failed to extract text")
        
        return results

if __name__ == "__main__":
    # Test the extractor
    extractor = PdfExtractor()
    
    print("🔍 PDF Text Extractor Test")
    print("=" * 40)
    
    # List available PDFs
    pdf_files = extractor.list_unlocked_pdfs()
    
    if pdf_files:
        print(f"Found {len(pdf_files)} PDF file(s):")
        for pdf in pdf_files:
            print(f"  - {Path(pdf).name}")
        
        # Extract text from first PDF
        first_pdf = pdf_files[0]
        print(f"\nExtracting text from: {Path(first_pdf).name}")
        text = extractor.extract_text(first_pdf)
        
        if text:
            print(f"\n📄 Extracted Text Preview:")
            print("-" * 40)
            print(text[:500] + "..." if len(text) > 500 else text)
            print("-" * 40)
            print(f"Total characters: {len(text)}")
        else:
            print("❌ No text extracted")
    else:
        print("No unlocked PDF files found in pdf_files/unlocked/")
        print("Please add unlocked PDF files to test extraction")
