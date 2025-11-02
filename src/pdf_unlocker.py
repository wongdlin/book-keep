import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from PyPDF2 import PdfReader, PdfWriter
from config import Config

class PdfUnlocker:
    def __init__(self, input_dir: Optional[str] = None, unlocked_dir: Optional[str] = None):
        self.input_dir = Path(input_dir) if input_dir else Config.get_pdf_input_dir()
        self.unlocked_dir = Path(unlocked_dir) if unlocked_dir else Config.get_pdf_unlocked_dir()
        
        # Create directories if they don't exist
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.unlocked_dir.mkdir(parents=True, exist_ok=True)

    def is_pdf_encrypted(self, file_path: str) -> bool:
        """Check if a PDF file is protected."""
        try:
            reader = PdfReader(file_path)
            return reader.is_encrypted
        except Exception as e:
            print(f"Error checking if PDF is encrypted: {e}")
            return False

    def unlock_pdf(self, pdf_path: str, password: List[str]) -> Tuple[bool, Optional[str]]:
        """Try to unlock a PDF file with a list of passwords."""
        try:
            reader = PdfReader(pdf_path)

            if not reader.is_encrypted:
                return True, None

            print(f"PDF is encrypted. Trying passwords...")

            for i, password in enumerate(password, 1):
                print(f"Trying password {i}/{len(password)}: {password}")

                if reader.decrypt(password):
                    print(f"Password {password} unlocked the PDF.")
                    return True, password

                reader = PdfReader(pdf_path)

            print(f"No matching password found in {len(password)} attempts")
            return False, None

        except Exception as e:
            print(f"Error unlocking PDF: {e}")
            return False, None

    def save_unlocked_pdf(self, input_path: str, output_path: str, password: Optional[str] = None):
        """Save an unlocked PDF file to the output directory."""
        try:
            reader = PdfReader(input_path)

            if reader.is_encrypted and password:
                reader.decrypt(password)

            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            with open(output_path, "wb") as output_file:
                writer.write(output_file)

        except Exception as e:
            print(f"Error saving unlocked PDF: {e}")
    
    def copy_pdf(self, input_path: str, output_path: str):
        """Copy a PDF file (for non-encrypted PDFs)"""
        try:
            import shutil
            shutil.copy2(input_path, output_path)
        except Exception as e:
            print(f"Error copying PDF: {e}")
            
    def process_pdf(self, pdf_name: str, passwords: List[str]) ->  Tuple[bool, Optional[str]]:
        """Process a PDF file"""
        pdf_path = self.input_dir / pdf_name

        if not pdf_path.exists():
            print(f"PDF file {pdf_name} not found in {self.input_dir}")
            return False, None
            
        print(f"Processing PDF file: {pdf_name}")

        if not self.is_pdf_encrypted(str(pdf_path)):
            print(f"PDF {pdf_name} is not encrypted. Moving to unlocked folder...")
            # Move non-encrypted PDF to unlocked folder
            unlocked_path = self.unlocked_dir / pdf_name
            self.copy_pdf(str(pdf_path), str(unlocked_path))
            print(f"PDF moved to: {unlocked_path.name}")
            return True, None

        success, password = self.unlock_pdf(str(pdf_path), passwords)

        if success:
            print(f"PDF {pdf_name} unlocked successfully with password: {password}")
            unlocked_path = self.unlocked_dir / pdf_name
            self.save_unlocked_pdf(str(pdf_path), str(unlocked_path), password)
            print(f"Unlocked PDF saved to: {unlocked_path.name}")
            return True, password
        else:
            print(f"Failed to unlock PDF {pdf_name}")
            return False, None
    
    def process_all_pdfs(self, passwords: List[str]) -> List[Tuple[bool, Optional[str]]]:
        """Process all PDF files in the input directory"""
        pdf_files = list(self.input_dir.glob("*.pdf"))

        if not pdf_files:
            print(f"No PDF files found in input directory")
            return {}

        print(f"Found {len(pdf_files)} PDF files to process")
        results = {}

        for pdf_file in pdf_files:
            success, password = self.process_pdf(pdf_file.name, passwords)
            results[pdf_file.name] = success

        successful = sum(1 for success in results.values() if success)
        print(f"\n📊 Summary: {successful}/{len(pdf_files)} PDFs processed successfully")

        return results
    